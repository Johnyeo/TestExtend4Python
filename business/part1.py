# coding:utf-8
from time import sleep


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