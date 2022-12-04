#-*-coding:utf8;-*-


# přihlašovací údaje
username = ""
password = ""
pin = ""
product = "ANDROID-PHONE"
dev = "androidportable"


import requests, json, uuid, sys
from urllib.parse import quote


headers = {"User-Agent": "okhttp/3.12.12"}
mac_num = hex(uuid.getnode()).replace('0x', '').upper()
mac = ':'.join(mac_num[i : i + 2] for i in range(0, 11, 2))


def main():
    req = requests.get("https://sledovanitv.cz/api/create-pairing?username=" + quote(username) + "&password=" + quote(password) + "&type=" + dev + "&product=" + product+ "&serial=" + mac, headers = headers).json()
    if req["status"] == 1:
        json_object = json.dumps(req, indent=4)
        with open("stvcz_data.json", "w") as outfile:
            outfile.write(json_object)
        print("Přihlášení úspěšné")
    else:
        print(req["error"])
    input("\nPro ukončení stiskněte klávesu Enter")
    sys.exit(0)


if __name__ == "__main__":
    main()