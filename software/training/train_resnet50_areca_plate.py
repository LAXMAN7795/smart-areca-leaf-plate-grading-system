import tensorflow as tf
from tensorflow.keras.models import Model
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.applications import ResNet50
from tensorflow.keras.applications.resnet50 import preprocess_input
from tensorflow.keras.layers import GlobalAveragePooling2D, Dense, Dropout
from tensorflow.keras.callbacks import EarlyStopping
import os

# --- Configuration (Shared) ---
FINE_TUNE_LEARNING_RATE = 1e-5  # 0.00001
INITIAL_LR = 1e-3              # Initial Learning Rate
INITIAL_EPOCHS = 10            # Reduced epochs for faster demonstration
FINE_TUNE_EPOCHS = 10          # Additional epochs for fine-tuning
BATCH_SIZE = 32
image_size = (224, 224) 
num_classes = 3 
DATA_ROOT = r"D:\ArecaLeaf_Dataset"

# --- Data Generator Setup ---

train_datagen = ImageDataGenerator(
    preprocessing_function=preprocess_input,
    rotation_range=20, width_shift_range=0.2, height_shift_range=0.2,
    shear_range=0.2, zoom_range=0.2, horizontal_flip=True,
    validation_split=0.2
)
validation_datagen = ImageDataGenerator(
    preprocessing_function=preprocess_input,
    validation_split=0.2
)

train_generator = train_datagen.flow_from_directory(
    DATA_ROOT, target_size=image_size, batch_size=BATCH_SIZE,
    class_mode='categorical', subset='training', seed=42
)
validation_generator = validation_datagen.flow_from_directory(
    DATA_ROOT, target_size=image_size, batch_size=BATCH_SIZE,
    class_mode='categorical', subset='validation', seed=42
)

# --- PHASE 1: Build & Train (Base Frozen) ---

input_shape = (image_size[0], image_size[1], 3)

base_model = ResNet50(
    weights='imagenet', 
    include_top=False,           
    input_shape=input_shape      
)

# FREEZE the weights of the base model
base_model.trainable = False

# Build the new classification head
x = base_model.output
x = GlobalAveragePooling2D()(x)
x = Dense(512, activation='relu')(x)
x = Dropout(0.3)(x) 
output_layer = Dense(num_classes, activation='softmax')(x)

# Create the final model (Now 'model' is defined)
model = Model(inputs=base_model.input, outputs=output_layer)

# Compile with initial higher LR
model.compile(
    optimizer=Adam(learning_rate=INITIAL_LR),
    loss='categorical_crossentropy',
    metrics=['accuracy']
)

print("\n--- PHASE 1: Initial Training (Base Frozen) ---")
print(f"Starting Training for {INITIAL_EPOCHS} epochs...")

history_initial = model.fit(
    train_generator,
    epochs=INITIAL_EPOCHS,
    validation_data=validation_generator,
    verbose=1,
    callbacks=[EarlyStopping(monitor='val_loss', patience=5, restore_best_weights=True)]
)

# --- PHASE 2: Fine-Tuning (Upper Layers Unfrozen) ---

# 1. UNFREEZE the base model entirely first
base_model.trainable = True

# 2. SELECTIVE FREEZING: Freeze layers up to 'conv4_block1_0_conv' 
# (This preserves the most basic features)
freeze_until_layer_name = 'conv4_block1_0_conv'
set_trainable = False
for layer in base_model.layers:
    if layer.name == freeze_until_layer_name:
        set_trainable = True
    if set_trainable:
        layer.trainable = True
    else:
        layer.trainable = False


# 3. RECOMPILE with the extremely low learning rate
model.compile(
    optimizer=Adam(learning_rate=FINE_TUNE_LEARNING_RATE), # <-- Low LR is key!
    loss='categorical_crossentropy',
    metrics=['accuracy']
)

print("\n--- PHASE 2: Fine-Tuning Configuration ---")
print(f"Total layers in ResNet base: {len(base_model.layers)}")
print(f"Layers set to be trainable (Fine-Tuning): {sum([layer.trainable for layer in base_model.layers])}")
print("---------------------------------------")


# 4. CONTINUE TRAINING
print(f"\nStarting Fine-Tuning for an additional {FINE_TUNE_EPOCHS} epochs...")

history_fine_tune = model.fit(
    train_generator,
    epochs=INITIAL_EPOCHS + FINE_TUNE_EPOCHS, # Total Epochs = 20
    initial_epoch=history_initial.epoch[-1] + 1, # Start from the next epoch after initial training
    validation_data=validation_generator,
    verbose=1,
    callbacks=[EarlyStopping(monitor='val_loss', patience=10, restore_best_weights=True)]
)

# --- Save Final Model ---
model.save('arecanut_resnet_fine_tuned.h5')
print("\nFinal fine-tuned model saved successfully!")