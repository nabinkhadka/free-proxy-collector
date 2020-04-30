import requests
from bs4 import BeautifulSoup
import socket
import urllib


def get_soup(url):
    return BeautifulSoup(requests.get(url).text)


soup = get_soup("https://free-proxy-list.net/")
trs = soup.find_all("tr")


def validate_ip(addr):
    try:
        socket.inet_aton(addr)
        return True
    except socket.error:
        return False


def validate_port(port):
    return str(port).isdigit() and 1000 < int(port) < 99999


def reachable(proxy, protocol):
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


for tr in trs:
    tds = tr.find_all("td")
    if tds:
        ip = tds[0].text
        if not validate_ip(ip):
            continue
        port = tds[1].text
        if not validate_port(port):
            continue
        proxy = f"{ip}:{port}"
        protocol = "https" if "yes" in tds[6].text.strip() else "http"
        if reachable(proxy, protocol):
            proxies.append(proxy)
        else:
            failed.append(proxy)

with open("proxies_list.txt", "w") as f:
    f.write("\n".join(proxies))
