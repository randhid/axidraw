# my_axidraw.py
"""
This contains the implementation of the AxiDraw class for initilization, validation,
reconfiguration, and control and querying of state using viam's Gantry API methods.
"""
import sys

from typing import Any, Dict, List, Optional, Sequence, Mapping, ClassVar
from typing_extensions import Self

from pyaxidraw import axidraw

from viam.proto.app.robot import ComponentConfig
from viam.components.gantry import Gantry
from viam.resource.types import Model, ModelFamily
from viam.operations import run_with_operation
from viam.module.types import Reconfigurable
from viam.proto.common import ResourceName
from viam.resource.base import ResourceBase
from viam.proto.common import Geometry
from viam.logging import getLogger

LOGGER = getLogger(__name__)

MM_TO_INCHES = 0.0393 #TODO check the resolution of this gantry
class AxiDraw(Gantry, Reconfigurable):
    """
    An AxiDraw Gantry component that connects to the controller via a usb connection and
    sets the starting positions of the plotter to 0,0,0.
    The lengths correspond to the AxiDrawV3  lengths and the servo is assumed 
    """
    def __init__(self, name: str):
        super().__init__(name)
        # Starting State
        self.lengths = [430.0 ,291.0,17.0]
        self.position = [0.0,0.0,0.0]
        self.is_stopped = True
        self.axi_draw = axidraw.AxiDraw()
        # Initialize class from eggbot's axidraw package
        self.axi_draw.interactive()       # Enter interactive context
        if not self.axi_draw.connect():   # Open serial port to AxiDraw;
            sys.exit()                  # Exit, if no connection.

    def __del__(self):
        self.axi_draw.disconnect()

    MODEL: ClassVar[Model] = Model(ModelFamily("peter", "eggbot"), "axidraw")

    # Constructor
    @classmethod
    def new(
        cls, config: ComponentConfig,
        dependencies: Mapping[ResourceName, ResourceBase]
        ) -> Self:
        """
        new_axidraw intializes the Axidraw class with the default state

        """
        my_axidraw = cls(config.name)
        my_axidraw.reconfigure(config, dependencies)
        return my_axidraw

    # Validates JSON Configuration
    @classmethod
    def validate(cls, config: ComponentConfig):
        """ does nothing, there are no attributes to change in this model """


    # Handles attribute reconfiguration
    def reconfigure(
        self,
        config: ComponentConfig,
        dependencies: Mapping[ResourceName, ResourceBase]
        ):
        """ reconfigure does nothing, there are no attributes to change in this model"""

    @run_with_operation
    async def get_position(self, *, extra: Optional[Dict[str, Any]] = None, timeout: Optional[float] = None, **kwargs) -> List[float]:
        """ gets the current position of the axidraw  """
        return self.position

    @run_with_operation
    async def move_to_position(
        self,
        positions: List[float],
        speeds: List[float],
        *,
        extra: Optional[Dict[str, Any]] = None,
        timeout: Optional[float] = None,
        **kwargs,
    ):
        """ moves the axidraw axes and servo to draw  """
        operation = self.get_operation(kwargs)
        self.is_stopped = False
        self.position = positions

        positions_inches = [i * MM_TO_INCHES for i in positions]

        if positions[2] > 0: # zero is the ground plane for the third axis - the servo
            #TODO: servo up/down through their position or an extra parameter as a bool
            # ask for user preference.
            self.axi_draw.moveto(
                # Move with pen up
                positions_inches[0], 
                positions_inches[1]) 
        else:
             # Move with pen down
            self.axi_draw.lineto(
                positions_inches[0], 
            positions_inches[1])

        self.is_stopped = True
        # Check if the operation is cancelled and, if it is, stop the gantry's motion
        if await operation.is_cancelled():
            await self.stop()


    async def get_lengths(self, *, extra: Optional[Dict[str, Any]] = None, timeout: Optional[float] = None, **kwargs) -> List[float]:
        """ returns the lengths of the axidraw axes """
        return self.lengths


    async def stop(self, *, extra: Optional[Dict[str, Any]] = None, timeout: Optional[float] = None, **kwargs):
        """ stops the axidraw """
        self.is_stopped = True

    async def home(self, *, extra: Optional[Dict[str, Any]] = None, timeout: Optional[float] = None, **kwargs) -> bool:
        """ sets the current position to 0,0,0 """
        await self.move_to_position([0, 0, 0], [50.0, 50.0, 50.0])
        return True
    
    async def is_moving(self) -> bool:
        """ queries whether the axidraw is moving """
        return not self.is_stopped
