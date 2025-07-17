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

class ProceduralLightPreset(PropertyGroup):
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
        max=10000
    )
    
    # Global Light Intensity Control
    global_intensity: FloatProperty(
        name="Global Intensity",
        description="Global multiplier for all light intensities",
        default=1.0,
        min=0.0,
        max=10,
        soft_min=0.0,
        soft_max=5    
    )
    
    # Mood Renderer
    mood_type: EnumProperty(
        name="Mood",
        description="Select a mood to automatically generate lighting",
        items=[
            ('NONE', "None", "No mood preset"),
            ('WARM', "Warm", "Warm and cozy atmosphere"),
            ('COLD', "Cold", "Cool and clinical atmosphere"),
            ('DRAMATIC', "Dramatic", "Dark and dramatic atmosphere"),
            ('ROMANTIC', "Romantic", "Soft and romantic lighting"),
            ('MYSTERIOUS', "Mysterious", "Dark and mysterious atmosphere"),
            ('ENERGETIC', "Energetic", "Bright and energetic lighting"),
            ('CALM', "Calm", "Soft and peaceful atmosphere"),
            ('SUNSET', "Sunset", "Golden hour lighting"),
            ('NIGHT', "Night", "Night time atmosphere"),
        ],
        default='NONE'
    )
    
    auto_apply_mood: BoolProperty(
        name="Auto Apply Mood",
        description="Automatically apply mood changes to existing lights",
        default=True
    )
    
    mood_intensity: FloatProperty(
        name="Mood Intensity",
        description="How strongly to apply the mood",
        default=1.0,
        min=0.0,
        max=2.0,
        soft_min=0.0,
        soft_max=10.5    
    )
    
    mood_applied: BoolProperty(
        name="Mood Applied",
        description="Whether a mood has been applied to the scene",
        default=False
    )
    
    intensity_curve: EnumProperty(
        name="Intensity Curve",
        description="How intensity affects light energy",
        items=[
            ('LINEAR', "Linear", "Linear intensity scaling"),
            ('EXPONENTIAL', "Exponential", "Exponential intensity scaling"),
            ('LOGARITHMIC', "Logarithmic", "Logarithmic intensity scaling"),
        ],
        default='LINEAR'
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
    presets: CollectionProperty(type=ProceduralLightPreset)
    active_preset_index: IntProperty(default=0)

classes = [
    ProceduralLightPreset,
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