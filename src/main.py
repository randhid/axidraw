"""
This module registers and intergrates EvilMadScientist's Axidraw with Viam 
as a gantry component so you can control and code the plotter for all your fun 
art projects.
"""
import asyncio

from viam.resource.registry import Registry, ResourceCreatorRegistration
from viam.components.gantry import Gantry
from viam.module.module import Module

from .my_axidraw import AxiDraw

async def main():
    """This function creates and starts a new module, after adding all desired resources.
    Resources must be pre-registered.
    """
    Registry.register_resource_creator(
        Gantry.SUBTYPE,
        AxiDraw.MODEL,
        ResourceCreatorRegistration(AxiDraw.new_axidraw, AxiDraw.validate_config)
        )
    module = Module.from_args()
    module.add_model_from_registry(Gantry.SUBTYPE, AxiDraw.MODEL)
    await module.start()

if __name__ == "__main__":
    asyncio.run(main())
