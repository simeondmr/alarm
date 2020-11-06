import RPi.GPIO as GPIO
from enum import Enum
from light_sensor import LightSensor
from server import Server

LIGHT_SENSOR_PIN = 8
BUTTON_PIN = 10
LED_CALIBRATION_NO_lIGHT_PIN = 40
LED_CALIBRATION_MAX_lIGHT_PIN = 38


class SetupState(Enum):
    CALIBRATION_NO_LIGHT = 0
    BUTTON_RELEASE = 1
    CALIBRATION_MAX_LIGHT = 2


light_sensor = LightSensor(LIGHT_SENSOR_PIN)


def calibration_light_sensor():
    state = SetupState.CALIBRATION_NO_LIGHT
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(BUTTON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(LED_CALIBRATION_NO_lIGHT_PIN, GPIO.OUT, initial=GPIO.LOW)
    GPIO.setup(LED_CALIBRATION_MAX_lIGHT_PIN, GPIO.OUT, initial=GPIO.LOW)
    while True:
        button_value = GPIO.input(BUTTON_PIN)
        if button_value == GPIO.LOW and state == SetupState.CALIBRATION_NO_LIGHT:
            light_sensor.calibrate_nolight()
            GPIO.output(LED_CALIBRATION_NO_lIGHT_PIN, GPIO.HIGH)
            state = SetupState.BUTTON_RELEASE
        elif button_value == GPIO.HIGH and state == SetupState.BUTTON_RELEASE:
            state = SetupState.CALIBRATION_MAX_LIGHT
        elif button_value == GPIO.LOW and state == SetupState.CALIBRATION_MAX_LIGHT:
            light_sensor.calibrate_maxlight()
            GPIO.output(LED_CALIBRATION_MAX_lIGHT_PIN, GPIO.HIGH)
            break


def main():
    calibration_light_sensor()
    Server("localhost", 10021).listen()

main()