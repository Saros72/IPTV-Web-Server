# -*- coding: utf-8 -*-


import requests, datetime, json, os
from urllib.parse import urlparse


try:
    with open("./providers/touchtv/touchtv_token.json", 'r') as openfile:
        data = json.load(openfile)
    token = data["touch_id"]
    UUID = data["UUID"]
except:
    token = ""
    UUID = ""
try:
    with open("./providers/touchtv/touchtv_channels.json", 'r') as openfile:
        channels = json.load(openfile)
except:
    channels = {}


def get_stream(id):
    id = id.split(".")[0]
    url = "http://sledovanietv.sk/download/noAccess-cs.m3u8"
    try:
        headers = {"Connection": "keep-alive", "Content-type": "application/json", "Accept": "application/json", "User-Agent": "touchTV/4.2.2 (Linux; Android TV 11; cs; Amlogic VONTAR X2) ExoPlayerLib/2.17.1", "Host": "am.di-vision.sk", "Accept-Encoding": "gzip", "Content-Length": "92"}
        data = {"token": str(token),"deviceId": str(UUID),"selector": id}
        req = requests.post("https://am.di-vision.sk/rest/auth/stream", json = data, headers = headers).json()
        url = req["streamUrlHls"] + "?k=" + req["jwt"]
    except:
        url = "http://sledovanietv.sk/download/noAccess-cs.m3u8"
    return url


def get_catchup(id, utc):
    url = "http://sledovanietv.sk/download/noAccess-cs.m3u8"
    id = id.split(".")[0]
    d1 = datetime.datetime.fromtimestamp(int(utc)).strftime('%Y-%m-%d')
    did = ""
    selector = ""
    try:
        headers = {"X-DeviceId": str(UUID), "X-MobileToken": str(token), "Connection": "keep-alive", "Accept-Encoding": "", "User-Agent": "touchTV/4.2.2 (Linux; Android TV 11; cs; Amlogic VONTAR X2) ExoPlayerLib/2.17.1", "Host": "am.di-vision.sk"}
        req = requests.get("https://am.di-vision.sk/rest/assetgroups/" + str(channels [id]["gid"]) + "/assetgroups", headers = headers).json()
        for p in req:
            d2 = datetime.datetime.fromtimestamp(int(str(p["date"])[:-3])).strftime('%Y-%m-%d')
            if d1 == d2:
                did = str(p["id"])
        if did != "":
            req = requests.get("https://am.di-vision.sk/rest/assetgroups/" + did + "/assets", headers = headers).json()
            for s in req:
                if int(utc + "000") == s["start"]:
                    selector = s["selector"]
            if selector != "":
                url = channels[id]["vod"] + selector + "/playlist.m3u8"
            else:
                url = "http://sledovanietv.sk/download/noAccess-cs.m3u8"
    except:
        url = "http://sledovanietv.sk/download/noAccess-cs.m3u8"
    return url