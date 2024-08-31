# BLINK DETECTOR SENSIBLE TO FACIAL ORIENTATION

import csv
import math
import sys
import time
from datetime import datetime

import cv2
import mediapipe as mp
import numpy as np

# right eyes indices
RIGHT_EYE =[ 362, 382, 381, 380, 374, 373, 390, 249, 263, 466, 388, 387, 386, 385,384, 398 ]
# Left eyes indices 
LEFT_EYE =[ 33, 7, 163, 144, 145, 153, 154, 155, 133, 173, 157, 158, 159, 160, 161 , 246 ] 
# Threshold for Blinking
BLINK_RATIO_THRESHOLD = 3.42

# define face mesh
mp_face_mesh = mp.solutions.face_mesh
face_mesh = mp_face_mesh.FaceMesh(min_detection_confidence=0.5, min_tracking_confidence=0.5)

# time constant
INITAL_TIME = time.time()

# returns direction of face, as text and char: l = left, r = right, d = down, f = forward
def get_face_orientation(results, img):
    img_h, img_w, img_c = img.shape
    face_3d = []
    face_2d = []

    text = 'no_orientation'
    direct = ' '

    if results.multi_face_landmarks:
        for face_landmarks in results.multi_face_landmarks:
            for idx, lm in enumerate(face_landmarks.landmark):
                if idx == 33 or idx == 263 or idx == 1 or idx == 61 or idx == 291 or idx == 199:
                    if idx == 1:
                        nose_2d = (lm.x * img_w, lm.y * img_h)
                        nose_3d = (lm.x * img_w, lm.y * img_h, lm.z * 8000)

                    x, y = int(lm.x * img_w), int(lm.y * img_h)

                    # Get the 2D Coordinates
                    face_2d.append([x, y])

                    # Get the 3D Coordinates
                    face_3d.append([x, y, lm.z])       
            
            # Convert it to the NumPy array
            face_2d = np.array(face_2d, dtype=np.float64)

            # Convert it to the NumPy array
            face_3d = np.array(face_3d, dtype=np.float64)

            # The camera matrix
            focal_length = 1 * img_w

            cam_matrix = np.array([ [focal_length, 0, img_h / 2],
                                    [0, focal_length, img_w / 2],
                                    [0, 0, 1]])

            # The Distance Matrix
            dist_matrix = np.zeros((4, 1), dtype=np.float64)

            # Solve PnP
            success, rot_vec, trans_vec = cv2.solvePnP(face_3d, face_2d, cam_matrix, dist_matrix)

            # Get rotational matrix
            rmat, jac = cv2.Rodrigues(rot_vec)

            # Get angles
            angles, mtxR, mtxQ, Qx, Qy, Qz = cv2.RQDecomp3x3(rmat)

            # Get the y rotation degree
            x = angles[0] * 360
            y = angles[1] * 360

            # print(y)

            # See where the user's head tilting
            if y < -10:
                text = "Looking Left"
                direct = 'l'
            elif y > 10:
                text = "Looking Right"
                direct = 'r'
            elif x < -10:
                text = "Looking Down"
                direct = 'd'
            else:
                text = "Forward"
                direct = 'f'


    return text, direct

# Returns the landmaks of a face given an image
def landmarks_detection(img, results, draw=False):
    img_height, img_width= img.shape[:2]
    # list[(x,y), (x,y)....]
    try:
        mesh_coord = [(int(point.x * img_width), int(point.y * img_height)) for point in results.multi_face_landmarks[0].landmark]

        if draw :
            [cv.circle(img, p, 2, (0,255,0), -1) for p in mesh_coord]

        # returning the list of tuples for each landmark 
        return mesh_coord
    except:
        print('No mesh')
        return []

# Euclaidean distance between two points
def euclaidean_distance(point, point1):
    x, y = point
    x1, y1 = point1
    distance = math.sqrt((x1 - x)**2 + (y1 - y)**2)
    return distance

# Calculates ratio of eyes (how open is the eye?)
# Returns average ratio, ratio for right eye and ratio for left eye
def blink_ratio(img, landmarks, right_indices, left_indices):
    # Right eyes 
    # horizontal line 
    rh_right = landmarks[right_indices[0]]
    rh_left = landmarks[right_indices[8]]
    # vertical line 
    rv_top = landmarks[right_indices[12]]
    rv_bottom = landmarks[right_indices[4]]

    # LEFT_EYE 
    # horizontal line 
    lh_right = landmarks[left_indices[0]]
    lh_left = landmarks[left_indices[8]]
    # vertical line 
    lv_top = landmarks[left_indices[12]]
    lv_bottom = landmarks[left_indices[4]]

    # Finding Distance Right Eye
    rhDistance = euclaidean_distance(rh_right, rh_left)
    rvDistance = euclaidean_distance(rv_top, rv_bottom)
    # Finding Distance Left Eye
    lvDistance = euclaidean_distance(lv_top, lv_bottom)
    lhDistance = euclaidean_distance(lh_right, lh_left)

    # Finding ratio of LEFT and Right Eyes
    if rvDistance != 0:
        ratio_r = rhDistance/rvDistance
    else:
        ratio_r = 0
    if lvDistance != 0:
        ratio_l = lhDistance/lvDistance
    else:
        ratio_l = 0
    ratio = (ratio_r+ratio_l)/2
    return ratio, ratio_r, ratio_l

# returns ratio depending on facial orientation
def oriented_ratio(ratio, ratio_r, ratio_l, direct_char):

    # left direction -> only right eye clearly visbile
    if direct_char == 'l':
        return ratio_r
    # right orientation -> only left eye clearly visible
    if direct_char == 'r':
        return ratio_l
    # for forward and down average ratio is used
    else:
        return ratio

# mesure time between blinks, if shorter than normal blink (150ms) then no "true" blink
# returns true_blink as boolean, new start time and the elapsed time
def get_true_bink(start):

    end = time.time()

    elapsed = end - start

    true_blink = True if elapsed > 0.15 else False
    #print(elapsed)

    start = time.time()
    return true_blink, start, elapsed

if __name__ == '__main__':

    # get participant from konsole input
    try:
        participant = sys.argv[1]
        print(participant)

    except:
        participant = "test"

    # Initiating to capture the video
    cap = cv2.VideoCapture(0)

    # blink counter
    blk_cntr = 0
    blk = False

    # ratios
    ratio, ratio_r, ratio_l = 0, 0 ,0

    # Open file for data storage
    file = open(participant + "_blink_detection.csv", 'w', newline='')
    writer = csv.writer(file, delimiter=';')
    writer.writerow(['time','blink','ratio', 'ratio_r', 'ratio_l', 'counted', 'orientation', 'still_closed', 'blink_length'])

    # start time for data saving and blink estimation
    start_time = time.time()

    # detect if eyes still closed
    still_closed = False
    true_blink = False

    # for blinking length
    blink_len = 0
    time_passed = time.time()


    # as long as video is captured
    while cap.isOpened():
        success, image = cap.read()

        # Flip the image horizontally for a later selfie-view display
        # Also convert the color space from BGR to RGB
        image = cv2.cvtColor(cv2.flip(image, 1), cv2.COLOR_BGR2RGB)

        # To improve performance
        image.flags.writeable = False
        
        # Get the result
        results = face_mesh.process(image)
        
        # To improve performance
        image.flags.writeable = True
        
        # Convert the color space from RGB to BGR
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)


        # detect face orientation
        direct_text, direct_char = get_face_orientation(results, image)

        #blink detection
        lm = landmarks_detection(image, results)
        if lm == []:
            ratio = 0
            ratio_r = 0
            ratio_l = 0
        
        else:
            ratio, ratio_r, ratio_l = blink_ratio(image, lm, RIGHT_EYE, LEFT_EYE)

        # decide which ratio to use based on face orientation TODO different Ratios
        ratio_correct = oriented_ratio(ratio, ratio_r, ratio_l, direct_char)

        # time stamps for blink length    
        if still_closed:
            blink_len += time.time() - INITAL_TIME - time_passed    
            
        else:
            blink_len = time.time() - INITAL_TIME - time_passed    

        time_passed = time.time() - INITAL_TIME

        if ratio_correct > BLINK_RATIO_THRESHOLD:
            #blk_cntr += 1
            #print(ratio_r, ratio_l)

            true_blink, start_time, _ = get_true_bink(start_time) # dont need elapsed time
            
            if true_blink:
                blk_cntr += 1
                still_closed = True

        else:
            still_closed = False
            true_blink = False


        # JUST DRAWING
        try:
            # horizontal line 
            rh_right = lm[RIGHT_EYE[0]]
            rh_left = lm[RIGHT_EYE[8]]
            # vertical line 
            rv_top = lm[RIGHT_EYE[12]]
            rv_bottom = lm[RIGHT_EYE[4]]
            # draw lines on right eyes 
            #cv2.line(image, rh_right, rh_left, (0, 255, 0), 2)
            cv2.line(image, rv_top, rv_bottom, (0, 255, 0), 2)
        except:
            pass


        # write file
        writer.writerow([datetime.now().strftime('%H:%M:%S.%f'), true_blink, ratio, ratio_r, ratio_l, blk_cntr, direct_char, still_closed, blink_len])


        # Display information on image
        cv2.putText(image, "Blinks: " + str(blk_cntr), (20, 60), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        cv2.putText(image, direct_text, (20, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
        cv2.imshow('Blink Detector', image)

        # use ESC to exit program
        if cv2.waitKey(5) & 0xFF == 27:
            break

file.close()

cap.release()
