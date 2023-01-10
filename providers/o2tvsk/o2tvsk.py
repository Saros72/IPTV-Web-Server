# -*- coding: utf-8 -*-


import requests, datetime, json, os
from urllib.parse import quote, unquote
from datetime import datetime
from providers.o2tvsk.login import O2TV_REPLACE_HD


try:
    with open("./providers/o2tvsk/o2sk_token.json", 'r') as openfile:
        data = json.load(openfile)
    token = data["token"]
    subscription = data["subscription"]
except:
    token = ""
    subscription = ""


def get_stream(id):
    id = id.split(".")[0]
    url = "http://sledovanietv.sk/download/noAccess-cs.m3u8"
    params = {"serviceType":"LIVE_TV", "subscriptionCode": subscription,"channelKey": unquote(id), "deviceType": "TABLET", "streamingProtocol":"HLS"}
    headers = { "X-Nangu-App-Version" : "Android#3.5.31.0-release", "X-Nangu-Device-Name" : "Lenovo B6000-H", "X-NanguTv-Device-size": "large", "X-NanguTv-Device-density": "213", "User-Agent" : "Dalvik/1.6.0 (Linux; U; Android 4.4.2; Lenovo B6000-H Build/KOT49H)", "Accept-Encoding": "gzip", "Connection" : "Keep-Alive" }
    cookies = { "access_token": token, "deviceId": "b7pzci54mrzbcvy"}
    try:
        req = requests.get('http://app.o2tv.cz/sws/server/streaming/uris.json', params=params, headers=headers, cookies=cookies).json()
        url = req["uris"][0]["uri"]
    except:
        url = "http://sledovanietv.sk/download/noAccess-cs.m3u8"
    return url


def get_catchup(id, utc, utcend):
    id = id.split(".")[0]
    start = utc
    if utcend == "":
        end = int(utc) + 18000
        now =  int(datetime.datetime.now().timestamp())
        if end > now:
            end = now - 200
    else:
        end = utcend
    url =  "http://sledovanietv.sk/download/noAccess-cs.m3u8"
    params = {"serviceType":"TIMESHIFT_TV", "subscriptionCode": subscription, "channelKey": unquote(id), "deviceType":"TABLET", "fromTimestamp": str(start) + '000', "streamingProtocol":"HLS", "toTimestamp": str(end) + '000'}
    headers = { "X-Nangu-App-Version" : "Android#3.5.31.0-release", "X-Nangu-Device-Name" : "Lenovo B6000-H", "X-NanguTv-Device-size": "large", "X-NanguTv-Device-density": "213", "User-Agent" : "Dalvik/1.6.0 (Linux; U; Android 4.4.2; Lenovo B6000-H Build/KOT49H)", "Accept-Encoding": "gzip", "Connection" : "Keep-Alive" }
    cookies = { "access_token": token, "deviceId": "b7pzci54mrzbcvy"}
    try:
        req = requests.get('http://app.o2tv.cz/sws/server/streaming/uris.json', params=params, headers=headers, cookies=cookies).json()
        url = req["uris"][0]["uri"]
    except:
        url = "http://sledovanietv.sk/download/noAccess-cs.m3u8"
    return url