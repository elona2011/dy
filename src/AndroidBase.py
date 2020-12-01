import subprocess
import cv2
import datetime
import sys
import os
import time
import numpy as np
import pathlib
from os import path

# 截图文件名
ScreenShotFileName = "Tmp01.png"
ScreenShotDetected = "Tmp02.png"
tmpImgPath = "/tmp/" + ScreenShotFileName
threshold = 0.7
dir_root = pathlib.Path(__file__).parent.absolute()


class AndroidBase():
    def __init__(self, id):
        self.id = id
        self.GetScreenSize()
        # self.width = 1080
        # self.height = 1920
        self.dir_root = "."
        self.threshold = 0.7  # 图像比对默认阈值

    # 打印日志
    def LogPrint(self, text):
        now = datetime.datetime.now()
        otherStyleTime = now.strftime("%Y-%m-%d %H:%M:%S")
        mystr = otherStyleTime + "  " + text
        print(mystr)

    # 重新定向命令
    def SendCommand(self, command):
        # os.system(str)
        subprocess.call(command, shell=True)
        #result = os.popen(command)
        # result.wait()
        # self.LogPrint(str(result))

    # 截屏
    def PullScreenShot(self):
        cmd = 'adb -s ' + self.id + ' shell screencap -p /sdcard/' + ScreenShotFileName
        self.SendCommand(cmd)
        imgPath = path.join(dir_root, 'imgs')
        cmd = 'adb -s ' + self.id + ' pull /sdcard/' + ScreenShotFileName + ' '+imgPath
        self.SendCommand(cmd)


    # 延时，时间单位为秒
    def Sleep(self, t):
        time.sleep(t)

    # wx
    def WX(self):
        cmd = 'adb -s ' + self.id + \
            ' shell am start com.tencent.mm/com.tencent.mm.ui.LauncherUI'
        # cmd = 'adb shell input text ' + str(txt)
        self.SendCommand(cmd)

    # 文字
    def Text(self, txt):
        cmd = 'adb shell am broadcast -a ADB_INPUT_TEXT --es msg ' + str(txt)
        # cmd = 'adb -s ' + self.id + ' shell input text ' + str(txt)
        self.SendCommand(cmd)

    # 单击操作
    def OneClick(self, x, y):
        cmd = 'adb -s ' + self.id + ' shell input tap ' + str(x) + ' ' + str(y)
        self.SendCommand(cmd)

    # 长按
    def LongClick(self, x, y):
        cmd = 'adb -s ' + self.id + ' shell input swipe ' + \
            str(x) + ' ' + str(y) + ' ' + str(x) + ' ' + str(y) + ' 3000'
        # print(cmd)
        self.SendCommand(cmd)

    # 双击操作
    def DoubleClock(self, x, y):
        pass

    # 返回按钮
    def ClickReturn(self):
        cmd = 'adb -s ' + self.id + ' shell input keyevent 4'
        self.SendCommand(cmd)

     # 滑动操作
    def Rolling(self, x1, y1, x2, y2):
        cmd = 'adb -s ' + self.id + ' shell input swipe ' + \
            str(x1) + ' ' + str(y1) + ' ' + str(x2) + ' ' + str(y2) + ' 500'
        self.SendCommand(cmd)

    # 上滑一半
    def RollingUpLittle(self):
        self.Rolling(int(self.width/2), int(self.height*3/4),
                     int(self.width/2), int(self.height*1/4))

    # 上滑屏幕
    def RollingUpScreen(self, step):
        self.Rolling(int(self.width/2), int(self.height/2),
                     int(self.width/2), int(self.height/2) - step)

    # 下滑屏幕
    def RollingDownScreen(self, step):
        self.Rolling(int(self.width/2), int(self.height/2),
                     int(self.width/2), int(self.height/2) + step)

    # 获取屏幕尺寸，非常重要
    def GetScreenSize(self):
        self.PullScreenShot()
        imgPath = path.join(dir_root, 'imgs', ScreenShotFileName)
        img = cv2.imread(imgPath, 3)
        self.height, self.width = img.shape[:2]
        print(self.height)
        print(self.width)

    # 点击电源键，点亮屏幕
    def LightScreen(self):
        cmd = 'adb -s ' + self.id + ' shell input keyevent 26'
        self.SendCommand(cmd)

    # 解锁屏幕
    def UnlockScreen(self, phone):
        self.LightScreen()
        self.Sleep(1)
        # 根据phone类型，选择滑动解锁方式
        if phone == 0:  # 上滑
            self.RollingUpScreen(800)

    # 1个条件比对
    def CompareOne(self, cond1):
        # 比对条件
        yes1, max_loc1 = self.MatchImg(cond1)
        # 检查
        if (yes1):
            return True
        else:
            return False

    # 2个条件比对
    def CompareTwo(self, cond1, cond2):
        # 比对条件
        yes1, max_loc1 = self.MatchImg(cond1)
        yes2, max_loc2 = self.MatchImg(cond2)
        # 检查
        if (yes1 and yes2):
            return True
        else:
            return False

    # 3个条件比对
    def CompareThree(self, cond1, cond2, cond3):
        # 比对条件
        yes1, max_loc1 = self.MatchImg(cond1)
        yes2, max_loc2 = self.MatchImg(cond2)
        yes3, max_loc3 = self.MatchImg(cond3)
        # 检查
        if (yes1 and yes2 and yes3):
            return True
        else:
            return False

    def resource_path(self, relative_path):
        """ Get absolute path to resource, works for dev and for PyInstaller """
        try:
            # PyInstaller creates a temp folder and stores path in _MEIPASS
            base_path = sys._MEIPASS
        except Exception:
            base_path = os.path.abspath(".")

        return os.path.join(base_path, relative_path)

    def MatchImg(self, partImgName):
        self.PullScreenShot()
        imgPath = path.join(dir_root, 'imgs', ScreenShotFileName)
        img_rgb = cv2.imread(imgPath, 3)
        # 原始图片
        # img_rgb = img.img_rgb
        img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)
        # cv2.imshow('output', img_gray)
        # cv2.waitKey(0)
        # cv2.destroyAllWindows()
        # 比对模板图片
        temp_url = path.join(dir_root, 'imgs', partImgName)
        print('temp_url', temp_url)
        # print(temp_url)
        template = cv2.imread(temp_url, 0)
        # 获取模板图片尺寸
        w, h = template.shape[::-1]
        # 比对操作
        res = cv2.matchTemplate(img_gray, template, cv2.TM_CCOEFF_NORMED)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
        # 比对结果坐标
        loc = np.where(res >= threshold)
        # min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res) # 找到最大值和最小值
        # print(cv2.minMaxLoc(res))
        # print(loc)

        bottom_loc = None
        # 描绘出外框
        for pt in zip(*loc[::-1]):
            if bottom_loc == None:
                bottom_loc = pt
            elif pt[1] > bottom_loc[1]:
                bottom_loc = pt
            # cv2.rectangle(
            #     img_rgb, pt, (pt[0] + w, pt[1] + h), (7, 249, 151), 2)
        # 保存识别目标后的图
        # cv2.imwrite(ScreenShotDetected, img_rgb)

        if bottom_loc != None:
            bottom_loc = [int(bottom_loc[0]), int(bottom_loc[1])]
            # img.point = bottom_loc
        # 检查比对结果
        for pp in loc:
            # 如果不为空，说明有比对成果的内容
            if len(pp):
                #print ("Yes")
                # print(pp)
                # min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(
                # res)  # 找到最大值和最小值
                #print (max_loc)
                return True, bottom_loc
            else:
                #print ("Empty")
                return False, []
