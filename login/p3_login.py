# -*- coding: utf-8 -*-

import urllib
import urllib3
import glob
import sqlite3
import os



url="http://192.168.1.27/xiaoxiang/login.php"
url_success = "http://192.168.1.27/xiaoxiang/main.php"

headers = {
    'host': "192.168.1.27",
    'connection': "keep-alive",
    'cache-control': "no-cache",
    'content-type': "application/x-www-form-urlencoded",
    'upgrade-insecure-requests': "1",
    'user-agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit" \
                  "/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36",
    'accept': "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    'accept-language': "zh-CN,en-US;q=0.8,en;q=0.6",
}

if __name__ == '__main__':
    data = {'name':'caca', "password":'c'}

    http = urllib3.PoolManager()
    r = http.request('POST', url, fields= data, headers = headers, redirect = False)
    headers['cookie'] = r.getheader('set-cookie')
    # r = http.request('GET', url, headers = headers)
    
    r = http.request('GET', url_success, headers = headers, redirect = False)
    print(r.data)
