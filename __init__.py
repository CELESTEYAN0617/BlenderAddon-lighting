bl_info = {
    "name": "Procedural Lighting System",
    "author": "Your Name",
    "version": (1, 0, 0),
    "blender": (4, 1, 0),
    "location": "3D Viewport > Sidebar > Lighting",
    "description": "Advanced procedural lighting system for scene management",
    "category": "Lighting",
    "support": "COMMUNITY",
}

import bpy # type: ignore
from . import ui
from . import operators
from . import properties
from . import presets
from . import utils

modules = [
    properties,
    operators,
    ui,
    presets,
    utils,
]

def register():
    for module in modules:
        module.register()

def unregister():
    for module in reversed(modules):
        module.unregister()

if __name__ == "__main__":
    register() 