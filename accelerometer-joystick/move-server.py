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
        if message == "up":
            await websocket.send("up")
        elif message == "down":
            await websocket.send("down")
        elif message == "left":
            await websocket.send("left")
        elif message == "right":
            await websocket.send("right")
        elif message == "stop":
            await websocket.send("stop")

async def main():
    async with serve(echo, "192.168.0.213", 8765, ssl=ssl_context):
        await asyncio.Future()

asyncio.run(main())