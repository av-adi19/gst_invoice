import sys
import torch
import cv2
import pytesseract
import numpy as np
import os

# Add the YOLOv5 directory to the Python path (assuming it's within the project)
sys.path.append(os.path.join(os.getcwd(), "yolov5"))

from yolov5.utils.general import non_max_suppression
from yolov5.models.common import DetectMultiBackend

class InvoiceProcessor:
    def __init__(self, model_path):
        print(f"Loading model from {model_path}")
        self.model = DetectMultiBackend(model_path)
        print("Model loaded successfully")

    def perform_ocr(self, image, boxes):
        data = {}
        for (x1, y1, x2, y2) in boxes:
            roi = image[y1:y2, x1:x2]
            text = pytesseract.image_to_string(roi, config='--psm 6')
            data[(x1, y1, x2, y2)] = text.strip()
        return data

    def process_invoice(self, image_path):
        image = cv2.imread(image_path)
        results = self.model(image)
        boxes = results.xyxy[0][:, :4].int().numpy()  # xyxy format
        class_names = results.names

        ocr_results = self.perform_ocr(image, boxes)
        invoice_data = {class_names[i]: ocr_results[i] for i in range(len(ocr_results))}
        return invoice_data
