from sensors.sensor import CalibrationException
from server.server import Server
from setup.setup import Setup

def main():
    setup = Setup()
    while True:
        try:
            setup.light_sensor_calibration()
            break
        except CalibrationException:
            pass
    Server("localhost", 10085, setup.sensors_manager, setup.alarm_subject).listen()

main()