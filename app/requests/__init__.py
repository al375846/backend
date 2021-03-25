import requests
from cv2 import *


class ReqManager(object):
    def __init__(self):
        pass

    def upload_image(self, img: str):
        file = {'file': open('../local/' + img, 'rb')}
        """url = 'https://syskaoh.herokuapp.com/images'"""
        url = 'http://127.0.0.1:8000/images'
        r = requests.post(url, files=file)
        print(r.text)
1