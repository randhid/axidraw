"""
This file registers the MyBase model with the Python SDK.
"""

from viam.components.gantry import Gantry
from viam.resource.registry import Registry, ResourceCreatorRegistration

from .my_axidraw import AxiDraw

Registry.register_resource_creator(
    Gantry.SUBTYPE,
    AxiDraw.MODEL,
    ResourceCreatorRegistration(AxiDraw.new, AxiDraw.validate))
