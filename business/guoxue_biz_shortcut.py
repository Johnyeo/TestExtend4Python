# coding:utf-8
import os
from time import sleep

import simplejson

from business import util_methods
from settings.configs import cookieSavedFile, cookieTxtName

import os
from time import sleep

import logging
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys

from business import util_methods
from settings.properties import *
import settings.configs

ave = configs.ave_wait
short = configs.short_wait
long = configs.long_wait


class Login(object):
    def __init__(self, driver, url, name, password='111111'):
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


class LoginAndOpen(object):
    def __init__(self, id, driver, url, name, password='111111',):
        Login(driver,url,name,password)
        driver.find_element_by_id(id).click()
        sleep(2)





COOKIES = []

class UseCookie(object):
    def __init__(self, driver, url, name, password='111111'):
        self.driver = driver
        self.url = url
        self.name = name
        self.password = password
        # 判断前后台账号
        if self.url.find('admin') != -1:
            self.accountType = 'admin'
        else:
            self.accountType = 'user'

    # 用cookie登录。如果cookie没保存则重新登录保存
    def login(self, target_url=None):
        # 目标跳转url如果为空，那就默认用类里面的url。
        if target_url == None:
            target_url = self.url
        if rw_cookies().check_if_cookie_saved():
            self.driver.get(target_url)
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
        Login(self.driver, self.url, self.name, self.password)
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
        pass

    def check_if_cookie_saved(self):
        fileExist = os.path.exists(cookieTxtName)
        print(fileExist)

        if fileExist:
            with open(cookieTxtName, 'r') as f:
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
            with open(cookieTxtName, 'r') as f:
                cookie_str = f.read()
            return cookie_str

        else:
            pass

    def rewrite_cookies(self, cookie_str):
        with open(cookieTxtName, 'w') as f:
            f.write(cookie_str)

    # 没有用到。 因为with open as会自动创建
    def create_cookies(self, cookie_str):
        if self.check_if_cookie_saved():
            pass
        else:
            with open(cookieTxtName, 'w') as f:
                f.write(cookie_str)


class NewVideo(object):
    def __init__(self, driver):
        self.driver = driver

    def build(self, type1 = None, type2 = None):
        name_str = util_methods.getPoem()
        name_str_ls = util_methods.splitPoem(name_str)

        Login(self.driver, adminLogin, admin['name'], admin['pwd'])
        sleep(ave)

        # 进入新建页面
        self.driver.find_element_by_id('spgl_tj').click()
        sleep(short)

        # 上传视频
        self.driver.find_element_by_id('uploadbtn_upload').click()
        sleep(ave)
        util_methods.uploadFile('mp4')
        sleep(long)
        print("上传视频ok")

        # 自定义文件名
        self.driver.find_element_by_id('wd_checkBox_isused_1').click()
        sleep(ave)
        coursename = self.driver.find_element_by_id('coursename')
        coursename.clear()
        coursename.send_keys(name_str_ls[0])
        sleep(long)
        print("自定义文件名ok")

        # 上传封面
        self.driver.find_element_by_id('sp_scfm_upload').click()
        sleep(short)
        util_methods.uploadFile('jpg')
        sleep(long)
        print("上传封面ok")

        # 系列的选择
        # 选择标签，
        tags = self.driver.find_element_by_class_name('lm-seriesbox')
        taglist = tags.find_elements_by_class_name('lm-series')
        # 点击第一个
        taglist[0].click()
        print("系列的选择ok")

        # 标签的选择
        # 选择标签，
        tags = self.driver.find_element_by_class_name('lm-labelbox')
        taglist = tags.find_elements_by_class_name('lm-label')
        # 点击第一个
        taglist[0].click()
        print("标签的选择ok")

        # 输入价格
        self.driver.find_element_by_id('courseprice').send_keys('0.01')
        print("输入价格ok")

        # 输入介绍内容
        self.driver.find_element_by_id('wd-editeditbox_courseintro').send_keys(name_str)
        # 上传内容介绍的图片
        self.driver.find_element_by_id('courseintro_insertimage').click()
        sleep(short)
        util_methods.uploadFile('jpg')
        sleep(long)
        print("输入介绍内容格ok")

        # 选择讲师
        # 点击添加讲师
        self.driver.find_element_by_id('spgl_tjjs').click()
        sleep(short)
        teacher = self.driver.find_elements_by_class_name('js-yxz-box')
        teacher[0].click()
        sleep(short)
        # 确定
        self.driver.find_element_by_id('xzjs_qd').click()
        print("点击添加讲师ok")

        if type1 == 'weike'or type2 == 'weike':
        # 选择微课
            self.driver.find_element_by_id('wd_checkBox_fbwk_01').click()
        if type1 == 'free' or type2 == 'free':
        # 选择免费
            self.driver.find_element_by_id('wd_checkBox_nomoney_0').click()

        # 点击保存
        self.driver.find_element_by_id('spgl_bc').click()
        print("点击保存ok")

        # 点击返回列表
        self.driver.find_element_by_id('hp-ret').click()
