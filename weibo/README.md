## 利用接口来抓取微博数据

分别启动 user_crawler.py 与 feeds_crawler.py 抓取用户信息与每个用户的微博，user_crawler.py 是必须启动的，如果只需要用户信息，可以不启动 feeds_crawler.py 

> user_crawler.py 抓取用户信息

> feeds_crawler.py 抓取用户的 feed 流，如果只需要用户信息，可以不运行这个文件

> mongo_db_manager.py mongo 数据库，需要修改mongo的配置信息，数据存储在 weibo 库下。保存微博的feed流

> mysql_db_manager.py mysql 数据库，用来保存用户信息