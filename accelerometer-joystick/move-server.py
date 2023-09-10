#!/usr/bin/env python

import asyncio
from websockets.server import serve
import json
import ssl
import pathlib

ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
localhost_pem = pathlib.Path(__file__).with_name("cert.pem")
ssl_context.load_cert_chain(localhost_pem)

async def echo(websocket):
    async for message in websocket:
        messageJson = json.loads(message)
        print(messageJson)
        direction = messageJson["direction"]
        value = messageJson["value"]
        match direction:
            case "up":
                print("up")
            case "down":
                print("down")
            case "left":
                print("left")
            case "right":
                print("right")
            case "stop":
                print("stop")
            case _:
                await websocket.send("unsupported")
                print("unsupported")

async def main():
    async with serve(echo, "192.168.0.213", 8765, ssl=ssl_context):
        await asyncio.Future()

asyncio.run(main())