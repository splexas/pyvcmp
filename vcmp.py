import asyncio
import logging


logger = logging.getLogger("vcmp")


class ListenerProtocol(asyncio.Protocol):
    def connection_made(self, transport):
        peername = transport.get_extra_info("peername")
        logger.info(f"Listener: got connection from {peername}")
        self.transport = transport

    def data_received(self, data):
        message = data.decode()
        logger.info(f"Listener: Data received: {message}")
        self.transport.close()


class WSAPIProtocol(asyncio.Protocol):
    def connection_made(self, transport):
        peername = transport.get_extra_info("peername")
        logger.info(f"WSAPI: got connection from {peername}")
        self.transport = transport

    def data_received(self, data):
        message = data.decode()
        logger.info(f"WSAPI: Data received: {message}")
        self.transport.close()


class VCMP:
    def __init__(self, listener_addr: tuple, wsapi_addr: tuple) -> None:
        self.listener_addr = listener_addr
        self.wsapi_addr = wsapi_addr

    async def init_listener(self):
        loop = asyncio.get_running_loop()
        server = await loop.create_server(
            lambda: ListenerProtocol(), self.listener_addr[0], self.listener_addr[1]
        )
        return server

    async def init_wsapi(self):
        loop = asyncio.get_running_loop()
        server = await loop.create_server(
            lambda: WSAPIProtocol(), self.wsapi_addr[0], self.wsapi_addr[1]
        )
        return server

    async def run(self):
        listener = await self.init_listener()
        wsapi = await self.init_wsapi()
        logger.info("Running both listener and wsapi TCP servers!")
        await asyncio.gather(listener.serve_forever(), wsapi.serve_forever())
