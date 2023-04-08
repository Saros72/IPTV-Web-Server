# -*- coding: utf-8 -*-


# nastavení serveru
HOST = "localhost"
PORT = 8888
# cesta k souborům
FILES_DIR = "./"


print("Spouští se server...")
import requests, bottle, json, os
from bottle import route, redirect, response, request, static_file, template, run
from datetime import datetime
from urllib.parse import urlparse, urlencode, parse_qsl, quote, unquote
from providers.o2tv import o2tv
from providers.o2tvsk import o2tvsk
from providers.kuki import kuki
from providers.stvcz import stvcz
from providers.stvsk import stvsk
from providers.rebit import rebit
from providers.telly import telly
from providers.net import net
from providers.tmobile import tmobile
from providers.magio import magio
from providers.orange import orange
from providers.sweet import sweet
from providers.touchtv import touchtv
from providers.antik import antik
from providers.lepsitv import lepsitv
from providers.ivysilani import ivysilani
import czech_sort


os.system("cls||clear")
style_home = "./templates/home.tpl"
style_links = "./templates/links.tpl"
bottle.debug(True)
catchup = ' catchup="append" catchup-source="?utc={utc}&utcend={utcend}",'
#catchup = ' timeshift="15",'
input_stream = "#KODIPROP:inputstream=inputstream.adaptive\n#KODIPROP:inputstream.adaptive.manifest_type=hls\n#KODIPROP:mimetype=application/x-mpegURL\n"
antik_key_cache = {"access": 1}
bottle.debug(True)


def patch_url(url, **kwargs):
    return urlparse(url)._replace(query=urlencode(dict(parse_qsl(urlparse(url).query), **kwargs))).geturl()


@route('/files/<filename:path>')
def send_static(filename):
    return static_file(filename, root = FILES_DIR)


@route("/ivysilani/playlist")
def ivysilani_playlist():
    t = ""
    for x,y in ivysilani.channels.items():
        t = t + '#EXTINF:-1 provider="iVysílání ČT" tvg-logo="' + y["logo"] + '",' + y["name"] + "\n" + input_stream + "http://" + str(HOST) + ":" + str(PORT)  + "/ivysilani/" + str(x) + ".m3u8\n"
    if t != "":
        t = "#EXTM3U\n" + t
    response.content_type = 'text/plain; charset=UTF-8'
    return t


@route("/ivysilani/<id>")
def ivysilani_play(id):
    stream = ivysilani.get_stream(id)
    response.content_type = "application/vnd.apple.mpegurl"
    return redirect(stream)


@route("/ivysilani/list")
def ivysilani_list():
    names = []
    info = {'title': 'iVysílání ČT'}
    try:
        for x,y in ivysilani.channels.items():
            names.append(('/ivysilani/' + str(x) + '.m3u8', y["name"]))    
        info["names"] = names
    except:
        return ""
    return template(style_links, info)


@route("/lepsitv/playlist")
def lepsitv_playlist():
    t = ""
    for x,y in lepsitv.channels.items():
        t = t + '#EXTINF:-1 provider="Lepší TV" tvg-logo="' + y["logo"] + '"' + catchup + y["name"] + "\n" + input_stream + "http://" + str(HOST) + ":" + str(PORT)  + "/lepsitv/" + str(x) + ".m3u8\n"
    if t != "":
        t = "#EXTM3U\n" + t
    response.content_type = 'text/plain; charset=UTF-8'
    return t


@route("/lepsitv/<id>")
def lepsitv_play(id):
    if 'utc' in request.query:
        stream = lepsitv.get_stream(id,
 str(request.query["utc"]))
    else:
        stream = lepsitv.get_stream(id, "")
    response.content_type = "application/vnd.apple.mpegurl"
    return redirect(stream)


@route("/lepsitv/list")
def lepsitv_list():
    names = []
    info = {'title': 'Lepší TV'}
    try:
        for x,y in lepsitv.channels.items():
            names.append(('/lepsitv/' + str(x) + '.m3u8', y["name"]))    
        info["names"] = names
    except:
        return ""
    return template(style_links, info)


@route("/touchtv/playlist")
def touchtv_playlist():
    t = ""
    for x,y in touchtv.channels.items():
        t = t + '#EXTINF:-1 provider="Touch TV" tvg-logo="' + y["logo"] + '"' + catchup + y["name"] + "\n" + input_stream + "http://" + str(HOST) + ":" + str(PORT)  + "/touchtv/" + str(x) + ".m3u8|User-Agent=okhttp/3.12.12\n"
    if t != "":
        t = "#EXTM3U\n" + t
    response.content_type = 'text/plain; charset=UTF-8'
    return t


@route("/touchtv/<id>")
def touchtv_play(id):
    if 'utc' in request.query:
        stream = touchtv.get_catchup(id,
 str(request.query["utc"]))
    else:
        stream = touchtv.get_stream(id)
    response.content_type = "application/vnd.apple.mpegurl"
    return redirect(stream)


@route("/touchtv/list")
def touchtv_list():
    names = []
    info = {'title': 'Touch TV'}
    try:
        for x,y in touchtv.channels.items():
            names.append(('/touchtv/' + str(x) + '.m3u8|User-Agent=okhttp/3.12.12', y["name"]))    
        info["names"] = names
    except:
        return ""
    return template(style_links, info)


@route("/sweet/playlist")
def sweet_playlist():
    t = ""
    for x,y in sweet.channels.items():
        t = t + '#EXTINF:-1 provider="Sweet TV" group-title="' + y["group"] + '"' + ' tvg-logo="' + y["logo"] + '"' + catchup + y["name"] + "\n" + input_stream + "#EXTVLCOPT:http-user-agent=okhttp/3.12.12\nhttp://" + str(HOST) + ":" + str(PORT)  + "/sweet/" + str(x) + ".m3u8\n"
    if t != "":
        t = "#EXTM3U\n" + t
    response.content_type = 'text/plain; charset=UTF-8'
    return t


@route("/sweet/<id>")
def sweet_play(id):
    if 'utc' in request.query:
        stream = sweet.get_catchup(id,
 request.query["utc"])
    else:
        stream = sweet.get_stream(id)
    response.content_type = "application/vnd.apple.mpegurl"
    return redirect(stream)


@route("/sweet/list")
def sweet_list():
    names = []
    info = {'title': 'Sweet TV'}
    try:
        for x,y in sweet.channels.items():
            names.append(('/sweet/' + str(x) + '.m3u8', y["name"]))    
        info["names"] = names
    except:
        return ""
    return template(style_links, info)


@route("/orange/playlist")
def orange_playlist():
    t = ""
    for x,y in orange.channels.items():
        t = t + '#EXTINF:-1 provider="Orange TV" group-title="' + y["group"].split(" ", 1)[1] + '" tvg-logo="' + y["logo"] + '"' + catchup + y["name"] + "\n" + input_stream + "http://" + str(HOST) + ":" + str(PORT)  + "/orange/" + str(x) + ".m3u8\n"
    if t != "":
        t = "#EXTM3U\n" + t
    response.content_type = 'text/plain; charset=UTF-8'
    return t


@route("/orange/<id>")
def orange_play(id):
    if 'utc' in request.query:
        if 'utcend' in request.query:
            end = request.query["utcend"]
        else:
            end = ""
        stream = orange.get_catchup(id,
 request.query["utc"], end)
    else:
        stream = orange.get_stream(id)
    response.content_type = "application/x-mpegURL"
    return redirect(stream)


@route("/orange/list")
def orange_list():
    names = []
    info = {'title': 'Orange TV'}
    try:
        for x,y in orange.channels.items():
            names.append(('/orange/' + str(x) + '.m3u8', y["name"]))    
        info["names"] = names
    except:
        return ""
    return template(style_links, info)


@route("/magio/playlist")
def magio_playlist():
    input_stream_ = "#KODIPROP:inputstream=inputstream.adaptive\n#KODIPROP:inputstream.adaptive.manifest_type=mpd\n#KODIPROP:mimetype=application/dash+xml\n"
    ch = magio.get_channels()
    t = ""
    for x,y in ch.items():
        t = t + '#EXTINF:-1 provider="Magio GO" group-title="' + y["group"] + '" tvg-logo="' +y["logo"] + '"' + catchup + y["name"].replace(" HD", "") + "\n" + input_stream_ + "http://" + str(HOST) + ":" + str(PORT)  + "/magio/" + str(x) + ".mpd\n"
    if t != "":
        t = "#EXTM3U\n" + t
    response.content_type = 'text/plain; charset=UTF-8'
    return t


@route("/magio/list")
def magio_list():
    names = []
    info = {'title': 'Magio GO'}
    ch = magio.get_channels()
    for x,y in ch.items():
        names.append(('/magio/' + str(x) + '.mpd', y["name"].replace(" HD", "")))    
    info["names"] = names
    return template(style_links, info)


@route("/magio/<id>")
def magio_play(id):
    if 'utc' in request.query:
        if 'utcend' in request.query:
            end = request.query["utcend"]
        else:
            now = int(datetime.now().timestamp())
            end = int(request.query["utc"]) + 10800
            if end > now:
                end = now - 60
        try:
            stream = magio.get_catchup(id,
 request.query["utc"], str(end))
        except:
            stream = magio.get_stream(id)
    else:
        stream = magio.get_stream(id)
    response.content_type = "application/dash+xml"
    return redirect(stream)


@route("/tmobile/playlist")
def tmobile_playlist():
    ch = tmobile.get_channels()
    t = ""
    for x,y in ch.items():
        t = t + '#EXTINF:-1 provider="T-Mobile TV GO" group-title="' + y["group"] + '" tvg-logo="' +y["logo"] + '"' + catchup + y["name"].replace(" HD", "") + "\n" + input_stream + "http://" + str(HOST) + ":" + str(PORT)  + "/tmobile/" + str(x) + ".m3u8\n"
    if t != "":
        t = "#EXTM3U\n" + t
    response.content_type = 'text/plain; charset=UTF-8'
    return t


@route("/tmobile/list")
def tmobile_list():
    names = []
    info = {'title': 'T-Mobile TV GO'}
    try:
        ch = tmobile.get_channels()
        for x,y in ch.items():
            names.append(('/tmobile/' + str(x) + '.m3u8', y["name"].replace(" HD", "")))    
        info["names"] = names
    except:
        return ""
    return template(style_links, info)


@route("/tmobile/<id>")
def tmobile_play(id):
    if 'utc' in request.query:
        if 'utcend' in request.query:
            end = request.query["utcend"]
        else:
            now = int(datetime.now().timestamp())
            end = int(request.query["utc"]) + 10800
            if end > now:
                end = now - 60
        stream = tmobile.get_catchup(id,
 request.query["utc"], str(end))
    else:
        stream = tmobile.get_stream(id)
    response.content_type = "application/x-mpegURL"
    return redirect(stream)


@route("/net/playlist")
def net_playlist():
    t = ""
    for x,y in net.channels.items():
        t = t + '#EXTINF:-1 provider="4NET.TV" tvg-logo="https://epg.tv.itself.cz/files/channel_logos/' + str(x) + '.png"' + catchup + y[0].replace(" HD", "") + "\n" + input_stream + "http://" + str(HOST) + ":" + str(PORT)  + "/net/" + str(x) + ".m3u8\n"
    if t != "":
        t = "#EXTM3U\n" + t
    response.content_type = 'text/plain; charset=UTF-8'
    return t


@route("/net/<id>")
def net_play(id):
    if 'utc' in request.query:
        if 'utcend' in request.query:
            end = request.query["utcend"]
        else:
            now = int(datetime.now().timestamp())
            end = int(request.query["utc"]) + 10800
            if end > now:
                end = now - 60
        try:
            stream = net.get_catchup(str(id.split(".")[0]),
 request.query["utc"], str(end))
        except:
            stream = net.channels[int(id.split(".")[0])][1]
    else:
        stream = net.channels[int(id.split(".")[0])][1]
    response.content_type = "application/x-mpegURL"
    return redirect(stream)


@route("/net/list")
def net_list():
    names = []
    info = {'title': '4NET.TV'}
    try:
        for x,y in net.channels.items():
            names.append(('/net/' + str(x) + '.m3u8', y[0].replace(" HD", "")))
        
        info["names"] = names
    except:
        return ""
    return template(style_links, info)


@route("/telly/playlist")
def telly_playlist():
    t = ""
    for x,y in telly.channels.items():
        t = t + '#EXTINF:-1 provider="Telly" tvg-logo="https://epg.tv.itself.cz/files/channel_logos/' + str(x) + '.png"' + catchup + y[0].replace(" HD", "") + "\n" + input_stream + "http://" + str(HOST) + ":" + str(PORT)  + "/telly/" + str(x) + ".m3u8\n"
    if t != "":
        t = "#EXTM3U\n" + t
    response.content_type = 'text/plain; charset=UTF-8'
    return t


@route("/telly/<id>")
def telly_play(id):
    if 'utc' in request.query:
        if 'utcend' in request.query:
            end = request.query["utcend"]
        else:
            now = int(datetime.now().timestamp())
            end = int(request.query["utc"]) + 10800
            if end > now:
                end = now - 60
        try:
            stream = telly.get_catchup(str(id.split(".")[0]),
 request.query["utc"], str(end))
        except:
            stream = telly.channels[int(id.split(".")[0])][1]
    else:
        stream = telly.channels[int(id.split(".")[0])][1]
    response.content_type = "application/x-mpegURL"
    return redirect(stream)


@route("/telly/list")
def telly_list():
    names = []
    info = {'title': 'Telly'}
    try:
        for x,y in telly.channels.items():
            names.append(('/telly/' + str(x) + '.m3u8', y[0].replace(" HD", "")))
        
        info["names"] = names
    except:
        return ""
    return template(style_links, info)


@route("/rebit/playlist")
def rebit_playlist():
    t = ""
    for x,y in rebit.channels.items():
        t = t + '#EXTINF:-1 provider="REBIT.tv" tvg-logo="' + y["logo"] + '"' + catchup + y["name"].replace(" HD", "") + "\n" + input_stream + "http://" + str(HOST) + ":" + str(PORT)  + "/rebit/" + str(x) + ".m3u8\n"
    if t != "":
        t = "#EXTM3U\n" + t
    response.content_type = 'text/plain; charset=UTF-8'
    return t


@route("/rebit/<id>")
def rebit_play(id):
    ch = rebit.channels[int(id.split(".")[0])]["id"]
    if 'utc' in request.query:
        if 'utcend' in request.query:
            end = request.query["utcend"]
        else:
            now = int(datetime.now().timestamp())
            end = int(request.query["utc"]) + 10800
            if end > now:
                end = now - 60
        try:
            stream = rebit.get_catchup(ch,
 request.query["utc"], str(end))
        except:
            stream = rebit.get_stream(id)
    else:
        stream = rebit.get_stream(ch)
    response.content_type = "application/x-mpegURL"
    return redirect(stream)


@route("/rebit/list")
def rebit_list():
    names = []
    info = {'title': 'REBIT.tv'}
    try:
        for x,y in rebit.channels.items():
            names.append(('/rebit/' + str(x) + '.m3u8', y["name"].replace(" HD", "")))    
        info["names"] = names
    except:
        return ""
    return template(style_links, info)


@route("/stvsk/playlist")
def stvsk_playlist():
    t = ""
    for x,y in stvsk.channels.items():
        if y["type"] == "tv":
            t = t + '#EXTINF:-1 provider="SledovanieTV.sk" group-title="' + y["group"] + '" tvg-logo="' +y["logo"] + '"' + catchup + y["name"] + "\n" + input_stream + "http://" + str(HOST) + ":" + str(PORT)  + "/stvsk/" + str(x) + ".m3u8\n"
        else:
            t = t + '#EXTINF:-1 provider="SledovanieTV.sk" radio="true" group-title="' + y["group"] + '" tvg-logo="' +y["logo"] + '"' + catchup + y["name"].replace(" HD", "") + "\nhttp://" + str(HOST) + ":" + str(PORT)  + "/stvsk/" + str(x) + ".m3u8\n"
    if t != "":
        t = "#EXTM3U\n" + t
    response.content_type = 'text/plain; charset=UTF-8'
    return t


@route("/stvsk/<id>")
def stvsk_play(id):
    if 'utc' in request.query:
        stream = stvsk.get_catchup(id,
 request.query["utc"], "")
    else:
        stream = stvsk.channels[id.split(".")[0]]["url"]
        if "PHPSESSID" in stream:
            sessid = stvsk.get_sessid()
            stream = patch_url(stream, PHPSESSID=sessid)
    response.content_type = "application/x-mpegURL"
    return redirect(stream)


@route("/stvsk/list")
def stvsk_list():
    names = []
    info = {'title': 'SledovanieTV.sk'}
    try:
        for x,y in stvsk.channels.items():
            names.append(('/stvsk/' + str(x) + '.m3u8', y["name"].replace(" HD", "")))
        info["names"] = names
    except:
        return ""
    return template(style_links, info)


@route("/stvcz/playlist")
def stvcz_playlist():
    t = ""
    for x,y in stvcz.channels.items():
        if y["type"] == "tv":
            t = t + '#EXTINF:-1 provider="SledovaniTV.cz" group-title="' + y["group"] + '" tvg-logo="' +y["logo"] + '"' + catchup + y["name"] + "\n" + input_stream + "http://" + str(HOST) + ":" + str(PORT)  + "/stvcz/" + str(x) + ".m3u8\n"
        else:
            t = t + '#EXTINF:-1 provider="SledovaniTV.cz" radio="true" group-title="' + y["group"] + '" tvg-logo="' +y["logo"] + '"' + catchup + y["name"].replace(" HD", "") + "\nhttp://" + str(HOST) + ":" + str(PORT)  + "/stvcz/" + str(x) + ".m3u8\n"
    if t != "":
        t = "#EXTM3U\n" + t
    response.content_type = 'text/plain; charset=UTF-8'
    return t


@route("/stvcz/<id>")
def stvcz_play(id):
    if 'utc' in request.query:
        stream = stvcz.get_catchup(id,
 request.query["utc"], "")
    else:
        stream = stvcz.channels[id.split(".")[0]]["url"]
        if "PHPSESSID" in stream:
            sessid = stvcz.get_sessid()
            stream = patch_url(stream, PHPSESSID=sessid)
    response.content_type = "application/x-mpegURL"
    return redirect(stream)


@route("/stvcz/list")
def stvcz_list():
    names = []
    info = {'title': 'SledovaniTV.cz'}
    try:
        for x,y in stvcz.channels.items():
            names.append(('/stvcz/' + str(x) + '.m3u8', y["name"].replace(" HD", "")))    
        info["names"] = names
    except:
        return ""
    return template(style_links, info)


@route("/kuki/playlist")
def kuki_playlist():
    t = ""
    for x,y in kuki.channels.items():
        if y["type"] == "tv":
            t = t + '#EXTINF:-1 provider="Kuki TV" tvg-logo="' + y["logo"] + '"' + catchup + y["name"].replace(" HD", "") + "\n" + input_stream + "http://" + str(HOST) + ":" + str(PORT)  + "/kuki/" + str(x) + ".m3u8\n"
        else:
            t = t + '#EXTINF:-1 provider="Kuki TV" radio="true" tvg-logo="' + y["logo"] + '"' + catchup + y["name"].replace(" HD", "") + "\n" + "http://" + str(HOST) + ":" + str(PORT)  + "/kuki/" + str(x) + ".m3u8\n"
    if t != "":
        t = "#EXTM3U\n" + t
    response.content_type = 'text/plain; charset=UTF-8'
    return t


@route("/kuki/<id>")
def kuki_play(id):
    if 'utc' in request.query:
        stream = kuki.get_stream(id.split(".")[0],
 str(request.query["utc"]))
    else:
        stream = kuki.get_stream(id.split(".")[0], "")
    response.content_type = "application/x-mpegURL"
    return redirect(stream)


@route("/kuki/list")
def kuki_list():
    names = []
    info = {'title': 'Kuki TV'}
    try:
        for x,y in kuki.channels.items():
            names.append(('/kuki/' + str(x) + '.m3u8', y["name"].replace(" HD", "")))    
        info["names"] = names
    except:
        return ""
    return template(style_links, info)


def replace_hd(n):
    if o2tv.O2TV_REPLACE_HD == 1 or o2tvsk.O2TV_REPLACE_HD == 1:
        n = n.replace(" HD", "")
    return n


@route("/o2tvsk/playlist")
def o2tvsk_playlist():
    try:
        with open("./providers/o2tvsk/o2sk_ids.json", 'r') as openfile:
            data = json.load(openfile)
    except:
        return ""
    t = ""
    for x,y in data.items():
        t = t + '#EXTINF:-1 provider="O2 TV SK" tvg-logo="' + y["logo"] + '"' + catchup + replace_hd(y["name"]) + "\n" + input_stream + "http://" + str(HOST) + ":" + str(PORT)  + "/o2tvsk/" + quote(x.replace("/", "|")) + ".m3u8\n"
    if t != "":
        t = "#EXTM3U\n" + t
    response.content_type = 'text/plain; charset=UTF-8'
    return t


@route("/o2tvsk/list")
def o2tvsk_list():
    try:
        with open("./providers/o2tvsk/o2sk_ids.json", 'r') as openfile:
            data = json.load(openfile)
    except:
        return ""
    names = []
    info = {'title': 'O2 TV SK'}
    try:
        for x,y in data.items():
            names.append(('/o2tvsk/' + quote(x.replace("/", "|")) + '.m3u8', replace_hd(y["name"])))
        info["names"] = names
    except:
        return ""
    return template(style_links, info)


@route("/o2tvsk/<id>")
def o2tvsk_play(id):
    id = unquote(id).replace("|", "/")
    if 'utc' in request.query:
        if 'utcend' in request.query:
            end = request.query["utcend"]
        else:
            end = ""
        stream = o2tvsk.get_catchup(id,
 request.query["utc"], end)
    else:
        stream = o2tvsk.get_stream(id)
    response.content_type = "application/x-mpegURL"
    return redirect(stream)


@route("/o2tv/playlist")
def o2tv_playlist():
    try:
        with open("./providers/o2tv/o2_ids.json", 'r') as openfile:
            data = json.load(openfile)
    except:
        return ""
    t = ""
    for x,y in data.items():
        t = t + '#EXTINF:-1 provider="O2 TV" tvg-logo="' + y["logo"] + '"' + catchup + replace_hd(y["name"]) + "\n" + input_stream + "http://" + str(HOST) + ":" + str(PORT)  + "/o2tv/" + quote(x.replace("/", "|")) + ".m3u8\n"
    if t != "":
        t = "#EXTM3U\n" + t
    response.content_type = 'text/plain; charset=UTF-8'
    return t


@route("/o2tv/list")
def o2tv_list():
    try:
        with open("./providers/o2tv/o2_ids.json", 'r') as openfile:
            data = json.load(openfile)
    except:
        return ""
    names = []
    info = {'title': 'O2 TV'}
    try:
        for x,y in data.items():
            names.append(('/o2tv/' + quote(x.replace("/", "|")) + '.m3u8', replace_hd(y["name"])))
        info["names"] = names
    except:
        return ""
    return template(style_links, info)


@route("/o2tv/<id>")
def o2tv_play(id):
    id = unquote(id).replace("|", "/")
    if 'utc' in request.query:
        if 'utcend' in request.query:
            end = request.query["utcend"]
        else:
            end = ""
        stream = o2tv.get_catchup(id,
 request.query["utc"], end)
    else:
        stream = o2tv.get_stream(id)
    response.content_type = "application/x-mpegURL"
    return redirect(stream)


@route("/antik/playlist2")
def antik_playlist2():
    url = antik.playlist_url2
    if url == "":
        return ""
    r = requests.get(url).json()[0]["channels"]
    channels = []
    for ch in r:
        t = ch["channel_title"]
        for s in ch["stream"]:
            u = s["url"].split("/")[-2]
            if "tzshift" not in u:
                channels.append(t + "|" + u)
    r = czech_sort.sorted(channels)
    t = ""
    for i in r:
        c = i.split("|")
        t = t + '#EXTINF:-1 provider="Antik TV",' + c[0] + "\n" + input_stream + "http://" + str(HOST) + ":" + str(PORT)  + "/antik/" + str(c[1]) + ".m3u8\n"
    t = "#EXTM3U\n" + t
    response.content_type = 'text/plain; charset=UTF-8'
    return t


@route("/antik/playlist")
def antik_playlist():
    url = antik.playlist_url
    if url == "":
        return ""
    r = requests.get(url).text
    ch = []
    r = r.split("/playlist.m3u8")
    for c in r:
        ch.append(c.split("|hls")[0].split("|")[-2].encode("ISO-8859-1").decode("utf-8") + "@" + c.split("/playlist.m3u8")[-1].split("/")[-1])
    r = czech_sort.sorted(ch)
    t = ""
    for i in r:
        c = i.split("@")
        t = t + '#EXTINF:-1 provider="Antik TV",' + c[0] + "\n" + input_stream + "http://" + str(HOST) + ":" + str(PORT)  + "/antik/" + str(c[1]) + ".m3u8\n"
    t = "#EXTM3U\n" + t
    response.content_type = 'text/plain; charset=UTF-8'
    return t


@route("/antik/list")
def antik_list():
    url = antik.playlist_url
    if url == "":
        return ""
    r = requests.get(url).text
    ch = []
    r = r.split("/playlist.m3u8")
    for c in r:
        ch.append(c.split("|hls")[0].split("|")[-2].encode("ISO-8859-1").decode("utf-8") + "@" + c.split("/playlist.m3u8")[-1].split("/")[-1])
    ch2 = []
    r = czech_sort.sorted(ch)
    for c in r:
        ch2.append("<a href=/antik/" + c.split("@")[1] + ".m3u8>" + c.split("@")[0]  + "</a><br>")
    return ",".join(ch2[:-1]).replace(">,", ">")


@route("/antik/list2")
def antik_list2():
    url = antik.playlist_url2
    if url == "":
        return ""
    r = requests.get(url).json()[0]["channels"]
    t = ""
    for ch in r:
        t = t + "<b>" + ch["channel_title"] + "</b>:"
        for s in ch["stream"]:
            u = s["url"].split("/")[-2]
            if "tzshift" not in u:
                t = t + "<br><a href=/antik/" + u + ".m3u8>" + u  + "</a>"
        t = t + "<br><br>|"
    t = ",".join(czech_sort.sorted(t.split("|"))[1:])
    return t


@route('/antik_key/<key_id>')
def antik_key(key_id):
    global antik_key_cache
    try:
        return antik_key_cache[key_id]
    except:
        pass
    try:
        url = antik.request_template()["url"] + antik.request_template()["id"]
        data = antik.request_data(key_id)
        data = json.dumps(data, indent=2).encode('utf-8')
        data_encrypt = antik.data_encrypt(data)
        response = requests.post( url, data = data_encrypt, headers = {"Content-Type": "application/x-www-form-urlencoded", "User-Agent": "Dalvik/2.1.0 (Linux; U; Android 10; Build/1.110111.020)", "Accept-Encoding": "gzip"}).content
        bin = antik.get_bin(response)
        antik_key_cache[key_id] = bin
        antik_key_cache["access"] = 1
        return bin
    except:
        antik_key_cache["access"] = 0
        return ''


@route('/antik/<u>')
def antik_play(u):
    if antik_key_cache["access"] == 0:
        response.content_type = "application/x-mpegURL"
        return '''#EXTM3U
#EXT-X-VERSION:3
#EXT-X-TARGETDURATION:10
#EXT-X-MEDIA-SEQUENCE:0
#EXTINF:10.000000,
http://sledovanietv.sk/download/noAccess-sk0.ts
#EXTINF:10.000000,
http://sledovanietv.sk/download/noAccess-sk1.ts
#EXT-X-ENDLIST'''
    url = "http://195.181.174.88/live/" + u.replace(".m3u8", "/playlist.m3u8")
    req = requests.get(url).text.replace("encrypted-file://", "http://" + HOST + ":" + str(PORT) + "/antik_key/")
    ret=""
    for line in req.splitlines():
        if line[-3:] == ".ts":
            ret += url.replace("playlist.m3u8", "")
        ret += (line + "\n")
    response.content_type = "application/x-mpegURL"
    return ret


@route("/")
def home():
    return template(style_home)


if __name__ == "__main__":
    run(host = HOST, port = PORT, reloader = False)