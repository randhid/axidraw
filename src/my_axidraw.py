# viamaxidraw.py
"""
This contains the implementation of the AxiDraw class for initilization, validation,
reconfiguration, and control and querying of state using viam's Gantry API methods.
"""

from typing import Any, Dict, List, Optional, Sequence, Mapping, ClassVar

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


class AxiDraw(Gantry, Reconfigurable):
    """
    An AxiDraw Gantry component that connects to the controller via a usb connection and
    sets the starting positions of the plotter to 0,0,0.
    The lengths correspond to the AxiDrawV3  lengths and the servo is assumed 
    """
    MODEL: ClassVar[Model] = Model(ModelFamily("viam", "eggbot"), "axidraw")
    def __init__(self, name: str):
        super().__init__(name)
        # Starting State
        self.lengths = [430.0 ,291.0,17.0]
        self.position = [0.0 ,0.0,0.0]
        self.is_stopped = True
        self.axi_draw = axidraw.AxiDraw()
        # Initialize class from eggbot's axidraw package
        self.axi_draw.interactive()       # Enter interactive context
        if not self.axi_draw.connect():   # Open serial port to AxiDraw;
            quit()                  # Exit, if no connection.

    def __del__(self):
        self.axi_draw.disconnect()

    # Constructor
    @classmethod
    def new_axidraw(
        cls, config: ComponentConfig,
        dependencies: Mapping[ResourceName, ResourceBase]
        ):
        """
        new_axidraw intializes the Axidraw class with the default state and

        """
        my_axidraw = cls(config.name)
        my_axidraw.reconfigure(config, dependencies)
        return my_axidraw

    # Validates JSON Configuration
    @classmethod
    def validate_config(cls, config: ComponentConfig) -> Sequence[str]:
        """ does nothing, there are no attributes to change in this model """


    # Handles attribute reconfiguration
    def reconfigure(
        self,
        config: ComponentConfig,
        dependencies: Mapping[ResourceName, ResourceBase]
        ):
        """ reconfigure does nothing, there are no attributes to change in this model"""

    async def get_position(self, extra: Optional[Dict[str, Any]] = None, **kwargs) -> List[float]:
        """ gets the current position of the axidraw  """
        return self.position

    @run_with_operation
    async def move_to_position(
        self,
        positions: List[float],
        speeds: List[float],
        extra: Optional[Dict[str, Any]] = None,
        **kwargs,
    ):
        """ moves the axidraw axes and servo to draw  """
        operation = self.get_operation(kwargs)
        self.is_stopped = False
        self.position = positions

        if positions[2] > 0: # zero is the ground plane for the third axis - the servo
            self.axi_draw.moveto(positions[0], positions[1]) # Move with pen up
        else:
            self.axi_draw.lineto(positions[0], positions[1]) # Move with pen down

        # Check if the operation is cancelled and, if it is, stop the gantry's motion
        if await operation.is_cancelled():
            await self.stop()


    async def get_lengths(self, extra: Optional[Dict[str, Any]] = None, **kwargs) -> List[float]:
        """ returns the lengths of the axidraw axes """
        return self.lengths


    async def stop(self, extra: Optional[Dict[str, Any]] = None, **kwargs):
        """ stops the axidraw """
        self.is_stopped = True

    async def home(self, extra: Optional[Dict[str, Any]] = None, **kwargs):
        """ sets the current position to 0,0,0 """
        self.position = [0,0,0]

    async def is_moving(self) -> bool:
        """ queries whether the axidraw is moving """
        return not self.is_stopped

    async def get_geometries(
        self,
        extra: Optional[Dict[str, Any]] = None,
        **kwargs) -> List[Geometry]:
        """ returns nothing - no geometries associated with axidraw """

    async def close(self):
        """ disconnects the axidraw """
        self.axi_draw.disconnect()
