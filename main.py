from Screen import Screen
from AndroidBase import AndroidBase
from Task import Task
import time
import subprocess
import threading
import traceback
from pathlib import Path

Path('/tmp').mkdir(parents=True, exist_ok=True)

cmd = 'adb devices'
pi = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
r = pi.stdout.read().decode('utf-8').split('\n')
r = r[1:-2]
rr = []
for n in r:
    rr.append(n.split('\t')[0])
print(rr)
print('使用方法：')
print('1 开启手机debug模式')
print('2 关闭屏幕上方经常弹出的消息通知')
print('3 usb线连接手机')
print('4 双击exe文件')


class myThread (threading.Thread):
    def __init__(self, id):
        threading.Thread.__init__(self)
        self.id = id

    def run(self):
        print("Starting " + self.id)
        newtask(self.id)


def newtask(id):
    task = Task(id)

    if task.width != 1080:
        print('分辨率'+str(task.width)+'，不支持，联系代理')
    else:
        while True:
            try:
                task.thumb()
                time.sleep(5)
            except KeyboardInterrupt:
                print(11)
                raise
            except Exception as e:
                print('出异常了，重启中。。。')
                print(e)
                traceback.print_exc()
                time.sleep(5)
                task.android.ClickReturn()
                time.sleep(5)
                task.android.ClickReturn()
                time.sleep(5)
                task.android.ClickReturn()
                time.sleep(5)
                task.android.ClickReturn()
                time.sleep(5)
                task.android.ClickReturn()
                time.sleep(5)
                task.android.WX()
                time.sleep(10)


for n in rr:
    try:
        thread = myThread(n)
        thread.daemon = True
        thread.start()
        while True:
            time.sleep(100)
    except KeyboardInterrupt:
        print(11)
        raise
    except Exception as e:
        print(e)
        traceback.print_exc()
