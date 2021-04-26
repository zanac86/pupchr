#!/usr/bin/python
# -*- coding: UTF-8 -*-

'''
Python script to update Chromium by Woolyss

https://woolyss.com/

https://chromium.woolyss.com

Directory structure

CHROMIUM [root dir]
│   pupchr.py
│   chrome-win.zip [downloaded build archive]
└───chrome-win [unpacked dir from zip]
    └───chrome.exe

Run pupchr.py inside root dir
'''

import os
import sys
import urllib.request as urlreq  # Python 3.
import json
from pathlib import Path
import shutil
import zipfile

ua = 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36'

url = "https://chromium.woolyss.com/api/v3/?os=windows&bit=64&out=json"
chrome_dir = "chrome-win"
zip_filename = "chrome-win.zip"


def RequestBuildInfo():
    req = urlreq.Request(url)
    req.add_header('User-Agent', ua)
    contents = urlreq.urlopen(req).read()
    # contents = '{"chromium": {"windows": {"architecture": "64-bit", "timestamp": 1566028218, "editor": "The Chromium Authors", "channel": "dev", "repository": "snapshots", "download": "https://storage.googleapis.com/chromium-browser-snapshots/Win_x64/687940/chrome-win.zip", "version": "78.0.3887.0", "revision": 687940, "commit": "7442e6d61ee165d113d1b865f79229a961ceb355", "flash_ppapi_version": "32.0.0.238"}}}'
    return json.loads(contents)


def PrintBuildInfo(a):
    print("Version: :", a["chromium"]["windows"]["version"])
    print("Revision :", a["chromium"]["windows"]["revision"])
    print("Download :", a["chromium"]["windows"]["download"])


def ClearDirectory(path):
    if Path(path).is_dir():
        print("Deleting dir ", path)
        shutil.rmtree(path)
    if Path(path).is_dir():
        print("Cannot delete dir ", path)
        sys.exit(1)
    print("Creating dir ", path)
    os.mkdir(path)


def UnpackZipFile(fn_zip, path):
    z = zipfile.ZipFile(fn_zip, "r")
    z.extractall(path)


def DownloadFile(url, filename):
    print("Downloading ", url)
    url_request = urlreq.Request(url)
    url_request.add_header('User-Agent', ua)
    url_connect = urlreq.urlopen(url_request)
    buffer_size = 1024*512
    with open(filename, 'wb') as f:
        while True:
            buffer = url_connect.read(buffer_size)
            if not buffer:
                break
            # an integer value of size of written data
            f.write(buffer)
    url_connect.close()


a = RequestBuildInfo()
PrintBuildInfo(a)

path_root = sys.path[0]
path_chrome_dir = os.path.join(sys.path[0], chrome_dir)
path_chrome_zip = os.path.join(sys.path[0], zip_filename)

ClearDirectory(path_chrome_dir)
DownloadFile(a["chromium"]["windows"]["download"], path_chrome_zip)
UnpackZipFile(zip_filename, path_root)

# os.remove(path_chrome_zip)
