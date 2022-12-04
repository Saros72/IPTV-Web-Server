#-*-coding:utf8;-*-


import requests, json, os, time
from datetime import datetime


channels = {}
try:
    with open("./providers/rebit/rebit_token.json", 'r') as openfile:
        data = json.load(openfile)
    token = data["token"]
    id = data["id"]
except:
    token = ""
    id = ""
headers = {"Content-Type": "application/json", "Authorization": "Bearer " + token, "x-television-client-id": id, "Host": "bbxnet.api.iptv.rebit.sk", "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:70.0) Gecko/20100101 Firefox/70.0"}
if token != "":
    req = requests.get("https://bbxnet.api.iptv.rebit.sk/television/channels", headers = headers)
    if req.status_code == 200:
        for r in req.json()["data"]:
            channels[r["channel"]] = {"name": r["title"], "logo": r["icon"], "id": r["id"]}


def get_stream(id):
    url = "http://sledovanietv.sk/download/noAccess-cs.m3u8"
    try:
        url = requests.get("https://bbxnet.api.iptv.rebit.sk/television/channels/" + str(id) + "/play", headers = headers).json()["data"]["link"]
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