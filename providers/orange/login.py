#-*-coding:utf8;-*-


import requests, json, sys


# přihlašovací údaje
username = ""
password = ""


def main():
    device_id = "b7pzci54mrzbcvy"
    channels = {}
    headers = {"X-NanguTv-App-Version": "Android#7.6.3", "X-NanguTv-Device-Name": "Nexus 7", "User-Agent": "Dalvik/2.1.0 (Linux; U; Android 5.1.1; Nexus 6 Build/LMY47A)", "Accept-Encoding": "gzip", "Connection": "Keep-Alive", "Content-Type": "application/x-www-form-urlencoded;charset=UTF-8"}
    params = {'grant_type': 'password', 'client_id': 'orangesk-mobile', 'client_secret': 'e4ec1e957306e306c1fd2c706a69606b', 'isp_id': '5', 'username': username, 'password': password, 'platform_id': 'b0af5c7d6e17f24259a20cf60e069c22', 'custom': 'orangesk-mobile', 'response_type': 'token'}
    req = requests.post('https://oauth01.gtm.orange.sk/oauth/token', data = params, headers = headers).json()
    if "access_token" in req:
        token = req["access_token"]
        cookies = {"access_token": token, "deviceId": device_id}
        req = requests.get("https://app01.gtm.orange.sk/sws//subscription/settings/subscription-configuration.json", headers = headers, cookies = cookies).json()
        subscription = req["subscription"]
        offer = req["billingParams"]["offers"]
        tariff = req["billingParams"]["tariff"]
        locality = req["locality"]
        data = {"token": token, "subscription": subscription}
        json_object = json.dumps(data, indent=4)
        with open("orange_token.json", "w") as outfile:
            outfile.write(json_object)
        params = {"locality": locality, "tariff": tariff , "isp": "5", "imageSize": "LARGE", "language": "slo", "deviceType": "MOBILE", "liveTvStreamingProtocol": "HLS", "offer": offer}
        j = requests.get('http://app01.gtm.orange.sk/sws/server/tv/channels.json', params=params, headers=headers, cookies=cookies).json()
        purchased_channels = j['purchasedChannels']
        items = j['channels']
        channelCategories = j['channelCategories']
        for channel_id, item in items.items():
            if channel_id in purchased_channels:
                live = item['liveTvPlayable']
                if live:
                    channel_key = str(item['channelKey'])
                    logo = str(item['logo'])
                    if not logo.startswith('https://'):
                        logo = 'https://app01.gtm.orange.sk/' + logo
                    name = str(item['channelName']).replace(" HD", "")
                    try:
                        categories = str(item['categories'][0])
                        group = channelCategories[categories]
                    except:
                        group = ""
                    channels[channel_key] = {"name": name, "logo": logo.replace("64x64", "256x256"), "group": group}
        json_object = json.dumps(channels, indent=4)
        with open("orange_channels.json", "w") as outfile:
            outfile.write(json_object)
        print("Přihlášení úspěšné")
    else:
        print(req["error"])
    input("\nPro ukončení stiskněte klávesu Enter")
    sys.exit(0)


if __name__ == "__main__":
    main()

