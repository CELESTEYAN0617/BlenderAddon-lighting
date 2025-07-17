import bpy
import json
import os
from bpy.types import Operator

class PROCLIGHT_OT_remove_preset(Operator):
    """Remove selected preset"""
    bl_idname = "procedural_lighting.remove_preset"
    bl_label = "Remove Preset"
    bl_options = {'REGISTER', 'UNDO'}
    
    def execute(self, context):
        props = context.scene.procedural_lighting
        
        if props.active_preset_index < len(props.presets):
            preset_name = props.presets[props.active_preset_index].name
            props.presets.remove(props.active_preset_index)
            
            # Adjust active index
            if props.active_preset_index >= len(props.presets):
                props.active_preset_index = len(props.presets) - 1
            
            self.report({'INFO'}, f"Removed preset: {preset_name}")
        else:
            self.report({'WARNING'}, "No preset selected")
        
        return {'FINISHED'}

class PROCLIGHT_OT_export_presets(Operator):
    """Export presets to file"""
    bl_idname = "procedural_lighting.export_presets"
    bl_label = "Export Presets"
    bl_options = {'REGISTER', 'UNDO'}
    
    filepath: bpy.props.StringProperty(
        name="File Path",
        description="Where to save the preset file",
        maxlen=1024,
        subtype='FILE_PATH'
    )
    
    def execute(self, context):
        props = context.scene.procedural_lighting
        
        # Convert presets to JSON-serializable format
        presets_data = []
        for preset in props.presets:
            preset_data = {
                "name": preset.name,
                "light_type": preset.light_type,
                "energy": preset.energy,
                "color": list(preset.color),
                "location": list(preset.location),
                "rotation": list(preset.rotation)
            }
            presets_data.append(preset_data)
        
        # Save to file
        try:
            with open(self.filepath, 'w') as f:
                json.dump(presets_data, f, indent=2)
            self.report({'INFO'}, f"Exported {len(presets_data)} presets")
        except Exception as e:
            self.report({'ERROR'}, f"Export failed: {str(e)}")
        
        return {'FINISHED'}
    
    def invoke(self, context, event):
        context.window_manager.fileselect_add(self)
        return {'RUNNING_MODAL'}

class PROCLIGHT_OT_import_presets(Operator):
    """Import presets from file"""
    bl_idname = "procedural_lighting.import_presets"
    bl_label = "Import Presets"
    bl_options = {'REGISTER', 'UNDO'}
    
    filepath: bpy.props.StringProperty(
        name="File Path",
        description="Preset file to import",
        maxlen=1024,
        subtype='FILE_PATH'
    )
    
    def execute(self, context):
        props = context.scene.procedural_lighting
        
        try:
            with open(self.filepath, 'r') as f:
                presets_data = json.load(f)
            
            # Import presets
            for preset_data in presets_data:
                preset = props.presets.add()
                preset.name = preset_data.get("name", "Imported Preset")
                preset.light_type = preset_data.get("light_type", "POINT")
                preset.energy = preset_data.get("energy", 10.0)
                preset.color = preset_data.get("color", [1.0, 1.0, 1.0])
                preset.location = preset_data.get("location", [0.0, 0.0, 5.0])
                preset.rotation = preset_data.get("rotation", [0.0, 0.0, 0.0])
            
            self.report({'INFO'}, f"Imported {len(presets_data)} presets")
        except Exception as e:
            self.report({'ERROR'}, f"Import failed: {str(e)}")
        
        return {'FINISHED'}
    
    def invoke(self, context, event):
        context.window_manager.fileselect_add(self)
        return {'RUNNING_MODAL'}

class PROCLIGHT_OT_load_builtin_presets(Operator):
    """Load built-in presets"""
    bl_idname = "procedural_lighting.load_builtin_presets"
    bl_label = "Load Built-in Presets"
    bl_options = {'REGISTER', 'UNDO'}
    
    def execute(self, context):
        props = context.scene.procedural_lighting
        
        # Clear existing presets
        props.presets.clear()
        
        # Built-in presets
        builtin_presets = [
            {
                "name": "Warm Studio",
                "light_type": "AREA",
                "energy": 50.0,
                "color": [1.0, 0.8, 0.6],
                "location": [0.0, 0.0, 5.0],
                "rotation": [0.0, 0.0, 0.0]
            },
            {
                "name": "Cool Daylight",
                "light_type": "SUN",
                "energy": 5.0,
                "color": [0.7, 0.9, 1.0],
                "location": [0.0, 0.0, 10.0],
                "rotation": [0.785, 0.0, 0.785]
            },
            {
                "name": "Dramatic Spot",
                "light_type": "SPOT",
                "energy": 100.0,
                "color": [1.0, 0.95, 0.9],
                "location": [5.0, 5.0, 8.0],
                "rotation": [-0.785, 0.0, 0.785]
            },
            {
                "name": "Soft Fill",
                "light_type": "AREA",
                "energy": 20.0,
                "color": [0.9, 0.9, 1.0],
                "location": [-3.0, 2.0, 4.0],
                "rotation": [0.0, 0.0, 0.0]
            },
            {
                "name": "Rim Light",
                "light_type": "POINT",
                "energy": 30.0,
                "color": [1.0, 0.7, 0.3],
                "location": [0.0, -5.0, 6.0],
                "rotation": [0.0, 0.0, 0.0]
            }
        ]
        
        # Add built-in presets
        for preset_data in builtin_presets:
            preset = props.presets.add()
            preset.name = preset_data["name"]
            preset.light_type = preset_data["light_type"]
            preset.energy = preset_data["energy"]
            preset.color = preset_data["color"]
            preset.location = preset_data["location"]
            preset.rotation = preset_data["rotation"]
        
        self.report({'INFO'}, f"Loaded {len(builtin_presets)} built-in presets")
        return {'FINISHED'}

class PROCLIGHT_OT_duplicate_preset(Operator):
    """Duplicate selected preset"""
    bl_idname = "procedural_lighting.duplicate_preset"
    bl_label = "Duplicate Preset"
    bl_options = {'REGISTER', 'UNDO'}
    
    def execute(self, context):
        props = context.scene.procedural_lighting
        
        if props.active_preset_index < len(props.presets):
            source_preset = props.presets[props.active_preset_index]
            
            # Create duplicate
            new_preset = props.presets.add()
            new_preset.name = f"{source_preset.name}_Copy"
            new_preset.light_type = source_preset.light_type
            new_preset.energy = source_preset.energy
            new_preset.color = source_preset.color
            new_preset.location = source_preset.location
            new_preset.rotation = source_preset.rotation
            
            # Set as active
            props.active_preset_index = len(props.presets) - 1
            
            self.report({'INFO'}, f"Duplicated preset: {source_preset.name}")
        else:
            self.report({'WARNING'}, "No preset selected")
        
        return {'FINISHED'}

classes = [
    PROCLIGHT_OT_remove_preset,
    PROCLIGHT_OT_export_presets,
    PROCLIGHT_OT_import_presets,
    PROCLIGHT_OT_load_builtin_presets,
    PROCLIGHT_OT_duplicate_preset,
]

def register():
    for cls in classes:
        bpy.utils.register_class(cls)

def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls) 