from googlesearch import search
from colorama import Fore
import threading
import random
import string
import httpx
import time
import json
import re

def scrape():
    content = ""
    links = ["https://api.proxyscrape.com/?request=displayproxies&proxytype=http&timeout=7000", "https://hidemy.name/en/proxy-list/?type=https", "http://spys.one/en/http-proxy-list/", "https://free-proxy-list.net/anonymous-proxy.html"]
    for link in links:
        r = httpx.get(link).text
        content += f"{r} "
    proxies = re.findall(r'\b(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\b:\d{2,5}', content)
    return proxies

def main():
    while True:
        try:
            proxy = random.choice(proxylist)
            proxies = {
                "http://": f"http://{proxy}",
                "https://": f"http://{proxy}",
            }
            with httpx.Client(proxies=proxies) as session:
                headers = {
                    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
                    "Accept-Encoding": "gzip, deflate, br",
                    "Accept-Language": "en-US,en;q=0.5",
                    "Cache-Control": "max-age=0",
                    "Connection": "keep-alive",
                    "Host": "discordapp.com",
                    "Sec-Fetch-Dest": "document",
                    "Sec-Fetch-Mode": "navigate",
                    "Sec-Fetch-Site": "none",
                    "Sec-Fetch-User": "?1",
                    "Upgrade-Insecure-Requests": "1",
                    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:97.0) Gecko/20100101 Firefox/97.0"
                }
                code = ''.join(random.choices(string.ascii_uppercase + string.ascii_lowercase + string.digits, k=16))
                url = f"https://discordapp.com/api/v9/entitlements/gift-codes/{code}?with_application=false&with_subscription_plan=true"
                resp1 = session.get(url, headers=headers)
                resp = json.loads(resp1.text)
                if resp["message"] == "Unknown Gift Code":                        
                    print(f"{Fore.RED}|>| Unknown Gift Code {code} ")
                    continue
                elif resp["message"] == "The resource is being rate limited.":
                    print(f"{Fore.YELLOW}|>| Proxy ratelimited")
                    continue
                elif resp["message"] == "You are being rate limited.":
                    print(f"{Fore.YELLOW}|>| Proxy ratelimited")
                    continue
                else:
                    print(f"{Fore.GREEN}|>| VALID NITRO https://discord.gift/{code}")
        except Exception as e:
            continue

if __name__ == "__main__":
    proxylist = scrape()
    proxycount = 0
    for proxy in proxylist:
        proxycount +=1
    print(f"{Fore.GREEN}500 threads starting {proxycount} proxies loaded")
    for i in range(500): threading.Thread(target=main).start()
