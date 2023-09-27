from typing import Protocol
from dataclasses import dataclass
from asyncio import Future
from websockets.server import serve
from pathlib import Path
from ssl import SSLContext, PROTOCOL_TLS_SERVER
from json import loads


@dataclass
class Message():
    direction: str
    speed: int


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
        self.ssl_context = SSLContext(PROTOCOL_TLS_SERVER)
        localhost_pem = Path(__file__).with_name("cert.pem")
        self.ssl_context.load_cert_chain(localhost_pem)

    async def start(self):
        async def echo(websocket):
            async for message in websocket:
                messageJson = loads(message)
                direction = messageJson["direction"]
                speed = int(messageJson["speed"])
                self.messageHandler.handleMessage(
                    message=Message(direction, speed))

        async with serve(echo, self.ipAddress, self.port, ssl=self.ssl_context):
            await Future()
