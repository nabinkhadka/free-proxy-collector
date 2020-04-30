import requests
from bs4 import BeautifulSoup
import socket
import urllib

MAXIMUM_LIST_EXPECTED = 10


def get_soup(url):
    return BeautifulSoup(requests.get(url).text)


soup = get_soup("https://free-proxy-list.net/")
trs = soup.find_all("tr")


def validate_ip(addr):
    print("Validating ip", addr)
    try:
        socket.inet_aton(addr)
        return True
    except socket.error:
        return False


def validate_port(port):
    print("Validating port", port)
    return str(port).isdigit() and 1000 < int(port) < 99999


def reachable(proxy, protocol):
    print("Checking reachability", protocol, proxy)
    proxy_support = urllib.request.ProxyHandler({protocol: proxy})
    opener = urllib.request.build_opener(proxy_support)
    try:
        f = opener.open("http://google.com/")
        f.read(1)
        return True
    except Exception:
        return False


proxies = list()
failed = list()


print("Total proxies listed", len(trs))
for tr in trs:
    tds = tr.find_all("td")
    if tds:
        ip = tds[0].text
        if not validate_ip(ip):
            continue
        port = tds[1].text
        if not validate_port(port):
            continue
        protocol = "https" if "yes" in tds[6].text.strip() else "http"
        proxy = f"{protocol}://{ip}:{port}"
        if reachable(proxy, protocol):
            print("Valid proxy found")
            proxies.append(proxy)
        else:
            print("Droping invalid proxy")
            failed.append(proxy)
        if len(proxies) > MAXIMUM_LIST_EXPECTED:
            break

with open("proxies_list.txt", "w") as f:
    f.write("\n".join(proxies))
