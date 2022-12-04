#-*-coding:utf8;-*-


# přihlašovací údaje
username = ""
password = ""


import requests, json, os, sys


def main():
    headers = {"Content-Type": "application/json", "Host": "bbxnet.api.iptv.rebit.sk", "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:70.0) Gecko/20100101 Firefox/70.0"}
    data = {"username": username, "password": password}
    req = requests.post("https://bbxnet.api.iptv.rebit.sk/auth/auth", json = data, headers = headers)
    if req.status_code == 200 or req.status_code == 201:
        token = req.json()["data"]["access_token"]
        headers = {"Content-Type": "application/json", "Authorization": "Bearer " + token, "Host": "bbxnet.api.iptv.rebit.sk", "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:70.0) Gecko/20100101 Firefox/70.0"}
        data = {"title": "PC-LINUX", "type": "computer", "child_lock_code": "0000"}
        req = requests.post("https://bbxnet.api.iptv.rebit.sk/television/client", json = data, headers = headers)
        if req.status_code == 200 or req.status_code == 201:
            id = req.json()["data"]["id"]
            data = {"token": token, "id": id}
            json_object = json.dumps(data, indent=4)
            with open("rebit_token.json", "w") as outfile:
                outfile.write(json_object)
            print("Přihlášení úspěšné")
        else:
            print(req.json()["message"])
    else:
        print(req.json()["message"])
    input("\nPro ukončení stiskněte klávesu Enter")
    sys.exit(0)


if __name__ == "__main__":
    main()