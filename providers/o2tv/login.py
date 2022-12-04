#-*-coding:utf8;-*-

# přihlašovací údaje
username = ""
password = ""


import requests, json, sys


def main():
    token = ""
    headers = {'X-NanguTv-App-Version': 'Android#6.4.1', 'User-Agent': 'Dalvik/2.1.0', 'Connection': 'Keep-Alive', 'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8', 'X-NanguTv-Device-Id' : 'b7pzci54mrzbcvy', 'X-NanguTv-Device-Name': 'TV-BOX'}
    post = {'grant_type': 'password', 'client_id': 'tef-web-portal-etnetera','client_secret': '2b16ac9984cd60dd0154f779ef200679', 'username': username, 'password': password, 'platform_id': '231a7d6678d00c65f6f3b2aaa699a0d0', 'language': 'cs'}
    req = requests.post('https://oauth.o2tv.cz/oauth/token', data = post, headers = headers)
    if req.status_code == 200:
        token = req.json()["access_token"]
    else:
        post = {'username' : username, 'password' : password} 
        req = requests.post('https://ottmediator.o2tv.cz/ottmediator-war/login', data = post, headers = headers)
        if req.status_code == 200:
            data = req.json()
            remote_access_token = data["remote_access_token"]
            for service in data['services']:
                service_id = service['service_id']
                service_desc = service['description']
            post = {'service_id' : service_id, 'remote_access_token' : remote_access_token}
            req = requests.post("https://ottmediator.o2tv.cz/ottmediator-war/loginChoiceService", data = post, headers = headers)
            if req.status_code == 200:
                post = {'grant_type' : 'remote_access_token', 'client_id' : 'tef-web-portal-etnetera', 'client_secret' : '2b16ac9984cd60dd0154f779ef200679', 'platform_id' : '231a7d6678d00c65f6f3b2aaa699a0d0', 'language' : 'cs', 'remote_access_token' : remote_access_token, 'authority' :  'tef-sso', 'isp_id' : '1'}
                req = requests.post('https://oauth.o2tv.cz/oauth/token', data = post, headers = headers)
                if req.status_code == 200:
                    token = req.json()["access_token"]
    if token != "":
        headers = {'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:75.0) Gecko/20100101 Firefox/75.0', 'Content-Type' : 'application/json'}
        headers.update({'x-o2tv-access-token' : token, 'x-o2tv-device-id' : 'b7pzci54mrzbcvy', 'x-o2tv-device-name' : 'TV-BOX'})
        req = requests.get('https://api.o2tv.cz/unity/api/v1/user/profile/', headers = headers).json()
        data = {"token": token, "subscription": req["code"]}
        json_object = json.dumps(data, indent=4)
        with open("o2_token.json", "w") as outfile:
            outfile.write(json_object)
        ch = req["ottChannels"]["live"]
        req = requests.get("https://api.o2tv.cz/unity/api/v1/channels/").json()["result"]
        channels = {}
        for c in req:
            key = c["channel"]["channelKey"]
            name = c["channel"]["name"]
            try:
                logo = "https://assets.o2tv.cz" + c["channel"]["images"]["color"]["url"]
            except:
                logo = ""
            if key in ch:
                channels[key] = ({"name": name, "logo": logo})
        json_object = json.dumps(channels, indent=4)
        with open("o2_ids.json", "w") as outfile:
            outfile.write(json_object)
        print("Přihlášení úspěšné")
    else:
        print("Nelze se přihlásit")
    input("\nPro ukončení stiskněte klávesu Enter")
    sys.exit(0)


if __name__ == "__main__":
    main()