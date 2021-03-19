import qrcode
import bson
import qrcode.image.svg

if __name__ == '__main__':
    img = qrcode.make(str(bson.ObjectId()))
    with open("imagen.png", "wb") as f:
        img.save(f)
