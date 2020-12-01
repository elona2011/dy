import cv2
# import numpy as np
from AndroidBase import AndroidBase
import time
from random import randrange
import json
from Api import Api


class Screen():
    def __init__(self, id):
        self.img = '/tmp/Tmp01.png'
        self.img_rgb = cv2.imread(self.img)
        self.img2 = cv2.imread(self.img)
        self.AndroidBase = AndroidBase(id)
        self.width = self.AndroidBase.width
        self.height = self.AndroidBase.height
        self.threshold = 0.7
        self.point = [0, 0]

    def clickTalking(self):
        self.AndroidBase.OneClick(200, self.height-100)
        time.sleep(3)

    def sendChinese(self, txt):
        for n in txt:
            self.AndroidBase.Text(n)

    def clickTalkingSend(self):
        self.AndroidBase.OneClick(self.width-60, self.height-135)
        time.sleep(3)

    def findYiGuanZu(self):
        r, loc = self.AndroidBase.MatchImg('yiguanzu.png')
        print(r)
        print(loc)
        if r:
            self.point = [loc[0], loc[1]]
        return r

    def findSiXing(self):
        r, loc = self.AndroidBase.MatchImg('sixing.png')
        print(r)
        print(loc)
        if r:
            self.point = [loc[0], loc[1]]
        return r

    def clickSiXingSend(self):
        r, loc = self.AndroidBase.MatchImg('send.png')
        print(r)
        print(loc)
        if r:
            self.point = [loc[0], loc[1]]
            self.click()

    def followHost(self):
        r, loc = self.AndroidBase.MatchImg('followHost.png')
        print(r)
        print(loc)
        if r:
            self.point = [loc[0], loc[1]]
            self.click()

    def clickFanNum(self):
        self.AndroidBase.OneClick(self.width-180, 190)
        time.sleep(2)

    def followFan(self):
        r, loc = self.AndroidBase.MatchImg('followFan.png')
        print(r)
        print(loc)
        if r:
            self.point = [loc[0], loc[1]]
            self.click()

    def thumbComment(self):
        comments = ('6666'
                    )
        self.AndroidBase.Text(comments[randrange(len(comments))])

    def findText(self, name):
        img = self.getImg()
        r = Api.find('findText', img=img, txt=name)
        if r['code'] == 0:
            self.point = [r['result'][0], r['result'][1]]
            return True
        return False

    def findFirstImg(self):
        img = self.getImg()
        img = self.cropImg(85, 600, 320, self.height)
        r = Api.find('findFirstImg', img=img)
        if r['code'] == 0:
            self.point = [r['result'][0]+85, r['result'][1]+600]
            return True
        return False

    def findFavoriteSend(self):
        img = self.getImg()
        img = self.cropImg(500, 500, 1080, self.height)
        r = Api.find('findFavoriteSend', img=img)
        if r['code'] == 0:
            self.point = [r['result'][0]+500, r['result'][1]+500]
            return True
        return False

    def findThumbIcon(self):
        img = self.getImg()
        img = self.cropImg(700, 0, 1080, self.height)
        r = Api.find('findThumbIcon', img=img)
        if r['code'] == 0:
            self.point = [r['result'][0]+700, r['result'][1]]
            return True
        return False

    def findReplyButton(self):
        img = self.getImg()
        img = self.cropImg(870, 0, 1080, self.height)
        r = Api.find('findReplyButton', img)
        if r['code'] == 0:
            self.point = [r['result'][0]+870, r['result'][1]]
            return True
        return False

    def findPlusButton(self):
        img = self.getImg()
        img = self.cropImg(960, 0, 1080, self.height)
        r = Api.find('findPlusButton', img)
        if r['code'] == 0:
            self.point = [r['result'][0]+960, r['result'][1]]
            return True
        return False

    def findSendButton(self):
        img = self.getImg()
        img = self.cropImg(880, 0, 1080, self.height)
        r = Api.find('findSendButton', img)
        if r['code'] == 0:
            self.point = [r['result'][0]+880, r['result'][1]]
            return True
        return False

    def findFavoriteButton(self):
        img = self.getImg()
        h = self.height-800
        img = self.cropImg(0, h, 1080, self.height)
        r = Api.find('findFavoriteButton', img)
        if r['code'] == 0:
            self.point = [r['result'][0], r['result'][1]+h]
            return True
        return False

    def findCommentIcon(self):
        img = self.getImg()
        img = self.cropImg(870, 0, 1080, self.height)
        r = Api.find('findCommentIcon', img)
        if r['code'] == 0:
            self.point = [r['result'][0]+870, r['result'][1]]
            return True
        return False

    def findVideoBlock(self):
        img = self.getImg()
        img = self.cropImg(0, 0, 380, self.height)
        r = Api.find('findVideoBlock', img)
        if r['code'] == 4:
            loc = r['result']
            self.AndroidBase.Rolling(
                loc[0], loc[1], loc[0], self.AndroidBase.height*5/6)
            img = self.getImg()
            r = Api.find('findVideoBlock', img)

        if r['code'] == 0:
            self.point = r['result'][:2]
            self.userIcon = r['result'][2]
            return True
        return False

    def matchUserIcon(self):
        img = self.getImg()
        img = self.cropImg(0, 0, 160, self.height)
        r = Api.find('findUserIcon', img=img, img2=self.userIcon)
        if r['code'] == 4:
            loc = r['result']
            self.AndroidBase.Rolling(
                loc[0], loc[1], loc[0], self.AndroidBase.height*6/7)
            img = self.getImg()
            r = Api.find('findUserIcon', img=img, img2=self.userIcon)
        if r['code'] == 4:
            loc = r['result']
            self.AndroidBase.Rolling(
                loc[0], loc[1], loc[0], self.AndroidBase.height*6/7)
            img = self.getImg()
            r = Api.find('findUserIcon', img=img, img2=self.userIcon)
        if r['code'] == 4:
            loc = r['result']
            self.AndroidBase.Rolling(
                loc[0], loc[1], loc[0], self.AndroidBase.height*6/7)
            img = self.getImg()
            r = Api.find('findUserIcon', img=img, img2=self.userIcon)
        if r['code'] == 0:
            self.point = r['result'][:2]
            return True
        return False

    def findActiveGroup(self):
        img = self.getImg()
        img = self.cropImg(0, 0, 200, self.height)
        r = Api.find('findActiveGroup', img)
        if r['code'] == 3:
            self.return1()
            return False

        if r['code'] == 0:
            self.point = r['result']
            return True
        return False

    def return1(self):
        self.AndroidBase.ClickReturn()
        time.sleep(4)

    def return2(self):
        self.AndroidBase.ClickReturn()
        time.sleep(4)
        self.AndroidBase.ClickReturn()
        time.sleep(4)

    def return3(self):
        self.AndroidBase.ClickReturn()
        time.sleep(3.5)
        self.AndroidBase.ClickReturn()
        time.sleep(4)
        self.AndroidBase.ClickReturn()
        time.sleep(4)

    def return4(self):
        self.AndroidBase.ClickReturn()
        time.sleep(4)
        self.AndroidBase.ClickReturn()
        time.sleep(3.7)
        self.AndroidBase.ClickReturn()
        time.sleep(3.1)
        self.AndroidBase.ClickReturn()
        time.sleep(4)

    def click(self, x=None, y=None):
        if x == None:
            x = self.point[0]
        if y == None:
            y = self.point[1]
        self.AndroidBase.OneClick(x+8, y+8)
        # cv2.rectangle(self.img2, (self.point[0], self.point[1]),
        #               (self.point[0] + 20, self.point[1] + 20), (7, 249, 151), 2)
        # cv2.imwrite("Tmp02.png", self.img2)
        time.sleep(2)

    def clickLong(self):
        print('long', self.point)
        self.AndroidBase.LongClick(self.point[0]+28, self.point[1]+28)

    def getImg(self):
        self.AndroidBase.PullScreenShot()
        self.img_rgb = cv2.imread(self.img)
        self.img2 = cv2.imread(self.img)
        with open(self.img, 'rb') as f:
            img = f.read()
        return img

    def addRect(self, loc, path):
        template = cv2.imread(path, 0)
        w, h = template.shape[::-1]
        cv2.rectangle(
            self.img_rgb, loc, (loc[0] + w, loc[1] + h), (7, 249, 151), 2)
        self.showImg(self.img_rgb)

    def showImg(self, img):
        cv2.namedWindow("output", cv2.WINDOW_NORMAL)
        cv2.imshow('output', img)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    def cropImg(self, x0, y0, x1, y1):
        crop_img = self.img_rgb[y0:y1, x0:x1]
        res, im_png = cv2.imencode('.png', crop_img)
        return im_png.tobytes()
