#!/usr/bin/env python

import asyncio
from websockets.server import serve
import json

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
    async with serve(echo, "0.0.0.0", 8765):
        await asyncio.Future()  # run forever

asyncio.run(main())