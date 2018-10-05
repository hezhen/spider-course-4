# -*- coding: utf-8 -*-
import requests
import re

# custom header
headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3',
    'Accept-Charset': 'utf-8',
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.2; WOW64; rv:47.0) Gecko/20100101 Firefox/47.0',
    'Connection': 'keep-alive'
}

if __name__ == '__main__':
    item_url = "https://detail.tmall.com/item.htm?id=561009686445"

    try:
        # ignore ssl error, optionally can set phantomjs path
        r = requests.get(item_url, headers=headers)

        with open('tmall_url.html', 'w+') as f:
            f.write(r.text)

        # 使用 (pattern) 进行获取匹配
        # +? 使用非贪婪模式
        # [^>\"\'\s] 匹配任意不为 > " ' 空格 制表符 的字符
        tmall_links = re.findall('href=[\"\']{1}(//detail.tmall.com/item.htm[^>\"\'\s]+?)"', r.text)
        taobao_links = re.findall('href=[\"\']{1}(//detail.taobao.com/item.htm[^>\"\'\s]+?)"', r.text)

        for link in tmall_links:
            print(link)
        for link in taobao_links:
            print(link)

    except Exception as err:
        print(err)