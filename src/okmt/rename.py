import os
import sys
from time import sleep

path = "/home/pi/KB_1815/src/public/resources/"
os.system("cp " + path + sys.argv[1] + " " + path + sys.argv[2])
sleep(15)
os.system("cp " + path + "initialize.mp3" + " " + path + "default.mp3")
