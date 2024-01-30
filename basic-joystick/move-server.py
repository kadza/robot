#!/usr/bin/env python

import asyncio
from dotenv import load_dotenv
import os
from websockets.server import serve

load_dotenv()


async def echo(websocket):
    async for message in websocket:
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
        else:
            await websocket.send(message)


async def main():
    async with serve(echo, os.environ['SOCKET_SERVER_ADDRESS'], int(os.environ['SOCKET_SERVER_PORT'])):
        await asyncio.Future()  # run forever

asyncio.run(main())
