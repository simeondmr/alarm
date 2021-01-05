from time import sleep

import RPi.GPIO as GPIO
from enum import Enum

from ads1115.ads1115_init import ADS1115Init
from notification.alarm_subject import AlarmSubject
from sensors.light_sensor import LightSensor
from sensors.sensor import CalibrationException
from sensors.sensors_manager import SensorsManager
from sensors.tdc310_thermistor import TDC310Thermistor
from server.server import Server
import adafruit_ads1x15.ads1115 as adafruit_ads1115

LIGHT_SENSOR_PIN = 14
BUTTON_PIN = 15
LED_CALIBRATION_NO_LIGHT_PIN = 21
LED_CALIBRATION_MAX_LIGHT_PIN = 20
DELAY_BUTTON_BOUNCE = 0.020


class SetupState(Enum):
    CALIBRATION_NO_LIGHT = 0
    BUTTON_RELEASE = 1
    CALIBRATION_MAX_LIGHT = 2

ads1115 = ADS1115Init(1)
alarm_subject = AlarmSubject()
light_sensor = LightSensor(adafruit_ads1115.P1, ads1115.ads, alarm_subject, True)
tdc310 = TDC310Thermistor(adafruit_ads1115.P0, ads1115.ads, alarm_subject, True)

def sensor_calibration():
    state = SetupState.CALIBRATION_NO_LIGHT
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(BUTTON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(LED_CALIBRATION_NO_LIGHT_PIN, GPIO.OUT, initial=GPIO.LOW)
    GPIO.setup(LED_CALIBRATION_MAX_LIGHT_PIN, GPIO.OUT, initial=GPIO.LOW)
    while True:
        button_value = GPIO.input(BUTTON_PIN)
        if button_value == GPIO.LOW and state == SetupState.CALIBRATION_NO_LIGHT:
            light_sensor.calibrate_min()
            GPIO.output(LED_CALIBRATION_NO_LIGHT_PIN, GPIO.HIGH)
            state = SetupState.BUTTON_RELEASE
        elif button_value == GPIO.HIGH and state == SetupState.BUTTON_RELEASE:
            state = SetupState.CALIBRATION_MAX_LIGHT
        elif button_value == GPIO.LOW and state == SetupState.CALIBRATION_MAX_LIGHT:
            light_sensor.calibrate_max()
            GPIO.output(LED_CALIBRATION_MAX_LIGHT_PIN, GPIO.HIGH)
            break
        sleep(DELAY_BUTTON_BOUNCE)
    light_sensor.check_calibration()


def main():
    light_sensor.start()
    tdc310.start()
    sensors_manager = SensorsManager([light_sensor, tdc310])
    while True:
        try:
            sensor_calibration()
            break
        except CalibrationException:     
            pass
    Server("localhost", 10067, sensors_manager, alarm_subject).listen()


main()