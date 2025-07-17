import bpy
import bmesh
import mathutils
from mathutils import Vector
import math
import random
from bpy.types import Operator

class PROCLIGHT_OT_generate_lights(Operator):
    """Generate procedural lights based on pattern"""
    bl_idname = "procedural_lighting.generate_lights"
    bl_label = "Generate Lights"
    bl_options = {'REGISTER', 'UNDO'}
    
    def execute(self, context):
        props = context.scene.procedural_lighting
        
        # Clear existing lights in group
        self.clear_existing_lights(props.light_group_name)
        
        # Create parent empty if needed
        parent_empty = None
        if props.auto_parent:
            parent_empty = self.create_parent_empty(props.light_group_name)
        
        # Generate lights based on pattern
        lights = []
        if props.pattern_type == 'CIRCLE':
            lights = self.generate_circle_pattern(props)
        elif props.pattern_type == 'GRID':
            lights = self.generate_grid_pattern(props)
        elif props.pattern_type == 'RANDOM':
            lights = self.generate_random_pattern(props)
        elif props.pattern_type == 'SPIRAL':
            lights = self.generate_spiral_pattern(props)
        elif props.pattern_type == 'WAVE':
            lights = self.generate_wave_pattern(props)
        
        # Parent lights to empty if needed
        if parent_empty:
            for light in lights:
                light.parent = parent_empty
        
        self.report({'INFO'}, f"Generated {len(lights)} lights")
        return {'FINISHED'}
    
    def clear_existing_lights(self, group_name):
        """Remove existing lights from the group"""
        objects_to_remove = []
        for obj in bpy.data.objects:
            if obj.name.startswith(group_name) and obj.type == 'LIGHT':
                objects_to_remove.append(obj)
        
        for obj in objects_to_remove:
            bpy.data.objects.remove(obj, do_unlink=True)
    
    def create_parent_empty(self, name):
        """Create an empty object to parent lights to"""
        empty_name = f"{name}_Controller"
        
        # Remove existing empty if it exists
        if empty_name in bpy.data.objects:
            bpy.data.objects.remove(bpy.data.objects[empty_name], do_unlink=True)
        
        empty = bpy.data.objects.new(empty_name, None)
        bpy.context.collection.objects.link(empty)
        empty.empty_display_type = 'ARROWS'
        empty.empty_display_size = 2.0
        
        return empty
    
    def create_light(self, name, location, props):
        """Create a single light with variations"""
        light_data = bpy.data.lights.new(name=name, type='POINT')
        light_object = bpy.data.objects.new(name, light_data)
        bpy.context.collection.objects.link(light_object)
        
        # Set location
        light_object.location = location
        
        # Apply energy with variation
        energy_var = random.uniform(-props.energy_variation, props.energy_variation)
        light_data.energy = props.base_energy * (1 + energy_var)
        
        # Apply color with variation
        color_var = random.uniform(-props.color_variation, props.color_variation)
        color = [max(0, min(1, c + color_var)) for c in props.base_color]
        light_data.color = color
        
        return light_object
    
    def generate_circle_pattern(self, props):
        """Generate lights in a circular pattern"""
        lights = []
        angle_step = 2 * math.pi / props.light_count
        
        for i in range(props.light_count):
            angle = i * angle_step
            x = math.cos(angle) * props.radius
            y = math.sin(angle) * props.radius
            z = props.height
            
            location = Vector((x, y, z))
            light_name = f"{props.light_group_name}_Circle_{i:02d}"
            light = self.create_light(light_name, location, props)
            lights.append(light)
        
        return lights
    
    def generate_grid_pattern(self, props):
        """Generate lights in a grid pattern"""
        lights = []
        grid_size = int(math.sqrt(props.light_count))
        spacing = props.radius * 2 / (grid_size - 1) if grid_size > 1 else 0
        
        count = 0
        for i in range(grid_size):
            for j in range(grid_size):
                if count >= props.light_count:
                    break
                
                x = (i - grid_size / 2) * spacing
                y = (j - grid_size / 2) * spacing
                z = props.height
                
                location = Vector((x, y, z))
                light_name = f"{props.light_group_name}_Grid_{count:02d}"
                light = self.create_light(light_name, location, props)
                lights.append(light)
                count += 1
        
        return lights
    
    def generate_random_pattern(self, props):
        """Generate lights in random positions"""
        lights = []
        
        for i in range(props.light_count):
            x = random.uniform(-props.radius, props.radius)
            y = random.uniform(-props.radius, props.radius)
            z = props.height + random.uniform(-2, 2)
            
            location = Vector((x, y, z))
            light_name = f"{props.light_group_name}_Random_{i:02d}"
            light = self.create_light(light_name, location, props)
            lights.append(light)
        
        return lights
    
    def generate_spiral_pattern(self, props):
        """Generate lights in a spiral pattern"""
        lights = []
        
        for i in range(props.light_count):
            t = i / props.light_count
            angle = t * 4 * math.pi
            radius = props.radius * t
            
            x = math.cos(angle) * radius
            y = math.sin(angle) * radius
            z = props.height + t * 5
            
            location = Vector((x, y, z))
            light_name = f"{props.light_group_name}_Spiral_{i:02d}"
            light = self.create_light(light_name, location, props)
            lights.append(light)
        
        return lights
    
    def generate_wave_pattern(self, props):
        """Generate lights in a wave pattern"""
        lights = []
        
        for i in range(props.light_count):
            t = i / props.light_count
            x = t * props.radius * 2 - props.radius
            y = math.sin(t * 4 * math.pi) * props.radius * 0.5
            z = props.height + math.cos(t * 6 * math.pi) * 2
            
            location = Vector((x, y, z))
            light_name = f"{props.light_group_name}_Wave_{i:02d}"
            light = self.create_light(light_name, location, props)
            lights.append(light)
        
        return lights

class PROCLIGHT_OT_clear_lights(Operator):
    """Clear all procedural lights"""
    bl_idname = "procedural_lighting.clear_lights"
    bl_label = "Clear Lights"
    bl_options = {'REGISTER', 'UNDO'}
    
    def execute(self, context):
        props = context.scene.procedural_lighting
        
        # Remove lights
        objects_to_remove = []
        for obj in bpy.data.objects:
            if obj.name.startswith(props.light_group_name):
                objects_to_remove.append(obj)
        
        for obj in objects_to_remove:
            bpy.data.objects.remove(obj, do_unlink=True)
        
        self.report({'INFO'}, f"Cleared procedural lights")
        return {'FINISHED'}

class PROCLIGHT_OT_setup_volumetrics(Operator):
    """Setup volumetric lighting"""
    bl_idname = "procedural_lighting.setup_volumetrics"
    bl_label = "Setup Volumetrics"
    bl_options = {'REGISTER', 'UNDO'}
    
    def execute(self, context):
        props = context.scene.procedural_lighting
        
        # Ensure we're using Cycles
        if context.scene.render.engine != 'CYCLES':
            context.scene.render.engine = 'CYCLES'
        
        # Create volumetric material
        vol_material = self.create_volumetric_material(props)
        
        # Create a cube to hold the volumetric material
        bpy.ops.mesh.primitive_cube_add(size=props.radius * 2, location=(0, 0, props.height))
        vol_cube = context.active_object
        vol_cube.name = f"{props.light_group_name}_Volume"
        
        # Assign material
        vol_cube.data.materials.append(vol_material)
        
        # Make it display as bounds
        vol_cube.display_type = 'BOUNDS'
        
        self.report({'INFO'}, "Volumetric lighting setup complete")
        return {'FINISHED'}
    
    def create_volumetric_material(self, props):
        """Create a volumetric material"""
        material = bpy.data.materials.new(name="VolumetricMaterial")
        material.use_nodes = True
        material.node_tree.clear()
        
        # Create nodes
        output_node = material.node_tree.nodes.new(type='ShaderNodeOutputMaterial')
        volume_scatter = material.node_tree.nodes.new(type='ShaderNodeVolumeScatter')
        
        # Set properties
        volume_scatter.inputs['Density'].default_value = props.volumetric_density
        volume_scatter.inputs['Color'].default_value = (*props.base_color, 1.0)
        
        # Connect nodes
        material.node_tree.links.new(volume_scatter.outputs['Volume'], output_node.inputs['Volume'])
        
        return material

class PROCLIGHT_OT_setup_bloom(Operator):
    """Setup bloom effect in compositor"""
    bl_idname = "procedural_lighting.setup_bloom"
    bl_label = "Setup Bloom"
    bl_options = {'REGISTER', 'UNDO'}
    
    def execute(self, context):
        props = context.scene.procedural_lighting
        
        # Enable compositor
        context.scene.use_nodes = True
        tree = context.scene.node_tree
        tree.nodes.clear()
        
        # Create nodes
        render_layers = tree.nodes.new(type='CompositorNodeRLayers')
        composite = tree.nodes.new(type='CompositorNodeComposite')
        
        # Bloom setup
        glare = tree.nodes.new(type='CompositorNodeGlare')
        glare.glare_type = 'BLOOM'
        glare.threshold = 1.0
        glare.intensity = props.bloom_intensity
        glare.size = 8
        
        # Connect nodes
        tree.links.new(render_layers.outputs['Image'], glare.inputs['Image'])
        tree.links.new(glare.outputs['Image'], composite.inputs['Image'])
        
        # Position nodes
        render_layers.location = (0, 0)
        glare.location = (300, 0)
        composite.location = (600, 0)
        
        self.report({'INFO'}, "Bloom effect setup complete")
        return {'FINISHED'}

class PROCLIGHT_OT_save_preset(Operator):
    """Save current lighting setup as preset"""
    bl_idname = "procedural_lighting.save_preset"
    bl_label = "Save Preset"
    bl_options = {'REGISTER', 'UNDO'}
    
    def execute(self, context):
        props = context.scene.procedural_lighting
        
        # Create new preset
        preset = props.presets.add()
        preset.name = f"Preset_{len(props.presets)}"
        preset.light_type = 'POINT'
        preset.energy = props.base_energy
        preset.color = props.base_color
        
        self.report({'INFO'}, f"Saved preset: {preset.name}")
        return {'FINISHED'}

class PROCLIGHT_OT_load_preset(Operator):
    """Load lighting preset"""
    bl_idname = "procedural_lighting.load_preset"
    bl_label = "Load Preset"
    bl_options = {'REGISTER', 'UNDO'}
    
    def execute(self, context):
        props = context.scene.procedural_lighting
        
        if props.active_preset_index < len(props.presets):
            preset = props.presets[props.active_preset_index]
            props.base_energy = preset.energy
            props.base_color = preset.color
            
            self.report({'INFO'}, f"Loaded preset: {preset.name}")
        else:
            self.report({'WARNING'}, "No preset selected")
        
        return {'FINISHED'}

classes = [
    PROCLIGHT_OT_generate_lights,
    PROCLIGHT_OT_clear_lights,
    PROCLIGHT_OT_setup_volumetrics,
    PROCLIGHT_OT_setup_bloom,
    PROCLIGHT_OT_save_preset,
    PROCLIGHT_OT_load_preset,
]

def register():
    for cls in classes:
        bpy.utils.register_class(cls)

def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls) 