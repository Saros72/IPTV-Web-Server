#-*-coding:utf8;-*-


import requests
import xml.etree.ElementTree as ET


channels = {"1": {"name": "ČT1", "logo": "https://raw.githubusercontent.com/Saros72/kodirepo/main/repo-19/service.iptv.web.server/ct.png"}, "2": {"name": "ČT2", "logo": "https://raw.githubusercontent.com/Saros72/kodirepo/main/repo-19/service.iptv.web.server/ct.png"}, "3": {"name": "ČT24", "logo": "https://raw.githubusercontent.com/Saros72/kodirepo/main/repo-19/service.iptv.web.server/ct.png"}, "4": {"name": "ČT Sport", "logo": "https://raw.githubusercontent.com/Saros72/kodirepo/main/repo-19/service.iptv.web.server/ct.png"}, "5": {"name": "ČT :D", "logo": "https://raw.githubusercontent.com/Saros72/kodirepo/main/repo-19/service.iptv.web.server/ct.png"}, "6": {"name": "ČT Art", "logo": "https://raw.githubusercontent.com/Saros72/kodirepo/main/repo-19/service.iptv.web.server/ct.png"}, "24": {"name": "iVysílání 1", "logo": "https://raw.githubusercontent.com/Saros72/kodirepo/main/repo-19/service.iptv.web.server/ct.png"}, "25": {"name": "iVysílání 2", "logo": "https://raw.githubusercontent.com/Saros72/kodirepo/main/repo-19/service.iptv.web.server/ct.png"}, "26": {"name": "iVysílání 3", "logo": "https://raw.githubusercontent.com/Saros72/kodirepo/main/repo-19/service.iptv.web.server/ct.png"}, "27": {"name": "iVysílání 4", "logo": "https://raw.githubusercontent.com/Saros72/kodirepo/main/repo-19/service.iptv.web.server/ct.png"}, "28": {"name": "iVysílání 5", "logo": "https://raw.githubusercontent.com/Saros72/kodirepo/main/repo-19/service.iptv.web.server/ct.png"}, "29": {"name": "iVysílání 6", "logo": "https://raw.githubusercontent.com/Saros72/kodirepo/main/repo-19/service.iptv.web.server/ct.png"}, "30": {"name": "iVysílání 7", "logo": "https://raw.githubusercontent.com/Saros72/kodirepo/main/repo-19/service.iptv.web.server/ct.png"}, "31": {"name": "iVysílání 8", "logo": "https://raw.githubusercontent.com/Saros72/kodirepo/main/repo-19/service.iptv.web.server/ct.png"}, "32": {"name": "iVysílání 9", "logo": "https://raw.githubusercontent.com/Saros72/kodirepo/main/repo-19/service.iptv.web.server/ct.png"}}


def get_stream(id):
    url = "http://sledovanietv.sk/download/noAccess-cs.m3u8"
    try:
        id = id.split(".")[0]
        headers = {"Content-type": "application/x-www-form-urlencoded", "Accept-encoding": "gzip", "Connection": "Keep-Alive", "User-Agent": "Dalvik/1.6.0 (Linux; U; Android 4.4.4; Nexus 7 Build/KTU84P)"}
        req = requests.post("https://www.ceskatelevize.cz/services/ivysilani/xml/token/", data = {'user': 'iDevicesMotion'}, headers = headers).content
        token = ET.fromstring(req).text
        req = requests.post("https://www.ceskatelevize.cz/services/ivysilani/xml/playlisturl/", data = {'quality': '1080p', 'playerType': 'iPad', 'token': token, 'ID': 'CT' + id, 'playlistType': 'json'}, headers = headers).content
        keyurl = ET.fromstring(req).text
        url = requests.get(keyurl, headers = headers).json()["playlist"][0]["streamUrls"]["main"]
    except:
        url = "http://sledovanietv.sk/download/noAccess-cs.m3u8"
    return url
