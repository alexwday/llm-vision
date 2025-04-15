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

print(f"Testing request without model name specification: {API_URL}")
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

# Different payload variations to try
payload_variations = [
    {
        "name": "Without model field - text only",
        "payload": {
            "messages": [
                {
                    "role": "user",
                    "content": "Hello, describe this truck."
                }
            ]
        }
    },
    {
        "name": "Without model field - with image",
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
        "name": "Simple content string - text only",
        "payload": {
            "messages": [
                {
                    "role": "user",
                    "content": "Hello, describe a truck."
                }
            ]
        }
    }
]

# Try each payload variation
for variation in payload_variations:
    print(f"\nTrying: {variation['name']}")
    print(f"Payload structure: {json.dumps(variation['payload'], indent=2)[:200]}...")
    
    try:
        headers = {'Content-Type': 'application/json'}
        response = requests.post(API_URL, headers=headers, json=variation['payload'], timeout=15)
        
        print(f"Status code: {response.status_code}")
        
        # Try to parse response as JSON
        try:
            json_response = response.json()
            response_excerpt = json.dumps(json_response, indent=2)
            if len(response_excerpt) > 300:
                response_excerpt = response_excerpt[:300] + "..."
            print(f"Response: {response_excerpt}")
            
            if response.status_code == 200:
                print("✅ This payload format might be correct!")
                
        except:
            # If not JSON, print text (limited)
            text = response.text[:200] + "..." if len(response.text) > 200 else response.text
            print(f"Response: {text}")
                
    except requests.exceptions.RequestException as e:
        print(f"Error: {str(e)}")
    
    print("-" * 50)

print("\nSUGGESTIONS:")
print("1. If any request succeeded, use that payload format")
print("2. Check if the endpoint is already model-specific")
print("3. Try to obtain documentation for the API")
print("4. The endpoint may require a specific request format")