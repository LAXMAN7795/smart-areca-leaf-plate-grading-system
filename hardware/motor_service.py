import socket
import sys
import time
from gpiozero import Motor, PWMOutputDevice
from signal import signal, SIGINT

# --- CONFIGURATION ---
HOST = '127.0.0.1'
PORT = 65432

# 1. Conveyor Belt Pins (L298N Channel 1)
CONVEYOR_IN1 = 17
CONVEYOR_IN2 = 27
CONVEYOR_ENA = 22
CONVEYOR_SPEED = 1.0

# 2. Sorter A Pins (Grade A Pusher)
# Connect to a 2nd Motor Driver
SORTER_A_IN1 = 5
SORTER_A_IN2 = 6
SORT_SPEED = 1.0
PUSH_TIME = 0.5 # Seconds to push out
RETRACT_TIME = 0.5 # Seconds to pull back

# 3. Sorter B Pins (Grade B Pusher)
SORTER_B_IN1 = 23
SORTER_B_IN2 = 24

# --- HARDWARE INITIALIZATION ---
print("🔌 Initializing Automation Hardware...")

try:
    # Setup Conveyor
    conveyor_enable = PWMOutputDevice(CONVEYOR_ENA)
    conveyor = Motor(forward=CONVEYOR_IN1, backward=CONVEYOR_IN2)
    
    # Setup Sorters (Assuming simple DC motors via Driver)
    # Note: We don't use PWM Enable for sorters for simplicity, just full speed 
    # (or you can add Enable pins if your driver needs them)
    sorter_a = Motor(forward=SORTER_A_IN1, backward=SORTER_A_IN2)
    sorter_b = Motor(forward=SORTER_B_IN1, backward=SORTER_B_IN2)
    
    print("   -> Hardware Ready: Conveyor + 2 Sorters")

except Exception as e:
    print(f"❌ Hardware Error: {e}")
    sys.exit(1)

# --- ACTION FUNCTIONS ---

def conveyor_run():
    conveyor_enable.value = CONVEYOR_SPEED
    conveyor.backward() # or forward(), depending on wiring
    print("   [CONVEYOR] ON")

def conveyor_stop():
    conveyor.stop()
    conveyor_enable.off()
    print("   [CONVEYOR] OFF")

def trigger_sorter(sorter, name):
    """
    Runs the motor forward to push, then backward to retract.
    """
    print(f"   [SORTER {name}] Pushing...")
    sorter.forward(speed=SORT_SPEED)
    time.sleep(PUSH_TIME)
    
    print(f"   [SORTER {name}] Retracting...")
    sorter.backward(speed=SORT_SPEED)
    time.sleep(RETRACT_TIME)
    
    sorter.stop()
    print(f"   [SORTER {name}] Done")

# --- SOCKET SERVER LOOP ---
def run_server():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind((HOST, PORT))
        s.listen()
        print(f"🚀 Service Listening on {HOST}:{PORT}")
        
        conn, addr = s.accept()
        with conn:
            print(f"✅ Logic Connected: {addr}")
            
            while True:
                data = conn.recv(1024)
                if not data: break
                
                cmd = data.decode('utf-8').strip()
                
                # --- COMMAND HANDLING ---
                if cmd == "START":
                    conveyor_run()
                elif cmd == "STOP":
                    conveyor_stop()
                elif cmd == "EXIT":
                    conveyor_stop()
                    break
                
                # Sorting Logic
                elif cmd == "SORT_A":
                    # We run sorting in a simplified blocking way here. 
                    # For advanced usage, this could be threaded.
                    trigger_sorter(sorter_a, "A")
                    
                elif cmd == "SORT_B":
                    trigger_sorter(sorter_b, "B")
                    
                elif cmd == "REJECT":
                    print("   [INFO] Reject - Letting plate pass")

def cleanup(signal, frame):
    print("\n⚠️ Emergency Stop...")
    conveyor_stop()
    sorter_a.stop()
    sorter_b.stop()
    sys.exit(0)

signal(SIGINT, cleanup)

if __name__ == "__main__":
    run_server()
