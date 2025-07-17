import bpy
from bpy.props import (
    BoolProperty,
    IntProperty,
    FloatProperty,
    FloatVectorProperty,
    EnumProperty,
    StringProperty,
    PointerProperty,
    CollectionProperty,
)
from bpy.types import PropertyGroup

class LightPreset(PropertyGroup):
    """Individual light preset settings"""
    name: StringProperty(
        name="Preset Name",
        default="New Preset"
    )
    
    light_type: EnumProperty(
        name="Light Type",
        items=[
            ('SUN', "Sun", "Sun light"),
            ('POINT', "Point", "Point light"),
            ('SPOT', "Spot", "Spot light"),
            ('AREA', "Area", "Area light"),
        ],
        default='POINT'
    )
    
    energy: FloatProperty(
        name="Energy",
        default=10.0,
        min=0.0,
        max=1000.0
    )
    
    color: FloatVectorProperty(
        name="Color",
        subtype='COLOR',
        default=(1.0, 1.0, 1.0),
        min=0.0,
        max=1.0
    )
    
    location: FloatVectorProperty(
        name="Location",
        subtype='TRANSLATION',
        default=(0.0, 0.0, 5.0)
    )
    
    rotation: FloatVectorProperty(
        name="Rotation",
        subtype='EULER',
        default=(0.0, 0.0, 0.0)
    )

class ProceduralLightingProperties(PropertyGroup):
    """Main properties for procedural lighting system"""
    
    # Pattern Generation
    pattern_type: EnumProperty(
        name="Pattern Type",
        items=[
            ('CIRCLE', "Circle", "Circular pattern"),
            ('GRID', "Grid", "Grid pattern"),
            ('RANDOM', "Random", "Random placement"),
            ('SPIRAL', "Spiral", "Spiral pattern"),
            ('WAVE', "Wave", "Wave pattern"),
        ],
        default='CIRCLE'
    )
    
    light_count: IntProperty(
        name="Light Count",
        default=8,
        min=1,
        max=100
    )
    
    radius: FloatProperty(
        name="Radius",
        default=10.0,
        min=0.1,
        max=100.0
    )
    
    height: FloatProperty(
        name="Height",
        default=5.0,
        min=-50.0,
        max=50.0
    )
    
    # Light Properties
    base_energy: FloatProperty(
        name="Base Energy",
        default=10.0,
        min=0.0,
        max=1000.0
    )
    
    energy_variation: FloatProperty(
        name="Energy Variation",
        default=0.2,
        min=0.0,
        max=1.0
    )
    
    base_color: FloatVectorProperty(
        name="Base Color",
        subtype='COLOR',
        default=(1.0, 1.0, 1.0),
        min=0.0,
        max=1.0
    )
    
    color_variation: FloatProperty(
        name="Color Variation",
        default=0.1,
        min=0.0,
        max=1.0
    )
    
    # Animation Properties
    animate_lights: BoolProperty(
        name="Animate Lights",
        default=False
    )
    
    animation_speed: FloatProperty(
        name="Animation Speed",
        default=1.0,
        min=0.1,
        max=10.0
    )
    
    # Rendering Effects
    use_volumetrics: BoolProperty(
        name="Use Volumetrics",
        default=False
    )
    
    volumetric_density: FloatProperty(
        name="Volumetric Density",
        default=0.1,
        min=0.0,
        max=1.0
    )
    
    use_bloom: BoolProperty(
        name="Use Bloom",
        default=False
    )
    
    bloom_intensity: FloatProperty(
        name="Bloom Intensity",
        default=0.5,
        min=0.0,
        max=2.0
    )
    
    # Management
    light_group_name: StringProperty(
        name="Light Group Name",
        default="ProceduralLights"
    )
    
    auto_parent: BoolProperty(
        name="Auto Parent to Empty",
        default=True,
        description="Automatically parent lights to an empty object for easy manipulation"
    )
    
    # Presets
    presets: CollectionProperty(type=LightPreset)
    active_preset_index: IntProperty(default=0)

classes = [
    LightPreset,
    ProceduralLightingProperties,
]

def register():
    for cls in classes:
        bpy.utils.register_class(cls)
    
    bpy.types.Scene.procedural_lighting = PointerProperty(type=ProceduralLightingProperties)

def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
    
    del bpy.types.Scene.procedural_lighting 