import mysql.connector
import hashlib
import time 
from datetime import datetime
from datetime import timedelta

import redis
from pymongo import MongoClient
from pymongo import IndexModel, ASCENDING, DESCENDING


class MongoManager:

    def __init__(self, server_ip='localhost', client=None, expires=timedelta(days=30)):
        """
        client: mongo database client
        expires: timedelta of amount of time before a cache entry is considered expired
        """
        # if a client object is not passed 
        # then try connecting to mongodb at the default localhost port 
        self.client = MongoClient(server_ip, 27017) if client is None else client
        #create collection to store cached webpages,
        # which is the equivalent of a table in a relational database
        self.db = self.client.spider

        # create index if db is empty
        if self.db.locations.count() is 0:
            self.db.mfw.create_index([("status", ASCENDING)])

    def dequeueItems(self, size):
        records = self.db.mfw.find({'status':'new'}).batch_size(50)

        ids = []
        for record in records:
            ids.append(record['_id'])
        
        self.db.mfw.update(
            {
                '_id': { '$in': ids }
            },
            {
                '$set': {'status': 'downloading'}
            }
        )

        if records:
            return records
        else:
            return None

    def finishItems(self, ids):
        self.db.mfw.update(
            {
                '_id': { '$in': ids }
            },
            {
                '$set': {'status': 'finish'}
            }
        )

    def clear(self):
        self.db.mfw.drop()

if __name__ == '__main__':
    mongo_mgr = MongoManager()
    records = mongo_mgr.dequeueItems(5)