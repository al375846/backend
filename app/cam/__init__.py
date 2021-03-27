import requests
from cv2 import *
from datetime import datetime

namedWindow("webcam")
vc = VideoCapture(0)
frame_period = 100
"""
url = 'http://127.0.0.1:8000/images/'
"""
url = 'https://syskaoh.herokuapp.com/images'

while True:
    for i in range(frame_period):
        frame = vc.read()[1]
    img_name = str(datetime.now().time()) + '.jpg'
    imshow("Device0", frame)
    img = imencode(".jpg", frame)[1]
    file = {'file': (img_name, img.tobytes(), 'image/jpeg', {'Expires': '0'})}
    r = requests.post(url, files=file)
    if waitKey(50) >= 0:
        break
