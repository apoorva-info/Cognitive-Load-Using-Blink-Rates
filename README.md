# 📊 Assessing Cognitive Load Using Blink Rates and Performance Metrics

This repository contains the code, data, and results associated with the research project "Assessing Cognitive Load Using Blink Rates and Performance Metrics in Digital Span Tasks." The project explores the relationship between cognitive load, as measured by blink rates, and performance accuracy across different levels of task difficulty.

## 🗂 Table of Contents
- [Introduction](#introduction)
- [Methods](#methods)
- [Results](#results)
- [Visualizations](#visualizations)
- [Usage](#usage)
- [Contributors](#contributors)
- [References](#references)

## 🧠 Introduction

In this study, we aimed to assess the cognitive load of users in a controlled environment using the webcam of their personal device. We evaluated the relationship between cognitive load and performance metrics during digital span tasks, where participants were asked to memorize and recall sequences of digits. Blink rates were monitored as a non-invasive indicator of cognitive load.

## 🛠 Blink Detection Sensitivity

This project incorporates a blink detection system that is sensitive to facial orientation. The system uses a webcam to monitor blinks and takes into account the orientation of the participant's face to ensure accurate detection. This feature is particularly useful in ensuring reliable data collection even when the participant's facial orientation varies slightly during the task.

## 🛠 Methods

### 🔧 Experimental Setup

- **Participants**: 10 participants aged between 20 and 30 years, with an equal gender distribution.
- **Equipment**: Standard computing device with an integrated camera and custom software for blink detection and digital span testing.
- **Conditions**: The experiment included three conditions:
  1. **Baseline**: Resting state to establish a baseline blink rate.
  2. **Task**: Performing the digital span test.
  3. **Recovery**: Resting state post-task to observe recovery patterns.

## 🧪 Experiment Procedure

### How the Digit Span Task Works

1. **Presentation**: The user is presented with a fixation cross followed by a random sequence of numbers displayed one by one.
2. **Display Duration**: Each number appears for 1 second, followed by a 0.1-second blank screen to distinguish between numbers.
3. **Input**: After the sequence, the user is asked to type the list into an input space and confirm the entry by pressing the spacebar.
4. **Trial**: Each sequence presentation and subsequent input is considered a single trial.
5. **Conditions**: The experiment includes three conditions based on the length of the number sequence:
   - Easy (3 digits)
   - Medium (5 digits)
   - Hard (8 digits)
6. **Repetition**: The entire process is repeated across multiple trials to ensure data reliability.

### Blink Detection Procedure

- The blink detection software operates concurrently with the digit span task.
- The system monitors the participant's blinks during each condition, recording blink frequency and correlating it with task difficulty.
- The software can be executed via the terminal or shell using the following command:
  ```bash
  python .\blink_detector_face_orientation_datetime.py <participant_id>
  ```
  Replace `<participant_id>` with the participant's identifier. If none is provided, it defaults to "test."  


### 📊 Data Processing

- **Blink Rate Monitoring**: Blink rates were monitored throughout the task using a Python script executed via Spyder IDE.
- **Accuracy Measurement**: Each participant's accuracy was calculated by comparing the number of digits correctly recalled with the total number displayed.
- **Data Analysis**: The data was cleaned, and outliers were removed following the guidelines by Leys et al. (2013). Mean and standard deviation of accuracies were calculated for each condition.

## 📈 Results

### 🎯 Performance Accuracy

- **Easy Condition**: Average accuracy of 58.89% with a high standard deviation, indicating variability in performance.
- **Medium Condition**: Average accuracy decreased to 45.64%.
- **Hard Condition**: The most challenging condition with an average accuracy of 28.21%.

### 👁️ Blink Rates

- **Easy Condition**: Average blink rate of 160.5 blinks per minute.
- **Medium Condition**: Increase in blink rate, indicating higher cognitive load.
- **Hard Condition**: Varied response with some participants showing stabilized or decreased blink rates, suggesting different cognitive strategies.

## 🖼 Visualizations

### Average Blink Counts for Each Digital Count
![Average Accuracy with Standard Deviation for Each Participant.png](images/Average%20Accuracy%20with%20Standard%20Deviation%20for%20Each%20Participant.png)

### Overall Accuracy by Condition
![Average Blink Count for Each Digital Count](images/Average%20Blink%20Count%20for%20Each%20Digital%20Count.png)

These visualizations highlight the relationship between task difficulty, cognitive load, and participant performance. The increase in blink rates from easy to medium tasks suggests greater cognitive effort, while the drop in accuracy with increasing task difficulty is consistent with existing cognitive load theories.

## 🚀 Usage

### 🔧 Prerequisites
- Python 3.9 or later
- Required libraries: `opencv-python`, `mediapipe`, `numpy`, `math`, `csv`, `time`, `datetime`, `sys`
- A functional webcam for real-time blink detection

### Running the Code

1. Clone the repository:
   ```sh
   git clone https://github.com/yourusername/assessing-cognitive-load.git
   cd assessing-cognitive-load
   jupyter notebook Assessing_Cognitive_Load.ipynb
   ```

## References

-  Gorin, H., et al. (2024). A Review of the Use of Gaze and Pupil Metrics to Assess Mental Workload.
-  Radhakrishnan, V., et al. (2023). Using Pupillometry and Gaze-Based Metrics for Understanding Drivers’ Mental Workload.
-  Mathôt, S., et al. (2023). Methods in Cognitive Pupillometry.
-  Gagl, B., et al. (2011). Systematic Influence of Gaze Position on Pupil Size Measurement.
-  Culemann, W., et al. (2023). Pupil vs. Eyelid: Evaluating the Accuracy of Blink Detection.