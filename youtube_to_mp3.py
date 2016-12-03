import wget
import requests
import time

fetch_urls = []


def generate_urls():
    f = open('/Users/tonyjia/Pictures/song/vid_urls.txt', 'r')
    for line in f:
        # line = 'http://www.youtube.com/watch?v=URYrz-xdxHw'
        ll = 'http://www.youtubeinmp3.com/fetch/?format=text&video='+line
        fetch_urls.append(ll)


def download_mp3s():
    f = open('/Users/tonyjia/Pictures/song/vid_urls_.txt', 'w')

    for download_url in fetch_urls:
        download_url = download_url.strip()
        r = requests.get(download_url)
        download_url = r.text.split('Link: ')
        if len(download_url) == 1:
            continue

        f.write(download_url[1])

        #print download_url[1]
        #wget.download(download_url[1])


def download_mp3s_from_file():
    f = open('/Users/tonyjia/Pictures/song/vid_urls_.txt', 'r')

    for line in f:
        wget.download(line)
        time.sleep(1)

#generate_urls()
#download_mp3s()
download_mp3s_from_file()

