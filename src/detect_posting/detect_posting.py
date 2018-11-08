import RPi.GPIO as GPIO
import time


PIRPinIn = 17
PIRPinOut = 16


def setup() -> None:
    GPIO.setwarnings(False)
    #set the gpio modes to BCM numbering
    GPIO.setmode(GPIO.BCM)
    #set BuzzerPin's mode to output,and initial level to HIGH(3.3V)
    #GPIO.setup(BuzzerPin,GPIO.OUT,initial=GPIO.HIGH)
    GPIO.setup(PIRPinIn,GPIO.IN)
    GPIO.setup(PIRPinOut,GPIO.IN)


def main():
    while True:
        #read Sw520dPin's level
        if(GPIO.input(PIRPinIn) != 0):
            print('Hello Sensor!!!')
            time.sleep(1)
        else:
            print ('No detect')
        time.sleep(1)


if __name__ == '__main__':
    main()