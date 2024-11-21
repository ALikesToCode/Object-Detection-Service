from ultralytics import YOLO
import cv2
import numpy as np
from pathlib import Path
from dataclasses import dataclass
from typing import List, Dict, Any

@dataclass
class Detection:
    bbox: List[float]
    confidence: float 
    class_name: str

class DetectionService:
    def __init__(self):
        self.model = YOLO('yolov8n.pt')
        self.colors = np.random.uniform(0, 255, size=(80, 3))
        
    def process_image(self, image_path: Path) -> Dict[str, Any]:
        img = cv2.imread(str(image_path))
        if img is None:
            raise ValueError("Invalid image file")
        
        img_draw = img.copy()
        results = self.model(img)
        detections = self._process_detections(results, img_draw)
        
        output_path = Path('uploads') / f"{image_path.stem}_detected{image_path.suffix}"
        cv2.imwrite(str(output_path), img_draw)
        
        return {
            'detections': detections,
            'annotated_image': str(output_path),
            'annotated_image_name': output_path.name
        }
    
    def _process_detections(self, results, img) -> List[Dict]:
        detections = []
        
        for r in results:
            boxes = r.boxes
            for box in boxes:
                x1, y1, x2, y2 = box.xyxy[0].tolist()
                confidence = float(box.conf[0])
                class_id = int(box.cls[0])
                class_name = self.model.names[class_id]
                
                detection = Detection(
                    bbox=[x1, y1, x2, y2],
                    confidence=confidence,
                    class_name=class_name
                )
                
                color = self.colors[class_id % len(self.colors)].tolist()
                self._draw_detection(img, detection, color)
                detections.append(detection.__dict__)
                
        return detections
    
    def _draw_detection(self, img, detection, color):
        x1, y1, x2, y2 = map(int, detection.bbox)
        confidence = detection.confidence
        label = f"{detection.class_name} {confidence:.2f}"
        
        cv2.rectangle(img, (x1, y1), (x2, y2), color, 2)
        
        text_size = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.7, 2)[0]
        cv2.rectangle(img, 
                     (x1, y1 - text_size[1] - 10),
                     (x1 + text_size[0], y1),
                     color, -1)
        
        cv2.putText(img, label,
                    (x1, y1 - 5),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.7, (255, 255, 255), 2)