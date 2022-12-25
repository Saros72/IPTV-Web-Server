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
from urllib.parse import quote
from providers.o2tv import o2tv
from providers.kuki import kuki
from providers.stvcz import stvcz
from providers.stvsk import stvsk
from providers.rebit import rebit
from providers.telly import telly
from providers.tmobile import tmobile
from providers.magio import magio
from providers.orange import orange
from providers.sweet import sweet
from providers.touchtv import touchtv


os.system("cls||clear")
style_home = "./templates/home.tpl"
style_links = "./templates/links.tpl"
bottle.debug(True)
catchup = ' catchup="append" catchup-source="?utc={utc}&utcend={utcend}",'
#catchup = ' timeshift="15",'
input_stream = "#KODIPROP:inputstream=inputstream.adaptive\n#KODIPROP:inputstream.adaptive.manifest_type=hls\n#KODIPROP:mimetype=application/x-mpegURL\n"


@route('/files/<filename:path>')
def send_static(filename):
    return static_file(filename, root = FILES_DIR)


@route("/touchtv/playlist")
def touchtv_playlist():
    t = ""
    for x,y in touchtv.channels.items():
        t = t + '#EXTINF:-1 provider="Touch TV" tvg-logo="' + y["logo"] + '"' + catchup + y["name"] + "\n" + input_stream + "http://" + str(HOST) + ":" + str(PORT)  + "/touchtv/" + str(x) + ".m3u8\n"
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
            names.append(('/touchtv/' + str(x) + '.m3u8', y["name"]))    
        info["names"] = names
    except:
        return ""
    return template(style_links, info)


@route("/sweet/playlist")
def sweet_playlist():
    t = ""
    for x,y in sweet.channels.items():
        t = t + '#EXTINF:-1 provider="Sweet TV" tvg-logo="' + y["logo"] + '"' + catchup + y["name"] + "\n" + input_stream + "http://" + str(HOST) + ":" + str(PORT)  + "/sweet/" + str(x) + ".m3u8\n"
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


@route("/o2tv/playlist")
def o2tv_playlist():
    try:
        with open("./providers/o2tv/o2_ids.json", 'r') as openfile:
            data = json.load(openfile)
    except:
        return ""
    t = ""
    for x,y in data.items():
        t = t + '#EXTINF:-1 provider="O2 TV" tvg-logo="' + y["logo"] + '"' + catchup + y["name"].replace(" HD", "") + "\n" + input_stream + "http://" + str(HOST) + ":" + str(PORT)  + "/o2tv/" + quote(x) + ".m3u8\n"
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
            names.append(('/o2tv/' + quote(x) + '.m3u8', y["name"].replace(" HD", "")))
        info["names"] = names
    except:
        return ""
    return template(style_links, info)


@route("/o2tv/<id>")
def o2tv_play(id):
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


@route("/")
def home():
    return template(style_home)


if __name__ == "__main__":
    run(host = HOST, port = PORT)