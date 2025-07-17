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
        
        # Apply energy with variation and global intensity
        energy_var = random.uniform(-props.energy_variation, props.energy_variation)
        base_energy = props.base_energy * (1 + energy_var)
        
        # Apply global intensity with curve
        final_energy = self.apply_intensity_curve(base_energy, props.global_intensity, props.intensity_curve)
        light_data.energy = final_energy
        
        # Apply color with variation
        color_var = random.uniform(-props.color_variation, props.color_variation)
        color = [max(0, min(1, c + color_var)) for c in props.base_color]
        light_data.color = color
        
        return light_object
    
    def apply_intensity_curve(self, base_energy, intensity, curve_type):
        """Apply an intensity curve to energy value"""
        if curve_type == 'LINEAR':
            return base_energy * intensity
        elif curve_type == 'EXPONENTIAL':
            return base_energy * (intensity ** 2)
        elif curve_type == 'LOGARITHMIC':
            return base_energy * (1 + math.log(max(1, intensity)))
        else:
            return base_energy * intensity
    
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
        # Clear nodes (compatible with Blender 4.x, no clear method)
        nodes = material.node_tree.nodes
        while nodes:
            nodes.remove(nodes[0])
        
        # Create nodes
        output_node = material.node_tree.nodes.new(type='ShaderNodeOutputMaterial')
        volume_scatter = material.node_tree.nodes.new(type='ShaderNodeVolumeScatter')
        
        # Set properties
        volume_scatter.inputs['Density'].default_value = props.volumetric_density
        # base_color needs to be a 3-element tuple, add1.0ke it RGBA
        color = tuple(props.base_color) + (1.0,)
        volume_scatter.inputs['Color'].default_value = color
        
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
        glare.threshold = max(0.0, 0.3 - props.bloom_intensity * 0.3)  # Lower threshold, more visible bloom
        glare.mix = 0.8  # Increase mix value for more visible bloom effect
        glare.size = 12  # Increase size for larger bloom range
        
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

class PROCLIGHT_OT_apply_global_intensity(Operator):
    """Apply global intensity to all procedural lights"""
    bl_idname = "procedural_lighting.apply_global_intensity"
    bl_label = "Apply Global Intensity"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        import math
        props = context.scene.procedural_lighting
        for obj in bpy.data.objects:
            if obj.name.startswith(props.light_group_name) and obj.type == 'LIGHT':
                # Recalculate energy
                base_energy = props.base_energy
                # Assuming no energy and color variation, can be extended if needed
                if props.intensity_curve == 'LINEAR':
                    obj.data.energy = base_energy * props.global_intensity
                elif props.intensity_curve == 'EXPONENTIAL':
                    obj.data.energy = base_energy * (props.global_intensity ** 2)
                elif props.intensity_curve == 'LOGARITHMIC':
                    obj.data.energy = base_energy * (1 + math.log(max(1, props.global_intensity)))
                else:
                    obj.data.energy = base_energy * props.global_intensity
        self.report({'INFO'}, "Applied global intensity to all lights")
        return {'FINISHED'}

class PROCLIGHT_OT_apply_mood(Operator):
    """Apply mood lighting to scene"""
    bl_idname = "procedural_lighting.apply_mood"
    bl_label = "Apply Mood"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        props = context.scene.procedural_lighting
        
        if props.mood_type == 'NONE':
            self.report({'INFO'}, "No mood selected")
            return {'FINISHED'}
        
        # Apply mood to world only
        self.apply_mood_to_world(context, props)
        
        # Don't apply mood to lights, keep user manually adjusted settings
        # if props.auto_apply_mood:
        #     self.apply_mood_to_lights(context, props)
        
        # Set mood as applied
        props.mood_applied = True
        
        self.report({'INFO'}, f"Applied {props.mood_type} mood (world only, lights unchanged)")
        return {'FINISHED'}
    
    def apply_mood_to_world(self, context, props):
        """Apply mood to world background"""
        world = context.scene.world
        if not world:
            world = bpy.data.worlds.new("World")
            context.scene.world = world
        
        world.use_nodes = True
        nodes = world.node_tree.nodes
        links = world.node_tree.links
        
        # Clear existing nodes
        nodes.clear()
        
        # Create output node
        output_node = nodes.new(type='ShaderNodeOutputWorld')
        
        # Get mood colors
        bg_color, bg_strength = self.get_mood_colors(props.mood_type, props.mood_intensity)
        
        # Create background node
        bg_node = nodes.new(type='ShaderNodeBackground')
        # Ensure color is 4-element RGBA format
        if len(bg_color) == 3:
            bg_node.inputs['Color'].default_value = (*bg_color, 1.0)
        else:
            bg_node.inputs['Color'].default_value = bg_color
        bg_node.inputs['Strength'].default_value = bg_strength
        
        # Connect nodes
        links.new(bg_node.outputs['Background'], output_node.inputs['Surface'])
    
    def apply_mood_to_lights(self, context, props):
        """Apply mood to existing lights"""
        for obj in bpy.data.objects:
            if obj.name.startswith(props.light_group_name) and obj.type == 'LIGHT':
                light_color, light_energy = self.get_mood_light_settings(props.mood_type, props.mood_intensity)
                
                # Apply color
                obj.data.color = light_color
                
                # Apply energy
                obj.data.energy = light_energy
    
    def get_mood_colors(self, mood_type, intensity):
        """Get background color and strength for mood"""
        mood_colors = {
            'WARM': ((1.0, 0.6, 0.1, 1.0), 0.6), # 典型暖橙色
            'COLD': ((0.2, 0.4, 0.8, 1.0), 0.4), # 冷蓝色
            'DRAMATIC': ((0.05, 0.0, 0.1, 1.0), 0.5), # 深紫色
            'ROMANTIC': ((0.7, 0.0, 0.3, 1.0), 0.6), # 粉紫色
            'MYSTERIOUS': ((0.05, 0.05, 0.15, 1.0), 0.5), # 深蓝色
            'ENERGETIC': ((0.9, 0.0, 0.2, 1.0), 0.9), # 亮黄色
            'CALM': ((0.4, 0.6, 0.8, 1.0), 0.5), # 淡蓝色
            'SUNSET': ((0.9, 0.4, 0.1, 1.0), 0.7), # 金橙色
            'NIGHT': ((0.02, 0.03, 0.08, 1.0), 0.3), # 深蓝色
        }
        if mood_type in mood_colors:
            color, strength = mood_colors[mood_type]
            strength *= intensity
            return color, strength
        else:
            return ((0.1, 0.1, 0.1, 1.0), 0.1)

    def get_mood_light_settings(self, mood_type, intensity):
        """Get light color and energy for mood"""
        mood_lights = {
            'WARM': ((1.0, 0.7, 0.2), 12.0),      # 暖黄光
            'COLD': ((0.4, 0.7, 1.0), 10.0),      # 冷蓝光
            'DRAMATIC': ((1.0, 0.1, 0.1), 15.0),  # 红光
            'ROMANTIC': ((1.0, 0.5, 0.7), 8.0),   # 粉光
            'MYSTERIOUS': ((0.0, 0.2, 0.4), 7.0), # 蓝光
            'ENERGETIC': ((1.0, 1.0, 0.3), 18.0), # 黄光
            'CALM': ((0.0, 0.6, 0.8), 7.0),       # 蓝光
            'SUNSET': ((1.0, 0.6, 0.2), 11.0),    # 橙光
            'NIGHT': ((0.0, 0.1, 0.2), 5.0),      # 夜光
        }
        if mood_type in mood_lights:
            color, energy = mood_lights[mood_type]
            energy *= intensity
            return color, energy
        else:
            return ((1.0, 1.0, 1.0), 10.0)

class PROCLIGHT_OT_reset_mood(Operator):
    """Reset mood and restore original lighting"""
    bl_idname = "procedural_lighting.reset_mood"
    bl_label = "Reset Mood"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        props = context.scene.procedural_lighting
        
        # Reset world to default
        world = context.scene.world
        if world and world.use_nodes:
            nodes = world.node_tree.nodes
            links = world.node_tree.links
            
            # Clear existing nodes
            nodes.clear()
            
            # Create default background
            output_node = nodes.new(type='ShaderNodeOutputWorld')
            bg_node = nodes.new(type='ShaderNodeBackground')
            bg_node.inputs['Color'].default_value = (0.1, 0.1, 0.1, 1.0)
            bg_node.inputs['Strength'].default_value = 0.1
            # Connect nodes
            links.new(bg_node.outputs['Background'], output_node.inputs['Surface'])
        
        # Don't reset lights, keep user manually adjusted settings
        
        # Reset mood state
        props.mood_applied = False
        props.mood_type = 'NONE'
        self.report({'INFO'}, "Mood reset to default (lights unchanged)")
        return {'FINISHED'}

classes = [
    PROCLIGHT_OT_generate_lights,
    PROCLIGHT_OT_clear_lights,
    PROCLIGHT_OT_setup_volumetrics,
    PROCLIGHT_OT_setup_bloom,
    PROCLIGHT_OT_save_preset,
    PROCLIGHT_OT_load_preset,
    PROCLIGHT_OT_apply_global_intensity,
    PROCLIGHT_OT_apply_mood,
    PROCLIGHT_OT_reset_mood,
]

def register():
    for cls in classes:
        bpy.utils.register_class(cls)

def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls) 