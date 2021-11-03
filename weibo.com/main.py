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

start = 1
end = 1
for i in range(start, end + 1):
    url = 'https://m.weibo.cn/search?containerid=' + \
        '231522type%3D1%26t%3D10%26q%3D%23日本旅行%23&luicode=10000011&lfid=100103type%3D1%26q%3D日本'
    html = requests.get(url, headers=headers).text
    soup = BeautifulSoup(html, 'html.parser')
    logging.info(soup)
    print('%d / %d' % (i, end))
logging.info('End')
