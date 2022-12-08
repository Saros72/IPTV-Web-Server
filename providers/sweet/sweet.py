# -*- coding: utf-8 -*-


import requests, json


try:
    with open("./providers/sweet/sweet_token.json", 'r') as openfile:
        data = json.load(openfile)
    refresh_token = data["refresh_token"]
except:
    refresh_token = ""
try:
    with open("./providers/sweet/sweet_channels.json", 'r') as openfile:
        channels = json.load(openfile)
except:
    channels = {}
UA ='Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:105.0) Gecko/20100101 Firefox/105.0'
UUID = "07d2453f-0031-4573-95d5-16b3237eb497"
headers = {'Host': 'api.sweet.tv', 'user-agent': UA, 'accept': 'application/json, text/plain, */*', 'accept-language': 'pl', 'x-device': '1;22;0;2;3.2.57', 'origin': 'https://sweet.tv', 'dnt': '1', 'referer': 'https://sweet.tv/'}


def get_token():
    data = {'device': {'type': 'DT_Web_Browser', 'application': {'type': 'AT_SWEET_TV_Player'}, 'model': UA, 'firmware': {'versionCode': 1, 'versionString': '3.2.57'}, 'uuid': UUID, 'supported_drm': {'widevine_modular': True}, 'screen_info': {'aspectRatio': 6, 'width': 1366, 'height': 768}}, 'refresh_token': refresh_token}
    req = requests.post("https://api.sweet.tv/AuthenticationService/Token.json", json = data, headers = headers).json()
    if req["result"] == "OK":
        return req["access_token"]
    else:
        return ""


def get_stream(id):
    try:
        id = id.split(".")[0]
        access_token = get_token()
        headers["authorization"] = "Bearer " + access_token
        data = {'without_auth': True, 'channel_id': int(id), 'accept_scheme': ['HTTP_HLS'], 'multistream': True}
        req = requests.post("https://api.sweet.tv/TvService/OpenStream.json", json = data, headers = headers).json()
        if req["result"] == "OK":
            url = "https://" + req["http_stream"]["host"]["address"] + req["http_stream"]["url"]
        else:
             url = "http://sledovanietv.sk/download/noAccess-cs.m3u8"
    except:
         url = "http://sledovanietv.sk/download/noAccess-cs.m3u8"
    return url


def get_catchup(id, utc):
    try:
        id = int(id.split(".")[0])
        ids = []
        ids.append(id)
        access_token = get_token()
        headers["authorization"] = "Bearer " + access_token
        data = {"epg_limit_prev":0,"epg_limit_next":1,"epg_current_time":int(utc),"need_epg":True,"need_icons":False,"need_big_icons":False,"need_categories":False,"need_offsets":False,"need_list":True,"channels":ids}
        req = requests.post("https://api.sweet.tv/TvService/GetChannels.json", json = data, headers = headers).json()
        if req["status"] == "OK":
            epg_id = req["list"][0]["epg"][0]["id"]
            data = {'without_auth': True, 'channel_id': int(id), 'accept_scheme': ['HTTP_HLS'], 'multistream': True, 'epg_id': int(epg_id)}
            req = requests.post("https://api.sweet.tv/TvService/OpenStream.json", json = data, headers = headers).json()
            if req["result"] == "OK":
                url = "https://" + req["http_stream"]["host"]["address"] + req["http_stream"]["url"]
            else:
                url = "http://sledovanietv.sk/download/noAccess-cs.m3u8"
        else:
            url = "http://sledovanietv.sk/download/noAccess-cs.m3u8"
    except:
         url = "http://sledovanietv.sk/download/noAccess-cs.m3u8"
    return url