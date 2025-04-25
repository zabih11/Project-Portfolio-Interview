This repository showcases two key projects demonstrating my experience with robotics, machine learning, and data science.

---
## 🤖 Assistive Autonomous Robot with Computer Vision, Speech Recognition, and SLAM

### Overview
An advanced robotics project integrating:

- **Real-time object detection:**  
  Powered by a custom YOLOv5 model and PyTorch for robust and accurate identification of common household objects.
  
- **Hand gesture control:**  
  Utilises MediaPipe to enable intuitive manipulation of the robot’s arm and grabber. Your hand and arm movements are directly interpreted as joint angles, allowing the robot to replicate your motions.

- **Object grabbing and retrieval pipeline:**  
  The robot autonomously detects target items, approaches them, uses its grabber to securely grasp them, and places them in a designated holder or basket.

- **Voice command processing:**  
  Seamlessly integrated through Google Speech-to-Text for recognising natural language commands. Commands such as "grab the orange" or "manual" automatically switch the robot to corresponding modes.

- **Simultaneous Localisation and Mapping (SLAM):**  
  Utilises a LiDAR sensor to create accurate maps of its environment for autonomous navigation and collision avoidance.

- **Integration with ROS2:**  
  Allows for distributed robotic control and real-time navigation through custom nodes and configurations.

### Features
The system demonstrates multimodal AI capabilities for:
- **Follow-Me Functionality:** Using SLAM data and holistic pose tracking, the robot can follow you while maintaining a safe distance.
- **Multimodal Navigation:** The robot autonomously scans rooms, maps the environment, and plans paths to avoid obstacles.
- **Natural Control Modes:** Switch seamlessly between manual hand gesture control, object retrieval mode, and autonomous follow-me mode.

---
## 🔧 Skills and Technologies Used

- **Python** for developing key algorithms and integration scripts.
- **ROS2** for distributed control, SLAM, and navigation planning.
- **OpenCV** for computer vision tasks and user interface development.
- **YOLOv5** for custom object detection and recognition.
- **SpeechRecognition** (Google Speech-to-Text API) for voice command processing.
- **MediaPipe** for hand gesture and holistic tracking.
- **SLAM** using a LiDAR sensor for mapping and localisation.

---

These were the core technologies employed to bring the project’s functionality to life, combining vision, voice, and navigation seamlessly.
---

> 📂 [Explore the project](./Assistive-Autonomous-Robot-With-Computer-Vision-Speech-Recognition-and-SLAM)
---

## 📈 Stock Trend Forecasting

A machine learning pipeline for forecasting stock price movements:

- **Data retrieval and feature engineering** from historical financial data
- **Model training** with LSTM and technical indicators
- **Model evaluation** using accuracy, F1 score, and loss tracking
- **Jupyter Notebooks** for visualization and interactive experimentation

This project demonstrates time series prediction, classification, and data visualization techniques in finance.

---
> 📂 [Explore the project](./Stock-Trend_Forecasting)

---
