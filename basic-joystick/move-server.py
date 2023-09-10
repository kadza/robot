#!/usr/bin/env python

import asyncio
from websockets.server import serve

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

async def main():
    async with serve(echo, "0.0.0.0", 8765):
        await asyncio.Future()  # run forever

asyncio.run(main())