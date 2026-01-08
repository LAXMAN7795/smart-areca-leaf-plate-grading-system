import cv2
import numpy as np
import time
import socket
import sys
import tensorflow as tf
from tensorflow.keras.models import load_model
from tensorflow.keras.applications.resnet50 import preprocess_input

# --- CONFIGURATION ---
MODEL_PATH = "arecanut_resnet_fine_tuned.h5"
HOST = '127.0.0.1'
PORT = 65432
TARGET_SIZE = (224, 224)
CLASS_LABELS = ["Grade A", "Grade B", "Reject"]

# --- PHYSICAL TIMING (TUNE THESE!) ---
# Time for plate to travel from Camera to Sorter B (while belt is running)
DELAY_TO_B =  1.5
# Detection Logic
BINARY_THRESHOLD = 100
MIN_AREA = 5000
BORDER_MARGIN = 5
IDLE_TIMEOUT = 30  

# --- 1. CONNECT TO MOTOR SERVICE ---
print("⏳ Connecting to Hardware Service...")
try:
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((HOST, PORT))
    print("✅ Connected to Motor Hardware")
except ConnectionRefusedError:
    print("❌ Error: Run 'motor_service.py' first!")
    sys.exit(1)

def send_cmd(cmd):
    try:
        sock.sendall(cmd.encode('utf-8'))
    except:
        pass

# --- 2. AI & CAMERA ---
print("⏳ Loading Model...")
model = load_model(MODEL_PATH)
print("✅ Model Loaded")

def prepare_image(crop):
    img = cv2.resize(crop, TARGET_SIZE)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    img = cv2.medianBlur(img, 3)
    img = np.expand_dims(img, axis=0).astype(np.float32)
    return preprocess_input(img)

def check_full_plate(frame):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    _, thresh = cv2.threshold(blurred, BINARY_THRESHOLD, 255, cv2.THRESH_BINARY)
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    if not contours: return False, None
    c = max(contours, key=cv2.contourArea)
    if cv2.contourArea(c) < MIN_AREA: return False, None
    
    x, y, w, h = cv2.boundingRect(c)
    h_img, w_img = frame.shape[:2]
    
    if (x <= BORDER_MARGIN or y <= BORDER_MARGIN or 
        x + w >= w_img - BORDER_MARGIN or y + h >= h_img - BORDER_MARGIN):
        return False, None
    
    cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
    cv2.putText(frame, "FULL PLATE", (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
    return True, frame[y:y+h, x:x+w]

def find_working_camera():
    for i in range(5):
        cap = cv2.VideoCapture(i)
        if cap.isOpened():
            ret, _ = cap.read()
            cap.release()
            if ret: return i
    return None

# --- 3. MAIN LOOP ---
def main():
    cam_idx = find_working_camera()
    if cam_idx is None: return

    cap = cv2.VideoCapture(cam_idx)
    cap.set(3, 640)
    cap.set(4, 480)

    print("🚀 System Started")
    
    # START CONVEYOR ONCE - IT WILL NOT STOP
    send_cmd("START") 
    last_plate_time = time.time()

    try:
        while True:
            ret, frame = cap.read()
            if not ret: break

            # Timeout Logic
            if time.time() - last_plate_time > IDLE_TIMEOUT:
                print("🛑 Idle Timeout - Stopping")
                break

            is_ready, plate_crop = check_full_plate(frame)

            if is_ready:
                last_plate_time = time.time()
                
                print("📸 Plate Detected (Processing on-the-fly...)")
                
                # NOTE: Motor is NOT stopped.
                # We use 'plate_crop' directly because the belt is moving.
                # If we tried to capture a new frame now, the plate would be gone.
                
                # 1. Predict
                input_tensor = prepare_image(plate_crop)
                preds = model.predict(input_tensor, verbose=0)
                idx = np.argmax(preds[0])
                label = CLASS_LABELS[idx]
                conf = preds[0][idx] * 100
                
                text = f"{label} ({conf:.1f}%)"
                print(f"✅ Result: {text}")
                
                # Show result on the live feed
                cv2.putText(frame, text, (20, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255), 3)
                cv2.imshow("Grading System", frame)
                cv2.waitKey(1)

                # --- SORTING LOGIC (Motor Keeps Running) ---
                
                if label == "Grade A":
                    print("   -> Sorter A: Triggering Immediately")
                    send_cmd("SORT_A")
                    # Motor runs in background, conveyor continues

                elif label == "Grade B":
                    print(f"   -> Sorter B: Waiting {DELAY_TO_B}s for travel...")
                    # We simply wait while the conveyor moves the plate to position B
                    time.sleep(DELAY_TO_B)
                    
                    print("   -> Sorter B: Triggering")
                    send_cmd("SORT_B")

                else: # Reject
                    print("   -> Reject: Letting it pass")
                    pass

                # Brief pause to ensure the CURRENT plate leaves the camera frame completely
                # This prevents grading the same plate 5 times while it slides past.
                time.sleep(1.5) 
                
                print("🔄 Ready for next plate...")
                continue

            cv2.imshow("Grading System", frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

    finally:
        # ONLY STOP WHEN PROGRAM EXITS
        send_cmd("EXIT")
        cap.release()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
