from lxml import etree
import threading
import time
from mongo_redis_mgr import MongoRedisUrlManager
import argparse
import socket

import urllib3

import os

# from hdfs import *
# from hdfs.util import HdfsError
from socket_client import SocketClient
import protocol_constants as pc
import json

import argparse

class arguments:
    pass

def parse_app_arguments():
    parser = argparse.ArgumentParser(prog='CrawlerClient', description='Start a crawler client')
    parser.add_argument('-S', '--host-all', type=str, nargs=1, help='Host server for all services')
    parser.add_argument('-s', '--host', type=str, nargs=1, help='Crawler host server address, default is localhost')
    parser.add_argument('-p', '--host-port', type=int, nargs=1, help='Crawler host server port number, default is 20100')
    parser.add_argument('-m', '--mongo', type=str, nargs=1, help='Mongo Server address, default is localhost')
    parser.add_argument('-n', '--mongo-port', type=int, nargs=1, help='Mongo port number, default is 27017')
    parser.add_argument('-r', '--redis', type=str, nargs=1, help='Redis server address, default is localhost')
    parser.add_argument('-x', '--redis-port', type=int, nargs=1, help='Redis port number, default is 6379')

    args = arguments()

    parser.parse_args(namespace=args)

    if args.host_all is not None:
        args.host = args.mongo = args.redis = args.host_all

    if args.host is None:
        args.host = 'localhost'

    if args.mongo is None:
        args.mongo = 'localhost'

    if args.redis is None:
        args.redis = 'localhost'

    if args.host_port is None:
        args.host_port = 9999

    if args.mongo_port is None:
        args.mongo_port = 27017

    if args.redis_port is None:
        args.redis_port = 6379 

parse_app_arguments()


def get_page_content(cur_url, depth):
    global dir_name, dbmanager

    print( "downloading %s at level %d" % (cur_url, depth))
    links = []
    try:
        http = urllib3.PoolManager()
        r = http.request('GET', cur_url, headers = request_headers)
        filename = cur_url[7:].replace('/', '_')

        #Write page to local files system
        fo = open("%s%s.html" % (dir_name, filename), 'wb+')
        fo.write(r.data)
        fo.close()
        dbmanager.finishUrl(cur_url)
    except IOError as err:
        print( "get_page_content()", err )
        raise
    except Exception as err :
        print( "get_page_content()", err )
        raise

    html = etree.HTML(r.data.lower().decode('utf-8'))
    hrefs = html.xpath(u"//a")

    for href in hrefs:
        try:
            if 'href' in href.attrib:
                val = href.attrib['href']
                if val.find('javascript:') != -1:
                    continue
                if val.startswith('http://') is False:
                    if val.startswith('/'):
                        val = 'http://www.mafengwo.cn' + val
                    else:
                        continue
                if val[-1] == '/':
                    val = val[0:-1]
                links.append(val)
                dbmanager.enqueueUrl(val, 'new', depth+1)
        except ValueError:
            continue

    dbmanager.set_url_links(cur_url, links)

def heartbeat():
    global server_status, run_heartbeat, client_id, hb_period
    skip_wait = False
    while run_heartbeat:
        if skip_wait is False:
            time.sleep(hb_period)
        else:
            skip_wait = False
        try:
            hb_request = {}
            hb_request[pc.MSG_TYPE] = pc.HEARTBEAT
            hb_request[pc.CLIENT_ID] = client_id
            print("sending a heartbeat! ", str(hb_request))
            hb_response_data = socket_client.send(json.dumps(hb_request))

            # should be network error
            if hb_response_data is None:
                continue
            
            # print( 'Heart Beat response', json.dumps(hb_response_data))
            response = json.loads(hb_response_data)

            err = response.get(pc.ERROR)
            if err is not None:
                if err == pc.ERR_NOT_FOUND:
                    register_request = {}
                    register_request[pc.MSG_TYPE] = pc.REGISTER
                    client_id = socket_client.send(json.dumps(register_request))

                    # skip heartbeat period and send next heartbeat immediately
                    skip_wait = True
                    heartbeat()
                    return
                return

            action = response.get(pc.ACTION_REQUIRED)
            if action is not None:
                action_request = {}
                if action == pc.PAUSE_REQUIRED:
                    server_status = pc.PAUSED
                    action_request[pc.MSG_TYPE] = pc.PAUSED
                elif action == pc.PAUSE_REQUIRED:
                    server_status = pc.RESUMED
                    action_request[pc.MSG_TYPE] = pc.RESUMED
                elif action == pc.SHUTDOWN_REQUIRED:
                    server_status = pc.SHUTDOWN
                    # stop heartbeat thread
                    return
                action_request[pc.CLIENT_ID] = client_id
                socket_client.send(json.dumps(action_request))
            else:
                server_status = response[pc.SERVER_STATUS]

        except socket.error as msg:
            print ("heartbeat error: ", msg)
            server_status = pc.STATUS_CONNECTION_LOST
            raise

def start_heart_beat_thread():
    try:
        t = threading.Thread(target=heartbeat, name=None)
        # set daemon so main thread can exit when receives ctrl-c
        t.setDaemon(True)
        t.start()
    except Exception as err:
        print( "Error: unable to start thread", err)
        raise

def crawl():
    # thread pool size
    max_num_thread = 5
    CRAWL_DELAY = 2
    global dbmanager, is_root_page, threads, hb_period = 

    while True:
        if server_status == pc.STATUS_PAUSED:
            time.sleep(hb_period)
            continue
        if server_status == pc.SHUTDOWN:
            run_heartbeat = False
            for t in threads:
                t.join()
            break
        try:
            curtask = dbmanager.dequeueUrl()
        except Exception:
            time.sleep(hb_period)
            continue
        
        # Go on next level, before that, needs to wait all current level crawling done
        if curtask is None:
            time.sleep(hb_period)
            continue
        else:
            print( 'current task is: ', curtask['url'], "at depth: ", curtask['depth'])

        # looking for an empty thread from pool to crawl

        if is_root_page is True:
            get_page_content(curtask['url'], curtask['depth'])
            is_root_page = False
        else:
            while True:    
                # first remove all finished running threads
                for t in threads:
                    if not t.is_alive():
                        threads.remove(t)
                if len(threads) >= max_num_thread:
                    time.sleep(CRAWL_DELAY)
                    continue
                try:
                    t = threading.Thread(target=get_page_content, name=None, args=(curtask['url'], curtask['depth']))
                    threads.append(t)
                    # set daemon so main thread can exit when receives ctrl-c
                    t.setDaemon(True)
                    t.start()
                    time.sleep(CRAWL_DELAY)
                    break
                except Exception as err:
                    print( "Error: unable to start thread", err)
                    raise
def finish():
    global client_id
    shutdown_request = {}
    shutdown_request[pc.MSG_TYPE] = pc.SHUTDOWN
    shutdown_request[pc.CLIENT_ID] = client_id
    socket_client.send(json.dumps(shutdown_request))


def init():
    global client_id

    if os.path.exists(dir_name) is False:
        os.mkdir(dir_name)
    dbmanager.clear()
    dbmanager.enqueueUrl('http://www.mafengwo.cn', 'new', 0 )

    register_request = {}
    register_request[pc.MSG_TYPE] = pc.REGISTER
    client_id = socket_client.send(json.dumps(register_request))


# initialize global variables
request_headers = {
    'host': "www.mafengwo.cn",
    'connection': "keep-alive",
    'cache-control': "no-cache",
    'upgrade-insecure-requests': "1",
    'user-agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.95 Safari/537.36",
    'accept': "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    'accept-language': "zh-CN,en-US;q=0.8,en;q=0.6"
}


# Initialize system variables
dir_name = 'mfw/'

# db manager
dbmanager = MongoRedisUrlManager()

is_root_page = True
threads = []

# use hdfs to save pages
# hdfs_client = InsecureClient('http://54.223.92.169:50070', user='ec2-user')

socket_client = SocketClient('localhost', 20010)
client_id = 0

hb_period = 5
run_heartbeat = True
server_status = pc.STATUS_RUNNING

init()
start_heart_beat_thread()
crawl()
finish()