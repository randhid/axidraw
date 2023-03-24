# my-python-robot/main.py

import asyncio
from viam.rpc.server import Server

from viamaxidraw import AxiDraw

async def main():
    srv = Server([AxiDraw('axidraw')])
    await srv.serve()

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except:
        pass