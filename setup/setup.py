from enum import Enum

from RPi import GPIO
from ads1115.ads1115_init import ADS1115Init
from notification.alarm_subject import AlarmSubject
from sensors.hc_sr501 import HCSR501
from sensors.light_sensor import LightSensor
from sensors.sensor import SensorType
from sensors.sensors_manager import SensorsManager
from sensors.tdc310_thermistor import TDC310Thermistor
from time import sleep
import adafruit_ads1x15.ads1115 as adafruit_ads1115


class SetupState(Enum):
    CALIBRATION_NO_LIGHT = 0
    BUTTON_RELEASE = 1
    CALIBRATION_MAX_LIGHT = 2


class Setup:
    LIGHT_SENSOR_PIN = 14
    BUTTON_PIN = 15
    LED_CALIBRATION_NO_LIGHT_PIN = 21
    LED_CALIBRATION_MAX_LIGHT_PIN = 20
    DELAY_BUTTON_BOUNCE = 0.020

    def __init__(self):
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BCM)
        #self.ads1115 = ADS1115Init(1)
        self.alarm_subject = AlarmSubject()
        #self.light_sensor = LightSensor(adafruit_ads1115.P1, self.ads1115.ads, self.alarm_subject, True)
        #self.tdc310 = TDC310Thermistor(adafruit_ads1115.P0, self.ads1115.ads, self.alarm_subject, True)

        self.hcsr501 = HCSR501(14, SensorType.PASSIVE_INFRARED, self.alarm_subject, False, True)
        self.sensors_manager = SensorsManager([self.hcsr501])
       # self.hcsr501.start()
        #self.light_sensor.start()
        #self.tdc310.start()

    def light_sensor_calibration(self):
        state = SetupState.CALIBRATION_NO_LIGHT
        GPIO.setup(self.BUTTON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.setup(self.LED_CALIBRATION_NO_LIGHT_PIN, GPIO.OUT, initial=GPIO.LOW)
        GPIO.setup(self.LED_CALIBRATION_MAX_LIGHT_PIN, GPIO.OUT, initial=GPIO.LOW)
        while True:
            button_value = GPIO.input(self.BUTTON_PIN)
            if button_value == GPIO.LOW and state == SetupState.CALIBRATION_NO_LIGHT:
                self.light_sensor.calibrate_min()
                GPIO.output(self.LED_CALIBRATION_NO_LIGHT_PIN, GPIO.HIGH)
                state = SetupState.BUTTON_RELEASE
            elif button_value == GPIO.HIGH and state == SetupState.BUTTON_RELEASE:
                state = SetupState.CALIBRATION_MAX_LIGHT
            elif button_value == GPIO.LOW and state == SetupState.CALIBRATION_MAX_LIGHT:
                self.light_sensor.calibrate_max()
                GPIO.output(self.LED_CALIBRATION_MAX_LIGHT_PIN, GPIO.HIGH)
                break
            sleep(self.DELAY_BUTTON_BOUNCE)
        self.light_sensor.check_calibration()