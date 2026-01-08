import cv2
import numpy as np
from tensorflow.keras.applications.resnet50 import preprocess_input

def preprocess_image(image_path):
    """
    Preprocessing pipeline for Areca Leaf Plate Grading System

    Steps:
    1. Read image using OpenCV
    2. Resize to 224x224
    3. Apply median filtering for noise removal
    4. Convert to float32
    5. Apply ImageNet normalization (ResNet50)
    6. Expand dimensions for CNN input
    """

    # 1. Read image (BGR format)
    image = cv2.imread(image_path)
    if image is None:
        raise ValueError("Error loading image")

    # 2. Resize image to 224x224
    image = cv2.resize(image, (224, 224))

    # 3. Median filtering (noise removal)
    image = cv2.medianBlur(image, 3)

    # 4. Convert to float32
    image = image.astype(np.float32)

    # 5. ImageNet normalization (ResNet50)
    image = preprocess_input(image)

    # 6. Expand dimensions -> (1, 224, 224, 3)
    image = np.expand_dims(image, axis=0)

    return image
