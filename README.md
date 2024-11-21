# **Object Detection Service**

## **Overview**
This project provides a microservice architecture for object detection, consisting of two primary components:

1. **UI Service**: A user-friendly web interface for uploading images and displaying results.
2. **AI Service**: Processes the uploaded images using an object detection model (e.g., YOLO) and returns:
   - A JSON response with detected objects.
   - A processed image with bounding boxes.

The services communicate through RESTful APIs, forming a seamless pipeline for object detection.

---

## **Features**

- **Easy-to-Use Web Interface**: Upload images via a web interface.
- **AI-Powered Detection**: Processes images with a state-of-the-art object detection model.
- **Dockerized Microservices**: Easily deployable with Docker Compose.
- **REST API**: Extensible and scalable architecture for integrating with other systems.
- **JSON Output**: Detection results in a structured format.
- **Processed Images**: Images with bounding boxes stored for visualization.

---

## **Project Structure**

```
object-detection-service/
├── docker-compose.yml     # Orchestrates the services
├── README.md              # Documentation
├── ui-service/            # UI Service
│   ├── Dockerfile         # Docker setup for UI Service
│   ├── requirements.txt   # Dependencies for UI Service
│   ├── app.py             # Flask application for the UI
│   ├── static/            # Static assets
│   │   ├── css/           # Stylesheets
│   │   │   └── style.css
│   │   ├── js/            # JavaScript files
│   │   │   └── main.js
│   │   └── uploads/       # Uploaded files
│   └── templates/         # HTML templates
│       └── index.html
└── ai-service/            # AI Service
    ├── Dockerfile         # Docker setup for AI Service
    ├── requirements.txt   # Dependencies for AI Service
    ├── app.py             # Flask application for AI processing
    ├── uploads/           # Processed images
    └── utils/             # Utility functions
        └── detection.py   # Core object detection logic
```

---

## **Getting Started**

### **1. Clone the Repository**

```bash
git clone https://github.com/ALikesToCode/Object-Detection-Service-AIMONK.git
cd Object-Detection-Service-AIMONK
```

---

### **2. Create Upload Directories**

Set up directories for image uploads and processed outputs:

```bash
mkdir -p ui-service/static/uploads
mkdir -p ai-service/uploads
chmod 777 ui-service/static/uploads
chmod 777 ai-service/uploads
```

---

### **3. Deployment Options**

#### **Option 1: Dockerized Deployment**

1. **Build Docker Containers**:
   ```bash
   docker-compose build
   ```

2. **Start the Services**:
   ```bash
   docker-compose up
   ```

3. **Access the UI**:
   - Open your browser and navigate to: `http://localhost:5000`.

---

#### **Option 2: Local Deployment (Without Docker)**

##### **UI Service**
1. Navigate to the `ui-service` directory:
   ```bash
   cd ui-service
   ```

2. Set up a virtual environment and install dependencies:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. Start the Flask app:
   ```bash
   python app.py
   ```

##### **AI Service**
1. Navigate to the `ai-service` directory:
   ```bash
   cd ai-service
   ```

2. Set up a virtual environment and install dependencies:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. Start the Flask app:
   ```bash
   python app.py
   ```

---

### **4. Testing the Pipeline**

1. Open the UI Service in your browser at `http://localhost:5000`.
2. Upload an image using the interface.
3. Results:
   - JSON response with detected objects.
   - Processed image with bounding boxes saved in `ui-service/static/uploads/`.

---

## **Troubleshooting**

### **Port Conflicts**
Ensure no other services are using the required ports (default: `5000` for UI, `5001` for AI):
```bash
lsof -i :5000
lsof -i :5001
```
Kill conflicting processes if needed:
```bash
kill -9 <PID>
```

### **Rebuild Containers**
If issues arise during Docker deployment:
```bash
docker-compose down
docker system prune -f
docker-compose up --build
```

### **Permissions**
Fix directory permissions for uploads:
```bash
chmod -R 777 ui-service/static/uploads
chmod -R 777 ai-service/uploads
```

---

## **API Endpoints**

### **UI Service**
- **GET `/`**: Displays the web interface for uploading images.
- **POST `/upload`**: Uploads an image and sends it to the AI Service.

### **AI Service**
- **POST `/detect`**:
  - **Request**: Image file (multipart/form-data).
  - **Response**:
    ```json
    {
      "detections": [
        {"class": "person", "confidence": 0.95, "bbox": [x1, y1, x2, y2]},
        {"class": "dog", "confidence": 0.89, "bbox": [x1, y1, x2, y2]}
      ]
    }
    ```

---

## **Future Improvements**

- **Scalability**: Add support for Kubernetes deployment.
- **Model Options**: Allow dynamic selection of object detection models (YOLOv5, YOLOv8, etc.).
- **Authentication**: Secure endpoints with API keys or OAuth.
- **Monitoring**: Integrate logging and monitoring (e.g., Prometheus, Grafana).
- **Batch Processing**: Support bulk image uploads.

---

## **Contributing**

1. Fork the repository.
2. Create a feature branch:
   ```bash
   git checkout -b feature-name
   ```
3. Commit your changes:
   ```bash
   git commit -m "Description of changes"
   ```
4. Push the branch and open a Pull Request.

---

## **License**

This project is licensed under the [MIT License](LICENSE).

