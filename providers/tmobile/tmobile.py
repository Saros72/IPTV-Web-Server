#-*-coding:utf8;-*-


import requests, os, sys, json, uuid
from datetime import datetime
from urllib.parse import urlparse


UA = "okhttp/3.12.12"
dev_name = "ANDROID-PHONE"


def get_data():
    try:
        with open("./providers/tmobile/tmobile_token.json", 'r') as openfile:
            data = json.load(openfile)
        accesstoken = data["accesstoken"]
        refreshtoken = data["refreshtoken"]
    except:
        accesstoken = ""
        refreshtoken = ""
    return accesstoken, refreshtoken


def set_data(data):
    json_object = json.dumps(data, indent=4)
    with open("./providers/tmobile/tmobile_token.json", "w") as outfile:
        outfile.write(json_object)


def get_stream(id):
    url = "http://sledovanietv.sk/download/noAccess-cs.m3u8"
    accesstoken, refreshtoken = get_data()
    params={"refreshToken": refreshtoken}
    headers={'Origin': 'https://www.magiogo.cz', 'Pragma': 'no-cache', 'Referer': 'https://www.magiogo.cz/', 'User-Agent': UA, 'Sec-Fetch-Mode': 'cors', 'Sec-Fetch-Site': 'cross-site'}
    req = requests.post("https://czgo.magio.tv/v2/auth/tokens", json = params, headers = headers).json()
    if req["success"] == True:
        accesstoken = req["token"]["accessToken"]
        refreshtoken = req["token"]["refreshToken"]
        set_data({"accesstoken": accesstoken, "refreshtoken": refreshtoken})
        params={"service": "LIVE", "name": dev_name, "devtype": "OTT_LINUX_4302", "id": int(id.split(".")[0]), "prof": "p5", "ecid": "", "drm": "verimatrix"}
        headers = {"authorization": "Bearer " + accesstoken, 'Origin': 'https://www.magiogo.cz', 'Pragma': 'no-cache', 'Referer': 'https://www.magiogo.cz/', 'Sec-Fetch-Mode': 'cors', 'Sec-Fetch-Site': 'cross-site', 'User-Agent': UA}
        req = requests.get("https://czgo.magio.tv/v2/television/stream-url", params = params, headers = headers).json()
        if req["success"] == True:
            url = req["url"]
            headers = {"Host": urlparse(url).netloc, "User-Agent": "ReactNativeVideo/3.13.2 (Linux;Android 10) ExoPlayerLib/2.10.3", "Connection": "Keep-Alive"}
            req = requests.get(url, headers = headers, allow_redirects=False)
            url = req.headers["location"]
        else:
            url = "http://sledovanietv.sk/download/noAccess-cs.m3u8"
    else:
        url = "http://sledovanietv.sk/download/noAccess-cs.m3u8"
    return url


def get_channels():
    accesstoken, refreshtoken = get_data()
    dev_name = "ANDROID-PHONE"
    params={"refreshToken": refreshtoken}
    headers={'Origin': 'https://www.magiogo.cz', 'Pragma': 'no-cache', 'Referer': 'https://www.magiogo.cz/', 'User-Agent': UA, 'Sec-Fetch-Mode': 'cors', 'Sec-Fetch-Site': 'cross-site'}
    req = requests.post("https://czgo.magio.tv/v2/auth/tokens", json = params, headers = headers).json()
    if req["success"] == True:
        accesstoken = req["token"]["accessToken"]
        refreshtoken = req["token"]["refreshToken"]
        set_data({"accesstoken": accesstoken, "refreshtoken": refreshtoken})
    params={"list": "LIVE", "queryScope": "LIVE"}
    headers = {"authorization": "Bearer " + accesstoken, 'Origin': 'https://www.magiogo.cz', 'Pragma': 'no-cache', 'Referer': 'https://www.magiogo.cz/', 'Sec-Fetch-Mode': 'cors', 'Sec-Fetch-Site': 'cross-site', 'User-Agent': UA}
    ch = {}
    try:
        req = requests.get("https://czgo.magio.tv/home/categories?language=cz", headers = headers).json()["categories"]
        categories = {}
        for cc in req:
            for c in cc["channels"]:
                categories[c["channelId"]] = cc["name"]
        req = requests.get("https://czgo.magio.tv/v2/television/channels", params = params, headers = headers).json()["items"]
        for c in req:
            group = categories[c["channel"]["channelId"]]
            ch[str(c["channel"]["channelId"])] = {"name": c["channel"]["name"], "logo": c["channel"]["logoUrl"], "group": group}
    except:
        ch = {}
    return ch


def get_catchup(id, utc, utcend):
    id = int(id.split(".")[0])
    accesstoken, refreshtoken = get_data()
    params={"refreshToken": refreshtoken}
    headers={'Origin': 'https://www.magiogo.cz', 'Pragma': 'no-cache', 'Referer': 'https://www.magiogo.cz/', 'User-Agent': UA, 'Sec-Fetch-Mode': 'cors', 'Sec-Fetch-Site': 'cross-site'}
    req = requests.post("https://czgo.magio.tv/v2/auth/tokens", json = params, headers = headers).json()
    if req["success"] == True:
        accesstoken = req["token"]["accessToken"]
        refreshtoken = req["token"]["refreshToken"]
        set_data({"accesstoken": accesstoken, "refreshtoken": refreshtoken})
        params={"service": "ARCHIVE", "name": dev_name, "devtype": "OTT_ANDROID", "id": int(id), "prof": "p5", "ecid": "", "drm": "verimatrix"}
        headers = {"authorization": "Bearer " + accesstoken, 'Origin': 'https://www.magiogo.cz', 'Pragma': 'no-cache', 'Referer': 'https://www.magiogo.cz/', 'Sec-Fetch-Mode': 'cors', 'Sec-Fetch-Site': 'cross-site', 'User-Agent': UA}
        date_time_start = datetime.fromtimestamp(int(utc))
        d_start = date_time_start.strftime("%Y-%m-%dT%H:%M:%S")
        date_time_end = datetime.fromtimestamp(int(utcend) + 15)
        d_end = date_time_end.strftime("%Y-%m-%dT%H:%M:%S")
        req = requests.get("https://czgo.magio.tv/v2/television/epg?filter=channel.id==" + str(id) + "%20and%20startTime=ge=" + d_start + ".000Z%20and%20endTime=le=" + d_end + ".000Z&limit=10&offset=0&lang=CZ", params = params, headers = headers).json()
        if req["success"] == True:
            scheduleId = str(req["items"][0]["programs"][0]["scheduleId"])
            params={"service": "ARCHIVE", "name": dev_name, "devtype": "OTT_LINUX_4302", "id": int(scheduleId), "prof": "p5", "ecid": "", "drm": "verimatrix"}
            headers = {"authorization": "Bearer " + accesstoken, 'Origin': 'https://www.magiogo.cz', 'Pragma': 'no-cache', 'Referer': 'https://www.magiogo.cz/', 'Sec-Fetch-Mode': 'cors', 'Sec-Fetch-Site': 'cross-site', 'User-Agent': UA}
            req = requests.get("https://czgo.magio.tv/v2/television/stream-url", params = params, headers = headers).json()
            if req["success"] == True:
                url = req["url"]
                headers = {"Host": urlparse(url).netloc, "User-Agent": "ReactNativeVideo/3.13.2 (Linux;Android 10) ExoPlayerLib/2.10.3", "Connection": "Keep-Alive"}
                req = requests.get(url, headers = headers, allow_redirects=False)
                url = req.headers["location"]
            else:
                url = "http://sledovanietv.sk/download/noAccess-cs.m3u8"
        else:
            url = "http://sledovanietv.sk/download/noAccess-cs.m3u8"
    else:
        url = "http://sledovanietv.sk/download/noAccess-cs.m3u8"
    return url