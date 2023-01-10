#-*-coding:utf8;-*-


import requests, json, os


channels = {}
try:
    with open("./providers/net/net_token.json", 'r') as openfile:
        data = json.load(openfile)
    token = data["token"]
except:
    token = ""
if token != "":
    data = {"device_token": token}
    req = requests.post("https://backoffice.as.4net.tv/api/device/getSources/", json = data, headers = {"Content-Type": "application/json"}).json()
    if req["success"] == True:
        for c in req["channels"]:
            channels[c["id"]] = ((c["name"], c["content_sources"][0]["stream_profile_urls"]["adaptive"]))


def get_catchup(id, utc, utcend):
    url = "http://sledovanietv.sk/download/noAccess-cs.m3u8"
    try:
        req = requests.get("https://backoffice.4net.tv/contentd/api/device/getContent?device_token=" + token + "&channel_id=" + id + "&start=" + utc + "&end=" + utcend + "&broadcast_offset=").json()
        if req["success"] == True:
            url = req["stream_uri"]
    except:
        url = "http://sledovanietv.sk/download/noAccess-cs.m3u8"
    return url

