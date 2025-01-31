import requests
import time

# Konfiguration
API_TOKEN = ''  # Ersetze mit deinem Cloudflare API Token
ZONE_ID = ''      # Ersetze mit deiner Zone ID
RECORD_ID = ''    # Ersetze mit der Record ID des DNS-Eintrags
DNS_NAME = ''      # Ersetze mit dem DNS-Namen, den du aktualisieren möchtest

def get_public_ip():
    #Holt die aktuelle öffentliche IP-Adresse.
    response = requests.get('https://api.ipify.org?format=json')
    return response.json()['ip']

def update_dns_record(ip):
    #Aktualisiert den DNS-Record mit der neuen IP-Adresse.
    url = f'https://api.cloudflare.com/client/v4/zones/{ZONE_ID}/dns_records/{RECORD_ID}'
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {API_TOKEN}'
    }
    data = {
        'type': 'A',  # Typ des DNS-Records
        'name': DNS_NAME,
        'content': ip,
        'ttl': 1,  # TTL (Time to Live)
        'proxied': False  # Setze auf True, wenn du Cloudflare Proxy verwenden möchtest
    }
    
    response = requests.put(url, headers=headers, json=data)
    
    if response.status_code == 200:
        print(f'DNS-Record erfolgreich aktualisiert auf: {ip}')
    else:
        print('Fehler beim Aktualisieren des DNS-Records:', response.json())

def main():
    current_ip = get_public_ip()
    print(f'Aktuelle IP: {current_ip}')
    
    while True:
        time.sleep(300)  # 5 Minuten warten
        new_ip = get_public_ip()
        if new_ip != current_ip:
            print(f'IP hat sich geändert: {new_ip}')
            update_dns_record(new_ip)
            current_ip = new_ip
        else:
            print('IP hat sich nicht geändert.')

if __name__ == '__main__':
    main()