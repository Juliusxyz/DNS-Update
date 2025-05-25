import requests
import time

# Confuguration
API_TOKEN = ''    # Cloudflare API Token
ZONE_ID = ''      # Zone ID
RECORD_ID = ''    # Record ID from DNS entry
DNS_NAME = ''     # DNS name, to update

def get_public_ip():
    # get current public ip
    response = requests.get('https://api.ipify.org?format=json')
    return response.json()['ip']

def update_dns_record(ip):
    # update DNS record with the new IP adresse.
    url = f'https://api.cloudflare.com/client/v4/zones/{ZONE_ID}/dns_records/{RECORD_ID}'
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {API_TOKEN}'
    }
    data = {
        'type': 'A',  # DNS record type
        'name': DNS_NAME,
        'content': ip,
        'ttl': 1,  # TTL (Time to Live)
        'proxied': False  # change to true, if you want to use cloudflare proxy
    }
    
    response = requests.put(url, headers=headers, json=data)
    
    if response.status_code == 200:
        print(f'DNS record successfully updated to: {ip}')
    else:
        print('Error while updating DNS entry:', response.json())

def main():
    current_ip = get_public_ip()
    print(f'Current ip: {current_ip}')
    
    while True:
        time.sleep(300)  # wait 5 minutes
        new_ip = get_public_ip()
        if new_ip != current_ip:
            print(f'IP adress has changed: {new_ip}')
            update_dns_record(new_ip)
            current_ip = new_ip
        else:
            print("IP adress didn't change.")

if __name__ == '__main__':
    main()