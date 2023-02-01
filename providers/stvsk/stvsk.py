#-*-coding:utf8;-*-

import requests, json, os
from datetime import datetime
from providers.stvsk.login import pin


channels = {}
headers = {"User-Agent": "okhttp/3.12.12"}
kd = "h265"
adaptive = "%2Cvast%2Cclientvast%2Cadaptive2%2Cwebvtt"
try:
    with open("./providers/stvsk/stvsk_data.json", 'r') as openfile:
        data = json.load(openfile)
    deviceId = data["deviceId"]
    passwordId = data["password"]
except:
    deviceId = ""
    passwordId = ""


def get_sessid():
    phpsessid = ""
    req = requests.get("https://sledovanietv.sk/api/device-login?deviceId=" + str(deviceId) + "&password=" + str(passwordId) + "&version=2.44.16&lang=sk&unit=default&capabilities=" + adaptive, headers = headers).json()
    if req["status"] == 1:
        phpsessid = req["PHPSESSID"]
        requests.get("https://sledovanietv.sk/api/pin-unlock?pin=" + str(pin) + "&PHPSESSID=" + phpsessid, headers = headers).json()
    return phpsessid


sessid = get_sessid()
if sessid != "":
    req = requests.get("https://sledovanietv.sk/api/get-stream-qualities?PHPSESSID=" + sessid).json()
    q = []
    for x in req["qualities"]:
        if x["allowed"] == 1:
            q.append(x["id"])
    q.sort()
    quality = str(q[-1])
    req = requests.get("https://sledovanietv.sk/api/playlist?quality=" + quality + "&capabilities=" + kd + adaptive + "&force=true&format=m3u8&type=&logosize=96&whitelogo=true&drm=&subtitles=1&PHPSESSID=" + sessid, headers = headers).json()
    if req["status"] == 1:
        groups = req["groups"]
        for d in req["channels"]:
            if d["locked"] == "none":
                url = d["url"]
                channels[d["id"]] = {"name": d["name"], "url": d["url"], "logo": d["logoUrl"], "type": d["type"], "group": groups[d["group"]]}


def get_catchup(id, utc, utcend):
    id = id.split(".")[0]
    date_time_start = datetime.fromtimestamp(int(utc) + 1)
    d_start = date_time_start.strftime("%Y-%m-%d+%H:%M:%S")
    url =  "http://sledovanietv.sk/download/noAccess-cs.m3u8"
    sessid = get_sessid()
    if sessid != "":
        req = requests.get("http://sledovanietv.sk/api/epg?time=" + d_start + "&duration=1439&detail=poster&channels=" + id + "&PHPSESSID=" + sessid, headers = headers).json()
        if req["status"] == 1:
            eventId = req["channels"][id][0]["eventId"]
            req = requests.get("https://sledovanietv.sk/api/get-stream-qualities?PHPSESSID=" + sessid).json()
            q = []
            for x in req["qualities"]:
                if x["allowed"] == 1:
                    q.append(x["id"])
            q.sort()
            quality = str(q[-1])
            req = requests.get("https://sledovanietv.sk/api/event-timeshift?format=m3u8&quality=" + quality + "&capabilities=" + kd + adaptive + "&force=true&eventId=" + eventId + "&overrun=1&PHPSESSID=" + sessid, headers = headers).json()
            if req["status"] == 1:
                url = req["url"]
    return url
