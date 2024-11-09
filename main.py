import asyncio
import configparser
import logging
from vcmp import VCMP

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger("vcmp")

if __name__ == "__main__":
    config = configparser.ConfigParser()
    config.read("./config.ini")

    listener_addr = config["listener"]["address"]
    listener_port = int(config["listener"]["port"])

    wsapi_addr = config["wsapi"]["address"]
    wsapi_port = int(config["wsapi"]["port"])

    logger.info(f"Listener address: {listener_addr}:{listener_port}")
    logger.info(f"WS API address: {wsapi_addr}:{wsapi_port}")

    vcmp = VCMP((listener_addr, listener_port), (wsapi_addr, wsapi_port))
    asyncio.run(vcmp.run())