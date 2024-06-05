import requests
import string
import itertools
import json
import time

# Example of function. Must be polymorphic and has the same output format
def godaddy(domain, token):
    
    url = 'https://api.ote-godaddy.com/v1/domains/available'

    params = {
        "domain": f"{domain}",
        # Optimize for time ('FAST') or accuracy ('FULL')
        "checkType": "FAST",
        # Whether or not to include domains available for transfer. If set to True, checkType is ignored
        "forTransfer": "false"
    }
     
    headers = {
        "accept": "application/json",
        "Authorization": f"sso-key {token}"
    }
    
    # Make the GET request
    def make_request():
        response = requests.get(url, headers=headers, params=params)
        if response.status_code == 200: # OK
            return response.json()
        elif response.status_code == 429: # Too many requests
            print("Requests number exceeded. Pausing and retrying request...")
            time.sleep(1)
            return make_request()  # Retry after waiting
        else:
            return response.status_code
    try:
        response_json = make_request()
    except:
        print("Temporary failure in establishing a new connection. Pausing and retrying request...")
        time.sleep(2)
        response_json = make_request()

    if isinstance(response_json, dict):
        if "available" in response_json:
            if response_json["available"]:
                return "Available"
            else:
                return "Exists"
    else:
        return (f"Error: {response_json}")

# Generates combination of domain names
def generate_domain_names(base_domain, repeat):
    letters = string.ascii_lowercase
    combinations = itertools.product(letters, repeat=repeat)
    domain_list = [f"{''.join(combo)}{base_domain}" for combo in combinations]
    return domain_list

def main():

    results = {}
    i = 1

    key = open(".env", "r")
    token = key.readline().strip()
    if not token:
        print ("WARNING! Please add credentials to .env file!")
        exit()

    f = open("names.txt", "r")
    if not f.readline().strip():
        print ("WARNING! Add at least one name to names.txt file!")
        exit()
    
    f = open("names.txt", "r")

    for base_domain in f.readlines():
        # Here you can change the size of prefix, current value is 2
        domains_to_check = generate_domain_names(base_domain.strip(), 2)
        print (f"Number of items to check: {len(domains_to_check)}.")
        
        for domain in domains_to_check:
            #time.sleep(1)
            status = godaddy(domain, token)
            results[domain] = status
            print(f"{i}.{domain}: {status}")
            i+=1

    with open("results.json", "w") as f:
        json.dump(results, f, indent=4)

    print ("The results are saved to results.json")

if __name__ == "__main__":
    main()