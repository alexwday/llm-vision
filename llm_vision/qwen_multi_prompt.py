# COPY THIS ENTIRE CODE BLOCK TO A JUPYTER NOTEBOOK CELL AND RUN IT

import requests
import base64
import json
import matplotlib.pyplot as plt
from PIL import Image
import io
from pathlib import Path
from urllib.request import urlretrieve
import os

# CONFIG - MODIFY THESE VALUES
API_URL = 'https://your-endpoint-url/v1/chat/completions'  # Replace with your actual endpoint
USE_SAMPLE_IMAGE = True  # Set to False to use your own image
YOUR_IMAGE_PATH = 'your_image.jpg'  # Only used if USE_SAMPLE_IMAGE = False

# List of prompts to try
PROMPTS = [
    "What do you see in this image?",
    "Describe the main objects in this image.",
    "What colors are present in this image?",
    "Is there anything unusual about this image?"
]

# Create image directory
os.makedirs('images', exist_ok=True)

# Set image path - either download sample or use provided path
if USE_SAMPLE_IMAGE:
    demo_url = 'https://raw.githubusercontent.com/facebookresearch/segment-anything/main/notebooks/images/truck.jpg'
    image_path = 'images/demo_image.jpg'
    urlretrieve(demo_url, image_path)
    print(f"Sample image downloaded to {image_path}")
else:
    image_path = YOUR_IMAGE_PATH
    print(f"Using image at {image_path}")

# Display the image
img = Image.open(image_path)
plt.figure(figsize=(10, 8))
plt.imshow(img)
plt.axis('off')
plt.title('Input Image')
plt.show()

# Function to encode image
def encode_image(image_path):
    with open(image_path, 'rb') as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')

# Encode the image once for all prompts
base64_image = encode_image(image_path)

# Function to query model
def query_model(prompt, base64_image):
    # Prepare headers and payload
    headers = {'Content-Type': 'application/json'}
    payload = {
        'model': 'qwen-2-vl',  # Adjust model name if needed
        'messages': [
            {
                'role': 'user',
                'content': [
                    {'type': 'text', 'text': prompt},
                    {'type': 'image_url', 'image_url': {'url': f'data:image/jpeg;base64,{base64_image}'}}
                ]
            }
        ],
        'max_tokens': 1000
    }
    
    print(f"Sending request to {API_URL}")
    print(f"Prompt: {prompt}")
    
    # Send request
    try:
        response = requests.post(API_URL, headers=headers, json=payload)
        response.raise_for_status()  # Raise exception for HTTP errors
        
        # Process response
        result = response.json()
        try:
            response_text = result['choices'][0]['message']['content']
            print('\nModel Response:\n')
            print(response_text)
            return response_text
        except KeyError:
            print('Unexpected response format')
            print('Raw response:', json.dumps(result, indent=2))
            return None
    except requests.exceptions.RequestException as e:
        print(f'Error: {str(e)}')
        return None

# Process each prompt
results = {}
for prompt in PROMPTS:
    print("\n" + "="*50 + "\n")
    result = query_model(prompt, base64_image)
    results[prompt] = result

# Summary
print("\n" + "="*50)
print("\nSUMMARY OF RESULTS:\n")
for prompt, result in results.items():
    print(f"Prompt: {prompt}")
    if result:
        print(f"Response: {result[:100]}..." if len(result) > 100 else f"Response: {result}")
    else:
        print("Response: Error or no response")
    print("-"*30)