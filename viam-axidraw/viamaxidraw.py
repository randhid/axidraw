# viamaxidraw.py

import asyncio
from typing import Any, Dict, Optional
from viam.components.gantry import Gantry, List
from viam.proto.common import WorldState
from viam.operations import run_with_operation
import serial
import json
from axidraw import motion 


DEFAULT_USB_ADDRESS = "/dev/tty.usbmodem11201"
DEFAULT_USB_BAUD = 9600

class AxiDraw(Gantry):
    # Subclass the Viam Arm component and implement the required functions

    def __init__(self, name: str):
        # Starting position
        self.lengths = List[0,0, 0]
        self.position = List[0,0, 0]
        self.servoUp = bool


        # Starting joint positions
        self.is_stopped = True
        super().__init__(name)
        self.ser.serial.Serial(DEFAULT_USB_ADDRESS, DEFAULT_USB_BAUD)

    def __del__(self):
        self.ser.close()

    async def get_position(self, extra: Optional[Dict[str, Any]] = None, **kwargs) -> List[float]:
        return self.position

    async def get_position(self, extra: Optional[Dict[str, Any]] = None, **kwargs) -> List[float]:
        return self.joint_positions

    @run_with_operation
    async def move_to_position(
        self,
        positions: List[float],
        world_state: Optional[WorldState] = None,
        extra: Optional[Dict[str, Any]] = None,
        **kwargs,
    ):
        operation = self.get_operation(kwargs)

        self.is_stopped = False
        self.position = List[0,0]

        # Simulate the length of time it takes for the arm to move to its new position
        for x in range(10):
            await asyncio.sleep(1)

            # Check if the operation is cancelled and, if it is, stop the arm's motion
            if await operation.is_cancelled():
                await self.stop()
                break

        self.is_stopped = True



    @run_with_operation
    async def get_lengths(self, extra: Optional[Dict[str, Any]] = None, **kwargs) -> List[float]:
        return self.lengths



    async def stop(self, extra: Optional[Dict[str, Any]] = None, **kwargs):
        self.is_stopped = True

    async def is_moving(self) -> bool:
        return not self.is_stopped