# COPY THIS ENTIRE CODE BLOCK TO A JUPYTER NOTEBOOK CELL AND RUN IT

import requests
import json
import base64
from urllib.request import urlretrieve
import os
from PIL import Image
import matplotlib.pyplot as plt

# CONFIG - MODIFY THESE VALUES
API_URL = 'https://your-endpoint-url/v1/chat/completions'  # Replace with your actual endpoint
MODEL_NAME = 'qwen'  # Using 'qwen' as model name

print(f"Testing with model name '{MODEL_NAME}' and fixing type issues: {API_URL}")
print("-" * 70)

# Download a sample image for testing
os.makedirs('images', exist_ok=True)
demo_url = 'https://raw.githubusercontent.com/facebookresearch/segment-anything/main/notebooks/images/truck.jpg'
image_path = 'images/demo_image.jpg'
urlretrieve(demo_url, image_path)
print(f"Sample image downloaded to {image_path}")

# Display the image
img = Image.open(image_path)
plt.figure(figsize=(8, 6))
plt.imshow(img)
plt.axis('off')
plt.title('Test Image')
plt.show()

# Encode the image
with open(image_path, 'rb') as image_file:
    base64_image = base64.b64encode(image_file.read()).decode('utf-8')

# Different payload formats to address "type missing" error
payload_formats = [
    {
        "name": "Standard format with explicit type fields",
        "payload": {
            "model": MODEL_NAME,
            "messages": [
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": "What do you see in this image?"
                        },
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/jpeg;base64,{base64_image}"
                            }
                        }
                    ]
                }
            ]
        }
    },
    {
        "name": "Adding 'type' to the message object",
        "payload": {
            "model": MODEL_NAME,
            "messages": [
                {
                    "role": "user",
                    "type": "multimodal",
                    "content": [
                        {
                            "type": "text",
                            "text": "What do you see in this image?"
                        },
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/jpeg;base64,{base64_image}"
                            }
                        }
                    ]
                }
            ]
        }
    },
    {
        "name": "Content as direct array with types",
        "payload": {
            "model": MODEL_NAME,
            "messages": [
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": "What do you see in this image?"
                        },
                        {
                            "type": "image",
                            "source": {
                                "type": "base64",
                                "data": base64_image
                            }
                        }
                    ]
                }
            ]
        }
    },
    {
        "name": "Without model specification",
        "payload": {
            "messages": [
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": "What do you see in this image?"
                        },
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/jpeg;base64,{base64_image}"
                            }
                        }
                    ]
                }
            ]
        }
    },
    {
        "name": "Simple image with text only - test baseline",
        "payload": {
            "model": MODEL_NAME,
            "messages": [
                {
                    "role": "user",
                    "content": "Hello, can you help me with a question about images?"
                }
            ]
        }
    }
]

# Try each format
for fmt in payload_formats:
    print(f"\nTrying: {fmt['name']}")
    print(f"Payload structure: {json.dumps(fmt['payload'], indent=2)[:200]}...")
    
    try:
        headers = {'Content-Type': 'application/json'}
        response = requests.post(API_URL, headers=headers, json=fmt['payload'], timeout=15)
        
        print(f"Status code: {response.status_code}")
        
        # Try to parse response as JSON
        try:
            json_response = response.json()
            response_excerpt = json.dumps(json_response, indent=2)
            if len(response_excerpt) > 300:
                response_excerpt = response_excerpt[:300] + "..."
            print(f"Response: {response_excerpt}")
            
            if response.status_code == 200:
                print("✅ This format might be correct!")
                
        except:
            # If not JSON, print text (limited)
            text = response.text[:200] + "..." if len(response.text) > 200 else response.text
            print(f"Response: {text}")
                
    except requests.exceptions.RequestException as e:
        print(f"Error: {str(e)}")
    
    print("-" * 50)

print("\nSUGGESTIONS:")
print("1. If any format succeeded, use that payload structure")
print("2. The 'type missing' error suggests the API expects certain type fields")
print("3. Try checking if your endpoint URL is correct")
print("4. Consider contacting the API provider for specific documentation")
print("5. Try a few more variations of the model name: 'qwen-vl', 'qwen-chat', etc.")