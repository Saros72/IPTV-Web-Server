# -*- coding: utf-8 -*-


# Antik přihlašovací údaje
username = ""
password = ""
# Přístupové heslo
antik_access = ""


import zlib
import binascii
import json
from Crypto.Cipher import AES
import Crypto.Random
import sys
import requests
import re
import os
import hashlib
from uuid import getnode as get_mac


headers = {"Content-Type": "application/x-www-form-urlencoded", "User-Agent": "Dalvik/2.1.0 (Linux; U; Android 10; Build/1.110111.020)", "Accept-Encoding": "gzip"}
BS = AES.block_size
pad = lambda x: x + (BS - len(x) % BS) * chr(BS - len(x) % BS).encode("ascii")
if sys.version_info[0] == 2:
    unpad = lambda s : s[0:-ord(s[-1])]
else:
    unpad = lambda s : s[0:-s[-1]]


class AESCipher:

	def __init__( self, key ):
		self.key = binascii.a2b_hex(key)

	def encrypt( self, raw ):
		raw = pad(raw)
		iv = Crypto.Random.new().read(AES.block_size);
		cipher = AES.new( self.key, AES.MODE_CBC, iv )
		return iv + cipher.encrypt( raw )

	def decrypt( self, enc, iv=None ):
		if iv == None:
			iv = enc[:16]
			enc= enc[16:]
		cipher = AES.new(self.key, AES.MODE_CBC, iv )
		return unpad(cipher.decrypt( enc))


def create_device_id():
    mac_str = ':'.join(("%012X" % get_mac())[i:i+2] for i in range(0, 12, 2))
    return hashlib.sha1( mac_str.encode("utf-8") ).hexdigest()[24:]


def create_auth_id(name):
		return hashlib.sha256( ("VFZN!" + antik_access + "iu#2&c0WBgU" + name + "ofOqtA4W%HO1snf+TLtw").encode("utf-8") ).hexdigest()


def create_aes_key(password):
		return hashlib.sha256(create_auth_id(password).encode("utf-8") ).hexdigest()


def request_template():
    url = "http://maxim.iptv.antik.sk:180/api.php?id="
    auth_id = create_auth_id(username)
    auth_key = create_aes_key(password)
    return { "url" : url, "id" : auth_id, "key" : auth_key }


def device_register(dev_id):
    data = {'function': 'Register', 'username': dev_id, 'device': {'vendor': 'Raspberry', 'model': 'Android_AntikTV_VOD', 'os_version': '10', 'app_version': '1.1.18', 'app_name': 'Antik TV', 'id': dev_id, 'ip': '192.168.1.2', 'lang': 'sk', 'type': 'stb', 'os': 'Android', 'service': 'OTT'}}
    url = "http://maxim.iptv.antik.sk:180/api.php?id=edd672c76ceb66f3dee985d1acc558f031e1342b2ad5d2d8ab0b55f45865b61b"
    data = json.dumps(data).encode("utf-8")
    data_encrypt= AESCipher("1a8a23be8bfcd5b8e7257a333d1f709b3abd0f1b4a306c38dc2f1689476753f9").encrypt( zlib.compress(bytes(data)))
    response = requests.post( url, data = data_encrypt, headers = headers).content
    return json.loads(zlib.decompress( AESCipher("1a8a23be8bfcd5b8e7257a333d1f709b3abd0f1b4a306c38dc2f1689476753f9").decrypt( response ) ))


if not os.path.exists("./providers/antik/dev_id.txt"):
    device_id = create_device_id()
    device_register(device_id)
    f = open("./providers/antik/dev_id.txt", "w")
    f.write(device_id)
    f.close()
else:
    device_id = open("./providers/antik/dev_id.txt", "r").read()


def data_decrypt(data):
    try:
        return AESCipher(create_aes_key(antik_access)).decrypt(bytes.fromhex(data)).decode("utf-8")
    except:
        return ""


def data_encrypt(data):
    return AESCipher(request_template()["key"]).encrypt( zlib.compress(bytes(data)))


def get_bin(res):
    return binascii.a2b_hex(json.loads(zlib.decompress( AESCipher(request_template()["key"]).decrypt( res) ))["key"])


def request_data(key_id):
    data = {"function": "GetContentKey", "id": "encrypted-file://" + key_id, "device": {"vendor": "Raspberry", "model": "Android_AntikTV_VOD", "os_version": "10", "app_version": "1.1.18", "app_name": "Antik TV", "id": device_id, "ip": "192.168.1.2", "lang": "sk", "type": "stb", "os": "Android", "service": "OTT"}}
    return data


playlist_url = data_decrypt("d74abea44713865768b3050396a70ce732fc4923b3e539d4ea7022e45dc6c6a45bac1b6d96e6a3c9c64c545dd855dec073e82612f0c0637e634e2dd577d0076ab82f8b1beb98d3d6ca64f993b016eab2")
playlist_url2 = data_decrypt("f2cfd697449d5302be2dfd35261fc4f51305abbe79272a80ae5b659587ba6be45267eac22cf37001d322cfe6ef04d69a5cd03ae375e989b66c79976dc397fe71f6459684d63683ae892e43de6905feb697887fc472bcb30940779858385197d8")