from typing import Protocol
from dataclasses import dataclass
from asyncio import Future
from websockets.server import serve, WebSocketServerProtocol
from pathlib import Path
from ssl import SSLContext, PROTOCOL_TLS_SERVER
from json import loads

# should it be generic?


@dataclass
class Message():
    direction: str
    speed: float


class MessageHandler(Protocol):
    def handleMessage(self, message: Message) -> None:
        pass


class RemoteController(Protocol):
    async def start(self) -> None:
        pass


class WifiRemoteController:
    def __init__(self, messageHandler: MessageHandler, ipAddress: str, port: int) -> None:
        self.messageHandler = messageHandler
        self.ipAddress = ipAddress
        self.port = port

    async def start(self):
        async def websocketHandler(websocket: WebSocketServerProtocol):
            async for message in websocket:
                messageJson = loads(message)
                direction = messageJson["direction"]
                speed = float(messageJson["speed"])
                self.messageHandler.handleMessage(
                    message=Message(direction, speed))

        async with serve(websocketHandler, self.ipAddress, self.port):
            await Future()
