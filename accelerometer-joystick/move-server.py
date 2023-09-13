#!/usr/bin/env python

import asyncio
from websockets.server import serve
import json
import ssl
import pathlib
import gpiozero

robot = gpiozero.Robot(left=(17,18), right=(27,22))

ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
localhost_pem = pathlib.Path(__file__).with_name("cert.pem")
ssl_context.load_cert_chain(localhost_pem)

async def echo(websocket):
    async for message in websocket:
        messageJson = json.loads(message)
        print(messageJson)
        direction = messageJson["direction"]
        value = float(messageJson["value"])
        if direction == "up":
            robot.forward(value)
        elif direction == "down":
            robot.backward(value)
        elif direction == "left":
            robot.left(value)
        elif direction == "right":
            robot.right(value)
        elif direction == "stop":
            robot.stop()

async def main():
    async with serve(echo, "192.168.0.213", 8765, ssl=ssl_context):
        await asyncio.Future()

asyncio.run(main())