# import requests
import json

url_base = 'http://134.175.182.112/'
token = '20e5644a83bb4356a9b1da1da0a66cb5'


class Api:

    @classmethod
    def find(cls, name, img, img2='', txt=''):
        url = url_base+'img/find'
        files = {'media': img}
        payload = {'token': token, 'name': name, 'txt': txt, 'img2': img2}
        # r = requests.post(url, data=payload, files=files)
        return cls.doResult(r)

    @classmethod
    def doResult(cls, r):
        if r.status_code == 200:
            # print(r.text)
            r = json.loads(r.text)
            print(r['msg'])

            return r
        else:
            print(str(r.status_code)+' 后台出错了')
            return {'code': -1}
