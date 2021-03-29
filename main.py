import sys

from sensors.sensor import CalibrationException
from server.server import Server
from setup.setup import Setup

def main():
    args = sys.argv[1:]
    setup = Setup()
    while True:
        try:
            #setup.light_sensor_calibration()
            break
        except CalibrationException:
            pass
    Server("192.168.1.11", int(args[0]), setup.sensors_manager, setup.alarm_subject).listen()

main()