from os import path, environ
from json import load
from sqlite3 import connect
from base64 import b64decode
from enum import Enum
from win32crypt import CryptUnprotectData
from cryptography.hazmat.primitives.ciphers.aead import AESGCM

# 两个主流浏览器的数据库路径
chrome_LocalState = path.join(
    environ['LOCALAPPDATA'], 'Google', 'Chrome', 'User Data', 'Local State')
chrome_LoginData = path.join(
    environ['LOCALAPPDATA'], 'Google', 'Chrome', 'User Data', 'Default', 'Login Data')
edge_LocalState = path.join(
    environ['LOCALAPPDATA'], 'Microsoft', 'Edge', 'User Data', 'Local State')
edge_LoginData = path.join(
    environ['LOCALAPPDATA'], 'Microsoft', 'Edge', 'User Data', 'Default', 'Login Data')


class BrowserUnsupportedErr(TypeError):
    def __init__(self, browser):
        self.browser = browser

    def __str__(self):
        return repr(self.browser)


class DBNotFoundErr(FileNotFoundError):
    def __init__(self, db):
        self.db = db

    def __str__(self):
        return repr(self.db)


class Browser(Enum):
    Edge = 1
    Chrome = 2


class Accounts:
    """用于获取账号的类"""

    def __init__(self, browser: Browser) -> None:
        self._browser = browser
        self._localState = ""  # LocalState文件路径
        self._loginData = ""  # LoginData文件路径
        self._res = []  # 存放账号密码
        self._decryptKey = b''  # 解密用的密钥
        self._conn,self._cursor  = None,None  # 数据库
        self._configInnerParas()  # 配置基础数据
        self._readDBContent()  # 获取数据库的账号密码
        self._getDecryptKey()  # 获取解密密钥
        self._decryptPassword()  # 解密密码

    def _configInnerParas(self) -> None:
        """配置内部参数"""
        # 确定浏览器的两个路径
        try:
            if self._browser == Browser.Edge:
                self._localState = edge_LocalState
                self._loginData = edge_LoginData
            elif self._browser == Browser.Chrome:
                self._localState = chrome_LocalState
                self._loginData = chrome_LoginData
            else:
                raise BrowserUnsupportedErr(self._browser)
        except BrowserUnsupportedErr:
            print("您指定的浏览器 %s 尚未支持" % self._browser)
        # 检查数据库是否存在
        try:
            if not path.exists(self._loginData):
                raise DBNotFoundErr(self._loginData)
            if not path.exists(self._localState):
                raise DBNotFoundErr(self._localState)
        except DBNotFoundErr:
            print("未找到相关文件: %s" % DBNotFoundErr)
        # 连接数据库
        self._conn = connect(self._loginData)
        self._cursor = self._conn.cursor()


    def _readDBContent(self) -> None:
        """获取数据库的账号密码（密码已被加密）"""
        self._res = self._cursor.execute(
            'SELECT origin_url, username_value, password_value FROM logins').fetchall()
        self._conn.close()

    def _getDecryptKey(self) -> None:
        """获取解密密钥"""
        with open(self._localState, 'r', encoding='utf-8') as f:  # 读取密钥
            base64_encrypted_key = load(f)['os_crypt']['encrypted_key']
        encrypted_key_with_header = b64decode(base64_encrypted_key)  # 解析密钥
        encrypted_key = encrypted_key_with_header[5:]
        self._decryptKey = CryptUnprotectData(
            encrypted_key, None, None, None, 0)[1]

    def _decryptPassword(self) -> None:
        """解密密码，将其更新到self.res中"""
        data = []
        for i in self._res:
            password = i[2]
            # 解密密码
            nonce, cipherBytes = password[3:15], password[15:]
            aes_gcm = AESGCM(self._decryptKey)
            plainBytes = aes_gcm.decrypt(nonce, cipherBytes, None)
            plainPassword = plainBytes.decode('utf-8')
            data.append(
                {"Website": i[0], "Account": i[1], "Password": plainPassword})
        self._res = data

    def display(self) -> None:
        """直接用Cmd展示数据库中的账号密码"""
        print("-------------%s-------------" % self._browser)
        for j in self._res:
            print("Website :", j["Website"])
            print("Account:", j["Account"])
            print("Password:", j["Password"])
            print("------------------------------")

    def getAccounts(self) -> list[dict[str, str]]:
        """返回账号密码列表，每个元素的格式均为{"Website", "Account", "Password"}"""
        return self._res


if __name__ == '__main__':
    a = Accounts(Browser.Chrome)
    a.display()
