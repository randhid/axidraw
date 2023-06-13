# viamaxidraw.py

import asyncio

from typing import Any, Dict, List, Optional, Sequence, Mapping
from typing_extensions import Self

import json
from pyaxidraw import axidraw

from viam.proto.app.robot import ComponentConfig
from viam.components.gantry import Gantry
from viam.resource.types import Model, ModelFamily
from viam.operations import run_with_operation
from viam.module.types import Reconfigurable
from viam.proto.common import ResourceName


DEFAULT_USB_ADDRESS = "/dev/tty.usbmodem11201"
DEFAULT_USB_BAUD = 9600

# Constructor
@classmethod
def new_axidraw(cls, config: ComponentConfig, dependencies: Mapping[ResourceName, ResourceGantry]) -> Self:
    axidraw = cls(AxiDraw(config.name))
    axidraw.reconfigure(config, dependencies)
    return axidraw

# Validates JSON Configuration
@classmethod
def validate_config(cls, config: ComponentConfig) -> Sequence[str]:
    # attribute = config.attributes.fields["attribute"].string_value
    # if attribute == "":
    #     raise Exception("Exception to axidraw placeholder")
    pass


# Handles attribute reconfiguration
def reconfigure(self, config: ComponentConfig, dependencies: Mapping[ResourceName, ResourceBase]):
    pass

class AxiDraw(Gantry):
    # Subclass the Viam Arm component and implement the required functions

    def __init__(self, name: str):
       
        # Starting position
        self.lengths = List[0,0,0]
        self.position = List[0,0,0]
        self.servoUp = bool


        # Starting joint positions
        self.is_stopped = True
        super().__init__(name)
        self.ad = axidraw.AxiDraw()          # Initialize class
        self.ad.interactive()                # Enter interactive context
        if not self.ad.connect():            # Open serial port to AxiDraw;
            quit()                      #   Exit, if no connection.

    def __del__(self):
        self.ad.disconnect()

    async def get_position(self, extra: Optional[Dict[str, Any]] = None, **kwargs) -> List[float]:
        return self.position

    @run_with_operation
    async def move_to_position(
        self,
        positions: List[float],
        extra: Optional[Dict[str, Any]] = None,
        **kwargs,
    ):
        operation = self.get_operation(kwargs)

        self.is_stopped = False
        self.position = List[positions]

        if positions[2] > 0:
            ad.moveto(positions[0], positions[1])
        else:
            ad.lineto(positions[0], positions[1])



        # Check if the operation is cancelled and, if it is, stop the gantry's motion
        if await operation.is_cancelled():
            await self.stop()


    @run_with_operation
    async def get_lengths(self, extra: Optional[Dict[str, Any]] = None, **kwargs) -> List[float]:
        return self.lengths


    async def stop(self, extra: Optional[Dict[str, Any]] = None, **kwargs):
        self.is_stopped = True

    async def is_moving(self) -> bool:
        return not self.is_stopped
