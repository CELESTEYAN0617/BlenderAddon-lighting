bl_info = {
    "name": "Procedural Lighting System",
    "author": "Your Name",
    "version": (1, 0, 0),
    "blender": (4, 5, 0),
    "location": "3D Viewport > Sidebar > Lighting",
    "description": "Advanced procedural lighting system for scene management",
    "category": "Lighting",
    "support": "COMMUNITY",
}

import bpy
from . import ui
from . import operators
from . import properties
from . import presets
from . import utils

def register():
    properties.register()
    operators.register()
    ui.register()
    presets.register()
    utils.register()

def unregister():
    utils.unregister()
    presets.unregister()
    ui.unregister()
    operators.unregister()
    properties.unregister()

if __name__ == "__main__":
    register() 