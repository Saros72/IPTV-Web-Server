# -*- coding: utf-8 -*-


import requests, datetime, json, os
from urllib.parse import quote


try:
    with open("./providers/orange/orange_token.json", 'r') as openfile:
        data = json.load(openfile)
    token = data["token"]
    subscription = data["subscription"]
except:
    token = ""
    subscription = ""
try:
    with open("./providers/orange/orange_channels.json", 'r') as openfile:
        channels = json.load(openfile)
except:
    channels = {}
device_id = "b7pzci54mrzbcvy"
headers = {"X-NanguTv-App-Version": "Android#7.6.3", "X-NanguTv-Device-Name": "Nexus 7", "User-Agent": "Dalvik/2.1.0 (Linux; U; Android 5.1.1; Nexus 6 Build/LMY47A)", "Accept-Encoding": "gzip", "Connection": "Keep-Alive", "Content-Type": "application/x-www-form-urlencoded;charset=UTF-8"}


def get_stream(id):
    id = id.split(".")[0]
    url = "http://sledovanietv.sk/download/noAccess-cs.m3u8"
    try:
        params = {"serviceType": "LIVE_TV", "subscriptionCode": subscription, "channelKey": id, "deviceType": "MOBILE", "streamingProtocol": "HLS"}
        cookies = {"access_token": token, "deviceId": device_id}
        req = requests.get("http://app01.gtm.orange.sk/sws/server/streaming/uris.json", params = params, headers = headers, cookies = cookies).json()
        url = req["uris"][-1]["uri"]
    except:
        url = "http://sledovanietv.sk/download/noAccess-cs.m3u8"
    return url


def get_catchup(id, utc, utcend):
    start = utc
    if utcend == "":
        end = int(utc) + 18000
        now =  int(datetime.datetime.now().timestamp())
        if end > now:
            end = now - 200
    else:
        end = utcend
    url =  "http://sledovanietv.sk/download/noAccess-cs.m3u8"
    try:
        cookies = {"access_token": token, "deviceId": device_id}
        params = {"serviceType": "TIMESHIFT_TV", "subscriptionCode": subscription, "channelKey": quote(id.split(".")[0]), "deviceType": "MOBILE", "streamingProtocol": "HLS", "fromTimestamp": str(start), "toTimestamp": str(end)}
        req = requests.get("http://app01.gtm.orange.sk/sws/server/streaming/uris.json", params = params, headers = headers, cookies = cookies).json()
        url = req['uris'][0]['uri']
    except:
        url = "http://sledovanietv.sk/download/noAccess-cs.m3u8"
    return url