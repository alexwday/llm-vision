# COPY THIS ENTIRE CODE BLOCK TO A JUPYTER NOTEBOOK CELL AND RUN IT

import requests
import json

# CONFIG - MODIFY THESE VALUES
API_URL = 'https://your-endpoint-url/v1/chat/completions'  # Replace with your actual endpoint

# Different payload formats to try
print(f"Testing different payload formats against: {API_URL}")
print("-" * 70)

# Format variations to try
formats = [
    {
        "name": "Standard OpenAI format",
        "payload": {
            "model": "qwen-2-vl",
            "messages": [
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": "Hello, this is a test."
                        }
                    ]
                }
            ]
        }
    },
    {
        "name": "Anthropic-style format",
        "payload": {
            "model": "qwen-2-vl",
            "prompt": "Human: Hello, this is a test.\n\nAssistant:",
            "max_tokens_to_sample": 1000
        }
    },
    {
        "name": "Legacy OpenAI completions format",
        "payload": {
            "model": "qwen-2-vl",
            "prompt": "Hello, this is a test.",
            "max_tokens": 1000
        }
    },
    {
        "name": "Simple message format",
        "payload": {
            "model": "qwen-2-vl",
            "messages": [
                {
                    "role": "user",
                    "content": "Hello, this is a test."
                }
            ]
        }
    }
]

# Try each format
for fmt in formats:
    print(f"\nTrying format: {fmt['name']}")
    print(f"Payload: {json.dumps(fmt['payload'], indent=2)}")
    
    try:
        # Common headers
        headers = {
            'Content-Type': 'application/json'
        }
        
        # Try with and without content-type header
        for use_header in [True, False]:
            if not use_header:
                print("\n  - Without Content-Type header:")
                response = requests.post(API_URL, json=fmt['payload'], timeout=10)
            else:
                print("\n  - With Content-Type header:")
                response = requests.post(API_URL, headers=headers, json=fmt['payload'], timeout=10)
                
            print(f"  Status code: {response.status_code}")
            
            # Try to parse response as JSON
            try:
                json_response = response.json()
                print(f"  Response: {json.dumps(json_response, indent=2)[:500]}...")
            except:
                # If not JSON, print text (limit to 200 chars)
                text = response.text[:200] + "..." if len(response.text) > 200 else response.text
                print(f"  Response: {text}")
                
    except requests.exceptions.RequestException as e:
        print(f"  Error: {str(e)}")
    
    print("-" * 50)

print("\nSUGGESTIONS:")
print("1. Check if the API requires a specific payload format")
print("2. Verify if authentication headers are needed")
print("3. Ask the API provider for example request formats")
print("4. Try using a different model name if 'qwen-2-vl' isn't recognized")