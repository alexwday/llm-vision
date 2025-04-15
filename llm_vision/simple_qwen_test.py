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
PROMPT = "What do you see in this image?"

print("Simple test for Qwen vision model")
print("-" * 40)

# Create directory and download test image
os.makedirs('images', exist_ok=True)
demo_url = 'https://raw.githubusercontent.com/facebookresearch/segment-anything/main/notebooks/images/truck.jpg'
image_path = 'images/demo_image.jpg'
urlretrieve(demo_url, image_path)

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

# Prepare the request - using the most likely format
headers = {'Content-Type': 'application/json'}

# Try with 'qwen' model name
payload = {
    "model": "qwen",
    "messages": [
        {
            "role": "user",
            "content": [
                {
                    "type": "text",
                    "text": PROMPT
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

print(f"Sending request to: {API_URL}")
print(f"Prompt: {PROMPT}")
print(f"Model: qwen")

# Send the request
try:
    response = requests.post(API_URL, headers=headers, json=payload, timeout=15)
    print(f"Status code: {response.status_code}")
    
    # Process response
    try:
        result = response.json()
        print("\nResponse:")
        print(json.dumps(result, indent=2))
        
        # Try to extract and display the model's answer if successful
        if response.status_code == 200 and "choices" in result:
            try:
                answer = result["choices"][0]["message"]["content"]
                print("\n" + "="*50)
                print("MODEL'S ANSWER:")
                print(answer)
                print("="*50)
            except (KeyError, IndexError):
                print("Couldn't extract model answer from the response")
    except:
        print("\nNon-JSON response:")
        print(response.text)
except Exception as e:
    print(f"Error: {str(e)}")

print("\nIf this test failed, try:")
print("1. Check if the API URL is correct")
print("2. Try using a different model name (qwen-vl, qwen-chat, etc.)")
print("3. Try different content formats from qwen_specific_test.py")
print("4. Check if authentication is required")