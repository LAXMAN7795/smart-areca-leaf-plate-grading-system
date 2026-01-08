#!/bin/bash

# --- CONFIGURATION ---
# UPDATE THESE TWO PATHS TO MATCH YOUR RASPBERRY PI SETUP
PROJECT_DIR="/home/arecanutgrading/Arecanut_Project"
VENV_PATH="/home/arecanutgrading/Arecanut_Project/ai_arecanut"

echo "==========================================="
echo "   STARTING ARECANUT SORTING SYSTEM"
echo "==========================================="

# 1. Start Motor Service (Sudo Mode) in Background
# We use 'sudo' because gpiozero needs hardware access
echo "[1/3] Starting Hardware Service (Sudo)..."
sudo python3 "$PROJECT_DIR/motor_service.py" &
MOTOR_PID=$! # Save Process ID to kill it later

# Wait 3 seconds for hardware to initialize and socket to open
sleep 3

# 2. Activate Virtual Environment
# This allows us to use TensorFlow/OpenCV without installing them globally
echo "[2/3] Activating AI Environment..."
source "$VENV_PATH/bin/activate"

# 3. Start Grading Logic
# This runs in the foreground. When you stop this, the script continues to cleanup.
echo "[3/3] Starting Grading Logic..."
python3 "$PROJECT_DIR/grading_logic.py"

# --- CLEANUP (Runs when Python script exits) ---
echo "==========================================="
echo "   SHUTTING DOWN"
echo "==========================================="
# Kill the background motor service so it doesn't keep running
sudo kill $MOTOR_PID
