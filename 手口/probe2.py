import requests, re
url = "https://www.jpx.co.jp/markets/derivatives/participant-volume/index.html"
txt = requests.get(url).text
links = re.findall(r'href="(.*?)"', txt)
for l in links:
    if "volume_by_participant" in l:
        print(l)
        
    if "zip" in l:
        print("ZIP:", l)
