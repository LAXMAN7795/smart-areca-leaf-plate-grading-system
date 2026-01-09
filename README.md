# Smart Areca Leaf Plate Grading System 🍃🤖

A fully automated system that uses Deep Learning (CNN) and Computer Vision to grade and sort Areca leaf plates in real-time. This project integrates a Raspberry Pi 5 with a custom hardware conveyor setup to classify plates into **Grade A**, **Grade B**, or **Reject** categories.

## 🎥 Project Demonstration
[**Click Here to Watch the Demo Video**](https://drive.google.com/file/d/1CUQ8drktJN9TOQkyK4JCsKVKV-kkpD0X/view?usp=sharing)

---

## 📖 Abstract
Manual inspection of Areca leaf plates is often slow, subjective, and prone to error. This project automates the quality assessment process using a **Convolutional Neural Network (ResNet50)** trained to identify texture, color uniformity, cracks, and shape defects.

The system captures images of plates moving on a conveyor belt, processes them on a **Raspberry Pi 5**, and mechanically sorts them into the correct bins using gear motors.

## ✨ Key Features
* **Real-Time Grading:** Classifies plates within 300-400 ms directly on the edge device.
* **High Accuracy:** Achieved over 90% accuracy using a fine-tuned ResNet50 model.
* **Automated Sorting:** Uses GPIO-controlled gear motors to physically divert plates into "Grade A", "Grade B", or "Reject" bins.
* **Cost-Effective Hardware:** Built using affordable components like Raspberry Pi and standard DC motors.

## 🛠️ Tech Stack

### Hardware
* **Microcontroller:** Raspberry Pi 5 (8GB RAM recommended)
* **Camera:** Raspberry Pi Camera Module (or high-res USB Webcam)
* **Motors:** DC Gear Motors (12V) for sorting and conveyor belt
* **Driver:** L298N Motor Driver Module
* **Power Supply:** 12V DC Adapter (Motors) + 5V USB-C (Raspberry Pi)

### Software & Libraries
* **Language:** Python 3
* **Deep Learning:** TensorFlow, Keras (ResNet50 Architecture)
* **Computer Vision:** OpenCV (`cv2`), NumPy
* **Hardware Control:** `gpiozero` or `RPi.GPIO`

## ⚙️ System Architecture
1.  **Image Acquisition:** The camera captures a top-down view of the plate on the conveyor.
2.  **Preprocessing:** Images are resized to 224x224, noise-reduced (Median Filter), and normalized.
3.  **Classification:** The image is passed to the `.h5` model (ResNet50) to predict the class.
4.  **Sorting Logic:**
    * **Grade A:** Motor 1 activates -> Bin A.
    * **Grade B:** Motor 2 activates -> Bin B.
    * **Reject:** No motor action -> Rejection Tray.

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
**Department of Artificial Intelligence & Data Science**
**SDM Institute of Technology, Ujire**

* **Harsha G V Subedar** (4SU22AD016)
* **Laxman Sannu Gouda** (4SU22AD025)
* **Rahul Malatesh Sannapujar** (4SU22AD043)
* **Sateerth Ganapati Palkar** (4SU23AD401)

## 🎓 Acknowledgments
Special thanks to our project guide **Mrs. Veena Bhat** (Asst. Professor & HOD) for her supervision and guidance throughout this project.
