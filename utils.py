import bpy
import bmesh
import mathutils
from mathutils import Vector, Euler
import math
import random
from bpy.types import Operator

class PROCLIGHT_OT_animate_lights(Operator):
    """Animate procedural lights"""
    bl_idname = "procedural_lighting.animate_lights"
    bl_label = "Animate Lights"
    bl_options = {'REGISTER', 'UNDO'}
    
    def execute(self, context):
        props = context.scene.procedural_lighting
        
        # Find all lights in the group
        lights = []
        for obj in bpy.data.objects:
            if obj.name.startswith(props.light_group_name) and obj.type == 'LIGHT':
                lights.append(obj)
        
        if not lights:
            self.report({'WARNING'}, "No lights found to animate")
            return {'FINISHED'}
        
        # Set up animation
        scene = context.scene
        frame_start = scene.frame_start
        frame_end = scene.frame_end
        
        # Animate each light
        for i, light in enumerate(lights):
            self.animate_light(light, i, props, frame_start, frame_end)
        
        self.report({'INFO'}, f"Animated {len(lights)} lights")
        return {'FINISHED'}
    
    def animate_light(self, light, index, props, frame_start, frame_end):
        """Animate a single light"""
        # Store original location
        original_location = light.location.copy()
        
        # Animation parameters
        speed = props.animation_speed
        offset = index * 0.5  # Phase offset for each light
        
        # Create keyframes
        for frame in range(frame_start, frame_end + 1):
            bpy.context.scene.frame_set(frame)
            
            # Time-based animation
            time = (frame - frame_start) * speed * 0.1 + offset
            
            # Circular motion
            radius_offset = math.sin(time) * 2.0
            height_offset = math.cos(time * 0.5) * 1.0
            
            # Update location
            light.location.x = original_location.x + radius_offset
            light.location.z = original_location.z + height_offset
            
            # Insert keyframe
            light.keyframe_insert(data_path="location", frame=frame)
            
            # Animate energy
            energy_offset = math.sin(time * 2.0) * 0.3 + 1.0
            light.data.energy = light.data.energy * energy_offset
            light.data.keyframe_insert(data_path="energy", frame=frame)
        
        # Set interpolation mode
        if light.animation_data and light.animation_data.action:
            for fcurve in light.animation_data.action.fcurves:
                for keyframe in fcurve.keyframe_points:
                    keyframe.interpolation = 'BEZIER'

class PROCLIGHT_OT_select_light_group(Operator):
    """Select all lights in the group"""
    bl_idname = "procedural_lighting.select_light_group"
    bl_label = "Select Light Group"
    bl_options = {'REGISTER', 'UNDO'}
    
    def execute(self, context):
        props = context.scene.procedural_lighting
        
        # Deselect all
        bpy.ops.object.select_all(action='DESELECT')
        
        # Select lights in group
        count = 0
        for obj in bpy.data.objects:
            if obj.name.startswith(props.light_group_name):
                obj.select_set(True)
                count += 1
        
        self.report({'INFO'}, f"Selected {count} objects")
        return {'FINISHED'}

class PROCLIGHT_OT_bake_lighting(Operator):
    """Bake lighting to lightmaps"""
    bl_idname = "procedural_lighting.bake_lighting"
    bl_label = "Bake Lighting"
    bl_options = {'REGISTER', 'UNDO'}
    
    def execute(self, context):
        # Ensure we're in Cycles
        if context.scene.render.engine != 'CYCLES':
            context.scene.render.engine = 'CYCLES'
        
        # Set up baking
        bpy.context.scene.cycles.bake_type = 'DIFFUSE'
        bpy.context.scene.render.bake.use_pass_direct = True
        bpy.context.scene.render.bake.use_pass_indirect = True
        
        # Select all mesh objects
        bpy.ops.object.select_all(action='DESELECT')
        for obj in bpy.data.objects:
            if obj.type == 'MESH':
                obj.select_set(True)
        
        # Bake
        try:
            bpy.ops.object.bake(type='DIFFUSE')
            self.report({'INFO'}, "Lighting baked successfully")
        except Exception as e:
            self.report({'ERROR'}, f"Baking failed: {str(e)}")
        
        return {'FINISHED'}

class PROCLIGHT_OT_optimize_lights(Operator):
    """Optimize light setup for performance"""
    bl_idname = "procedural_lighting.optimize_lights"
    bl_label = "Optimize Lights"
    bl_options = {'REGISTER', 'UNDO'}
    
    def execute(self, context):
        props = context.scene.procedural_lighting
        
        # Find all lights in the group
        lights = []
        for obj in bpy.data.objects:
            if obj.name.startswith(props.light_group_name) and obj.type == 'LIGHT':
                lights.append(obj)
        
        if not lights:
            self.report({'WARNING'}, "No lights found to optimize")
            return {'FINISHED'}
        
        # Optimization settings
        for light in lights:
            light_data = light.data
            
            # Reduce shadow samples for performance
            if hasattr(light_data, 'shadow_soft_size'):
                light_data.shadow_soft_size = min(light_data.shadow_soft_size, 1.0)
            
            # Limit light radius
            if hasattr(light_data, 'shadow_buffer_size'):
                light_data.shadow_buffer_size = '1024'
        
        self.report({'INFO'}, f"Optimized {len(lights)} lights")
        return {'FINISHED'}

def get_light_distribution_stats(context):
    """Get statistics about light distribution"""
    props = context.scene.procedural_lighting
    
    lights = []
    for obj in bpy.data.objects:
        if obj.name.startswith(props.light_group_name) and obj.type == 'LIGHT':
            lights.append(obj)
    
    if not lights:
        return {"count": 0}
    
    # Calculate statistics
    locations = [light.location for light in lights]
    energies = [light.data.energy for light in lights]
    
    # Distance from center
    distances = [location.length for location in locations]
    avg_distance = sum(distances) / len(distances)
    
    # Energy stats
    avg_energy = sum(energies) / len(energies)
    min_energy = min(energies)
    max_energy = max(energies)
    
    return {
        "count": len(lights),
        "avg_distance": avg_distance,
        "avg_energy": avg_energy,
        "min_energy": min_energy,
        "max_energy": max_energy
    }

def create_light_preview_material():
    """Create a material for light preview"""
    material = bpy.data.materials.new(name="LightPreview")
    material.use_nodes = True
    material.node_tree.clear()
    
    # Create nodes
    output_node = material.node_tree.nodes.new(type='ShaderNodeOutputMaterial')
    emission_node = material.node_tree.nodes.new(type='ShaderNodeEmission')
    
    # Set properties
    emission_node.inputs['Strength'].default_value = 1.0
    emission_node.inputs['Color'].default_value = (1.0, 1.0, 0.8, 1.0)
    
    # Connect nodes
    material.node_tree.links.new(emission_node.outputs['Emission'], output_node.inputs['Surface'])
    
    return material

def setup_world_lighting(hdri_path=None):
    """Set up world lighting"""
    world = bpy.context.scene.world
    
    if not world:
        world = bpy.data.worlds.new("World")
        bpy.context.scene.world = world
    
    # Enable nodes
    world.use_nodes = True
    world.node_tree.nodes.clear()
    
    # Create nodes
    output_node = world.node_tree.nodes.new(type='ShaderNodeOutputWorld')
    background_node = world.node_tree.nodes.new(type='ShaderNodeBackground')
    
    if hdri_path:
        # Use HDRI
        env_texture = world.node_tree.nodes.new(type='ShaderNodeTexEnvironment')
        env_texture.image = bpy.data.images.load(hdri_path)
        
        # Connect nodes
        world.node_tree.links.new(env_texture.outputs['Color'], background_node.inputs['Color'])
    else:
        # Use solid color
        background_node.inputs['Color'].default_value = (0.1, 0.1, 0.1, 1.0)
    
    background_node.inputs['Strength'].default_value = 0.1
    
    # Connect to output
    world.node_tree.links.new(background_node.outputs['Background'], output_node.inputs['Surface'])

classes = [
    PROCLIGHT_OT_animate_lights,
    PROCLIGHT_OT_select_light_group,
    PROCLIGHT_OT_bake_lighting,
    PROCLIGHT_OT_optimize_lights,
]

def register():
    for cls in classes:
        bpy.utils.register_class(cls)

def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls) 