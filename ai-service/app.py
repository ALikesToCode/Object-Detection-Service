from flask import Flask, request, jsonify, send_file
import torch
from utils.detection import DetectionService
import os
from pathlib import Path
import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

app = Flask(__name__)
UPLOAD_FOLDER = Path('uploads')
UPLOAD_FOLDER.mkdir(exist_ok=True)

detection_service = DetectionService()

@app.route('/detect', methods=['POST'])
def detect():
    logger.debug("Received detection request")
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    
    file = request.files['file']
    if not file.filename:
        return jsonify({'error': 'No selected file'}), 400

    filepath = UPLOAD_FOLDER / file.filename
    file.save(filepath)
    logger.debug(f"Saved uploaded file to {filepath}")
    
    try:
        results = detection_service.process_image(filepath)
        logger.debug(f"Detection completed. Results: {results}")
        return jsonify(results)
    except Exception as e:
        logger.error(f"Error during detection: {str(e)}", exc_info=True)
        return jsonify({'error': str(e)}), 500

@app.route('/images/<path:filename>')
def get_image(filename):
    try:
        image_path = UPLOAD_FOLDER / filename
        if image_path.exists():
            return send_file(image_path, mimetype='image/jpeg')
        else:
            logger.error(f"Image not found: {image_path}")
            return jsonify({'error': 'Image not found'}), 404
    except Exception as e:
        logger.error(f"Error serving image: {str(e)}")
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001) 