from contextlib import nullcontext
import cv2
import requests
import shutil
from PIL import Image, ImageChops

from requests.api import request


url='http://192.168.14.40/cam-hi.jpg'

r = requests.get(url, stream = True)

with open("imsc.jpg",'wb') as f:
    shutil.copyfileobj(r.raw, f)


def CalcImageHash(FileName):
    image = cv2.imread(FileName)
    resized = cv2.resize(image, (8,8), interpolation = cv2.INTER_AREA)
    gray_image = cv2.cvtColor(resized, cv2.COLOR_BGR2GRAY)
    avg=gray_image.mean()
    ret, threshold_image = cv2.threshold(gray_image, avg, 255, 0)
    
    _hash=""
    for x in range(8):
        for y in range(8):
            val=threshold_image[x,y]
            if val==255:
                _hash=_hash+"1"
            else:
                _hash=_hash+"0"
            
    return _hash

def CompareHash(hash1,hash2):
    l=len(hash1)
    i=0
    count=0
    while i<l:
        if hash1[i]!=hash2[i]:
            count=count+1
        i=i+1
    return count
        

hash1=CalcImageHash('im.jpg')
hash2=CalcImageHash('imcs.jpg')
print(hash1)
print(hash2)
print(CompareHash(hash1, hash2))


im1 = Image.open("im.jpg")
im2 = Image.open("imcs.jpg")

diff = ImageChops.difference(im1, im2)

diff.save("dif.jpg")



print(diff.getbbox())
