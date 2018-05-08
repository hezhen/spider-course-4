# -*- coding: utf-8 -*-
import hashlib
import threading
from collections import deque

from selenium import webdriver
import re
from lxml import etree
import time
from pybloomfilter import BloomFilter

from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

user_agent = (
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_4) " +
    "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/29.0.1547.57 Safari/537.36"
)

# 进入浏览器设置
options = webdriver.ChromeOptions()
# 设置中文
options.add_argument('lang=zh_CN.UTF-8')

# ---------- Important ----------------
# 设置为 headless 模式，调试的时候可以去掉
# -------------------------------------
options.add_argument("--headless")

# 更换头部
# options.add_argument('user-agent="Mozilla/5.0 (iPod; U; CPU iPhone OS 2_1 like Mac OS X; ja-jp) AppleWebKit/525.18.1 (KHTML, like Gecko) Version/3.1.1 Mobile/5F137 Safari/525.20"')
feeds_crawler = webdriver.Chrome(chrome_options=options)

feeds_crawler.set_window_size(1920, 1200)  # optional

domain = 'weibo.cn'
url_home = "http://passport." + domain + "/signin/login"

download_bf = BloomFilter(1024*1024*16, 0.01)
cur_queue = deque()

# feeds_crawler.find_element_by_class_name('WB_detail')
# time = feeds_crawler.find_elements_by_xpath('//div[@class="WB_detail"]/div[@class="WB_from S_txt2"]/a[0]').text

seed_user = 'http://weibo.com/yaochen'

min_mblogs_allowed = 100
max_follow_fans_ratio_allowed = 3

def get_element_by_xpath(cur_driver, path):
    tried = 0
    while tried < 6:
        html = cur_driver.page_source
        tr = etree.HTML(html)
        elements = tr.xpath(path)
        if len(elements) == 0:
            time.sleep(1)
            tried += 1
            continue
        return elements

def extract_feed(feeds):
    for i in range(0,20):
        scroll_to_bottom()
        for element in feeds_crawler.find_elements_by_class_name('WB_detail'):
            tried = 0
            while tried < 3:
                try:
                    feed = {}
                    feed['time'] = element.find_element_by_xpath('.//div[@class="WB_from S_txt2"]').text
                    feed['content'] = element.find_element_by_class_name('WB_text').text
                    feed['image_names'] = []
                    for image in element.find_elements_by_xpath('.//li[contains(@class,"WB_pic")]/img'):
                        feed['image_names'].append(re.findall('/([^/]+)$', image.get_attribute('src')))
                    feeds.append(feed)
                    print('--------------------')
                    print(feed['time'])
                    print(feed['content'])
                    break
                except Exception:
                    tried += 1
                    time.sleep(1)
        if go_next_page(feeds_crawler) is False:
            return feeds


def go_next_page(cur_driver):
    try:
        next_page = cur_driver.find_element_by_xpath('//a[contains(@class, "page next")]').get_attribute('href')
        print('next page is ' + next_page)
        cur_driver.get(next_page)
        time.sleep(3)
        return True
    except Exception:
        print('next page is not found')
        return False


def fetch_user(user_link):
    print('downloading ' + user_link)
    feeds_crawler.get(user_link)
    
    # 提取用户姓名
    account_name = get_element_by_xpath(feeds_crawler, '//h1')[0].text

    photo = get_element_by_xpath(feeds_crawler, '//p[@class="photo_wrap"]/img')[0].get('src')

    account_photo = re.findall('/([^/]+)$', photo)

    # 提取他的关注主页
    follows_link = get_element_by_xpath(feeds_crawler, '//a[@class="t_link S_txt1"]')[0].get('href')

    print('account: ' + account_name)
    print('follows link is ' + follows_link)

    feeds = []
    users = []

    t_feeds = threading.Thread(target=extract_feed, name=None, args=(feeds,))
    # t_users = threading.Thread(target=extract_user, name=None, args=(users,))

    t_feeds.setDaemon(True)
    # t_users.setDaemon(True)

    t_feeds.start()
    # t_users.start()

    t_feeds.join()

def login(username, password):
    print('Login')
    feeds_crawler.get(url_home)
    time.sleep(2)
    print('find click button to login')
    feeds_crawler.find_element_by_id('loginName').send_keys(username)
    feeds_crawler.find_element_by_id('loginPassword').send_keys(password)
    # 执行 click()
    feeds_crawler.find_element_by_id('loginAction').click()
    # 也可以使用 execute_script 来执行一段 javascript
    # feeds_crawler.execute_script('document.getElementsByClassName("W_btn_a btn_32px")[0].click()')

def crawl():
    while True:
        fetch_user(seed_user)

if __name__ == '__main__':
    try:
        login('18600663368', 'Xi@oxiang66')
        crawl()
    finally:
        feeds_crawler.close()
