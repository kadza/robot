from typing import Protocol
import gpiozero
import time

class Robot(Protocol):
    def get_distance(self) -> float:
        pass

    def forward(self, speed: float) -> None:
        pass

    def backward(self, speed: float) -> None:
        pass

    def left(self, speed: float) -> None:   
        pass

    def right(self, speed: float) -> None:
        pass

    def stop(self) -> None:
        pass


class PiRobot:
    def __init__(
        self,
        distanceTriggerPinNumber: int,
        distanceEchoPinNumber: int,
        leftMotorPinNumbers: tuple[int,int],
        rightMotorPinNumbers: tuple[int, int]
    ) -> None:
        self.distanceTriggerPin = gpiozero.OutputDevice(
            distanceTriggerPinNumber)
        self.distanceEchoPin = gpiozero.DigitalInputDevice(
            distanceEchoPinNumber)
        self.robot = gpiozero.Robot(
            left=leftMotorPinNumbers, right=rightMotorPinNumbers)

    def get_distance(self) -> float:
        pulse_start = 0
        pulse_end = 0
        
        self.distanceTriggerPin.on()
        time.sleep(0.00001)
        self.distanceTriggerPin.off()
        
        while self.distanceEchoPin.is_active == False:
            pulse_start = time.time()

        while self.distanceEchoPin.is_active == True:
            pulse_end = time.time()

        pulse_duration = pulse_end - pulse_start
        distance = 34300 * (pulse_duration/2)
        round_distance = round(distance, 2)

        return (round_distance)
    
    def forward(self, speed: float) -> None:
        self.robot.forward(speed)

    def backward(self, speed: float) -> None:
        self.robot.backward(speed)

    def left(self, speed: float) -> None:
        self.robot.left(speed)

    def right(self, speed: float) -> None:
        self.robot.right(speed)

    def stop(self) -> None:
        self.robot.stop()
