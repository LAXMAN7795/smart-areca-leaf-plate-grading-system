import tensorflow as tf
from preprocessing.image_preprocessing import preprocess_image

# Load trained model
model = tf.keras.models.load_model("model/arecanut_resnet_fine_tuned.h5")

# Class labels
class_labels = {
    0: "Grade A",
    1: "Grade B",
    2: "Reject"
}

# Preprocess image
processed_image = preprocess_image("sample_plate.jpg")

# Predict
prediction = model.predict(processed_image)
predicted_class = class_labels[prediction.argmax()]

print("Predicted Grade:", predicted_class)
