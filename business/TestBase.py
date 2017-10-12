# coding:utf-8
import time
import unittest

import logging
from selenium import webdriver

from settings import properties, configs, changeDNS


class TestBase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        if configs.printLog == True:
            logging.basicConfig(filename=configs.log_file, level=logging.INFO, format = '%(asctime)s - %(levelname)s:%(messages)s')
        else:
            pass

    def setUp(self):
        self.driver = webdriver.Chrome()
        self.driver.implicitly_wait(5)
        self.driver.maximize_window()
        self.record_list = []
        # 设置等待时间
        self.ave_wait = configs.ave_wait
        # 设置case完成后是否关闭浏览器
        self.keepBrowserOpen = False
        # 检查dns
        changeDNS.checkDNS(configs.Environment)
        # 日志设置


    def tearDown(self):
        if self.keepBrowserOpen:
            time.sleep(3600)

        else:
            self.driver.quit()
        self.keepBrowserOpen = False


