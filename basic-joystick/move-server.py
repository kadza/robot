#!/usr/bin/env python

from asyncio import create_task, sleep, run
from remote_controller import Message, WifiRemoteController
from robot import PiRobot, Robot
from dotenv import load_dotenv
import os
from websockets.server import serve


load_dotenv()

global direction
global distance

direction = "start"
min_distance = 50
distance = 100


async def prevent_crash(robot: Robot):
    while True:
        global direction
        global distance
        distance = robot.get_distance()
        print("prevent_crash distance: " + str(distance))
        print("prevent_crash direction: " + str(direction))
        if distance <= min_distance and direction == "left":
            print("stopped")
            robot.stop()

        await sleep(1)


class DirectionMessageHandler:
    def __init__(self, robot: Robot):
        self.robot = robot

    def handleMessage(self, message: Message):
        print(message)
        global direction
        direction = message.direction
        speed = message.speed
        if direction == "N":
            global distance
            if distance > min_distance:
                self.robot.forward(speed)
        elif direction == "S":
            self.robot.backward(speed)
        elif direction == "W":
            self.robot.left(speed)
        elif direction == "E":
            self.robot.right(speed)
        elif direction == "C":
            self.robot.stop()


class PrintMessageHandler:
    def handleMessage(self, message: Message):
        print(message)


async def main():
    robot = PiRobot(23, 24, (17, 18), (27, 22))
    remoteController = WifiRemoteController(
        messageHandler=DirectionMessageHandler(robot), ipAddress=os.environ['SOCKET_SERVER_ADDRESS'], port=int(os.environ['SOCKET_SERVER_PORT']))

    # prevent_crash_task = create_task(prevent_crash(robot))
    websocket_server_task = create_task(remoteController.start())

    # await prevent_crash_task
    await websocket_server_task

run(main())
