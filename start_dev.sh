#!/bin/bash

cd ai-service
source venv/bin/activate
python app.py &
AI_PID=$!
cd ..

sleep 2

cd ui-service
source venv/bin/activate
python app.py &
UI_PID=$!
cd ..

wait $AI_PID $UI_PID 