#!/usr/bin/env python

import asyncio
from websockets.server import serve
import json
import ssl
import pathlib
import gpiozero
import time

min_distance = 20
robot = gpiozero.Robot(left=(17, 18), right=(27, 22))
trigger = gpiozero.OutputDevice(23)
echo = gpiozero.DigitalInputDevice(24)
ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
localhost_pem = pathlib.Path(__file__).with_name("cert.pem")
ssl_context.load_cert_chain(localhost_pem)
global direction
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


def prevent_crash():
    global direction
    global distance
    distance = get_Distance(trigger, echo)
    print(distance)
    if distance <= min_distance and direction == "up" :
        robot.stop()

    time.sleep(1000)

async def echo(websocket):
    async for message in websocket:
        messageJson = json.loads(message)
        print(messageJson)
        global direction
        direction = messageJson["direction"]
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

async def main():
    task1 = asyncio.create_task(start_server())

    await task1

    while True:
        prevent_crash()

asyncio.run(main())
