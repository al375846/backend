import requests
from cv2 import *
from datetime import datetime

namedWindow("webcam")
vc = VideoCapture(0)
frame_period = 100
url = 'http://127.0.0.1:8000/images/'
"""url = 'https://syskaoh.herokuapp.com/images'"""
img_name = str(datetime.now().time()) + '.jpg'

while True:
    for i in range(frame_period):
        next_vc, frame = vc.read()
    imshow("Device0", frame)
    imwrite(img_name, frame)
    file = {'file': open('./' + img_name, 'rb')}
    r = requests.post(url, files=file)
    if waitKey(50) >= 0:
        break



