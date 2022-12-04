# -*- coding: utf-8 -*-


import requests, datetime, json, os
from urllib.parse import quote


try:
    with open("./providers/o2tv/o2_token.json", 'r') as openfile:
        data = json.load(openfile)
    token = data["token"]
    subscription = data["subscription"]
except:
    token = ""
    subscription = ""


def get_stream(id):
    url = "http://sledovanietv.sk/download/noAccess-cs.m3u8"
    headers = {'X-NanguTv-App-Version': 'Android#6.4.1', 'User-Agent': 'Dalvik/2.1.0', 'Connection': 'Keep-Alive', 'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8', 'X-NanguTv-Device-Id' : 'b7pzci54mrzbcvy', 'X-NanguTv-Device-Name': 'TV-BOX', 'X-NanguTv-Access-Token': token}
    try:
        data = requests.get('https://app.o2tv.cz/sws/server/streaming/uris.json?serviceType=LIVE_TV&deviceType=STB&streamingProtocol=HLS&subscriptionCode=' + str(subscription) + '&channelKey=' + quote(id.split(".")[0]) + '&encryptionType=NONE', headers = headers).json()
        for d in data["uris"]:
            if d["resolution"] == "HD":
                url = d["uri"]
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
    headers = {'X-NanguTv-App-Version': 'Android#6.4.1', 'User-Agent': 'Dalvik/2.1.0', 'Connection': 'Keep-Alive', 'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8', 'X-NanguTv-Device-Id' : 'b7pzci54mrzbcvy', 'X-NanguTv-Device-Name': 'TV-BOX', 'X-NanguTv-Access-Token': token}
    req = requests.get('https://app.o2tv.cz/sws/server/streaming/uris.json?serviceType=TIMESHIFT_TV&deviceType=STB&streamingProtocol=HLS&subscriptionCode=' + subscription +'&fromTimestamp=' + str(start) + '000&toTimestamp=' + str(end) + '000&channelKey=' + quote(id.split(".")[0]) + '&encryptionType=NONE', headers = headers)
    if req.status_code == 200:
        return req.json()['uris'][0]['uri']
    else:
        return url