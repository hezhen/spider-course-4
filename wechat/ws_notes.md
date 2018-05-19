https://mp.weixin.qq.com/mp/profile_ext?action=getmsg&__biz=MjAzNzMzNTkyMQ==&f=json&offset=10&count=10&is_ok=1&scene=124&uin=777&key=777&pass_ticket=gBYwkCSGTQfokPu2Qoi6k8yT0jmUhuCn9FIMOBy60Rg%3D&wxtoken=&appmsg_token=930_gtCOZ%252B7AVpsyBO%252BDxUVtIowUMTb4R6vZhnvY1g~~&x5=1&f=json

https://mp.weixin.qq.com/mp/profile_ext?action=getmsg&__biz=MjAzNzMzNTkyMQ==&f=json&offset=20&count=10&is_ok=1&scene=124&uin=777&key=777&pass_ticket=gBYwkCSGTQfokPu2Qoi6k8yT0jmUhuCn9FIMOBy60Rg%3D&wxtoken=&appmsg_token=930_gtCOZ%252B7AVpsyBO%252BDxUVtIowUMTb4R6vZhnvY1g~~&x5=1&f=json

https://mp.weixin.qq.com/mp/profile_ext?action=home&__biz=MjAzNzMzNTkyMQ==&scene=124&devicetype=android-24&version=26051036&lang=zh_CN&nettype=WIFI&a8scene=3&pass_ticket=gBYwkCSGTQfokPu2Qoi6k8yT0jmUhuCn9FIMOBy60Rg%3D&wx_header=1

--------------------------------------------------------
#Second Day
--------------------------------------------------------
https://mp.weixin.qq.com/mp/profile_ext?action=getmsg&__biz=MjAzNzMzNTkyMQ==&f=json&offset=10&count=10&is_ok=1&scene=124&uin=777&key=777&pass_ticket=gBYwkCSGTQfokPu2Qoi6k8yT0jmUhuCn9FIMOBy60Rg%3D&wxtoken=&appmsg_token=930_0Nt7rOUlbrRMGttBW5n5eHFSLtFXreWiw1-vaA~~&x5=1&f=json


Host:mp.weixin.qq.com
Connection:keep-alive
Upgrade-Insecure-Requests:1
User-Agent:
Mozilla/5.0 (Linux; Android 7.0; SM-G9350 Build/NRD90M; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/53.0.2785.49 Mobile MQQBrowser/6.2 TBS/043613 Safari/537.36 MicroMessenger/6.5.16.1120 NetType/WIFI Language/zh_CN:
x-wechat-uin:MjQxMzA5MTE1
x-wechat-key:54320db02e367ad0994fe2a32e1687070bf56aae6283def1c629abdf5be1c46c4224f05d1687783694311095a678ca70f3e9332f9e25f604cf6cfa4086c22e1df76427cc63022b2f9c8e0b16db880645
Accept:text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/wxpic,image/sharpp,*/*;q=0.8
Accept-Encoding:gzip, deflate
Accept-Language:zh-CN,en-US;q=0.8
Cookie:wxtokenkey=d5f52765b21852efcb36c5bfe192342ca7a5ebfdbd3a9b300a343f7a9abd3b97; wxuin=241309115; pass_ticket=gBYwkCSGTQfokPu2Qoi6k8yT0jmUhuCn9FIMOBy60Rg=; wap_sid2=CLuriHMSXHAzQjJkRkZSNEFtZEtYbk1JR1FuLWxJVTI0c1VsQlNDMHNuYUtwOVFUZ2V3c21NOE1WMDdsRlBCWVBXdnZpQU9NOXR4TnZTbWhLVzJXUjk3bk1fSFRxSURBQUF+ML6LptAFOA1AlU4=
Q-UA2:QV=3&PL=ADR&PR=WX&PP=com.tencent.mm&PPVN=6.5.16&TBSVC=43601&CO=BK&COVC=043613&PB=GE&VE=GA&DE=PHONE&CHID=0&LCID=9422&MO= SM-G9350 &RL=1080*1920&OS=7.0&API=24
Q-GUID:0fc56071e3c199aabbd6e0c113b788cb
Q-Auth:31045b957cf33acf31e40be2f3e71c5217597676a9729f1b



--------------------------------------------------------
#empty results
--------------------------------------------------------

{
    "ret": 0,
    "errmsg": "ok",
    "msg_count": 0,
    "can_msg_continue": 0,
    "general_msg_list": "{\"list\":[]}",
    "next_offset": 139
}
--------------------------------------------------------
#adb tools
--------------------------------------------------------

### Downloading 
https://developer.android.com/studio/command-line/adb.html

https://dl.google.com/android/repository/platform-tools-latest-linux.zip

https://dl.google.com/android/repository/platform-tools-latest-darwin.zip

链接: https://pan.baidu.com/s/1bo1QsHL 密码: vdrg

## Methods

### Connection
// use ip 
$ adb tcpip 5555
// connect
$ adb connect device_ip_address
// list devices
$ adb devices
// kill adb server
$ adb kill-server

// choose a target and send command
adb -s serial_number command 

// send swipe command: adb shell input swipe x0 y0 x1 y1
$ adb shell input swipe 200 1000 200 200


--------------------------------------------------------
#Run anyproxy
--------------------------------------------------------
anyproxy -i --rule wxrule.js

