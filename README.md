# Smart Areca Leaf Plate Grading System 🍃🤖

A fully automated system that uses Deep Learning (CNN) and Computer Vision to grade and sort Areca leaf plates in real-time. [cite_start]This project integrates a Raspberry Pi 5 with a custom hardware conveyor setup to classify plates into **Grade A**, **Grade B**, or **Reject** categories[cite: 1, 92, 98].

## 🎥 Project Demonstration
[**Click Here to Watch the Demo Video**](https://drive.google.com/file/d/1CUQ8drktJN9TOQkyK4JCsKVKV-kkpD0X/view?usp=sharing)

---

## 📖 Abstract
[cite_start]Manual inspection of Areca leaf plates is often slow, subjective, and prone to error[cite: 64]. [cite_start]This project automates the quality assessment process using a **Convolutional Neural Network (ResNet50)** trained to identify texture, color uniformity, cracks, and shape defects[cite: 93].

[cite_start]The system captures images of plates moving on a conveyor belt, processes them on a **Raspberry Pi 5**, and mechanically sorts them into the correct bins using gear motors [cite: 96-98].

## ✨ Key Features
* [cite_start]**Real-Time Grading:** Classifies plates within 300-400 ms directly on the edge device[cite: 309].
* [cite_start]**High Accuracy:** Achieved over 90% accuracy using a fine-tuned ResNet50 model[cite: 699].
* [cite_start]**Automated Sorting:** Uses GPIO-controlled gear motors to physically divert plates into "Grade A", "Grade B", or "Reject" bins [cite: 597-598].
* [cite_start]**Cost-Effective Hardware:** Built using affordable components like Raspberry Pi and standard DC motors[cite: 258].

## 🛠️ Tech Stack

### [cite_start]Hardware [cite: 284-286]
* **Microcontroller:** Raspberry Pi 5 (8GB RAM recommended)
* **Camera:** Raspberry Pi Camera Module (or high-res USB Webcam)
* **Motors:** DC Gear Motors (12V) for sorting and conveyor belt
* **Driver:** L298N Motor Driver Module
* **Power Supply:** 12V DC Adapter (Motors) + 5V USB-C (Raspberry Pi)

### [cite_start]Software & Libraries [cite: 278-281]
* **Language:** Python 3
* **Deep Learning:** TensorFlow, Keras (ResNet50 Architecture)
* **Computer Vision:** OpenCV (`cv2`), NumPy
* **Hardware Control:** `gpiozero` or `RPi.GPIO`

## ⚙️ System Architecture
1.  [cite_start]**Image Acquisition:** The camera captures a top-down view of the plate on the conveyor[cite: 291].
2.  [cite_start]**Preprocessing:** Images are resized to 224x224, noise-reduced (Median Filter), and normalized[cite: 295].
3.  [cite_start]**Classification:** The image is passed to the `.h5` model (ResNet50) to predict the class[cite: 300, 304].
4.  **Sorting Logic:**
    * [cite_start]**Grade A:** Motor 1 activates -> Bin A[cite: 311].
    * [cite_start]**Grade B:** Motor 2 activates -> Bin B[cite: 311].
    * [cite_start]**Reject:** No motor action -> Rejection Tray[cite: 311].

## 🚀 Installation & Setup

1.  **Clone the Repository**
    ```bash
    git clone [https://github.com/YourUsername/smart-areca-grading-system.git](https://github.com/YourUsername/smart-areca-grading-system.git)
    cd smart-areca-grading-system
    ```

2.  **Install Dependencies**
    ```bash
    pip install tensorflow opencv-python numpy RPi.GPIO
    ```

3.  **Hardware Wiring**
    * Connect the L298N driver inputs to the defined GPIO pins on the Raspberry Pi.
    * Ensure the Camera module is enabled in `raspi-config`.

4.  **Run the System**
    ```bash
    python main_grading_script.py
    ```
    *(Note: Ensure your trained model `resnet_custom_preprocessed.h5` is in the project directory)*

## 👥 Team Members
[cite_start]**Department of Artificial Intelligence & Data Science** **SDM Institute of Technology, Ujire** [cite: 20-21]

* [cite_start]**Harsha G V Subedar** (4SU22AD016) [cite: 1006-1007]
* [cite_start]**Laxman Sannu Gouda** (4SU22AD025) [cite: 1011-1012]
* [cite_start]**Rahul Malatesh Sannapujar** (4SU22AD043) [cite: 1016-1017]
* [cite_start]**Sateerth Ganapati Palkar** (4SU23AD401) [cite: 1021-1022]

## 🎓 Acknowledgments
Special thanks to our project guide **Mrs. [cite_start]Veena Bhat** (Asst. Professor & HOD) for her supervision and guidance throughout this project [cite: 14-15].