"""
Sample Scene Script for Procedural Lighting System
This script demonstrates how to use the addon programmatically
and creates a sample scene with procedural lighting.

Run this script in Blender with the addon enabled to see a demonstration.
"""

import bpy
import bmesh
import mathutils
from mathutils import Vector

def clear_scene():
    """Clear the default scene"""
    # Delete default objects
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete(use_global=False)
    
    # Clear materials
    for material in bpy.data.materials:
        bpy.data.materials.remove(material)

def create_sample_objects():
    """Create sample objects to light"""
    
    # Create a ground plane
    bpy.ops.mesh.primitive_plane_add(size=20, location=(0, 0, 0))
    ground = bpy.context.object
    ground.name = "Ground"
    
    # Create ground material
    ground_material = bpy.data.materials.new(name="GroundMaterial")
    ground_material.use_nodes = True
    ground_material.node_tree.nodes.clear()
    
    # Setup ground material nodes
    output_node = ground_material.node_tree.nodes.new(type='ShaderNodeOutputMaterial')
    principled = ground_material.node_tree.nodes.new(type='ShaderNodeBsdfPrincipled')
    
    # Set material properties
    principled.inputs['Base Color'].default_value = (0.3, 0.3, 0.3, 1.0)
    principled.inputs['Roughness'].default_value = 0.7
    
    # Connect nodes
    ground_material.node_tree.links.new(principled.outputs['BSDF'], output_node.inputs['Surface'])
    ground.data.materials.append(ground_material)
    
    # Create a central sphere
    bpy.ops.mesh.primitive_uv_sphere_add(radius=2, location=(0, 0, 2))
    sphere = bpy.context.object
    sphere.name = "CenterSphere"
    
    # Create sphere material
    sphere_material = bpy.data.materials.new(name="SphereMaterial")
    sphere_material.use_nodes = True
    sphere_material.node_tree.nodes.clear()
    
    # Setup sphere material nodes
    output_node = sphere_material.node_tree.nodes.new(type='ShaderNodeOutputMaterial')
    principled = sphere_material.node_tree.nodes.new(type='ShaderNodeBsdfPrincipled')
    
    # Set material properties
    principled.inputs['Base Color'].default_value = (0.8, 0.2, 0.2, 1.0)
    principled.inputs['Metallic'].default_value = 0.0
    principled.inputs['Roughness'].default_value = 0.3
    
    # Connect nodes
    sphere_material.node_tree.links.new(principled.outputs['BSDF'], output_node.inputs['Surface'])
    sphere.data.materials.append(sphere_material)
    
    # Create some cubes around the scene
    cube_positions = [
        (5, 5, 1), (-5, 5, 1), (5, -5, 1), (-5, -5, 1),
        (0, 7, 1), (0, -7, 1), (7, 0, 1), (-7, 0, 1)
    ]
    
    for i, pos in enumerate(cube_positions):
        bpy.ops.mesh.primitive_cube_add(size=1.5, location=pos)
        cube = bpy.context.object
        cube.name = f"Cube_{i+1}"
        
        # Create cube material
        cube_material = bpy.data.materials.new(name=f"CubeMaterial_{i+1}")
        cube_material.use_nodes = True
        cube_material.node_tree.nodes.clear()
        
        # Setup cube material nodes
        output_node = cube_material.node_tree.nodes.new(type='ShaderNodeOutputMaterial')
        principled = cube_material.node_tree.nodes.new(type='ShaderNodeBsdfPrincipled')
        
        # Vary the colors
        hue = i / len(cube_positions)
        color = mathutils.Color((hue, 0.7, 0.8))
        color.hsv = (hue, 0.7, 0.8)
        
        principled.inputs['Base Color'].default_value = (*color, 1.0)
        principled.inputs['Roughness'].default_value = 0.4
        
        # Connect nodes
        cube_material.node_tree.links.new(principled.outputs['BSDF'], output_node.inputs['Surface'])
        cube.data.materials.append(cube_material)

def setup_camera():
    """Setup camera for the scene"""
    bpy.ops.object.camera_add(location=(8, -8, 6))
    camera = bpy.context.object
    camera.name = "MainCamera"
    
    # Point camera at the center sphere
    constraint = camera.constraints.new(type='TRACK_TO')
    constraint.target = bpy.data.objects.get("CenterSphere")
    constraint.track_axis = 'TRACK_NEGATIVE_Z'
    constraint.up_axis = 'UP_Y'
    
    # Set as active camera
    bpy.context.scene.camera = camera

def setup_render_settings():
    """Setup render settings for the scene"""
    scene = bpy.context.scene
    
    # Set render engine to Cycles
    scene.render.engine = 'CYCLES'
    
    # Set resolution
    scene.render.resolution_x = 1920
    scene.render.resolution_y = 1080
    
    # Set samples (lower for faster preview)
    scene.cycles.samples = 128
    
    # Enable denoising
    scene.cycles.use_denoising = True

def demo_procedural_lighting():
    """Demonstrate procedural lighting features"""
    
    # Get the procedural lighting properties
    props = bpy.context.scene.procedural_lighting
    
    print("=== Procedural Lighting Demo ===")
    print("Creating different lighting patterns...")
    
    # Demo 1: Circle pattern
    print("\n1. Circle Pattern Demo")
    props.pattern_type = 'CIRCLE'
    props.light_count = 8
    props.radius = 12.0
    props.height = 8.0
    props.base_energy = 30.0
    props.energy_variation = 0.2
    props.base_color = (1.0, 0.9, 0.8)
    props.color_variation = 0.1
    props.light_group_name = "CircleLights"
    
    # Generate lights
    bpy.ops.procedural_lighting.generate_lights()
    print(f"Generated {props.light_count} lights in circle pattern")
    
    # Wait a moment, then clear
    bpy.ops.wm.redraw_timer(type='DRAW_WIN_SWAP', iterations=30)
    
    # Demo 2: Grid pattern
    print("\n2. Grid Pattern Demo")
    props.pattern_type = 'GRID'
    props.light_count = 9
    props.radius = 10.0
    props.height = 6.0
    props.base_energy = 25.0
    props.base_color = (0.8, 0.9, 1.0)
    props.light_group_name = "GridLights"
    
    # Clear previous lights and generate new ones
    bpy.ops.procedural_lighting.clear_lights()
    bpy.ops.procedural_lighting.generate_lights()
    print(f"Generated {props.light_count} lights in grid pattern")
    
    # Demo 3: Setup volumetrics
    print("\n3. Volumetric Lighting Demo")
    props.use_volumetrics = True
    props.volumetric_density = 0.1
    bpy.ops.procedural_lighting.setup_volumetrics()
    print("Volumetric lighting configured")
    
    # Demo 4: Setup bloom
    print("\n4. Bloom Effect Demo")
    props.use_bloom = True
    props.bloom_intensity = 0.7
    bpy.ops.procedural_lighting.setup_bloom()
    print("Bloom effect configured")
    
    # Demo 5: Animation
    print("\n5. Animation Demo")
    props.animate_lights = True
    props.animation_speed = 1.5
    bpy.ops.procedural_lighting.animate_lights()
    print("Light animation created")
    
    # Demo 6: Load built-in presets
    print("\n6. Built-in Presets Demo")
    bpy.ops.procedural_lighting.load_builtin_presets()
    print(f"Loaded {len(props.presets)} built-in presets")
    
    # Demo 7: Final spiral pattern
    print("\n7. Final Spiral Pattern Demo")
    props.pattern_type = 'SPIRAL'
    props.light_count = 12
    props.radius = 8.0
    props.height = 5.0
    props.base_energy = 40.0
    props.base_color = (1.0, 0.7, 0.3)
    props.light_group_name = "SpiralLights"
    
    bpy.ops.procedural_lighting.clear_lights()
    bpy.ops.procedural_lighting.generate_lights()
    print(f"Generated {props.light_count} lights in spiral pattern")
    
    print("\n=== Demo Complete ===")
    print("You can now:")
    print("- Adjust light properties in the sidebar")
    print("- Switch between different patterns")
    print("- Try the animation controls")
    print("- Render the scene to see bloom and volumetrics")

def main():
    """Main function to run the demo"""
    print("Starting Procedural Lighting System Demo...")
    
    # Check if addon is enabled
    if not hasattr(bpy.context.scene, 'procedural_lighting'):
        print("ERROR: Procedural Lighting System addon is not enabled!")
        print("Please enable the addon in Blender preferences first.")
        return
    
    # Clear scene and create sample objects
    clear_scene()
    create_sample_objects()
    setup_camera()
    setup_render_settings()
    
    # Run the lighting demo
    demo_procedural_lighting()
    
    print("\nDemo scene created successfully!")
    print("Switch to rendered view to see the full effect.")

if __name__ == "__main__":
    main() 