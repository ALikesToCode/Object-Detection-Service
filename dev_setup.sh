#!/bin/bash

echo "Creating virtual environments..."
python -m venv ui-service/venv
python -m venv ai-service/venv

echo "Setting up UI service..."
source ui-service/venv/bin/activate
pip install -r ui-service/requirements.txt
deactivate

echo "Setting up AI service..."
source ai-service/venv/bin/activate
pip install -r ai-service/requirements.txt
deactivate

echo "Creating upload directories..."
mkdir -p ui-service/static/uploads
mkdir -p ai-service/uploads

echo "Setting permissions..."
chmod 777 ui-service/static/uploads
chmod 777 ai-service/uploads

echo "Creating development environment files..."
echo "FLASK_ENV=development
FLASK_DEBUG=1
AI_SERVICE_URL=http://localhost:5001
UPLOAD_FOLDER=static/uploads" > ui-service/.env.dev

echo "FLASK_ENV=development
FLASK_DEBUG=1
UPLOAD_FOLDER=uploads
MODEL_PATH=yolov8n.pt" > ai-service/.env.dev

echo "Setup complete! To start the services:"
echo "1. Terminal 1: cd ui-service && source venv/bin/activate && python app.py"
echo "2. Terminal 2: cd ai-service && source venv/bin/activate && python app.py" 