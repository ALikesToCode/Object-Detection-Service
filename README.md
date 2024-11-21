# Object Detection Microservice

A modern microservice-based object detection system using YOLOv8 and Flask. The system provides real-time object detection through a user-friendly web interface.

## Features

- Real-time object detection using YOLOv8
- Modern, responsive web interface
- Drag-and-drop image upload
- Image preview and fullscreen view
- Download detected images
- JSON output of detections
- Production-ready Docker deployment with Gunicorn
- Development environment setup

## Prerequisites

- Python 3.9+
- Docker and Docker Compose (for containerized deployment)
- Git

## Quick Start

### Production Deployment

1. Clone the repository:
```bash
git clone https://github.com/ALikesToCode/Object-Detection-Service-AIMONK/
cd Object-Detection-Service-AIMONK
```

2. Start services in production mode:
```bash
chmod +x start_prod.sh
./start_prod.sh
```

3. Access the application at: http://localhost:5000

To view logs:
```bash
docker-compose logs -f
```

To stop services:
```bash
docker-compose down
```

### Development Mode

1. Setup the development environment:
```bash
chmod +x dev_setup.sh
./dev_setup.sh
```

2. Start the services:
```bash
# Terminal 1 (AI Service)
cd ai-service
source venv/bin/activate
python app.py

# Terminal 2 (UI Service)
cd ui-service
source venv/bin/activate
python app.py
```

3. Access the application at: http://localhost:5000

## Project Structure

```
object-detection-service/
├── ai-service/               # AI detection service
│   ├── app.py               # Main AI service application
│   ├── utils/               # Utility functions
│   │   └── detection.py     # Detection logic
│   └── uploads/             # Processed images
├── ui-service/              # User interface service
│   ├── app.py              # Main UI application
│   ├── static/             # Static files
│   │   ├── css/
│   │   ├── js/
│   │   └── uploads/        # Uploaded images
│   └── templates/          # HTML templates
├── docker-compose.yml      # Docker composition
├── start_prod.sh          # Production startup script
└── dev_setup.sh          # Development setup script
```

## Deployment Modes

### Production Mode
- Uses Gunicorn WSGI server
- Multiple worker processes
- Runs as a background service
- Proper signal handling
- Production-grade logging

### Development Mode
- Uses Flask development server
- Debug mode enabled
- Auto-reloading
- Detailed error pages

## API Endpoints

### UI Service (Port 5000)
- `GET /`: Main web interface
- `POST /upload`: Upload and process image

### AI Service (Port 5001)
- `POST /detect`: Process image and return detections
- `GET /images/<filename>`: Retrieve processed images

## Environment Variables
- UI Service:
  - `FLASK_ENV`: Development/Production mode
  - `AI_SERVICE_URL`: AI service endpoint
  - `UPLOAD_FOLDER`: Upload directory path

- AI Service:
  - `FLASK_ENV`: Development/Production mode
  - `UPLOAD_FOLDER`: Directory for processed images

## Troubleshooting

### Common Issues
1. Port conflicts:
```bash
# Check ports
lsof -i :5000
lsof -i :5001
```

2. Permission issues:
```bash
# Fix permissions
chmod 777 ui-service/static/uploads
chmod 777 ai-service/uploads
```

3. Docker issues:
```bash
# Reset containers
docker-compose down
docker system prune -f
docker-compose up --build
```

4. Logs not showing:
```bash
# View real-time logs
docker-compose logs -f

# View specific service logs
docker-compose logs -f ui-service
docker-compose logs -f ai-service
```

## Contributing

1. Fork the repository
2. Create your feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License.


