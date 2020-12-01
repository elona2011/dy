from AndroidBase import AndroidBase
from Screen import Screen
import subprocess
import time
from random import uniform

cmd = 'adb devices'
pi = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
r = pi.stdout.read().decode('utf-8').split('\n')
r = r[1:-2]
rr = []
for n in r:
    rr.append(n.split('\t')[0])
print(rr)


class Task():
    def __init__(self, id):
        self.screen = Screen(id)
        self.android = self.screen.AndroidBase
        self.width = self.android.width

    def chat(self):
        self.screen.clickTalking()
        self.screen.sendChinese(
            '求关注，必回关！求关注，必回关！求关注，必回关！')
        self.screen.clickTalkingSend()

    def checkNoFollow(self):
        rr = self.screen.findYiGuanZu()
        if rr:
            self.screen.click(200)
            rr = self.screen.findSiXing()
            if rr:
                self.screen.click()
                self.screen.clickTalking()
                self.screen.sendChinese(
                    '宝宝，我关注你了，你也要关注我一下哦')
                self.screen.clickSiXingSend()
                self.android.ClickReturn()

    def followHost(self):
        self.screen.followHost()

    def followFans(self):
        self.screen.clickFanNum()
        m = round(uniform(1.0, 4.0), 1)
        time.sleep(m)
        self.screen.followFan()
        self.screen.followFan()
        self.screen.followFan()
        self.screen.followFan()
        self.screen.followFan()
        self.android.ClickReturn()
        m = round(uniform(3.0, 10.0), 1)
        time.sleep(m)
        self.android.RollingUpLittle()

    def screenShot(self):
        self.android.PullScreenShot()

    def doubleClick(self):
        self.android.OneClick(200, 800)
        self.android.OneClick(200, 800)

for id in rr:
    task = Task(id)
    while True:
        # task.followHost()
        # m = round(uniform(2.0, 10.0), 1)
        # time.sleep(m)
        # task.chat()
        task.doubleClick()
        # task.checkNoFollow()
        # task.followFans()
        # task.screenShot()
        m = round(uniform(1.0, 5.0), 1)
        time.sleep(m)
