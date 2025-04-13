# api/upscale.py
import os
import time
from http import HTTPStatus
import torch
from PIL import Image
import numpy as np
from io import BytesIO
from realesrgan import RealESRGAN

def load_model():
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    model = RealESRGAN(device, scale=4)
    model.load_weights('weights/RRDB_ESRGAN_x4.pth', download=False)
    return model

model = load_model()

def handler(req):
    try:
        start_time = time.time()
        
        # Check file size
        if req.headers['content-length'] > 5_000_000:  # 5MB limit
            return {
                'statusCode': HTTPStatus.BAD_REQUEST,
                'body': {'error': 'File size too large (max 5MB)'}
            }

        image_file = req.files.get('image')
        img = Image.open(image_file).convert('RGB')
        
        # Processing
        sr_image = model.predict(np.array(img))
        
        # Save output
        buffered = BytesIO()
        sr_image.save(buffered, format="PNG")
        img_str = f"data:image/png;base64,{base64.b64encode(buffered.getvalue()).decode()}"
        
        # Check total processing time
        if (time.time() - start_time) > 8:  # Vercel timeout 10s
            return {
                'statusCode': HTTPStatus.REQUEST_TIMEOUT,
                'body': {'error': 'Processing timeout'}
            }

        return {
            'statusCode': HTTPStatus.OK,
            'body': {'hd_image': img_str}
        }

    except Exception as e:
        return {
            'statusCode': HTTPStatus.INTERNAL_SERVER_ERROR,
            'body': {'error': str(e)}
        }
