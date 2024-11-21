# **Object Detection Service**

## **Overview**
This project implements an object detection microservice composed of two main components:
1. **UI Service**: Allows users to upload images for detection via a web interface.
2. **AI Service**: Processes uploaded images using an object detection model (e.g., YOLO) and returns the results in JSON format along with a processed image containing bounding boxes.

The services communicate seamlessly to provide a complete object detection pipeline.

---

## **Project Structure**

```
object-detection-service/
├── docker-compose.yml     # Orchestrates the two services
├── README.md              # Documentation
├── ui-service/            # UI Service folder
│   ├── Dockerfile         # Docker configuration for UI Service
│   ├── requirements.txt   # Dependencies for UI Service
│   ├── app.py             # Flask application for the UI
│   ├── static/            # Static files
│   │   ├── css/           # CSS files
│   │   │   └── style.css
│   │   ├── js/            # JavaScript files
│   │   │   └── main.js
│   │   └── uploads/       # Uploaded images
│   └── templates/         # HTML templates
│       └── index.html
└── ai-service/            # AI Service folder
    ├── Dockerfile         # Docker configuration for AI Service
    ├── requirements.txt   # Dependencies for AI Service
    ├── app.py             # Flask application for AI processing
    ├── uploads/           # Directory for AI processed images
    └── utils/             # Utility functions
        └── detection.py   # Object detection logic
```

---

## **Setup Instructions**

### **1. Clone the Repository**

```bash
git clone <repository-url>
cd object-detection-service
```

---

### **2. Create Upload Directories**

```bash
mkdir -p ui-service/static/uploads
mkdir -p ai-service/uploads
chmod 777 ui-service/static/uploads
chmod 777 ai-service/uploads
```

---

### **3. Run with Docker**

1. **Build the Docker Containers**:
   ```bash
   docker-compose build
   ```

2. **Start the Services**:
   ```bash
   docker-compose up
   ```

---

### **4. Run Locally (Without Docker)**

#### **UI Service**
1. Navigate to the UI Service folder:
   ```bash
   cd ui-service
   ```
2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Start the Flask app:
   ```bash
   python app.py
   ```

#### **AI Service**
1. Navigate to the AI Service folder:
   ```bash
   cd ai-service
   ```
2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Start the Flask app:
   ```bash
   python app.py
   ```

---

### **5. Troubleshooting**

#### **Check for Port Conflicts**
- Verify if ports `5000` (UI Service) or `5001` (AI Service) are in use:
  ```bash
  lsof -i :5000
  lsof -i :5001
  ```

- Kill the conflicting processes if needed:
  ```bash
  kill -9 <PID>
  ```

#### **Rebuild Containers**
If any issues arise during Docker runs:
1. Stop and remove all containers:
   ```bash
   docker-compose down
   docker system prune -f
   ```
2. Rebuild and start the containers:
   ```bash
   docker-compose up --build
   ```

#### **Fix Upload Directory Permissions**
Ensure the upload directories have the correct permissions:
```bash
sudo chown -R $USER:$USER ui-service/static/uploads
sudo chown -R $USER:$USER ai-service/uploads
```

---

## **Usage**

1. **Access the UI**: Open the UI service in your browser at `http://localhost:5000`.
2. **Upload an Image**: Use the interface to upload an image.
3. **View Results**: 
   - JSON output with detected objects.
   - Processed image with bounding boxes (saved in the appropriate upload directories).

---

## **Development Notes**

- The UI service is built with Flask and serves a simple interface for uploading images.
- The AI service leverages a lightweight object detection model (e.g., YOLO) for image processing.
- Both services communicate via REST API calls.

---

## **Production Considerations**

- Use environment variables for sensitive configurations like API keys or model paths.
- Set up proper logging for error tracking.
- Use a reverse proxy (e.g., Nginx) for better performance and security.
- Configure Docker volumes for persistent storage.

