#!/usr/bin/env python

import asyncio
from websockets.server import serve
import json
import ssl
import pathlib
import gpiozero
import time

min_distance = 30
robot = gpiozero.Robot(left=(17, 18), right=(27, 22))
triggerPin = gpiozero.OutputDevice(23)
echoPin = gpiozero.DigitalInputDevice(24)
ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
localhost_pem = pathlib.Path(__file__).with_name("cert.pem")
ssl_context.load_cert_chain(localhost_pem)
global direction
direction = "start"
global distance
distance = 100

def get_Distance(trigger, echo):
    trigger.on()
    time.sleep(0.00001)
    trigger.off()

    while echo.is_active == False:
        pulse_start = time.time()

    while echo.is_active == True:
        pulse_end = time.time()

    pulse_duration = pulse_end - pulse_start

    distance = 34300 * (pulse_duration/2)

    round_distance = round(distance, 2)

    return (round_distance)


async def prevent_crash():
    while True:
        global direction
        global distance
        distance = get_Distance(triggerPin, echoPin)
        print("prevent_crash distance: " + str(distance))
        print("prevent_crash direction: " + str(direction))
        if distance <= min_distance and direction == "left":
            print("stopped")
            robot.stop()

        await asyncio.sleep(1)

async def echo(websocket):
    async for message in websocket:
        messageJson = json.loads(message)
        global direction
        direction = messageJson["direction"]
        print("echo message: " + str(messageJson))
        print("echo direction: " + str(direction))
        value = float(messageJson["value"])
        if direction == "up":
            global distance
            if distance > min_distance:
                robot.forward(value)
        elif direction == "down":
            robot.backward(value)
        elif direction == "left":
            robot.left(value)
        elif direction == "right":
            robot.right(value)
        elif direction == "stop":
            robot.stop()

async def start_server():
    async with serve(echo, "192.168.0.213", 8765, ssl=ssl_context):
        await asyncio.Future()
        
async def test():
    i = 0
    while True:
        print(i)
        i = i + 1
        await asyncio.sleep(1)

async def main():
    prevent_crash_task = asyncio.create_task(prevent_crash())
    websocket_server_task = asyncio.create_task(start_server())

    await prevent_crash_task
    await websocket_server_task

asyncio.run(main())

