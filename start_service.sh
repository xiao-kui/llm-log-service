#!/bin/bash
# Startup script: run backend and/or frontend
# Usage:
#   ./start.sh [mode]
# mode options:
#   all      -> start both backend and frontend
#   backend   -> start only backend
#   frontend  -> start only frontend
# Default: all

# Add current directory to PYTHONPATH
export PYTHONPATH=$PWD

# Fixed ports
BACKEND_PORT=9015
FRONTEND_PORT=8016

# Mode selection
MODE=${1:-all}

# Start backend
start_backend() {
    echo "[INFO] Starting backend (port: $BACKEND_PORT)"
    python -B ./backend/main.py --port $BACKEND_PORT &
}

# Start frontend
start_frontend() {
    echo "[INFO] Starting frontend (port: $FRONTEND_PORT)"
    streamlit run ./frontend/stui/home.py --server.port $FRONTEND_PORT &
    echo "Frontend available at: http://localhost:$FRONTEND_PORT"
}

case $MODE in
    all)
        start_backend
        start_frontend
        ;;
    backend)
        start_backend
        ;;
    frontend)
        start_frontend
        ;;
    *)
        echo "[ERROR] Invalid mode: $MODE"
        echo "Usage: ./start.sh [all|backend|frontend]"
        exit 1
        ;;
esac

echo "[INFO] Startup complete (mode: $MODE)"
