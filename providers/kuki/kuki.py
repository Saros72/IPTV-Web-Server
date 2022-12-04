#-*-coding:utf8;-*-

import requests, json, os, time
from datetime import datetime


channels = {}
try:
    sn = open("./providers/kuki/kuki_sn", "r").read()
except:
    sn = ""


if sn != "":
    data = {"sn": "kuki2.0_" + sn}
    req = requests.post("https://as.kuki.cz/api-v2/register", data = data).json()
    if req["state"] == "OK":
        headers = {"x-sessionkey": req["session_key"]}
        req = requests.get("https://as.kuki.cz/api-v2/channel-list", headers = headers).json()
        for r in req:
            channels[r["ident"]] = {"name": r["name"], "logo": "https://media.kuki.cz/imagefactory/channel_logo/channel-left-panel/fhd/" + r["epgLogo"], "type": r["streamType"]}


def get_stream(id, utc):
    try:
        data = {"sn": "kuki2.0_" + sn}
        req = requests.post("https://as.kuki.cz/api-v2/register", data = data).json()
        if req["state"] == "OK":
            data = {"type": "live", "ident": id}
            headers = {"x-sessionkey": req["session_key"]}
            req = requests.post("https://as.kuki.cz/api-v2/sign/video", data = data, headers = headers).json()
            sign = req["sign"]["sign"]
            expires = req["sign"]["expires"]
            baseUrl = req["baseUrl"]
            if utc == "":
                url = baseUrl + id + "/stream.m3u8?resolution=2&dialect=c2&forcelive=1&dd=1&fpsint=0&epd=0&dt=smarttv&hevc=1&wv=0&type=live&expires=" + str(expires) + "&sign=" + sign
            else:
                url = baseUrl + id + "/stream.m3u8?resolution=2&dialect=c2&forcelive=1&dd=1&fpsint=0&epd=0&dt=smarttv&hevc=1&wv=0&type=ts&expires=" + str(expires) + "&sign=" + sign + "&start=" + str(utc) + "000"
        else:
             url = "http://sledovanietv.sk/download/noAccess-cs.m3u8"
    except:
         url = "http://sledovanietv.sk/download/noAccess-cs.m3u8"
    return url


def get_catchup(id, utc, utcend):
    url = "http://sledovanietv.sk/download/noAccess-cs.m3u8"
    try:
        utc = int(utc) + (time.timezone)
        date_time_start = datetime.fromtimestamp(int(utc))
        date_time_end = datetime.fromtimestamp(int(utc) + 120)
        dfrom = date_time_start.strftime("%Y-%m-%d+%H:%M:%S")
        dto = date_time_end.strftime("%Y-%m-%d+%H:%M:%S")
        req = requests.get("https://bbxnet.api.iptv.rebit.sk/television/channels/" + id + "/programmes?filter[start][ge]=" + dfrom + "&filter[start][le]=" + dto, headers = headers).json()["data"][0]["id"]
        url = requests.get("https://bbxnet.api.iptv.rebit.sk/television/channels/" + str(id) + "/play/" + req, headers = headers).json()["data"]["link"]
    except:
        url = "http://sledovanietv.sk/download/noAccess-cs.m3u8"
    return url