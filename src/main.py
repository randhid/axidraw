
import asyncio

from viam.resource.registry import Registry, ResourceCreatorRegistration
from my_axidraw import AxiDraw

from viam.components.gantry import Gantry
from viam.module.module import Module

async def main():
    """This function creates and starts a new module, after adding all desired resources.
    Resources must be pre-registered. For an example, see the `__init__.py` file.
    Args:
        address (str): The address to serve the module on
    """
    Registry.register_resource_creator(
        Gantry.SUBTYPE, 
        AxiDraw.MODEL, 
        ResourceCreatorRegistration(AxiDraw.new_axidraw, AxiDraw.validate_config))
    
    module = Module.from_args()
    module.add_model_from_registry(Gantry.SUBTYPE, AxiDraw.MODEL)
    await module.start()

if __name__ == "__main__":
    asyncio.run(main())
