# Blink Detector Sensitive to Facial Orientation

## Overview

This project implements a blink detector that is sensitive to facial orientation. The program uses a webcam to capture video, processes the video to detect blinks, and records various metrics in a CSV file. The blink detection is influenced by the orientation of the face, adjusting the detection criteria based on whether the face is looking forward, left, right, or downward.

## Installation
1. Clone the repository:
    ```sh
    git clone https://github.com/ansh-info/Eye-Blink-Detetction.git
    ```
2. Navigate to the project directory:
    ```sh
    cd Eye Blink Detetction
    ```
3. Install the required packages:
    ```sh
    pip install -r requirements.txt
    ```


### Additional Packages

- math (standard library)
- csv (standard library)
- time (standard library)
- datetime (standard library)
- sys (standard library)

### Hardware

- A functional webcam

## Usage

To use the blink detector, execute the program via the shell or terminal:

```bash
python blink_detector_face_orientation_datetime.py test_data
```

`test_data` is a placeholder for the participant ID. If none is provided, it defaults to `test`.

The program will open a video stream from your webcam, displaying the facial orientation and the number of detected blinks. To exit the program, press `ESC`.

### CSV Output

A CSV file will be created in the background containing the following columns:

- `time`: Time in seconds since the program started
- `blink`: Boolean, `True` if a blink is detected
- `ratio`: Average openness ratio of both eyes
- `ratio_r`: Openness ratio of the right eye
- `ratio_l`: Openness ratio of the left eye
- `counted`: Number of detected blinks
- `orientation`: Facial orientation (`l` for left, `r` for right, `d` for down, `f` for forward)
- `still_closed`: Boolean, `True` if the eyes remain closed (e.g., longer blink)
- `blink_length`: Time difference in seconds to the last measurement, accumulates if `still_closed` is `True`

### Blink Detection Based on Orientation

- Forward or Downward: Uses the average ratio of both eyes.
- Left: Uses the ratio of the right eye.
- Right: Uses the ratio of the left eye.

## Note

The program is sensitive to camera positioning. It works best when the camera is at the same height as the eyes. Higher camera angles still work well for forward orientation, but may incorrectly count blinks when looking left or right. Downward orientation is also more challenging for accurate blink detection.

The program performs better if the subject does not wear glasses.

## References

- [Eye Blink Detector and Counter with Mediapipe](https://medium.com/@aiphile/eyes-blink-detector-and-counter-mediapipe-a66254eb002c)
- [Head Pose Estimation using Python](https://towardsdatascience.com/head-pose-estimation-using-python-d165d3541600)

