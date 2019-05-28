#! /usr/bin/env python
import logging
import datetime
import time
import numpy as np
import picamera
import Adafruit_DHT
import RPi.GPIO as GPIO
import picamera.array


__author__ = 'cstolz@cisco.com'
__copyright__ = 'Copyright (c) 2017 Cisco Systems. All rights reserved.'

__images__ = 'images/'

logging.basicConfig(filename='log/create_lab_image.log', level=logging.INFO)

DEBUG = 1
GPIO.setmode(GPIO.BCM)

#start a webeserver from images directory via shell
#python3 -m http.server 8080 > /dev/null 2>&1 &


def capture_still_high_light(annotation):
    with picamera.PiCamera() as camera:
        camera.rotation = 180
        camera.resolution = (1280, 720)
        camera.framerate = 24
        camera.annotate_text = annotation
        time.sleep(2)
        camera.capture(__images__+'high-light-{}.jpg'.format(
        	   datetime.datetime.now()))
        camera.close()


def capture_still_low_light(annotation):
    with picamera.PiCamera() as camera:
        camera.rotation = 180
        camera.resolution = (1280, 720)
        camera.framerate = 1
        camera.shutter_speed = 6000000
        camera.iso = 800
        camera.annotate_text = annotation
        time.sleep(30)
        camera.exposure_mode = 'off'
        camera.capture(__images__+'low-light-{}.jpg'.format(
        	   datetime.datetime.now()))
        camera.close()


def light_meter():
    with picamera.PiCamera() as camera:
        camera.resolution = (100, 75)
        with picamera.array.PiRGBArray(camera) as stream:
            camera.exposure_mode = 'auto'
            camera.awb_mode = 'auto'
            camera.capture(stream, format='rgb')
            pix_avg = int(np.average(stream.array[..., 1]))
    return pix_avg


def rc_time(rc_pin):
    reading = 0
    GPIO.setup(rc_pin, GPIO.OUT)
    GPIO.output(rc_pin, GPIO.LOW)
    time.sleep(0.1)
    GPIO.setup(rc_pin, GPIO.IN)
    while GPIO.input(rc_pin) == GPIO.LOW:
        reading += 1
    return reading


if __name__ == '__main__':
    while True:
        try:
            TIME_STAMP = str(datetime.datetime.now())
            HUMIDITY, TEMP = Adafruit_DHT.read_retry(11, 4)
            LAB_TEMP = '{} Temperature: {} Humidity: {}'.format(
                TIME_STAMP, HUMIDITY, TEMP)
            if light_meter() > 3:
                capture_still_high_light(LAB_TEMP)
            else:
                capture_still_low_light(LAB_TEMP)
            logging.info('[%s] Lab Image Taken', TIME_STAMP)
        except Exception as err:
            logging.error('[%s] Lab Image Failed %s', TIME_STAMP, err)
    time.sleep(43200)
