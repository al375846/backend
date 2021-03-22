import requests


def upload_image(img: str):
    file = {'file': open('../local/' + img, 'rb')}
    """url = 'https://syskaoh.herokuapp.com/images'"""
    url = 'http://127.0.0.1:8000/images'
    r = requests.post(url, files=file)
    print(r.text)


upload_image('index.jpeg')

