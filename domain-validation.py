import requests
import string
import itertools
import json
import time

# Example of function. Must be polymorphic and has the same output format
def godaddy(domain):
    url = 'https://api.ote-godaddy.com/v1/domains/available'

    params = {
        "domain": f"{domain}",
        # Optimize for time ('FAST') or accuracy ('FULL')
        "checkType": "FAST",
        # Whether or not to include domains available for transfer. If set to True, checkType is ignored
        "forTransfer": "false"
    }
     
    headers = {
        'accept': 'application/json',
        # Replace below with your credentials [key]:[secret]
        'Authorization': 'sso-key YOUR_API_KEY:YOUR_API_SECRET'
    }
    
    # Make the GET request
    response = requests.get(url, headers=headers, params=params)
    
    if response.status_code == 200:
        if response.json()["available"] == True:
            return "Available"
        else:
            return "Exists"
    else:
        return f"Error: {response.status_code}"

# Generates combination of domain names
def generate_domain_names(base_domain, repeat):
    letters = string.ascii_lowercase
    combinations = itertools.product(letters, repeat=repeat)
    domain_list = [f"{''.join(combo)}{base_domain}" for combo in combinations]
    return domain_list

def main():

    f = open("names.txt", "r")
    results = {}
    i = 1
    
    for base_domain in f.readlines():
        # Here you can change the size of prefix, current value is 2
        domains_to_check = generate_domain_names(base_domain, 2)
        print (f"Number of items to check: {len(domains_to_check)}.")
        
        for domain in domains_to_check:
            time.sleep(0.8)
            status = godaddy(domain)
            results[domain] = status
            print(f"{i}.{domain}: {status}")
            i+=1

    with open('results.json', 'w') as f:
        json.dump(results, f, indent=4)

    print ("The  results are saved to results.json")

if __name__ == "__main__":
    main()