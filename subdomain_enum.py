import requests
import threading

domain = 'google.com'

with open('subdomains.txt') as file:
    subdomains = file.read().splitlines()

discovered_subdomains = []
lock = threading.Lock()

def check_subdomain(subdomain):
    url = f'http://{subdomain}.{domain}'
    print(f"[*] Testing: {url}")
    try:
        requests.get(url, timeout=3)
    except (requests.ConnectionError, requests.Timeout, requests.RequestException):
        pass
    else:
        print("[+] Discovered subdomain:", url)
        with lock:
            discovered_subdomains.append(url)

threads = []

for subdomain in subdomains:
    thread = threading.Thread(target=check_subdomain, args=(subdomain,))
    thread.start()
    threads.append(thread)

for thread in threads:
    thread.join()

with open("discovered_subdomains.txt", 'w') as f:
    for subdomain in discovered_subdomains:
        print(subdomain, file=f)

print(f"\n[✓] Total discovered subdomains: {len(discovered_subdomains)}")

