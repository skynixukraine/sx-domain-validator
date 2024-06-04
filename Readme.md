# Domain validation script

This script leverages the GoDaddy API to perform real-time checks and provides informative results.

## Requirements
- Python 3
- requests library (pip install requests)
- A GoDaddy developer account with an API key and secret

## Prerequisites
Register here https://developer.godaddy.com/ and create the `key:secret` combination here: https://developer.godaddy.com/keys

Update credentials here:

```python
headers = {
    'accept': 'application/json',
    'Authorization': 'sso-key YOUR_API_KEY:YOUR_API_SECRET'
}
```
Please refer to the comments in `domain-validation.py`.

## How it works
1. The script reads the list of names from the `names.txt` file.
2. It then creates a list of domains to check by adding the prefix (all possible letter combinations) to each name in `names.txt` file. The default lengh of prefix is 2 letters.
3. The results of the domain availability check are written to the `results.json`

## How to run

```bash
python3 domain-validation.py
```