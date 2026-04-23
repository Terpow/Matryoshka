import requests
import re
import json
import hashlib
import base64

BASE_URL = "https://task.zostansecurity.ninja"

def unwrap_matryoshka(data):
    """Function to unwrap the infinite Base64 encoding"""
    current = data
    iteration = 0
    while True:
        try:
            # Try to decode the current string
            decoded_bytes = base64.b64decode(current)
            decoded_text = decoded_bytes.decode('utf-8')
            
            # If we find an '@' symbol, then it is email
            if "@" in decoded_text:
                return decoded_text.strip(), iteration
            
            current = decoded_text
            iteration += 1
        except:
            # If it cannot be decoded further, return what we have
            return current, iteration

def solve():
    session = requests.Session()
    session.headers.update({"User-Agent": "Mozilla/5.0 Chrome/120.0.0.0"})

    # STEP 0 
    print("Step 0: Getting the initial link...")
    r0 = session.get(BASE_URL)
    m0 = re.search(r'/\?step=1&challenge=([a-f0-9]+)&timestamp=(\d+)', r0.text)
    
    # STEP 1 
    print("Step 1: Activation and getting new keys...")
    url1 = BASE_URL + m0.group(0)
    r1 = session.get(url1)
    
    # Extract NEW keys from the response text
    c2 = re.search(r'X-challenge: ([a-f0-9]+)', r1.text).group(1)
    t2 = re.search(r'X-timestamp: (\d+)', r1.text).group(1)

    # STEP 2 
    print("Step 2: Fetching the data 'dump'...")
    r2 = session.get(f"{BASE_URL}/?step=2", headers={"X-Challenge": c2, "X-Timestamp": t2})
    
    # STEP 3 
    print("Step 3: Hash mathematics...")
    c3 = re.search(r'challenge: ([a-f0-9]+)', r2.text).group(1)
    t3 = re.search(r'timestamp: (\d+)', r2.text).group(1)
    json_str = re.search(r'(\{.*?\})', r2.text, re.DOTALL).group(1)
    data = json.loads(json_str)
    
    # Sorting from Z -> A
    sorted_keys = sorted(data.keys(), reverse=True)
    kv_string = "&".join([f"{k}={data[k]}" for k in sorted_keys])
    final_hash = hashlib.sha256(kv_string.encode()).hexdigest()
    
    # FINAL 
    print("Sending the final report...")
    r3 = session.post(f"{BASE_URL}/?step=3", data={
        "challenge": c3,
        "timestamp": t3,
        "hash": final_hash
    })
    
    # Look for the encrypted email in the response
    raw_response = r3.text
    print("🔍 Searching for the email in the 'matryoshka'...")
    
    # Extract the Base64 string itself (it is usually the longest block)
    base64_match = re.search(r'([A-Za-z0-9+/]{100,}=*)', raw_response)
    
    if base64_match:
        email, rounds = unwrap_matryoshka(base64_match.group(1))
        print("\n" + "*" * 50)
        print(f"VICTORY! It took {rounds} rounds of decoding.")
        print(f"CONTACT EMAIL: {email}")
        print("*" * 50)
    else:
        print("Failed to find the Base64 block in the response.")
        print("Server response:", raw_response)

if __name__ == "__main__":
    solve()
