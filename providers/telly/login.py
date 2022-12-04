#-*-coding:utf8;-*-

import requests, json, os, uuid, re, sys


# párovací kód 
code = ""


def main():
    mac = ':'.join(re.findall('..', '%012x' % uuid.getnode()))
    data = {"pairing_code": str(code), "brand_code": "telly"}
    req = requests.post("https://backoffice0-vip.tv.itself.cz/api/device/pairDeviceByPairingCode/", json = data, headers = {"Content-Type": "application/json"}).json()
    if req["success"] == True:
        token = req["token"]
        data = {"device_token": token, "device_type_code": "ANDROIDTV", "model": "XiaomiTVBox", "name": "STB", "serial_number": "unknown", "mac_address": mac}
        req = requests.post("https://backoffice0-vip.tv.itself.cz/api/device/completeDevicePairing/", json = data, headers = {"Content-Type": "application/json"}).json()
        if req["success"] == True:
            data = {"token": token}
            json_object = json.dumps(data, indent=4)
            with open("telly_token.json", "w") as outfile:
                outfile.write(json_object)
            print("Spárováno")
        else:
            print(req["message"])
    else:
        print(req["message"])
    input("\nPro ukončení stiskněte klávesu Enter")
    sys.exit(0)


if __name__ == "__main__":
    main()
