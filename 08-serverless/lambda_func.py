import io
import os
import requests
from PIL import Image
import numpy as np
import onnxruntime as ort

# 1. Initialize the ONNX session globally so it stays warm between Lambda calls
MODEL_PATH = "hair_classifier_empty.onnx"
session = ort.InferenceSession(MODEL_PATH)
input_name = session.get_inputs()[0].name
output_name = session.get_outputs()[0].name

def preprocess_image(image_url):
    # Download the image
    response = requests.get(image_url, timeout=10)
    response.raise_for_status()
    
    # Open and convert to RGB
    img = Image.open(io.BytesIO(response.content)).convert('RGB')
    
    # Resize to (200, 200) as required
    img = img.resize((200, 200), Image.Resampling.NEAREST)
    
    # Convert to NumPy array and normalize to [0, 1] range
    x = np.array(img, dtype=np.float32) / 255.0
    
    # Apply ImageNet mean and std standardization manually (since we don't use torchvision)
    mean = np.array([0.485, 0.456, 0.406], dtype=np.float32)
    std = np.array([0.229, 0.224, 0.225], dtype=np.float32)
    x = (x - mean) / std
    
    # Change shape from (H, W, C) to (C, H, W)
    x = x.transpose(2, 0, 1)
    
    # Add batch dimension -> (1, C, H, W)
    x = np.expand_dims(x, axis=0)
    
    return x

def lambda_handler(event, context):
    # Extract URL from the event payload
    url = event['url']
    
    # Preprocess
    X = preprocess_image(url)
    
    # Run Inference
    outputs = session.run([output_name], {input_name: X})
    
    # Convert result to a standard Python list so it can be serialized to JSON
    prediction = outputs[0].tolist()
    
    return {
        "prediction": prediction
    }
