# -*- coding: utf-8 -*-

import urllib3
import urllib
from urllib.parse import quote
import string

headers = {
    'accept': "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
    'accept-encoding': "gzip, deflate, br",
    'accept-language': "zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7",
    'cache-control': "no-cache",
    'connection': "keep-alive",
    'host': "www.baidu.com",
    'upgrade-insecure-requests': "1",
    'user-agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36",
}

url_format = 'https://www.baidu.com/s?wd='

item_name = '阿尔伯特·爱因斯坦'

url = url_format + item_name

url = quote(url,safe=string.printable)

http = urllib3.PoolManager()
r = http.request('GET', url, headers=headers)
f = open( item_name + '.baidu.html', 'wb+')
f.write(r.data)
f.close()

baidu_cache_urls = re.findall('http\:\/\/cache\.baiducontent\.com[^"]+', r.data)