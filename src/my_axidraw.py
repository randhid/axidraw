# viamaxidraw.py

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


class AxiDraw(Gantry, Reconfigurable):
    MODEL: ClassVar[Model] = Model(ModelFamily("viam", "eggbot"), "axidraw")
    def __init__(self, name: str):
        super().__init__(name)
       
        # Starting 
        self.lengths = [430.0 ,291.0,17.0]
        self.position = [0.0 ,0.0,0.0]
        self.servoUp = False


        self.is_stopped = True
        self.ad = axidraw.AxiDraw()  
        # Initialize class
        self.ad.interactive()                # Enter interactive context
        if not self.ad.connect():            # Open serial port to AxiDraw;
            quit()                      #   Exit, if no connection.

    def __del__(self):
        self.ad.disconnect()

    # Constructor
    @classmethod
    def new_axidraw(cls, config: ComponentConfig, dependencies: Mapping[ResourceName, ResourceBase]):
        axidraw = cls(config.name)
        axidraw.reconfigure(config, dependencies)
        return axidraw

    # Validates JSON Configuration
    @classmethod
    def validate_config(cls, config: ComponentConfig) -> Sequence[str]:
        pass


    # Handles attribute reconfiguration
    def reconfigure(self, config: ComponentConfig, dependencies: Mapping[ResourceName, ResourceBase]):
        pass

    async def get_position(self, extra: Optional[Dict[str, Any]] = None, **kwargs) -> List[float]:
        return self.position

    @run_with_operation
    async def move_to_position(
        self,
        positions: List[float],
        speeds: List[float],
        extra: Optional[Dict[str, Any]] = None,
        **kwargs,
    ):
        operation = self.get_operation(kwargs)

        self.is_stopped = False
        self.position = positions

        if positions[2] > 0:
            self.ad.moveto(positions[0], positions[1])
        else:
            self.ad.lineto(positions[0], positions[1])



        # Check if the operation is cancelled and, if it is, stop the gantry's motion
        if await operation.is_cancelled():
            await self.stop()


    async def get_lengths(self, extra: Optional[Dict[str, Any]] = None, **kwargs) -> List[float]:
        return self.lengths


    async def stop(self, extra: Optional[Dict[str, Any]] = None, **kwargs):
        self.is_stopped = True
        
    async def home(self, extra: Optional[Dict[str, Any]] = None, **kwargs):
        self.position = [0,0,0]

    async def is_moving(self) -> bool:
        return not self.is_stopped
    
    async def get_geometries(self, extra: Optional[Dict[str, Any]] = None, **kwargs) -> List[Geometry]:
        pass

    async def close(self):
        self.ad.disconnect()

