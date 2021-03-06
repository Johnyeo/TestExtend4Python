# coding:utf-8
import datetime
import os
import unittest
from time import sleep

import logging
from HTMLTestRunner import HTMLTestRunner
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys

from business import util_methods
from business.TestBase import TestBase
from business.guoxue_biz_shortcut import Login,LoginAndOpen
from settings.properties import *
import settings.configs

ave = configs.ave_wait
short = configs.short_wait
long = configs.long_wait
loginPass = True
name = {}

class StudyManage(TestBase):
    # 后台登录
    @unittest.skipIf(False, "login pass")
    def test0010_login(self):
        # 登录
        Login(self.driver, adminLogin, admin['name'], admin['pwd'])
        self.assertTrue(self.driver.title == '视频管理-云上国学', msg='验证失败，页面未跳转到视频管理 page redirect failed')
        sleep(ave)
        self.assertEqual(True, self.driver.title == '视频管理-云上国学')

    # 新建视频，上传视频图片等
    # @unittest.skipIf(test0010_login, "login Failed")
    @unittest.skipIf(False,'test')
    def test0020_new_video(self):
        # 登录
        Login(self.driver, adminLogin, admin['name'], admin['pwd'])
        self.assertTrue(self.driver.title == '视频管理-云上国学', msg='验证失败，页面未跳转到视频管理 page redirect failed')
        sleep(ave)

        # 进入新建页面
        self.driver.find_element_by_id('spgl_tj').click()
        try:
            self.driver.find_element_by_id('uploadbtn_upload').click()
        except NoSuchElementException:
            self.assertTrue(False, msg="上传按钮未找到，页面切换不成功")

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
    @unittest.skipIf(False,'test')
    def test0021_new_video(self):
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
    @unittest.skipIf(False, 'test')
    def test0022_new_video(self):
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
        serie_tagid1 = serie_tagid1.replace('serie_', '')
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
        logging.info("完成系列选择")

    # 新建视频第三部分 - 标签
    @unittest.skipIf(False, 'test')
    def test0023_new_video(self):
        Login(self.driver, adminLogin, admin['name'], admin['pwd'])
        sleep(ave)

        # 进入新建页面
        self.driver.find_element_by_id('spgl_tj').click()
        sleep(ave)
        sleep(short)
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
        print("完成标签选择")

    # 新建视频第四部分 - 添加讲师
    @unittest.skipIf(False,'test')
    def test0024_new_video(self):
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
        self.driver.find_element_by_class_name('js-name').find_element_by_tag_name('i').click()
        # 验证是否删除成功
        try:
            self.driver.find_element_by_class_name('js-name')
        except NoSuchElementException as e:
            self.assertTrue(True, '讲师删除成功 teacher deleted success')
        logging.info('讲师测试运行完成 0125 done')

    # 新建视频第五部分 - 新建标签
    @unittest.skipIf(True,"测试通过，不频繁创建标签")
    def test0025_new_video(self):
        Login(self.driver, adminLogin, admin['name'], admin['pwd'])
        sleep(ave)
        # 第几个标签
        i = 0

        # 进入新建页面
        self.driver.find_element_by_id('spgl_tj').click()
        sleep(short)
        # 标签框div
        labelboxes = self.driver.find_elements_by_class_name('wdLabelbox-qz-label')
        # 标签输入框
        labeltext = labelboxes[i].find_element_by_class_name('wdLabelbox-qz-labeltext')
        # 获取随机字串
        labelname = util_methods.splitPoem(util_methods.getPoem())
        sleep(long)
        # 测试 “系列”
        labeltext.send_keys(labelname[i])
        sleep(short)
        # 输入标签名字之后，回车
        labeltext.send_keys(Keys.ENTER)
        # 验证是否成功
        try:
            text = labelboxes[i].find_element_by_class_name('wdLabelbox-qz-labelspana').text
            self.assertEqual(text, labelname[i])
        except NoSuchElementException as e:
            print('标签%s未找到' % (labelname[i]))

    # 价格，介绍，保存 整体走一遍
    @unittest.skipIf(False,'test')
    def test0026_new_video(self):
        name_str = util_methods.getPoem()
        name_str_ls = util_methods.splitPoem(name_str)
        global name
        name['video'] = name_str_ls[0]

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
        coursename.send_keys(name["video"])
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
        sleep(ave)

        # 选择微课
        # self.driver.find_element_by_id('wd_checkBox_fbwk_01').click()
        # 选择免费
        # self.driver.find_element_by_id('wd_checkBox_nomoney_0').click()

        # 点击保存
        self.driver.find_element_by_id('spgl_bc').click()
        sleep(long)
        print('保存完毕')

        # 点击返回列表
        self.driver.find_element_by_class_name('hp-ret').click()
        sleep(ave)

        # 验证课程是否创建成功
        table = self.driver.find_element_by_id('spgl_table')
        # 每一行是一个tr
        trs = table.find_elements_by_tag_name('tr')
        # 第一行是标题， 正文从tr 1 开始。 td是列。
        tds = trs[1].find_elements_by_tag_name('td')
        name_exp = tds[1].text

        self.assertEqual(name_exp, name["video"],"视频未被查询到创建失败 video created failed")

    # 学习管理 - 教材管理
    @unittest.skipIf(False,'test')
    def test0030_new_book(self):
        # 登录
        Login(self.driver, adminLogin, admin['name'], admin['pwd'])
        sleep(ave)
        self.driver.find_element_by_id('jcgl').click()
        sleep(ave)
        self.assertTrue(self.driver.title == '教材管理-云上国学', msg='验证失败，页面未跳转到教材管理 page redirect failed')
        sleep(ave)
        sleep(ave)

    #  新增教材
    @unittest.skipIf(True, 'test')
    def test0031_new_book(self):
        # 获取随机名字
        name_str = util_methods.getPoem()
        name_str_ls = util_methods.splitPoem(name_str)
        sleep(ave)
        global name
        name['book']=name_str_ls[0]
        print(name['book'])

        # 登录
        Login(self.driver, adminLogin, admin['name'], admin['pwd'])
        sleep(ave)
        self.driver.find_element_by_id('jcgl').click()
        sleep(ave)
        print("进入教材管理ok")

        # 点击新建
        self.driver.find_element_by_id('jc_tj').click()
        sleep(ave)

        # 上传教材
        self.driver.find_element_by_id('uploadbtn_upload').click()
        sleep(ave)
        util_methods.uploadFile('pdf')
        sleep(long)
        print('上传文件ok')

        # 输入教材名字
        self.driver.find_element_by_id('wd_checkBox_isused_1').click()
        sleep(short)
        self.driver.find_element_by_id('coursename').clear()
        self.driver.find_element_by_id('coursename').send_keys(name['book'])
        sleep(short)
        print('输入教材名字')

        # 选择分类
        # 点击第一个分类框
        self.driver.find_element_by_id('code_coursecategory1').click()
        cat = self.driver.find_element_by_id('dmBody')
        options = cat.find_elements_by_tag_name('tr')
        options[0].click()
        # 第二个
        self.driver.find_element_by_id('code_coursecategory2').click()
        cat = self.driver.find_element_by_id('dmBody')
        options = cat.find_elements_by_tag_name('tr')
        options[0].click()
        # 第三个
        self.driver.find_element_by_id('code_coursecategory3').click()
        cat = self.driver.find_element_by_id('dmBody')
        options = cat.find_elements_by_tag_name('tr')
        options[0].click()

        # 选择标签
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

        # 输入作者
        self.driver.find_element_by_id('author').send_keys(name_str_ls[1])
        sleep(short)
        print('输入作者')

        # 点击保存
        self.driver.find_element_by_id('jcgl_bc').click()
        sleep(long)

        # 点击返回列表
        self.driver.find_element_by_class_name('hp-ret').click()
        sleep(ave)

        # 验证课程是否创建成功
        table = self.driver.find_element_by_id('jc_table')
        # 每一行是一个tr
        trs = table.find_elements_by_tag_name('tr')
        # 第一行是标题， 正文从tr 1 开始。 td是列。
        tds = trs[1].find_elements_by_tag_name('td')
        name_exp = tds[1].text

        self.assertEqual(name_exp, name['book'],"教材 未被查询到创建失败 book created failed")

    # 学习管理 - 直播管理
    @unittest.skipIf(False,'test')
    def test0040_new_broadcast(self):
        # 登录
        Login(self.driver, adminLogin, admin['name'], admin['pwd'])
        sleep(ave)
        self.driver.find_element_by_id('zbgl').click()
        sleep(ave)
        logging.info('hello')
        self.assertTrue(self.driver.title == '直播管理-云上国学', msg='验证失败，页面未跳转到直播管理 page redirect failed')
        sleep(ave)

    #  新增直播
    @unittest.skipIf(False, 'test')
    def test0041_new_broadcast(self):
        # 获取随机名字
        name_str = util_methods.getPoem()
        name_str_ls = util_methods.splitPoem(name_str)
        today = datetime.datetime.now().strftime('%d')
        tomorrow = str(int(today)+1)
        sleep(ave)
        global name
        name['broadcast'] = name_str_ls[0]

        # 登录
        Login(self.driver, adminLogin, admin['name'], admin['pwd'])
        sleep(ave)
        self.driver.find_element_by_id('zbgl').click()
        sleep(ave)
        print("进入直播管理ok")

        # 点击新建
        self.driver.find_element_by_id('zbgl_xj').click()
        sleep(ave)

        # 输入直播名字
        self.driver.find_element_by_id('coursename').send_keys(name['broadcast'])
        sleep(short)
        print('输入直播名字')

        # 选择标签
        tags = self.driver.find_element_by_class_name('lm-labelbox')
        taglist = tags.find_elements_by_class_name('lm-label')
        # 点击第一个
        taglist[0].click()
        print("标签的选择ok")

        # 输入价格
        self.driver.find_element_by_id('courseprice').send_keys('0.01')
        print("输入价格ok")

        # 选择日期 -- 今天+1  -- 月末会有问题
        self.driver.find_element_by_id('zbgl_zbsj').click()
        self.driver.find_element_by_id('zbgl_zbsj_'+ tomorrow).click()

        # 选择时间长度
        self.driver.find_element_by_id('code_TIMELENGTH').click()
        self.driver.find_element_by_id('dmBody').find_element_by_class_name('DMRB2').click()

        # 输入人数
        self.driver.find_element_by_id('courseupperlimit').send_keys('10')

        # 添加授课者
        self.driver.find_element_by_id('zbgl_tjskz').click()
        sleep(ave)
        teacher_ls = self.driver.find_element_by_id('skz_list').find_elements_by_tag_name('li')
        teacher_ls[1].click()
        # 翻页
        self.driver.find_element_by_id('wdtable_pagecountnext_skz_list').click()
        sleep(short)
        teacher_ls = self.driver.find_element_by_id('skz_list').find_elements_by_tag_name('li')
        teacher_ls[1].click()
        sleep(short)
        # 确定添加
        self.driver.find_element_by_id('xzskz_qd').click()
        sleep(short)
        # 点击保存
        self.driver.find_element_by_id('zbgl_bc').click()
        error_msg = self.driver.find_element_by_id('prompt-text-error').text
        sleep(long)
        print(error_msg)
        # 点击返回列表
        self.driver.find_element_by_class_name('hp-ret').click()
        sleep(ave)

        # 验证课程是否创建成功
        table = self.driver.find_element_by_id('zbgl_table')
        # 每一行是一个tr
        trs = table.find_elements_by_tag_name('tr')

        targetIsFound = False
        for tr in trs:
            tds = tr.find_elements_by_tag_name('td')
            name_exp = tds[1].text
            print(name_exp)
            if name_exp == name['broadcast']:
                targetIsFound = True
                break
        if targetIsFound:
            print("创建成功")
        else:
            self.assertTrue(False, "直播 未被查询到，确认是否在下一页？ book created failed")

    # 进入培训管理
    @unittest.skipIf(False, "test")
    def test0050_openPeixunguanli(self):
        # 登录并进入培训管理
        LoginAndOpen('pxgl',self.driver, adminLogin, admin['name'], admin['pwd'])
        # 验证
        self.assertTrue(self.driver.title == '培训管理-云上国学', msg='培训管理跳转失败 page redirect failed')
        sleep(ave)

    # 培训管理-新建-培训介绍
    @unittest.skipIf(False, "test")
    def test0051_peixunjieshao(self):
        # 登录并进入培训管理
        LoginAndOpen('pxgl',self.driver, adminLogin, admin['name'], admin['pwd'])
        # 点击新建
        self.driver.find_element_by_id('px_add').click()
        # 验证
        classname = self.driver.find_element_by_id('px_pxjs').get_attribute('class')
        self.assertEqual('active',classname,'没有打开培训介绍页面')

    # 培训管理-新建-培训介绍 不输入名字
    @unittest.skipIf(False, "test")
    def test0052_3_name(self):
        # 登录并进入培训管理
        LoginAndOpen('pxgl',self.driver, adminLogin, admin['name'], admin['pwd'])
        # 点击新建
        self.driver.find_element_by_id('px_add').click()
        # 不输入名字，点击保存
        self.driver.find_element_by_id('px_bc').click()
        sleep(ave)
        error_msg = self.driver.find_element_by_id('prompt-text-error').text
        print(error_msg)
        error_msg = '名称：不能为空'
        self.assertEqual('名称：不能为空',error_msg,'错误提示没有弹出，或者不符1')
        # 关闭提示
        self.driver.find_element_by_id('prompt-wd_prompt_close-error').click()
        sleep(ave)
        # 不输入名字，点击下一步
        self.driver.find_element_by_id('px_next').click()
        sleep(ave)
        error_msg2 = self.driver.find_element_by_id('prompt-text-error').text
        self.assertEqual('名称：不能为空',error_msg2,'错误提示没有弹出，或者不符2')
        # 关闭提示
        self.driver.find_element_by_id('prompt-wd_prompt_close-error').click()

    # 输入曾经存在的培训的名字
    @unittest.skipIf(False, "test")
    def test0054_name(self):
        # 登录并进入培训管理
        LoginAndOpen('pxgl',self.driver, adminLogin, admin['name'], admin['pwd'])
        # 获取一个存在的培训名称
        peixun_name = self.driver.find_element_by_class_name('pxgl-mc').text
        # 点击新建
        self.driver.find_element_by_id('px_add').click()
        # 输入名称
        self.driver.find_element_by_id('pxjs_mc').send_keys(peixun_name)
        # 点击保存
        self.driver.find_element_by_id('px_bc').click()
        sleep(ave)
        error_msg = self.driver.find_element_by_id('prompt-text-error').text
        self.assertEqual('名称：培训任务名称已存在',error_msg,'错误提示没有弹出，或者不符1')
        # 关闭提示
        self.driver.find_element_by_id('prompt-wd_prompt_close-error').click()
        # 不输入名字，点击下一步
        self.driver.find_element_by_id('px_next').click()
        sleep(ave)
        error_msg = self.driver.find_element_by_id('prompt-text-error').text
        self.assertEqual('名称：培训任务名称已存在',error_msg,'错误提示没有弹出，或者不符2')
        # 关闭提示
        self.driver.find_element_by_id('prompt-wd_prompt_close-error').click()

    # 培训删除
    @unittest.skipIf(True, "test")
    def test0055_savePeixun(self):
        # 登录并进入培训管理
        LoginAndOpen('pxgl',self.driver, adminLogin, admin['name'], admin['pwd'])

        # 元素对象
        peixun_ls = self.driver.find_elements_by_class_name('hp-pxgl-div')

        # 找到删除按钮进行删除
        try:
            peixun_ls[0].find_element_by_class_name('px_sc').click()
            name_exp = peixun_ls[0].find_element_by_class_name('pxgl-mc').text
        except NoSuchElementException:
            self.assertTrue(False, msg="没有可以删除的对象 No target to be deleted")

        sleep(ave)
        # 弹出窗口,点击确定
        self.driver.find_element_by_id('prompt-wd_prompt_close-ok-confirm').click()
        sleep(ave)

        # 元素对象
        peixun_ls = self.driver.find_elements_by_class_name('hp-pxgl-div')
        for peixun in peixun_ls:
            print(name_exp)
            name_act = peixun.find_element_by_class_name('pxgl-mc').text
            print(name_act)

            if name_exp == name_act:
                self.assertTrue(False,msg='培训仍然存在，没有删除 delete failed')
        print("循环结束，原来的培训名称已经不存在，删除成功")

    # 新增培训 - 第一页
    @unittest.skipIf(False, "test")
    def test0056_savePeixun(self):
        # 获取随机名字
        name_str = util_methods.getPoem()
        name_str_ls = util_methods.splitPoem(name_str)
        name['training'] = name_str_ls[0]
        # 登录并进入培训管理
        LoginAndOpen('pxgl',self.driver, adminLogin, admin['name'], admin['pwd'])

        # 点击新建
        self.driver.find_element_by_id('px_add').click()

        # 输入名称
        self.driver.find_element_by_id('pxjs_mc').send_keys(name['training'])
        print('输入名称')

        # 上传封面
        self.driver.find_element_by_id('pxjs_sc_upload').click()
        util_methods.uploadFile('jpg')
        sleep(long)
        print('上传封面')

        # 上传介绍文字和图片
        self.driver.find_element_by_id('wd-editeditbox_pxjs').send_keys(name_str)
        # 上传内容介绍的图片
        self.driver.find_element_by_id('pxjs_insertimage').click()
        sleep(short)
        util_methods.uploadFile('jpg')
        sleep(long)
        print("输入介绍内容格")

        # 课程体系
        self.driver.find_element_by_id('wd-editeditbox_kctx').send_keys(name_str)
        # 上传内容介绍的图片
        self.driver.find_element_by_id('kctx_insertimage').click()
        sleep(ave)
        util_methods.uploadFile('png')
        sleep(long)
        print("输入课程体系")

        # 点击添加讲师
        self.driver.find_element_by_id('px_tjjs').click()
        sleep(short)
        teacher = self.driver.find_elements_by_class_name('js-yxz-box')
        teacher[0].click()
        sleep(short)
        # 确定
        self.driver.find_element_by_id('xzjs_qd').click()
        sleep(ave)
        print('添加讲师')

        # 保存
        self.driver.find_element_by_id('px_bc').click()
        sleep(long)
        error_msg = self.driver.find_element_by_id('prompt-text-error').text
        print(error_msg)
        print('保存')

        # 返回列表
        self.driver.find_element_by_class_name('hp-ret').click()
        sleep(long)
        print('返回列表')

        # 获取第一个培训的名字
        train_ls = self.driver.find_elements_by_class_name('pxgl-mc')
        name_exp  = train_ls[0].text

        # 断言
        self.assertEqual(name_exp,name['training'],msg="培训名字未找到 training name not found")

    #  新增培训 - 第二页
    @unittest.skipIf(False, 'test')
    def test0057_new_training(self):
        # 登录
        Login(self.driver, adminLogin, admin['name'], admin['pwd'])
        sleep(ave)
        self.driver.find_element_by_id('pxgl').click()
        sleep(ave)
        print("进入培训管理ok")

    # 选择第一个培训（刚刚创建的）
        trains = self.driver.find_elements_by_class_name('pxgl-mc')
        trains[0].click()
        sleep(ave)

    # 进入第二页
        self.driver.find_element_by_id('px_next').click()
        sleep(ave)

    # 新建版块
        self.driver.find_element_by_id('px_xjbk').click()
        sleep(ave)
    # 新建内容
        self.driver.find_element_by_id('px_xjnr').click()
        sleep(ave)
    #   新建内容 - 添加视频
        self.driver.find_element_by_id('nrlx_sp').click()
        table = self.driver.find_element_by_id('pxnr_xzsp')
        sleep(long)
        # 全选
        table.find_element_by_id('wd_checkBox_wdtablecheckall').click()
        # 取消全选
        table.find_element_by_id('wd_checkBox_wdtablecheckall').click()
        sleep(short)
        # 选择两个
        checkboxes = table.find_elements_by_class_name('wd-checkbox-check')
        checkboxes[1].click()
        checkboxes[2].click()
        # 确认选择
        self.driver.find_element_by_id('xzsp_qd').click()
        sleep(long)

        # 下一步（点击下一步就相当于保存了）
        self.driver.find_element_by_id('px_next').click()
        # 返回列表
        sleep(ave)
        self.driver.find_element_by_class_name('hp-ret').click()
        sleep(ave)

    @unittest.skipIf(False, 'test')
    def test0057_lxt_new_training(self):
        # 登录
        Login(self.driver, adminLogin, admin['name'], admin['pwd'])
        sleep(ave)
        self.driver.find_element_by_id('pxgl').click()
        sleep(ave)
        print("进入培训管理ok")

        # 选择第一个培训（刚刚创建的）
        trains = self.driver.find_elements_by_class_name('pxgl-mc')
        trains[0].click()
        sleep(ave)

        # 进入第二页
        self.driver.find_element_by_id('px_next').click()
        sleep(ave)

    # 新建内容
        self.driver.find_element_by_id('px_xjnr').click()
        sleep(ave)
    #   新建内容 - 添加练习题
        self.driver.find_element_by_id('nrlx_lxt').click()
        sleep(long)
        # 点击加入试题篮
        button = self.driver.find_elements_by_class_name('stl-jr')
        # 选择三道题
        button[0].click()
        sleep(short)
        button[1].click()
        sleep(short)
        button[2].click()
        sleep(short)
        # 确定
        self.driver.find_element_by_id('stl_qd').click()
        sleep(ave)
        # 再次确定（此处可以更详细的测试但是略过）
        self.driver.find_element_by_id('lxt_bjqd').click()
        sleep(ave)

    # 下一步（点击下一步就相当于保存了）
        self.driver.find_element_by_id('px_next').click()
        sleep(ave)
    # 返回列表
        self.driver.find_element_by_class_name('hp-ret').click()
        sleep(ave)

    #  新增培训 - 第三页
    @unittest.skipIf(False, 'test')
    def test0058_new_training(self):
        # 登录
        Login(self.driver, adminLogin, admin['name'], admin['pwd'])
        sleep(ave)
        self.driver.find_element_by_id('pxgl').click()
        sleep(ave)
        print("进入培训管理ok")

    # 选择第一个培训（刚刚创建的）
        trains = self.driver.find_elements_by_class_name('pxgl-mc')
        trains[0].click()
        sleep(ave)

    # 进入第三页
        self.driver.find_element_by_id('px_next').click()
        sleep(ave)
        self.driver.find_element_by_id('px_next').click()
        sleep(ave)

    # 填写证书名称（直接写死比较方便。因为可以重复）
        self.driver.find_element_by_id('jysz_zsmc').send_keys('【测试】证书名字')

    # 选择试卷
        self.driver.find_element_by_id('jysz_xzsj').click()
        sleep(ave)
        # 弹出窗口
        window1 = self.driver.find_element_by_id('pxnr_xzsj')
        radio_ls = window1.find_elements_by_class_name('wd-radio-check')
        print(len(radio_ls))
        # 点击第一个
        radio_ls[0].click()
        # 确定
        window1.find_element_by_id('xzsj_qd').click()
        sleep(ave)

    # 选择结业证书模板
        self.driver.find_element_by_id('jysz_xzmb').click()
        sleep(ave)
        # 弹出窗口
        window2 = self.driver.find_element_by_id('pxnr_xzmb')
        radio_ls2 = window2.find_elements_by_class_name('wd-radio-check')
        print(len(radio_ls2))
        # 点击第一个
        radio_ls2[0].click()
        # 确定
        window2.find_element_by_id('xzmb_qd').click()
        sleep(ave)

    # 下一步（点击下一步就相当于保存了）
        self.driver.find_element_by_id('px_next').click()
        sleep(ave)

    #  新增培训 - 第四页
    @unittest.skipIf(False, 'test')
    def test0059_new_training(self):
        # 登录
        Login(self.driver, adminLogin, admin['name'], admin['pwd'])
        sleep(ave)
        self.driver.find_element_by_id('pxgl').click()
        sleep(ave)
        print("进入培训管理ok")

    # 选择第一个培训（刚刚创建的）
        trains = self.driver.find_elements_by_class_name('pxgl-mc')
        trains[0].click()
        sleep(ave)

    # 进入第四页
        self.driver.find_element_by_id('px_next').click()
        sleep(ave)
        self.driver.find_element_by_id('px_next').click()
        sleep(ave)
        self.driver.find_element_by_id('px_next').click()
        sleep(ave)

    # 都选择免费
        self.driver.find_element_by_id('wd_checkBox_dj_kc_free').click()
        self.driver.find_element_by_id('wd_checkBox_dj_jyks_free').click()
        # self.driver.find_element_by_id('wd_checkBox_dj_rzks_free').click()

    # 认证输入0.01元
        self.driver.find_element_by_id('dj_rzks').send_keys('0.01')
    # 保存
        self.driver.find_element_by_id('px_bc').click()
        sleep(ave)
    # 返回列表
        self.driver.find_element_by_class_name('hp-ret').click()
        sleep(ave)

    # 把培训发布
    @unittest.skipIf(False, 'test')
    def test0060_new_training(self):
        # 选择第一个培训（刚刚创建的）
        trains = self.driver.find_elements_by_class_name('pxgl-mc')
        name_str = trains[0].text
        trains[0].click()
        sleep(ave)

        # 进入第四页
        self.driver.find_element_by_id('px_next').click()
        sleep(ave)
        self.driver.find_element_by_id('px_next').click()
        sleep(ave)
        self.driver.find_element_by_id('px_next').click()
        sleep(ave)

    # 点击发布按钮
        self.driver.find_element_by_id('px_fb').click()
        print('发布完成')
        sleep(long)

    # 元素对象
        peixun_ls = self.driver.find_elements_by_class_name('hp-pxgl-div')
        state = peixun_ls[0].find_element_by_class_name('zt-wfb').text
        print(state)

# 视频管理用例组
def videoSuite():
    testcases = ['test0020_new_video',
                 'test0021_new_video',
                 'test0022_new_video',
                 'test0023_new_video',
                 'test0024_new_video',
                 'test0025_new_video',
                 'test0026_new_video',
                 ]
    suite = unittest.TestSuite(testcases)
    return suite

# 教材管理用例组
def bookSuite():
    testcases = ['test0030_new_book',
                 'test0031_new_book',
                 ]
    suite = unittest.TestSuite(map(StudyManage, testcases))
    return suite

# 直播管理用例组
def broadCastSuite():
    testcases = ['test0040_new_broadcast',
                 'test0041_new_broadcast',
                 ]
    suite = unittest.TestSuite(testcases)
    return suite

# 培训管理用例组
def peixunSuite():
    testcases = ['test0050_openPeixunguanli',
                 'test0051_peixunjieshao',
                 'test0052_3_name',
                 'test0054_name',
                 'test0055_savePeixun',
                 'test0056_savePeixun',
                 'test0057_new_training',
                 'test0057_lxt_new_training',
                 'test0058_new_training',
                 'test0059_new_training',
                 'test0060_new_training',
                 ]
    suite = unittest.TestSuite({StudyManage:testcases})
    return suite

if __name__ == "__main__":
    # 单独执行
    # suite.addTest(StudyManage('test0122_new_video'))
    # 执行全部
    # suite = unittest.defaultTestLoader.loadTestsFromTestCase(StudyManage)
    # 成组执行
    suite = unittest.TestSuite([
        # videoSuite(),
        bookSuite(),
        # broadCastSuite(),
        # peixunSuite(),
                   ])

    if configs.generateReport:
        # 生成报告：
        path = os.getcwd() + "_report.html"
        print(path)
        with open(path, "wb") as f:
            runner = HTMLTestRunner.HTMLTestRunner(stream=f, title="测试报告", description="云上国学后台自动化测试报告")
            runner.run(suite)
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