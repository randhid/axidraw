
import asyncio
import sys

from axidraw import AxiDraw

from viam.components.gantry import Gantry
from viam.module.module import Module
from .odrive import Odrive

async def main(address: str):
    """This function creates and starts a new module, after adding all desired resources.
    Resources must be pre-registered. For an example, see the `__init__.py` file.
    Args:
        address (str): The address to serve the module on
    """
    module = Module(address)
    module.add_model_from_registry(Gantry.SUBTYPE, AxiDraw.MODEL)
    await module.start()

if __name__ == "__main__":
    # if len(sys.argv) != 2:
    #     raise Exception("Need socket path as command line argument")
    asyncio.run(main())

# my-python-robot/main.py
# import asyncio
# from viam.rpc.server import Server

# from axidraw import AxiDraw

# async def main():
#     srv = Server([AxiDraw('axidraw')])
#     await srv.serve()

# if __name__ == '__main__':
#     try:
#         asyncio.run(main())
#     except:
#         pass
