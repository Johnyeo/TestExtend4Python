# coding:utf-8
import time
import unittest

from selenium import webdriver

from settings import properties, configs, changeDNS


class TestBase(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Chrome()
        self.driver.implicitly_wait(5)
        self.driver.maximize_window()
        self.record_list = []
        self.ave_wait = configs.ave_wait
        self.keepBrowserOpen = False
        changeDNS.checkDNS(configs.Environment)

    def tearDown(self):
        if self.keepBrowserOpen:
            time.sleep(3600)

        else:
            self.driver.quit()
        self.keepBrowserOpen = False