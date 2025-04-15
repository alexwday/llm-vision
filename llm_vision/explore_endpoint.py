# COPY THIS ENTIRE CODE BLOCK TO A JUPYTER NOTEBOOK CELL AND RUN IT

import requests
from bs4 import BeautifulSoup
import json
import re

# CONFIG - MODIFY THESE VALUES
# Use the endpoint URL with trailing slash that returned HTML
API_URL = 'https://your-endpoint-url/v1/models/'  # Replace with your actual endpoint that returned 200

print(f"Exploring endpoint with HTML response: {API_URL}")
print("-" * 70)

# Function to fetch and parse HTML content
def explore_html_endpoint(url):
    try:
        print(f"Fetching content from: {url}")
        
        # Try different headers to see what works best
        headers_to_try = [
            {},  # No headers
            {'Accept': 'text/html'},
            {'Accept': 'application/json'}
        ]
        
        best_response = None
        for i, headers in enumerate(headers_to_try):
            print(f"\nTrying request {i+1} with headers: {headers}")
            response = requests.get(url, headers=headers, timeout=10)
            print(f"Status code: {response.status_code}")
            
            if response.status_code == 200:
                best_response = response
                print("✅ Successful response!")
                break
        
        if not best_response:
            print("❌ No successful responses.")
            return
        
        response = best_response
        content_type = response.headers.get('Content-Type', '')
        print(f"Content type: {content_type}")
        
        # Process depending on content type
        if 'json' in content_type.lower():
            # Process as JSON
            try:
                data = response.json()
                print("\nJSON CONTENT:")
                print(json.dumps(data, indent=2))
                
                # Look for useful information
                extract_useful_info_from_json(data)
                
            except:
                print("Failed to parse JSON response.")
                print(response.text[:500])
                
        elif 'html' in content_type.lower() or response.text.strip().startswith(('<html', '<!DOCTYPE html')):
            # Process as HTML
            print("\nHTML CONTENT DETECTED")
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Print page title
            title = soup.title.string if soup.title else "No title"
            print(f"Page title: {title}")
            
            # Extract visible text (truncated)
            text = soup.get_text(strip=True)
            print(f"\nPage text (excerpt): {text[:300]}...")
            
            # Look for links
            links = soup.find_all('a')
            if links:
                print("\nLinks found:")
                for i, link in enumerate(links[:20]):  # Show first 20 links
                    href = link.get('href')
                    text = link.get_text(strip=True) or link.get('title') or "No text"
                    print(f"  {i+1}. {text[:40]}: {href}")
                    
                if len(links) > 20:
                    print(f"  ...and {len(links)-20} more links")
            
            # Look for list items or table data (common in directory listings)
            list_items = soup.find_all(['li', 'td'])
            if list_items:
                print("\nPotential directory items or table data:")
                for i, item in enumerate(list_items[:20]):
                    print(f"  {i+1}. {item.get_text(strip=True)[:50]}")
                    
                if len(list_items) > 20:
                    print(f"  ...and {len(list_items)-20} more items")
            
            # Look for specific patterns in text that might indicate model names
            look_for_model_names(response.text)
            
        else:
            # Unknown content type
            print("\nUNKNOWN CONTENT TYPE")
            print("Raw content (excerpt):")
            print(response.text[:500])
            
            # Try to detect JSON or HTML
            try:
                json.loads(response.text)
                print("\nContent appears to be JSON despite content type. Try parsing as JSON.")
            except:
                if response.text.strip().startswith(('<html', '<!DOCTYPE html')):
                    print("\nContent appears to be HTML despite content type. Try parsing as HTML.")
            
            # Look for patterns anyway
            look_for_model_names(response.text)
            
    except Exception as e:
        print(f"Error exploring endpoint: {str(e)}")

# Function to extract useful info from JSON
def extract_useful_info_from_json(data):
    print("\nExtracting useful information from JSON...")
    
    # Look for arrays that might contain model information
    arrays = []
    if isinstance(data, list):
        arrays.append(("root", data))
    elif isinstance(data, dict):
        for key, value in data.items():
            if isinstance(value, list) and len(value) > 0:
                arrays.append((key, value))
    
    for name, array in arrays:
        print(f"\nFound array '{name}' with {len(array)} items:")
        
        # Print first few items
        for i, item in enumerate(array[:5]):
            if isinstance(item, dict):
                print(f"  {i+1}. {json.dumps(item, indent=2)}")
            else:
                print(f"  {i+1}. {item}")
                
        if len(array) > 5:
            print(f"  ...and {len(array)-5} more items")
    
    # Look for specific keys
    if isinstance(data, dict):
        interesting_keys = ['model', 'models', 'name', 'id', 'version', 'data']
        for key in interesting_keys:
            if key in data:
                print(f"\nFound '{key}': {data[key]}")

# Function to look for patterns that might indicate model names
def look_for_model_names(text):
    print("\nLooking for potential model names or identifiers...")
    
    # Patterns that might indicate model names or IDs
    patterns = [
        r'qwen[\w-]*',  # Starts with qwen
        r'gpt[\w-]*',   # Starts with gpt
        r'llama[\w-]*', # Starts with llama
        r'model[\w-]*', # Starts with model
        r'id["\']?\s*:\s*["\']([^"\']+)["\']', # JSON-like id field
        r'name["\']?\s*:\s*["\']([^"\']+)["\']', # JSON-like name field
    ]
    
    for pattern in patterns:
        matches = re.findall(pattern, text, re.IGNORECASE)
        if matches:
            unique_matches = set(matches)
            print(f"Matches for pattern '{pattern}':")
            for match in list(unique_matches)[:10]:  # Show up to 10 unique matches
                print(f"  - {match}")
            
            if len(unique_matches) > 10:
                print(f"  ...and {len(unique_matches)-10} more matches")

# Explore the endpoint
explore_html_endpoint(API_URL)

# Try a few variations of the URL
url_variations = [
    API_URL.rstrip('/'),  # Without trailing slash
    API_URL + 'qwen',     # With potential model name
    '/'.join(API_URL.split('/')[:-2]) + '/',  # Parent directory
]

print("\n" + "="*70)
print("TRYING URL VARIATIONS:")

for url in url_variations:
    print("\n" + "="*50)
    explore_html_endpoint(url)