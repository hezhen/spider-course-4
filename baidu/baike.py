# -*- coding: utf-8 -*-

import urllib3
import urllib
from urllib.parse import quote
import string

url_format = 'https://baike.baidu.com/item/'

item_name = '阿尔伯特·爱因斯坦'

url = url_format + item_name

url = quote(url,safe=string.printable)

http = urllib3.PoolManager()
r = http.request('GET', url)
f = open( item_name + '.baike.html', 'wb+')
f.write(r.data)
f.close()