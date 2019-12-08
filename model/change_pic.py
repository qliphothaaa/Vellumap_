import base64
import os
import sys

def imageToStr(imagefile):
    with open(imagefile, 'rb') as f:
        image_byte = base64.b64encode(f.read())
    image_str = image_byte.decode('ascii')
    return image_str


def strToImage(imgstr, filename):
    image_str = imgstr.encode('ascii')
    image_byte = base64.b64decode(image_str)
    image_file = open('./pic/temp/'+filename, 'wb')
    image_file.write(image_byte)
    image_file.close()
    return './pic/temp/'+filename

if __name__ == "__main__":
    picstr = imageToStr('../pic/full.jpg')
    strToImage(picstr, 'new.jpg')
    

