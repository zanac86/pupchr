#!/usr/bin/python
# -*- coding: UTF-8 -*-
'''
ungoogled-chromium
A lightweight approach to removing Google web service dependency
https://github.com/Eloston/ungoogled-chromium


Downloads for ungoogled-chromium
https://ungoogled-software.github.io/ungoogled-chromium-binaries/
'''

import urllib.request as urlreq  # Python 3.
import os
import sys
import re
from pathlib import Path
import shutil
import zipfile


def findUrl(html, r):
    s = str(html)
    m = re.search(r, s)
    if m is None:
        print("No url %s in html %s" % (r, html))
        return None
    return str(m.group(0))


def getPage(url):
    ua = 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36'
    req = urlreq.Request(url)
    req.add_header('User-Agent', ua)
    content = urlreq.urlopen(req).read()
    return content


def RequestBuildInfo():
    url0 = "https://ungoogled-software.github.io"
    url = url0+"/ungoogled-chromium-binaries/"
    buildRe = "/ungoogled-chromium-binaries/releases/windows/64bit/[-\\.\\w]+"
    zipRe = "https://github.com/tangalbert919/ungoogled-chromium-binaries/releases/download/[-/\\.\\w]+\\.zip"
    print("Requesting build page...")
    buildUrl = url0 + findUrl(getPage(url), buildRe)
    print("Requesting release page...")
    releaseUrl = findUrl(getPage(buildUrl), zipRe)
    return releaseUrl


def ClearDirectory(path):
    if Path(path).is_dir():
        print("Deleting dir ", path)
        shutil.rmtree(path)
    if Path(path).is_dir():
        print("Cannot delete dir ", path)
        sys.exit(1)


def UnpackZipFile(fn_zip, path):
    z = zipfile.ZipFile(fn_zip, "r")
    z.extractall(path)


def GetTopDirInZip(fn_zip):
    z = zipfile.ZipFile(fn_zip, "r")
    fn = z.filelist[0].filename
    s = fn.split("/")
    topDir = s[0]
    return topDir


def DownloadFile(url, filename):
    ua = 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36'
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


zipUrl = RequestBuildInfo()
if zipUrl is None:
    sys.exit(1)
print(zipUrl)

chrome_dir = "chrome-win"
zip_filename = "chrome-win.zip"
path_root = sys.path[0]
path_chrome_dir = os.path.join(sys.path[0], chrome_dir)
path_chrome_zip = os.path.join(sys.path[0], zip_filename)

ClearDirectory(path_chrome_dir)

DownloadFile(zipUrl, path_chrome_zip)

UnpackZipFile(zip_filename, path_root)

topDir = GetTopDirInZip(zip_filename)

os.rename(topDir, chrome_dir)
# os.remove(path_chrome_zip)
