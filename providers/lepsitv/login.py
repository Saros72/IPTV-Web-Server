#-*-coding:utf8;-*-


# přihlašovací údaje
username = ""
password = ""


import requests, os, re, json, sys, urllib3
import http.cookiejar as cookielib


UA ='Mozilla/5.0 (SMART-TV; LINUX; Tizen 5.5) AppleWebKit/537.36 (KHTML, like Gecko) 69.0.3497.106.1/5.5 TV Safari/537.36'
COOKIEFILE = "gonet.cookie"
data_path = "gonet.data"
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
sess = requests.Session()
sess.cookies = cookielib.LWPCookieJar(COOKIEFILE)
cj = sess.cookies


def main():
    headers = {'Host': 'www.gonet.tv', 'User-Agent': UA, 'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8', 'Accept-Language': 'pl,en-US;q=0.7,en;q=0.3', 'Upgrade-Insecure-Requests': '1'}
    response = sess.get('https://www.gonet.tv/pl/', headers=headers, verify=False)    
    headers = {'Host': 'www.gonet.tv', 'User-Agent': UA, 'Accept': 'application/json, text/javascript, */*; q=0.01', 'Accept-Language': 'pl,en-US;q=0.7,en;q=0.3', 'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8', 'X-Requested-With': 'XMLHttpRequest', 'Origin': 'https://www.gonet.tv', 'Referer': 'https://www.gonet.tv/pl/'}    
    data={'page':'login','action':'login','user_name':username,'user_password':password}
    response = sess.post('https://www.gonet.tv/web/ajax.php', headers=headers, cookies=cj, data=data,verify=False).json()
    if response["status"] == "ok":
        headers = {'Host': 'www.gonet.tv', 'User-Agent': UA, 'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8', 'Accept-Language': 'pl,en-US;q=0.7,en;q=0.3', 'Upgrade-Insecure-Requests': '1', 'Cache-Control': 'max-age=0'}        
        response = sess.get('https://www.gonet.tv/pl/', headers=headers, cookies=cj,verify=False)
        html = (response.text).replace("\'",'"')
        sitemain = re.findall('CONST_WWW_ONLINETV\s*=\s"([^"]+)',html)[0]
        headers = {'Host': 'www.gonet.tv', 'User-Agent': UA, 'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8', 'Accept-Language': 'pl,en-US;q=0.7,en;q=0.3', 'Referer': 'https://www.gonet.tv/pl/', 'Upgrade-Insecure-Requests': '1'}
        response = sess.get(sitemain, headers=headers, cookies=cj,verify=False)
        html = (response.text).replace("\'",'"')        
        key,valu = re.findall('setcookie\("(.+?)",\s*"(.+?)"\)',html,re.DOTALL+re.IGNORECASE)[0]
        cj.save(COOKIEFILE, ignore_discard = True)
        data = {"key": valu}
        json_object = json.dumps(data, indent=4)
        with open(data_path, "w") as outfile:
            outfile.write(json_object)
        cj.save(COOKIEFILE, ignore_discard = True)
        print("Přihlášení úspěšné")
    else:
        print(response["error"]["message"])
    input("\nPro ukončení stiskněte klávesu Enter")
    sys.exit(0)


if __name__ == "__main__":
    main()

