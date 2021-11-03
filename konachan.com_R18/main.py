import requests
from bs4 import BeautifulSoup
import os
import traceback
import re

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36",
    "Connection": "keep-alive",
    "Referer": "image / webp, image / *, * / *;q = 0.8",
    "Accept": "image/webp,image/*,*/*;q=0.8"
}

def download(url, filename):
    if os.path.exists(filename):
        print('file exists!')
        return
    try:
        r = requests.get(url, stream=True, timeout=10, headers=headers)
        r.raise_for_status()
        with open(filename, 'wb') as f:
            for chunk in r.iter_content(chunk_size=1024):
                if chunk:  # filter out keep-alive new chunks
                    f.write(chunk)
                    f.flush()
        return filename
    except KeyboardInterrupt:
        if os.path.exists(filename):
            os.remove(filename)
        raise KeyboardInterrupt
    except Exception:
        traceback.print_exc()
        if os.path.exists(filename):
            os.remove(filename)


if os.path.exists('imgs') is False:
    os.makedirs('imgs')

start = 1
end = 10710
for i in range(start, end + 1):
    url = 'https://konachan.com/post?page=%d&tags=' % i
    html = requests.get(url, headers=headers).text
    soup = BeautifulSoup(html, 'html.parser')
    questionable = soup.find_all('img', alt=re.compile("Explicit"))
    for p in questionable:
        for img in p.parent.parent.parent.find_all(class_="directlink largeimg"):
            target_url = img['href']
            filename = os.path.join('imgs', target_url.split('/')[-1])
            download(target_url, filename)
        for img in p.parent.parent.parent.find_all(class_="directlink smallimg"):
            target_url = img['href']
            filename = os.path.join('imgs', target_url.split('/')[-1])
            download(target_url, filename)
    print('%d / %d' % (i, end))
