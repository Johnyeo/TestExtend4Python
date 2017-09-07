# coding:utf-8
import os
import unittest
from time import sleep

import logging
from HTMLTestRunner import HTMLTestRunner
from selenium.common.exceptions import NoSuchElementException

from business import util_methods
from business.TestBase import TestBase
from business.part1 import Login, UseCookie
from settings.properties import *
import settings.configs

ave = configs.ave_wait
short = configs.short_wait
long = configs.long_wait
loginPass = True

class studyManage(TestBase):
    # 后台登录
    @unittest.skipIf(True, "login pass")
    def test0010_login(self):
        # 登录
        Login(self.driver,adminLogin, admin['name'],admin['pwd'])
        self.assertTrue(self.driver.title == '视频管理-云上国学', msg='验证失败，页面未跳转到视频管理 page redirect failed')
        sleep(ave)
        if self.driver.title == '视频管理-云上国学':
            return True
        else:
            return False

    # 新建视频，上传视频图片等
    # @unittest.skipIf(test0010_login, "login Failed")
    def test0120_new_video(self):
        # 登录
        Login(self.driver, adminLogin, admin['name'], admin['pwd'])
        self.assertTrue(self.driver.title == '视频管理-云上国学',msg='验证失败，页面未跳转到视频管理 page redirect failed')
        sleep(ave)

        # 进入新建页面
        self.driver.find_element_by_id('spgl_tj').click()
        try:
            self.driver.find_element_by_id('uploadbtn_upload').click()
        except NoSuchElementException as e:
            self.assertTrue(False,msg="上传按钮未找到，页面切换不成功 uploadbutton not found" )

        # 上传操作
        sleep(ave)
        util_methods.uploadFile('mp4')
        sleep(long)
        # 通过视频名是否为空判断是否上传成功
        self.assertIsNotNone(self.driver.find_element_by_id('videoname').text, msg='视频未上传成功 video upload failed')

        # 自定义文件名
        self.driver.find_element_by_id('wd_checkBox_isused_1').click()
        sleep(ave)
        coursename = self.driver.find_element_by_id('coursename')
        coursename.clear()
        coursename.send_keys(util_methods.getPoem())
        sleep(long)

    # 新建视频第二部分 - 上传图
    def test0123_new_video(self):
        Login(self.driver, adminLogin, admin['name'], admin['pwd'])
        sleep(ave)

        # 进入新建页面
        self.driver.find_element_by_id('spgl_tj').click()


        # 上传封面
        self.driver.find_element_by_id('sp_scfm_upload').click()
        sleep(short)
        util_methods.uploadFile('jpg')
        sleep(long)
        # 通过封面按钮变化判断是否上传成功
        self.assertTrue(self.driver.find_element_by_id('spgl_fmcz').text == '删除', msg='视频未上传成功 video upload failed')
        sleep(ave)

    # 新建视频第二部分 - 系列
    def test0124_new_video(self):
        Login(self.driver, adminLogin, admin['name'], admin['pwd'])
        sleep(ave)

        # 进入新建页面
        self.driver.find_element_by_id('spgl_tj').click()


        # 系列的选择
        # 选择标签，
        tags = self.driver.find_element_by_class_name('lm-seriesbox')
        taglist = tags.find_elements_by_class_name('lm-series')
        # 点击第一个
        taglist[0].click()
        serie_tagid1 = taglist[0].get_attribute('id')
        serie_tagid1 = serie_tagid1.replace('serie_','')
        try:
            self.driver.find_element_by_id(serie_tagid1)
        except NoSuchElementException as e:
            self.assertTrue(False, msg="标签未添加成功 tag select failed")
        sleep(short)

        # 打开标签选择框
        tags.find_element_by_class_name('lm-oper-more').click()
        sleep(short)
        # 1. 点击标签删除
        self.driver.find_element_by_id('bq_'+ serie_tagid1).click()
        # 验证点
        try:
            self.driver.find_element_by_class_name('lm-bqxz-scxz')
        except NoSuchElementException as e:
            self.assertTrue(True, msg="标签删除成功 tag deleted")
        sleep(short)

        # 2. 点击标签添加
        self.driver.find_element_by_class_name('lm-bqmc').click()
        sleep(short)
        # 验证点
        try:
            self.driver.find_element_by_class_name('lm-bqxz-xzbq')
        except NoSuchElementException as e:
            self.assertTrue(False, msg="标签添加失败 tag select failed")
        sleep(ave)

        # 关闭标签选择
        self.driver.find_element_by_id('gxpt_bqxz').find_element_by_class_name('wd-prompt-close').click()
        sleep(long)
        logging.info("完成系列选择")

    # 新建视频第三部分 - 标签
    def test0125_new_video(self):
        Login(self.driver, adminLogin, admin['name'], admin['pwd'])
        sleep(ave)

        # 进入新建页面
        self.driver.find_element_by_id('spgl_tj').click()

        # 标签的选择
        # 选择标签，
        tags = self.driver.find_element_by_class_name('lm-labelbox')
        taglist = tags.find_elements_by_class_name('lm-label')
        # 点击第一个
        taglist[0].click()
        serie_tagid1 = taglist[0].get_attribute('id')
        serie_tagid1 = serie_tagid1.replace('label_', '')
        try:
            self.driver.find_element_by_id(serie_tagid1)
        except NoSuchElementException as e:
            self.assertTrue(False, msg="标签未添加成功 tag select failed")
        sleep(short)

        # 打开标签选择框
        tags.find_element_by_class_name('lm-oper-more').click()
        sleep(short)
        # 1. 点击标签删除
        self.driver.find_element_by_id('bq_' + serie_tagid1).click()
        # 验证点
        try:
            self.driver.find_element_by_class_name('lm-bqxz-scxz')
        except NoSuchElementException as e:
            self.assertTrue(True, msg="标签删除成功 tag deleted")
        sleep(short)

        # 2. 点击标签添加
        self.driver.find_element_by_class_name('lm-bqmc').click()
        sleep(short)
        # 验证点
        try:
            self.driver.find_element_by_class_name('lm-bqxz-xzbq')
        except NoSuchElementException as e:
            self.assertTrue(False, msg="标签添加失败 tag select failed")
        sleep(ave)

        # 关闭标签选择
        self.driver.find_element_by_id('gxpt_bqxz').find_element_by_class_name('wd-prompt-close').click()
        sleep(long)
        logging.info("完成标签选择")


    # 新建视频第四部分 - 添加讲师
    def test0125_new_video(self):
        Login(self.driver, adminLogin, admin['name'], admin['pwd'])
        sleep(ave)

        # 进入新建页面
        self.driver.find_element_by_id('spgl_tj').click()
        sleep(short)
        # 点击添加讲师
        self.driver.find_element_by_id('spgl_tjjs').click()
        sleep(short)
        teacher = self.driver.find_elements_by_class_name('js-yxz-box')
        teacher[0].click()
    #     删除老师
        self.driver.find_element_by_class_name('js-name').find_element_by_tag_name('i').click
        # 验证是否删除成功
        try:
            self.driver.find_element_by_class_name('js-name')
        except NoSuchElementException as e:
            self.assertTrue(True,'讲师删除成功 teacher deleted success')
        logging.info('讲师测试运行完成 0125 done')

    # 学习管理 - 教材管理
    @unittest.skip(True)
    def test0130_new_book(self):
        # 登录
        Login(self.driver, adminLogin, admin['name'], admin['pwd'])
        sleep(ave)
        self.driver.find_element_by_id('jcgl').click()
        sleep(ave)
        self.assertTrue(self.driver.title == '教材管理-云上国学',msg='验证失败，页面未跳转到教材管理 page redirect failed')
        sleep(ave)
        sleep(ave)

    # 学习管理 - 直播管理
    @unittest.skip(True)
    def test0140_new_book(self):
        # 登录
        Login(self.driver, adminLogin, admin['name'], admin['pwd'])
        sleep(ave)
        self.driver.find_element_by_id('zbgl').click()
        sleep(ave)
        logging.info('hello')
        self.assertTrue(self.driver.title == '直播管理-云上国学', msg='验证失败，页面未跳转到直播管理 page redirect failed')
        sleep(ave)



if __name__ == "__main__":
    # 添加测试用例

    suite = unittest.TestSuite()
    suite.addTest(studyManage('test0125_new_video'))
    print('Test running ...')
    logging.info("testtesttest")

    if configs.generateReport:
        # 生成报告：
        path = os.getcwd() + "_report.html"
        with open(path, "wb") as f:
            runner = HTMLTestRunner.HTMLTestRunner(stream=f, title = "测试报告", description="云上国学后台自动化测试报告")
            runner.run(suite())
    else:
        # 不生成报告：
        if configs.outputLog:
            # 输出控制台
            runner = unittest.TextTestRunner()
            runner.run(suite)

        else:
            # 不输出控制台
            result = unittest.TestResult()
            suite().run(result)









