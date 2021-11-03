import requests
from bs4 import BeautifulSoup
import os
import traceback
import re
import time
import logging

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36",
    "Connection": "keep-alive",
    "Referer": "image / webp, image / *, * / *;q = 0.8",
    "Accept": "image/webp,image/*,*/*;q=0.8"
}

def download(url, filename):
    if os.path.exists(filename):
        print('file exists!')
        logging.info('file exists!')
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


def create_folder(foldername):
    if os.path.exists(foldername) is False:
        os.makedirs(foldername)


logging.basicConfig(filename='log.txt', level=logging.INFO)
logging.info('Start')
create_folder('imgs')
create_folder('imgs/' + 'characters')

start = 347050
end = 1000000
for i in range(start, end + 1):
    url = 'https://donmai.us/posts/%d' % i
    html = requests.get(url, headers=headers).text
    soup = BeautifulSoup(html, 'html.parser')
    information = soup.find('section', id='post-information')
    if information is None:
        continue
    if information.find('a', string=re.compile("B")) is None:
        continue
    characters = soup.find('ul', class_='character-tag-list')
    if characters is None:
        if information.find('li', string="Rating: Safe"):
            create_folder('imgs/' + 'Safe')
            target_url = information.find('a', string=re.compile("B"))['href']
            filename = os.path.join('imgs/' + 'Safe', target_url.split('/')[-1])
            download(target_url, filename)
        elif information.find('li', string="Rating: Questionable"):
            create_folder('imgs/' +  'Questionable')
            target_url = information.find('a', string=re.compile("B"))['href']
            filename = os.path.join('imgs/' + 'Questionable', target_url.split('/')[-1])
            download(target_url, filename)
        elif information.find('li', string="Rating: Explicit"):
            create_folder('imgs/' + 'Explicit')
            target_url = information.find('a', string=re.compile("B"))['href']
            filename = os.path.join('imgs/' + 'Explicit', target_url.split('/')[-1])
            download(target_url, filename)
    elif characters.find('a', class_='search-tag'):
        if characters.find('a', class_='search-tag').string is None:
            continue
        foldername = characters.find('a', class_='search-tag').string.replace(" ","_")
        create_folder('imgs/' + 'characters/' + foldername)
        if information.find('li', string="Rating: Safe"):
            create_folder('imgs/' + 'characters/' + foldername + '/' + 'Safe')
            target_url = information.find('a', string=re.compile("B"))['href']
            filename = os.path.join('imgs/' + 'characters/' + foldername + '/' + 'Safe', target_url.split('/')[-1])
            download(target_url, filename)
        elif information.find('li', string="Rating: Questionable"):
            create_folder('imgs/' + 'characters/' + foldername + '/' + 'Questionable')
            target_url = information.find('a', string=re.compile("B"))['href']
            filename = os.path.join('imgs/' + 'characters/' + foldername + '/' + 'Questionable', target_url.split('/')[-1])
            download(target_url, filename)
        elif information.find('li', string="Rating: Explicit"):
            create_folder('imgs/' + 'characters/' + foldername + '/' + 'Explicit')
            target_url = information.find('a', string=re.compile("B"))['href']
            filename = os.path.join('imgs/' + 'characters/' + foldername + '/' + 'Explicit', target_url.split('/')[-1])
            download(target_url, filename)
    logging.info(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + '  %d / %d' % (i, end))
    print('%d / %d' % (i, end))
logging.info('End')
