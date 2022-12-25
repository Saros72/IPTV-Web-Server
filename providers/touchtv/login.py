#-*-coding:utf8;-*-


# touchTV id
id = ""


import requests, json, os, sys, uuid
UUID = str(uuid.uuid4())


def main():
    data = {}
    channels = {}
    headers = {"X-DeviceId": UUID, "X-MobileToken": id, "Connection": "keep-alive", "Accept-Encoding": "", "User-Agent": "touchTV/4.2.2 (Linux; Android TV 11; cs; Amlogic VONTAR X2) ExoPlayerLib/2.17.1", "Host": "am.di-vision.sk"}
    req = requests.get("https://am.di-vision.sk/rest/assetgroups", headers = headers)
    if req.status_code == 200 or req.status_code == 201:
        data["touch_id"] = str(id)
        data["UUID"] = str(UUID)
        json_object = json.dumps(data, indent=4)
        with open("touchtv_token.json", "w") as outfile:
            outfile.write(json_object)
        for ch in req.json():
            channels[str(ch["selector"])] = {"name": ch["title"].replace(" HD", ""), "logo": ch["logoUrl"], "gid": ch["id"], "epgId": ch["epgId"], "vod": ch["vodUrlPrefix"]}
        json_object = json.dumps(channels, indent=4)
        with open("touchtv_channels.json", "w") as outfile:
            outfile.write(json_object)
        print("Přihlášení úspěšné")
    else:
        print("Přihlášení se nezdařilo")
    input("\nPro ukončení stiskněte klávesu Enter")
    sys.exit(0)


if __name__ == "__main__":
    main()