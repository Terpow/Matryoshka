
# Cybersecurity Challenge Solver: Multi-Stage "Matryoshka" Automation

This repository contains a Python-based automation tool designed to solve a multi-stage technical challenge provided by `zostansecurity.ninja`. The script demonstrates advanced skills in web automation, cryptographic hashing, and recursive data decoding.

## Project Overview

The goal of the challenge was to programmatically interact with a web server through several stages to retrieve a hidden "encrypted" contact email address. The process required handling dynamic parameters, custom HTTP headers, and a complex "matryoshka" style encoding.

## 🛠 Features & Techniques Used

* **Session Management:** Uses `requests.Session` to maintain state and cookies across multiple HTTP requests.
* **Regex Extraction:** Employs complex Regular Expressions (`re`) to parse challenge tokens, timestamps, and JSON-like strings from raw HTML/Text responses.
* **Cryptographic Hashing:** Implements **SHA-256** hashing logic. It sorts data keys in descending order (Z -> A), formats them into a query string, and computes a hash for verification.
* **Recursive Decoding:** Features a robust "Matryoshka" unwrapper that recursively decodes **Base64** strings until the final target (email) is identified via pattern matching.
* **Custom Headers:** Handles non-standard HTTP headers (e.g., `X-Challenge`, `X-Timestamp`) required for server-side validation.

## 🚀 How it Works

The script follows a 4-step logic:

1.  **Step 0 (Handshake):** Initial GET request to extract the starting challenge token and timestamp.
2.  **Step 1 (Activation):** Activates the session and captures security headers returned by the server.
3.  **Step 2 (Data Dump):** Fetches a payload containing a JSON object that needs to be processed.
4.  **Step 3 (The Math):** Sorts the JSON keys alphabetically (reversed), concatenates them, hashes the result with SHA-256, and POSTs it back.
5.  **Final Stage:** Receives a deeply nested Base64 string and runs a `while` loop to unwrap the layers until the HR email address is revealed.

##  Prerequisites

* Python 3.x
* `requests` library

```bash
pip install requests
```

##  Usage

Simply run the script:

```bash
python task_solver.py
```

### Example Output:
```text
Step 0: Getting the initial link...
Step 1: Activation and getting new keys...
Step 2: Fetching the data 'dump'...
Step 3: Hash mathematics...
Sending the final report...
Searching for the email in the 'matryoshka'...

**************************************************
VICTORY! It took 50 rounds of decoding.
CONTACT EMAIL: hr@example-company.com
**************************************************
```

## Disclaimer!!!
This script was developed for educational and ethical hacking purposes as part of a cybersecurity challenge.

