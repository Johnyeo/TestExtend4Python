# coding:utf-8
import os
from time import sleep

import simplejson

from settings.configs import cookieSavedFile, cookieTxtName


class Login(object):
    def __init__(self, driver, url, name, password = '111111'):
        self.driver = driver
        self.driver.get(url)

        # 判断url里有没有admin，如果没有就是前台登录，如果有就是 !=-1 后台登录
        if url.find('admin') != -1:
            self.driver.find_element_by_id('ht-login-usernameVal').send_keys(name)
            self.driver.find_element_by_id('ht-login-passwordVal').send_keys(password)
            self.driver.find_element_by_id('hp-login-btn').click()
            sleep(2)
        else:
            self.driver.find_element_by_id('qtdl-phone').send_keys(name)
            self.driver.find_element_by_id('qtdl-password').send_keys(password)
            self.driver.find_element_by_id('hp-qtdlBtn').click()
            sleep(2)


COOKIES = []
class UseCookie(object):
    def __init__(self, driver, url, name, password = '111111'):
        self.driver = driver
        self.url = url
        self.name = name
        self.password = password
        # 判断前后台账号
        if self.url.find('admin')!= -1:
            self.accountType = 'admin'
        else:
            self.accountType = 'user'

    # 用cookie登录。如果cookie没保存则重新登录保存
    def login(self):
        if rw_cookies().check_if_cookie_saved():
            self.apply_cookies(self.driver)
        else:
            self.login_to_save_users_cookie()

    # 把cookie存入txt
    def save_cookies_into_txt(self, raw_cookies):
        # 对原始cookie处理， 去掉domain。 domain是给浏览器用的。 服务器不要这个。
        global COOKIES
        for cookie in raw_cookies:
            temp_cookie = cookie.copy()
            del temp_cookie['domain']
            COOKIES.append(temp_cookie)

        if rw_cookies().check_if_cookie_saved():
            pass
        else:
            rw_cookies().rewrite_cookies(self.transfer_cookie_dict_to_str(COOKIES))

    def login_to_save_users_cookie(self):
        Login(self.driver,self.url,self.name,self.password)
        sleep(2)
        COOKIES = self.driver.get_cookies()
        self.save_cookies_into_txt(COOKIES)

    def read_cookie_from_txt(self):
        if rw_cookies().check_if_cookie_saved():
            cookie_str = rw_cookies().read_cookies()
            cookie_dict = self.transfer_cookie_str_to_dict(cookie_str)
            return cookie_dict

    def apply_cookies(self, driver):
        cookies = self.read_cookie_from_txt()
        for cookie in cookies:
            driver.add_cookie(cookie)
            print(cookie)

    # cookie由字典到字串互相转换
    def transfer_cookie_str_to_dict(self, cookie_str):
        cookie_dict = simplejson.loads(cookie_str)
        return cookie_dict

    def transfer_cookie_dict_to_str(self, cookie_dict):
        cookie_str = simplejson.dumps(cookie_dict)
        return cookie_str

# 读写和判断cookie.txt
# 这里经过考虑，cookie和case存在一起比较方便。要删除很多以前写的代码有点心疼。
class rw_cookies(object):
    def __init__(self):
        # 当前目录的名字
        # 此函数会把最后一个目录名字和路径分开
        project_root = os.path.split(os.getcwd())
        print(project_root)
        # 检验一个文件是不是存在，此种方法用于cookie.txt和文件不再同一个文件夹下cookieSavedFile在config中设置
        self.cookie_saved_dir = os.path.join(project_root[0], cookieSavedFile)
        self.cookie_file_path = ""

    def check_if_cookie_saved(self):
        self.cookie_file_path = os.path.join(self.cookie_saved_dir, cookieTxtName)
        # 当前路径
        print(os.getcwd())
        fileExist = os.path.exists(self.cookie_file_path)
        print(fileExist)

        if fileExist:

            with open(self.cookie_file_path, 'r') as f:
                content = f.read()
            if len(content) == 0:
                print("The cookie file is empty.")
                # 空的文件，和没有，是一样的
                return False
            else:
                return True

        else:
            print("The cookie file is not existed.")
            return False

    def read_cookies(self):
        if self.check_if_cookie_saved():
            with open(self.cookie_file_path, 'r') as f:
                cookie_str = f.read()
            return cookie_str

        else:
            pass

    def rewrite_cookies(self, cookie_str):
        with open(self.cookie_file_path, 'w') as f:
            f.write(cookie_str)

    # 没有用到。 因为with open as会自动创建
    def create_cookies(self, cookie_str):
        if self.check_if_cookie_saved():
            pass
        else:
            with open(self.cookie_file_path, 'w') as f:
                f.write(cookie_str)




