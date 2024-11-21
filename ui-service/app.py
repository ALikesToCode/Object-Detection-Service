from flask import Flask, render_template, request, jsonify
import requests
from pathlib import Path
from werkzeug.utils import secure_filename
import os
from typing import Tuple, Dict, Any
from dotenv import load_dotenv
import logging

if os.getenv('FLASK_ENV') == 'development':
    load_dotenv('.env.dev')
else:
    load_dotenv()

logging.basicConfig(
    level=logging.INFO,
    format='[%(asctime)s] [%(process)d] [%(levelname)s] %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S %z'
)
logger = logging.getLogger(__name__)

app = Flask(__name__)
UPLOAD_FOLDER = Path(os.getenv('UPLOAD_FOLDER', 'static/uploads'))
MAX_CONTENT_LENGTH = 16 * 1024 * 1024
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
AI_SERVICE_URL = os.getenv('AI_SERVICE_URL', 'http://localhost:5001')

UPLOAD_FOLDER.mkdir(parents=True, exist_ok=True)
app.config.update(
    UPLOAD_FOLDER=str(UPLOAD_FOLDER),
    MAX_CONTENT_LENGTH=MAX_CONTENT_LENGTH
)

def allowed_file(filename: str) -> bool:
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def process_upload(file) -> Tuple[Dict[str, Any], int]:
    if not allowed_file(file.filename):
        logger.warning(f"Invalid file type attempted: {file.filename}")
        return {'error': 'Invalid file type'}, 400
        
    filename = secure_filename(file.filename)
    filepath = UPLOAD_FOLDER / filename
    file.save(filepath)
    logger.info(f"Saved uploaded file: {filename}")

    try:
        logger.info("Initiating object detection request")
        with open(filepath, 'rb') as f:
            response = requests.post(f'{AI_SERVICE_URL}/detect', files={'file': f}, timeout=30)
        response.raise_for_status()
        
        result = response.json()
        detected_filename = result['annotated_image_name']
        detected_image_url = f"{AI_SERVICE_URL}/images/{detected_filename}"
        
        img_response = requests.get(detected_image_url, timeout=30)
        
        if img_response.status_code == 200:
            detected_path = UPLOAD_FOLDER / detected_filename
            with open(detected_path, 'wb') as f:
                f.write(img_response.content)
            
            logger.info(f"Successfully processed image: {filename}")
            return {
                'result': result['detections'],
                'original_image': f'/static/uploads/{filename}',
                'detected_image': f'/static/uploads/{detected_filename}'
            }, 200
        else:
            logger.error("Failed to retrieve detection result image")
            return {'error': 'Failed to download detected image'}, 500
            
    except requests.RequestException as e:
        logger.error(f"AI service communication error: {str(e)}")
        return {'error': f'AI Service Error: {str(e)}'}, 500
    except Exception as e:
        logger.error(f"Processing error: {str(e)}")
        return {'error': f'Unexpected error: {str(e)}'}, 500

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        logger.warning("Upload attempted without file")
        return jsonify({'error': 'No file part'}), 400
    
    file = request.files['file']
    if not file.filename:
        logger.warning("Upload attempted with empty filename")
        return jsonify({'error': 'No selected file'}), 400

    result, status_code = process_upload(file)
    return jsonify(result), status_code

if __name__ == '__main__':
    env = os.getenv('FLASK_ENV', 'production')
    logger.info(f"Starting UI service in {env} mode")
    logger.info(f"AI Service URL configured as: {AI_SERVICE_URL}")
    
    debug_mode = env == 'development'
    app.run(host='0.0.0.0', port=5000, debug=debug_mode)