# File: qwen_test.py
# Contains code snippets designed to be copied into Jupyter notebook cells

import requests
import base64
import json
import matplotlib.pyplot as plt
from PIL import Image
import io
from pathlib import Path

# --- Cell 1: Configuration ---

def setup_config():
    """Configure API endpoint - Run this cell first"""
    # API endpoint for Qwen 2 VL
    # Replace with your actual endpoint
    API_URL = 'https://your-endpoint-url/v1/chat/completions'
    
    # Function to encode images
    def encode_image(image_path):
        with open(image_path, 'rb') as image_file:
            return base64.b64encode(image_file.read()).decode('utf-8')
    
    return API_URL, encode_image

# --- Cell 2: Download Sample Image (Optional) ---

def download_sample_image():
    """Download a sample image for testing - Run this cell if you don't have a test image"""
    from urllib.request import urlretrieve
    import os
    
    # Create directory if it doesn't exist
    os.makedirs('images', exist_ok=True)
    
    # Download sample image
    demo_url = 'https://raw.githubusercontent.com/facebookresearch/segment-anything/main/notebooks/images/truck.jpg'
    image_path = 'images/demo_image.jpg'
    urlretrieve(demo_url, image_path)
    
    print(f"Sample image downloaded to {image_path}")
    return image_path

# --- Cell 3: Model Query Function ---

def create_query_function(API_URL, encode_image):
    """Create a function to query the Qwen 2 VL model - Run this cell after setup"""
    
    def query_model(image_path, prompt):
        # Encode the image
        base64_image = encode_image(image_path)
        
        # Prepare headers (adjust if authentication is required)
        headers = {
            'Content-Type': 'application/json',
            # 'Authorization': 'Bearer YOUR_API_KEY',  # Uncomment if needed
        }
        
        # Prepare payload according to chat completions API format with image
        payload = {
            'model': 'qwen-2-vl',  # Adjust model name if needed
            'messages': [
                {
                    'role': 'user',
                    'content': [
                        {
                            'type': 'text',
                            'text': prompt
                        },
                        {
                            'type': 'image_url',
                            'image_url': {
                                'url': f'data:image/jpeg;base64,{base64_image}'
                            }
                        }
                    ]
                }
            ],
            'max_tokens': 1000
        }
        
        # Send request
        try:
            response = requests.post(API_URL, headers=headers, json=payload)
            response.raise_for_status()  # Raise exception for HTTP errors
            return response.json()
        except requests.exceptions.RequestException as e:
            return {'error': str(e)}
    
    return query_model

# --- Cell 4: Helper Function to Display Image and Response ---

def create_analysis_function(query_model):
    """Create a function to analyze images with the model - Run this cell after query_model"""
    
    def analyze_image(image_path, prompt):
        # Display the image
        img = Image.open(image_path)
        plt.figure(figsize=(10, 8))
        plt.imshow(img)
        plt.axis('off')
        plt.title('Input Image')
        plt.show()
        
        # Query the model
        print(f'Prompt: {prompt}')
        result = query_model(image_path, prompt)
        
        # Extract and display the response
        if 'error' in result:
            print(f'Error: {result["error"]}')
        else:
            try:
                response_text = result['choices'][0]['message']['content']
                print('\nModel Response:\n')
                print(response_text)
            except KeyError as e:
                print(f'Unexpected response format: {e}')
                print('Raw response:', json.dumps(result, indent=2))
        
        return result
    
    return analyze_image

# --- Cell 5: Example Usage ---

def example_usage():
    """Example of how to use the functions - Copy and modify this cell as needed"""
    # Setup
    API_URL, encode_image = setup_config()
    query_model = create_query_function(API_URL, encode_image)
    analyze_image = create_analysis_function(query_model)
    
    # Download a sample image or use your own
    # image_path = download_sample_image()  # Uncomment to download a sample image
    image_path = 'images/your_image.jpg'  # Replace with your image path
    
    # Analyze the image
    prompt = "Describe this image in detail."
    result = analyze_image(image_path, prompt)
    
    # You can also try different prompts
    # prompts = [
    #     "What objects do you see in this image?",
    #     "Is there anything unusual in this image?",
    #     "Describe the colors and composition of this image."
    # ]
    # 
    # for prompt in prompts:
    #     print("\n" + "-"*50 + "\n")
    #     analyze_image(image_path, prompt)

# --- Quick test example ---

def quick_test():
    """A quick test of the Qwen 2 VL model - Copy this entire function to a cell"""
    # Setup
    API_URL = 'https://your-endpoint-url/v1/chat/completions'  # Replace with actual endpoint
    
    def encode_image(image_path):
        with open(image_path, 'rb') as image_file:
            return base64.b64encode(image_file.read()).decode('utf-8')
            
    # Download a sample image
    from urllib.request import urlretrieve
    import os
    
    os.makedirs('images', exist_ok=True)
    demo_url = 'https://raw.githubusercontent.com/facebookresearch/segment-anything/main/notebooks/images/truck.jpg'
    image_path = 'images/demo_image.jpg'
    urlretrieve(demo_url, image_path)
    
    # Display the image
    img = Image.open(image_path)
    plt.figure(figsize=(10, 8))
    plt.imshow(img)
    plt.axis('off')
    plt.title('Input Image')
    plt.show()
    
    # Encode the image
    base64_image = encode_image(image_path)
    
    # Prepare payload
    headers = {'Content-Type': 'application/json'}
    payload = {
        'model': 'qwen-2-vl',
        'messages': [
            {
                'role': 'user',
                'content': [
                    {'type': 'text', 'text': 'What do you see in this image?'},
                    {'type': 'image_url', 'image_url': {'url': f'data:image/jpeg;base64,{base64_image}'}}
                ]
            }
        ],
        'max_tokens': 1000
    }
    
    # Send request
    response = requests.post(API_URL, headers=headers, json=payload)
    
    # Display response
    if response.status_code == 200:
        result = response.json()
        try:
            response_text = result['choices'][0]['message']['content']
            print('\nModel Response:\n')
            print(response_text)
        except KeyError:
            print('Unexpected response format')
            print('Raw response:', json.dumps(result, indent=2))
    else:
        print(f'Error: {response.status_code}')
        print(response.text)