#!/usr/bin/python3

import time, smtplib
import RPi.GPIO as GPIO
from datetime import datetime
from pololu_drv8835_rpi import motors

from local_config import EMAIL, PASSWORD

# setup GPIO switch
GPIO.setmode(GPIO.BCM)
GPIO.setup(21, GPIO.IN, pull_up_down=GPIO.PUD_UP) # or try 16


def run_up(seconds, speed):
    print('running up for %s seconds' % seconds)
    motors.motor2.setSpeed(speed)
    time.sleep(seconds)
    motors.motor2.setSpeed(0)
    print('up completed')

def run_down(speed):
    print('run down to switch')
    speed = -speed # change motor direction
    while True:
        input_state = GPIO.input(21)
        motors.motor2.setSpeed(speed)
        if input_state == False:
            print('switch pressed')
            motors.motor2.setSpeed(0)
            break

def send_email(now, status, subject = 'From the Chickens'):
    addr = EMAIL
    server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
    server.login(addr, PASSWORD)

    msg = "door ran %s; status: %s " % (now, status)

    BODY = '\r\n'.join(['To: %s' % addr,
                    'From: %s' % addr,
                    'Subject: %s' % subject,
                    '', msg])

    server.sendmail(addr, addr, BODY)
    server.quit()
