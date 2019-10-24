#settings
import time
import picamera

import os
#import subprocess

from twython import Twython
from auth import (
    consumer_key,
    consumer_secret,
    access_token,
    access_token_secret
)

#camera
with picamera.PiCamera() as camera:
 camera.resolution = (1024, 768)
 camera.start_preview()
 # Camera warm-up time
 time.sleep(1)
 camera.capture('my_picture.jpg')
 
twitter = Twython(
    consumer_key,
    consumer_secret,
    access_token,
    access_token_secret
)

#CPU remperature
#temp = subprocess.getoutput("vcgencmd measure_temp").split('=')
cmd = '/opt/vc/bin/vcgencmd measure_temp'
line = os.popen(cmd).readline().strip()
temp = line.split('=')[1].split("'")[0]

#message = "Hello world - here's a picture!" 
photo = open('my_picture.jpg','rb')
response = twitter.upload_media(media=photo)
twitter.update_status(status=temp,  media_ids=[response['media_id']])
 
print("Tweeted: %s" % temp)

