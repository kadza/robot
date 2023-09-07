#!/usr/bin/env python

import asyncio
from websockets.server import serve

async def echo(websocket):
    async for message in websocket:
        
        match message:
            case "up":
                await websocket.send("up")
                print("up")
            case "down":
                await websocket.send("down")
                print("down")
            case "left":
                await websocket.send("left")
                print("left")
            case "right":
                await websocket.send("right")
                print("right")
            case "stop":
                await websocket.send("stop")
                print("stop")
            case _:
                await websocket.send("unsupported")
                print("unsupported")

async def main():
    async with serve(echo, "0.0.0.0", 8765):
        await asyncio.Future()  # run forever

asyncio.run(main())