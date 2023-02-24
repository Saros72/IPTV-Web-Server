#-*-coding:utf8;-*-


import requests, os, re, json, urllib3
from datetime import datetime, timedelta
import http.cookiejar as cookielib
from urllib.parse import urlparse


UA ='Mozilla/5.0 (SMART-TV; LINUX; Tizen 5.5) AppleWebKit/537.36 (KHTML, like Gecko) 69.0.3497.106.1/5.5 TV Safari/537.36'
COOKIEFILE = "./providers/lepsitv/gonet.cookie"
data_path = "./providers/lepsitv/gonet.data"
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
sess = requests.Session()
sess.cookies = cookielib.LWPCookieJar(COOKIEFILE)
cj = sess.cookies
channels = {}
try:
    cj.load(COOKIEFILE)
    with open(data_path, 'r') as openfile:
        data = json.load(openfile)
    key = data["key"]
    headers = {'Host': 'www.gonet.tv', 'User-Agent': UA, 'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8', 'Accept-Language': 'pl,en-US;q=0.7,en;q=0.3', 'Upgrade-Insecure-Requests': '1'}
    url = "https://www.xn--lep-tma39c.tv/api/program0.php?auth=" + key + "&profil=&zobrazeno=0&network=&k=1&c=h265&no_alternative=&zarizeni=&m3u8_test=0&requests[0][stations]=1&requests[1][preklady]=1"
    response = sess.get(url, headers=headers, cookies=cj,verify=False)
    html = (response.text).replace("\'",'"')
    jsdata = response.json()[0]
    for x in jsdata:
        if "nezobrazovat" not in x:
            channels[str(x["id"])] = {"name": x["stanice"], "logo": x["stanice_logo"]}
except:
    pass


def get_stream(id, utc):
    stream_url = "http://sledovanietv.sk/download/noAccess-cs.m3u8"
    try:
        id = id.split(".")[0]
        cj.load(COOKIEFILE)
        with open(data_path, 'r') as openfile:
            data = json.load(openfile)
        key = data["key"]
        if utc == "":
            now = datetime.now()
            now1 = now + timedelta(minutes = 1)
            now2 = now + timedelta(minutes = 2)
            ts = now1.strftime('%Y-%m-%d %H:%M')
            te = now2.strftime('%Y-%m-%d %H:%M')
        else:
            ts = datetime.fromtimestamp(int(utc) + 60).strftime('%Y-%m-%d %H:%M')
            te = datetime.fromtimestamp(int(utc) + 120).strftime('%Y-%m-%d %H:%M') 
        headers = {'Host': 'www.xn--lep-tma39c.tv', 'User-Agent': UA, 'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8', 'Accept-Language': 'pl,en-US;q=0.7,en;q=0.3', 'Upgrade-Insecure-Requests': '1', 'Cache-Control': 'max-age=0'}
        url = "https://www.xn--lep-tma39c.tv/api/program0.php?auth=" + key + "&profil=&zobrazeno=0&network=&k=1&c=hevc50&no_alternative=&zarizeni=&m3u8_test=1&s=" + id + "&force_stream=&offset=-1&tdif=1&ts=" + ts + "&te=" + te
        response = sess.get(url, headers=headers, cookies=cj,verify=True)
        jsdata = response.json()[id]["porady"]
        pid = list(jsdata.keys())[0]
        now = datetime.now()
        if utc == "":
            url = "https://www.xn--lep-tma39c.tv/api/program0.php?auth=" + key + "&profil=&zobrazeno=&network=&k=1&c=h265&no_alternative=&zarizeni=&m3u8_test=1&s=" + id + "&force_stream=&offset=-1&tdif=1&porad=" + pid
            offs = int(now.timestamp()) - jsdata[pid]["casod"] + 160
        else:
            url = "https://www.xn--lep-tma39c.tv/api/program0.php?auth=" + key + "&profil=&zobrazeno=&network=&k=1&c=h265&no_alternative=&zarizeni=&m3u8_test=1&s=" + id + "&force_stream=&porad=" + pid
            offs = 240
        response = sess.get(url, headers=headers, cookies=cj,verify=True)
        stream = response.json()["stream"]["auto"]
        parsed_url = urlparse(stream)
        server = parsed_url.netloc
        headers = {'Host': 'www.xn--lep-tma39c.tv', 'User-Agent': UA, 'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8', 'Accept-Language': 'pl,en-US;q=0.7,en;q=0.3', 'Upgrade-Insecure-Requests': '1', 'Cache-Control': 'max-age=0'}
        url = "https://www.xn--lep-tma39c.tv/api/overeniP.php?auth=" + key + "&profil=&token=&server=" + server
        if utc != "":
            url=url + '&stanice=' + pid
        response = sess.get(url, headers=headers, cookies=cj,verify=True)
        token=response.text
        if not 'redefine.' in server:
            url =     'https://'+server+'/tt.php'
            response = sess.get(url, headers=headers, cookies=cj,verify=True)
            tt = (response.text).replace(' ','%20').replace('"','')            
            stream = stream.split('&offset=')[0]
            stream_url = stream+'&tt=%40TT%40&u='+token+'&offset='+str(offs)+'&tt='+tt+'&a='
        else:
            stream_url = stream+'|User-Agent='+UA
    except:
        stream_url = "http://sledovanietv.sk/download/noAccess-cs.m3u8"
    return stream_url

