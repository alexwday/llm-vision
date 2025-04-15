# COPY THIS ENTIRE CODE BLOCK TO A JUPYTER NOTEBOOK CELL AND RUN IT

import requests
import json

# CONFIG - MODIFY THESE VALUES
API_URL = 'https://your-endpoint-url/v1/chat/completions'  # Replace with your actual endpoint

# Different model names to try
model_names = [
    "qwen-2-vl",
    "qwen-vl-2",
    "qwen-vl",
    "qwen2-vl", 
    "qwen2vl",
    "qwen-2-vision",
    "qwen-vl-plus",
    "qwen-2",
    "qwen2",
    "qwen",
    "qwen-plus",
    # Add any other variations you want to try
]

print(f"Testing different model names against: {API_URL}")
print("-" * 70)

# Base payload structure 
def make_payload(model_name):
    return {
        "model": model_name,
        "messages": [
            {
                "role": "user",
                "content": "Hello, this is a test."
            }
        ]
    }

# Headers
headers = {'Content-Type': 'application/json'}

# Try each model name
for model in model_names:
    print(f"\nTrying model name: '{model}'")
    payload = make_payload(model)
    
    try:
        response = requests.post(API_URL, headers=headers, json=payload, timeout=10)
        print(f"Status code: {response.status_code}")
        
        # Try to parse response as JSON
        try:
            json_response = response.json()
            print(f"Response: {json.dumps(json_response, indent=2)[:300]}...")
            
            # Check if there's an error message related to the model
            if response.status_code != 200 and "model" in str(json_response).lower() and "error" in str(json_response).lower():
                print("⚠️ The model name seems to be incorrect.")
            elif response.status_code == 200:
                print("✅ This model name might be correct!")
                
        except:
            # If not JSON, print text (limit to 200 chars)
            text = response.text[:200] + "..." if len(response.text) > 200 else response.text
            print(f"Response: {text}")
                
    except requests.exceptions.RequestException as e:
        print(f"Error: {str(e)}")
    
    print("-" * 50)

print("\nNow, let's check if the API has an endpoint to list available models...")

# Try to get a list of available models
models_url = '/'.join(API_URL.split('/')[:-2]) + '/v1/models'
print(f"\nChecking models endpoint: {models_url}")

try:
    response = requests.get(models_url, timeout=10)
    print(f"Status code: {response.status_code}")
    
    try:
        json_response = response.json()
        print(f"Response: {json.dumps(json_response, indent=2)[:500]}...")
        
        # Try to extract model names if possible
        if "data" in json_response and isinstance(json_response["data"], list):
            print("\nPossible model names found:")
            for model in json_response["data"]:
                if "id" in model:
                    print(f"- {model['id']}")
    except:
        text = response.text[:200] + "..." if len(response.text) > 200 else response.text
        print(f"Response: {text}")
        
except requests.exceptions.RequestException as e:
    print(f"Error: {str(e)}")

print("\nSUGGESTIONS:")
print("1. If any model name returned a 200 status, use that one")
print("2. Ask your provider for the exact model name to use")
print("3. Check if you need to add authentication to your requests")
print("4. Check if the endpoint URL path is correct (v1/chat/completions vs. something else)")