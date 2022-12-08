#-*-coding:utf8;-*-


# přihlašovací údaje
email = ""
password = ""


import requests, uuid, json, sys


UUID = "07d2453f-0031-4573-95d5-16b3237eb497"
UA ='Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:105.0) Gecko/20100101 Firefox/105.0'


def main():
    channels = {}
    headers = {'Host': 'api.sweet.tv', 'user-agent': UA, 'accept': 'application/json, text/plain, */*', 'accept-language': 'pl', 'x-device': '1;22;0;2;3.2.57', 'origin': 'https://sweet.tv', 'dnt': '1', 'referer': 'https://sweet.tv/'}
    data = {'device': {'type': 'DT_Web_Browser', 'application': {'type': 'AT_SWEET_TV_Player'}, 'model': UA, 'firmware': {'versionCode': 1, 'versionString': '3.2.57'}, 'uuid': UUID, 'supported_drm': {'widevine_modular': True}, 'screen_info': {'aspectRatio': 6, 'width': 1366, 'height': 768}}, 'email': email, 'password': password}
    req = requests.post("https://api.sweet.tv/SigninService/Email.json", json = data, headers = headers).json()
    if req["result"] == "OK":
        json_object = json.dumps(req, indent=4)
        with open("sweet_token.json", "w") as outfile:
            outfile.write(json_object)
        headers["authorization"] = "Bearer " + req["access_token"]
        data = {'need_epg': False, 'need_list': True, 'need_categories': False, 'need_offsets': False, 'need_hash': False, 'need_icons': False, 'need_big_icons': False,}
        req = requests.post("https://api.sweet.tv/TvService/GetChannels.json", json = data, headers = headers).json()
        if req["status"] == "OK":
            for ch in req["list"]:
                channels[str(ch["id"])] = {"name": ch["name"].replace(" HD", ""), "logo": ch["icon_url"]}
            json_object = json.dumps(channels, indent=4)
            with open("sweet_channels.json", "w") as outfile:
                outfile.write(json_object)
            print("Přihlášení úspěšné")
        else:
            print(req["result"])
    else:
        print(req["result"])
    input("\nPro ukončení stiskněte klávesu Enter")
    sys.exit(0)


if __name__ == "__main__":
    main()