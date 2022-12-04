#-*-coding:utf8;-*-


# přihlašovací údaje
username = ""
password = ""


import requests, uuid, json, os, sys


if not os.path.exists("kuki_sn"):
    sn = str(uuid.uuid4()).replace("-", "")
    f = open("kuki_sn", "w")
    f.write(sn)
    f.close()
else:
    sn = open("kuki_sn", "r").read()


def main():
    try:
        data = {"sn": "kuki2.0_" + sn, "device_type": "mobile", "device_model": "ANDROID-PHONE","product_name": "ANDROID-PHONE","mac": "00:00:00:00:00:00", "version_fw": "10", "version_portal": "2.1.3(2.1.3-d36574b1)", "boot_mode": "unknown", "claimed_device_id": "unknown $ a836d55cd792bf06", "hw_platform": "MOBILE.ANDROID"}
        req = requests.post("https://as.kuki.cz/api-v2/register", data = data).json()
        req_token = req["reg_token"]
        session_key = req["session_key"]
        headers = {'Content-Type': 'application/json; charset=utf-8', 'Host': 'customercare.eywa.kuki.cz', 'user-agent': 'Mozilla/5.0', 'referer': 'https://konto.kuki.cz/prihlaseni', 'origin': 'https://konto.kuki.cz', 'x-requested-with': 'cz.kuki.v2', 'accept': 'application/json'}
        data = {"email": username, "password": password}
        req = requests.post("https://customercare.eywa.kuki.cz/v1/users/actions/login/", json = data, headers = headers).json()
        token = req["token"]
        user_id = req["user_id"]
        headers = {'authorization': 'Token ' + token, 'Content-Type': 'application/json; charset=utf-8', 'Host': 'customercare.eywa.kuki.cz', 'user-agent': 'Mozilla/5.0', 'referer': 'https://konto.kuki.cz/parovani-zarizeni', 'origin': 'https://konto.kuki.cz', 'x-requested-with': 'cz.kuki.v2', 'accept': 'application/json'}
        data = {"code": req_token}
        req = requests.post('https://customercare.eywa.kuki.cz/v1/hardware/action/pair/', json = data, headers = headers).json()
        if req["status"] == "OK":
            print("Přihlášení úspěšné")
        else:
            print(req["status"])
    except:
        print("Nelze se přihlásit")
    input("\nPro ukončení stiskněte klávesu Enter")
    sys.exit(0)


if __name__ == "__main__":
    main()