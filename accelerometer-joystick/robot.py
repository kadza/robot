from typing import Protocol
import gpiozero #type: ignore
import time

class Robot(Protocol):
    def get_distance(self) -> float:
        #is it the bes option
        return 0

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
        #it's float not int according to docs https://gpiozero.readthedocs.io/en/stable/api_boards.html?highlight=robot#robot
        self.robot.forward(speed)  # type: ignore

    def backward(self, speed: float) -> None:
        self.robot.backward(speed)  # type: ignore

    def left(self, speed: float) -> None:
        self.robot.left(speed)  # type: ignore

    def right(self, speed: float) -> None:
        self.robot.right(speed)  # type: ignore

    def stop(self) -> None:
        self.robot.stop()


class PiRobotWithSteeringMotor:
    steeringMotorPosition = 0

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
        self.leftMotor = gpiozero.Motor(leftMotorPinNumbers[0], leftMotorPinNumbers[1])
        self.rightMotor = gpiozero.Motor(rightMotorPinNumbers[0], rightMotorPinNumbers[1])

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
        #it's float not int according to docs https://gpiozero.readthedocs.io/en/stable/api_boards.html?highlight=robot#robot
        self.rightMotor.forward(speed)  # type: ignore

    def backward(self, speed: float) -> None:
        self.rightMotor.backward(speed)  # type: ignore

    def left(self, speed: float) -> None:
        if self.steeringMotorPosition < 2:
            self.leftMotor.forward(speed)  # type: ignore
            self.steeringMotorPosition = self.steeringMotorPosition + 1

    def right(self, speed: float) -> None:
        if self.steeringMotorPosition > -2
            self.leftMotor.backward(speed)  # type: ignore
            self.steeringMotorPosition = self.steeringMotorPosition - 1

    def stop(self) -> None:
        self.rightMotor.stop()
        self.leftMotor.stop()
