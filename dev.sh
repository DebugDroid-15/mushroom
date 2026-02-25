#!/bin/bash
# Development helper script
# Use locally for testing, not on Raspberry Pi

case "$1" in
    "install")
        echo "Installing dependencies for development..."
        python3 -m venv venv
        source venv/bin/activate
        pip install -r requirements.txt
        echo "✓ Installation complete"
        echo "Activate virtual environment: source venv/bin/activate"
        ;;
    
    "run")
        echo "Starting Flask server..."
        source venv/bin/activate
        python3 app.py
        ;;
    
    "test")
        echo "Testing Modbus sensor..."
        source venv/bin/activate
        python3 modbus_sensor.py
        ;;
    
    "format")
        echo "Formatting Python code..."
        source venv/bin/activate
        python3 -m py_compile modbus_sensor.py app.py
        echo "✓ Code syntax valid"
        ;;
    
    "clean")
        echo "Cleaning up..."
        rm -rf venv __pycache__ *.pyc
        echo "✓ Cleanup complete"
        ;;
    
    *)
        echo "Soil Monitoring System - Development Helper"
        echo ""
        echo "Usage: $0 {install|run|test|format|clean}"
        echo ""
        echo "Commands:"
        echo "  install   - Setup Python virtual environment and dependencies"
        echo "  run       - Start Flask development server"
        echo "  test      - Test Modbus sensor connection"
        echo "  format    - Check Python code syntax"
        echo "  clean     - Remove virtual environment and cache"
        echo ""
        exit 1
        ;;
esac
