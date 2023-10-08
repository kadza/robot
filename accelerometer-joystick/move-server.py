from remote_controller import Message, WifiRemoteController
from robot import Robot, PiRobot
from asyncio import create_task, sleep, run

global direction
global distance

direction = "start"
min_distance = 30
distance = 100


async def prevent_crash(robot: Robot):
    while True:
        global direction
        global distance
        distance = robot.get_distance()
        print("prevent_crash distance: " + str(distance))
        print("prevent_crash direction: " + str(direction))
        if distance <= min_distance and direction == "up":
            print("stopped")
            robot.stop()

        await sleep(1)


class DirectionMessageHandler:
    def __init__(self, robot: Robot):
        self.robot = robot

    def handleMessage(self, message: Message):
        direction = message.direction
        speed = message.speed
        if direction == "up":
            global distance
            if distance > min_distance:
                self.robot.forward(speed)
        elif direction == "down":
            self.robot.backward(speed)
        elif direction == "left":
            self.robot.left(speed)
        elif direction == "right":
            self.robot.right(speed)
        elif direction == "stop":
            self.robot.stop()


async def main():
    robot = PiRobot(23, 24, (17, 18), (27, 22))
    remoteController = WifiRemoteController(
        messageHandler = DirectionMessageHandler(robot=robot), ipAddress="192.168.0.213", port=8765)

    prevent_crash_task = create_task(prevent_crash(robot=robot))
    websocket_server_task = create_task(remoteController.start())

    await prevent_crash_task
    await websocket_server_task

run(main())
