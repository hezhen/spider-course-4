import json
import threading

import requests
import time

from mysql_db_manager import CrawlDatabaseManager

start_uid = '1496814565'

CRAWL_DELAY = 2

class UsersCrawler:
    url_format = 'https://m.weibo.cn/api/container/getIndex?containerid=231051_-_followers_-_%s&page=%d'

    querystring = {"version":"v4"}

    payload = "------WebKitFormBoundary7MA4YWxkTrZu0gW\r\nContent-Disposition: form-data; name=\"version\"\r\n\r\nv4\r\n------WebKitFormBoundary7MA4YWxkTrZu0gW--"
    headers = {
        'content-type': "multipart/form-data; boundary=----WebKitFormBoundary7MA4YWxkTrZu0gW",
        'host': "m.weibo.cn",
        'connection': "keep-alive",
        'cache-control': "no-cache",
        'upgrade-insecure-requests': "1",
        'user-agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_4) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/11.1 Safari/605.1.15",
        'accept': "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        'accept-encoding': "gzip, deflate, sdch, br",
        'accept-language': "zh-CN,en-US;q=0.8,en;q=0.6",
        'Cookie': 'SUB=_2A2533pSEDeRhGeBP7FoW9SvEwjiIHXVVIDzMrDV6PUJbkdAKLUvukW1NRSUhSB1dD7AIeLf4smfqbCKFvILCjiSz; SUHB=03o1B1VamvmZEj; _T_WM=173d13c1c3dbed1a2391ba0453fc3160; SCF=AuGj08St8RzhZXXgaRZbwjaLR00o4RbjETtDYFhR9ua_RqIuk7CPW0WDsMeHFX2Z6RsswDupzaD6AzUJb78qB0M.',
        'postman-token': "0b85ea3b-073b-a799-4593-61095e4ed01a"
    }

    # response = requests.request("GET", url, data=payload, headers=headers, params=querystring)

    db_manager = None

    threads = []

    run = False

    def __init__(self):
        self.db_manager = CrawlDatabaseManager(10)

    def get_users(self, uid, page):
        url = (self.url_format)%(uid, page)
        response = requests.request("GET", url, data=self.payload, headers=self.headers, params=self.querystring)
        return response.text

    def get_uid(self):
        return self.db_manager.dequeue_user()

    def start(self):
        self.run = True
        t = threading.Thread(target=self.crawl_feeds, name=None)
        self.threads.append(t)
        # set daemon so main thread can exit when receives ctrl-c
        t.setDaemon(True)
        t.start()

    def crawl_users(self):
        kickstart = True
        self.run = True

        while self.run:
            if kickstart:
                kickstart = False
                uid = start_uid
            else:
                uid = self.get_uid()
            user_str = self.get_users(uid, 1)
            users = json.loads(user_str)
            for user in users['cards'][1]['card_group']:
                name = user['user']['screen_name']
                user_id = user['user']['id']
                followers_count = user['user']['followers_count']
                follow_count = user['user']['follow_count']
                description = user['user']['description']
                self.db_manager.enqueue_user(user_id,
                                             name=name,
                                             follow_count=follow_count,
                                             followers_count=followers_count,
                                             description=description)
            time.sleep(CRAWL_DELAY)
            print(users)
            break

if __name__ == '__main__':
    user_crawler = UsersCrawler()
    user_crawler.crawl_users()