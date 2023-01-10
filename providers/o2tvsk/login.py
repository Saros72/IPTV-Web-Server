#-*-coding:utf8;-*-

# přihlašovací údaje
username = ""
password = ""
# nahradit "HD" v názvu kanálu
# ano = 1, ne = 0
O2TV_REPLACE_HD = 0


import requests, json, sys


def main():
    headers = { "X-Nangu-App-Version" : "Android#3.5.31.0-release", "X-Nangu-Device-Name" : "Lenovo B6000-H", "X-NanguTv-Device-size": "large", "X-NanguTv-Device-density": "213", "User-Agent" : "Dalvik/1.6.0 (Linux; U; Android 4.4.2; Lenovo B6000-H Build/KOT49H)", "Accept-Encoding": "gzip", "Connection" : "Keep-Alive" }
    data = {'grant_type' : 'password', 'client_id' : 'tef-production-mobile', 'client_secret' : '627a4f43b2eea512702127e09c3921fc', 'username' : username, 'password' : password, 'platform_id' : '231a7d6678d00c65f6f3b2aaa699a0d0', 'language' : 'sk'}
    req = requests.post('https://oauth.o2tv.cz/oauth/token', data=data, headers=headers)
    if req.status_code == 200:
        token = req.json()["access_token"]
        cookies = { "access_token": token, "deviceId": "b7pzci54mrzbcvy"}
        req = requests.get('http://app.o2tv.cz/sws/subscription/settings/subscription-configuration.json', headers=headers, cookies=cookies)
        if req.status_code == 200:
            if "subscription" in req.json():
                j = req.json()
                subscription = j["subscription"]
                offer = j["billingParams"]["offers"]
                tariff = j["billingParams"]["tariff"]
                locality = j["locality"]
                data = {"token": token, "subscription": subscription}
                json_object = json.dumps(data, indent=4)
                with open("o2sk_token.json", "w") as outfile:
                    outfile.write(json_object)
                params = { "locality": locality, "tariff": tariff, "isp": "3", "language": "slo", "deviceType": "MOBILE", "liveTvStreamingProtocol":"HLS", "offer": offer}
                req = requests.get('http://app.o2tv.cz/sws/server/tv/channels.json', params=params, headers=headers, cookies=cookies)
                if req.status_code == 200:
                    j = req.json()
                    channels = {}
                    purchased_channels = j['purchasedChannels']
                    items = j['channels']
                    for channel_id, item in items.items():
                        if channel_id in purchased_channels:
                            live = item['liveTvPlayable']
                            if live:
                                key = item['channelKey']
                                try:
                                    logo = item['logo'].replace("38x38", "256x256")
                                except:
                                    logo = ""
                                name = item['channelName']
                                channels[key] = ({"name": name, "logo": logo})
                    json_object = json.dumps(channels, indent=4)
                    with open("o2sk_ids.json", "w") as outfile:
                        outfile.write(json_object)
                    print("Přihlášení úspěšné")
        else:
            print(req.json()["errorMessage"])
    else:
        print("Nelze se přihlásit")
    input("\nPro ukončení stiskněte klávesu Enter")
    sys.exit(0)


if __name__ == "__main__":
    main()