# COPY THIS ENTIRE CODE BLOCK TO A JUPYTER NOTEBOOK CELL AND RUN IT

import requests
import json
import time

# CONFIG - MODIFY THESE VALUES
API_URL = 'https://your-endpoint-url/v1/chat/completions'  # Replace with your actual endpoint

# List of methods to try
METHODS = ['GET', 'POST', 'OPTIONS']

print(f"Diagnosing API endpoint: {API_URL}")
print("-" * 50)

# Try different HTTP methods
for method in METHODS:
    print(f"\nTesting {method} request...")
    try:
        if method == 'GET':
            response = requests.get(API_URL, timeout=10)
        elif method == 'POST':
            # Minimal payload
            headers = {'Content-Type': 'application/json'}
            payload = {
                'model': 'qwen-2-vl',
                'messages': [{'role': 'user', 'content': 'Hello'}]
            }
            response = requests.post(API_URL, headers=headers, json=payload, timeout=10)
        elif method == 'OPTIONS':
            response = requests.options(API_URL, timeout=10)
            
        print(f"Status code: {response.status_code}")
        print(f"Response headers: {dict(response.headers)}")
        
        # Try to parse response as JSON
        try:
            json_response = response.json()
            print(f"JSON response: {json.dumps(json_response, indent=2)}")
        except:
            # If not JSON, print text (limit to 500 chars)
            text = response.text[:500] + "..." if len(response.text) > 500 else response.text
            print(f"Text response: {text}")
            
    except requests.exceptions.RequestException as e:
        print(f"Error: {str(e)}")
    print("-" * 30)

# Check endpoint path variants
print("\nTesting endpoint path variants...")
base_url = '/'.join(API_URL.split('/')[:-2]) + '/'  # Get base URL
endpoints = [
    "v1/chat/completions",
    "v1/completions",
    "chat/completions"
]

for endpoint in endpoints:
    test_url = base_url + endpoint
    print(f"\nTrying: {test_url}")
    try:
        # Simple GET request just to check if endpoint exists
        response = requests.get(test_url, timeout=5)
        print(f"Status code: {response.status_code}")
        if response.status_code < 404:
            print("✓ This endpoint may be valid (non-404 response)")
    except requests.exceptions.RequestException as e:
        print(f"Error: {str(e)}")

print("\n" + "=" * 50)
print("\nSUGGESTIONS:")
print("1. Check the exact API endpoint URL with your provider")
print("2. Verify if the endpoint requires authentication (like an API key)")
print("3. Check if the endpoint has specific format requirements")
print("4. Try contacting the API provider for documentation")
print("5. Check if the service is available and your network can access it")