# coding:utf-8
import os
import random
import re
import time

import datetime

import subprocess

import simplejson
import wmi
from urllib import request


record_list = []
ave_wait = 1

# 切换窗口
def switch_window_to(driver, target_page_title):
    for window1 in driver.window_handles:
        driver.switch_to.window(window1)
        print('焦点转到了',end='')
        print(driver.title)
        if driver.title == target_page_title:
            break

# 运行某个文件
def openProjectFileAt(currentpath,file_path):
    new = os.path.abspath(os.path.join(currentpath, os.pardir))  # 获取上一级目录
    new2 = os.path.join(new, file_path)  # 拼接上脚本的路径
    subprocess.Popen(new2)

# webdriver只能操作浏览器之内的东西。如果上传窗口打开，需要其他辅助工具。
# 上传图片。利用autoit的脚本。脚本在business里设置和修改。
# 上传什么文件， 是在autoit的脚本里决定的。 要修改就需要修改autoit的脚本，因此做不到参数化,
# 此处的地址是找脚本用的。每一个文件，对应一个脚本。利用subprocess打开脚本。
def uploadFile(type, file_path = None):
    if file_path == None:
        current = os.getcwd()
        if type == "mp4":
            openProjectFileAt(current,"business\\uploadMp4.exe")
        elif type == "jpg":
            openProjectFileAt(current, "business\\uploadJpg.exe")
        elif type == 'pdf':
            openProjectFileAt(current, "business\\uploadPdf.exe")
        else:
            print("material里面没有这个文件，请确认参数")
    else:
        subprocess.Popen(file_path)


def gen_name(param):


    return None

# 从古诗文网的名句页爬取古诗,第一个参数是页数，第二个参数是条数。p如果超过范围，则随机一个。num大于1则生产一个list
# 爬取古诗的作为文件的随机名字
def getPoem(p = 0, num = 1):
    #  p是古诗文网的页数,114页一共
    #  如果p = 0 则传入随机数。如果p = 具体数字则传入具体的数字
    if  p > 114 or p <=0:
        pageRange = range(1, 115)
        p = random.sample(pageRange, 1)
        p = str(p[0])
    else:
        p = str(p)
    url = 'http://so.gushiwen.org/mingju/Default.aspx?p=%s&c=&t='% p
    response = request.urlopen(url)
    page = response.read()
    page = page.decode('utf-8')
    pattern = re.compile(r'[\u4e00-\u9fa5].*(?=</a><span )')
    match_list = re.findall(pattern, page, )
    result = random.sample(match_list, num)
    if num == 1:
        return result[0]
    elif num <= 0:
        return match_list
    else:
        return result

def getCertainLength(tar_str,num = 0):
    if num <= 0:
        return tar_str
    else:
        result = tar_str[0:num]
        return result

def splitPoem(tar_str):
    tar_str = tar_str.replace('，',' ')
    tar_str = tar_str.replace('。',' ')
    tar_str = tar_str.replace('？',' ')
    tar_str = tar_str.replace('；',' ')
    tar_str = tar_str.replace('！',' ')
    result = tar_str.split()
    return result

# 将记录下来的名字的字典，用simplejosn转换成字符串，然后写入namelist.txt
def recordName(self, name_dict):
    simplejson.dumps(name_dict )
    with open("namelist.txt",'w') as f:
        f.write(name_dict)
    print("writing, the old namelist will be overwrite")

# 通过key获取字典里的值
def fetchName(self, key):
    with open("namelist.txt","r") as f:
        content = f.readline()
    name_dict = simplejson.loads()
    if name_dict.has_key(key):
        return  name_dict[key]
    else:
        print ("参数错误，key不在字典中 key doesn't exist")

