import bpy
from bpy.types import Panel

class PROCLIGHT_PT_main_panel(Panel):
    """Main procedural lighting panel"""
    bl_label = "Procedural Lighting"
    bl_idname = "PROCLIGHT_PT_main_panel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Lighting"
    
    def draw(self, context):
        layout = self.layout
        props = context.scene.procedural_lighting
        
        # Title
        layout.label(text="Procedural Lighting System", icon='LIGHT_SUN')
        layout.separator()
        
        # Pattern Selection
        box = layout.box()
        box.label(text="Pattern Generation", icon='MESH_GRID')
        box.prop(props, "pattern_type")
        box.prop(props, "light_count")
        box.prop(props, "radius")
        box.prop(props, "height")
        
        # Light Properties
        box = layout.box()
        box.label(text="Light Properties", icon='LIGHT')
        box.prop(props, "base_energy")
        box.prop(props, "energy_variation")
        box.prop(props, "base_color")
        # Generation Buttons
        row = box.row(align=True)
        row.operator("procedural_lighting.generate_lights", icon='ADD')
        row.operator("procedural_lighting.clear_lights", icon='TRASH')
        box.prop(props, "color_variation")
        # Global Intensity
        box.separator()
        box.label(text="Global Intensity", icon='LIGHT_HEMI')
        box.prop(props, "global_intensity", slider=True)
        box.prop(props, "intensity_curve")
        box.operator("procedural_lighting.apply_global_intensity", icon='FILE_TICK')
        
        # Mood Renderer
        box = layout.box()
        box.label(text="Mood Renderer", icon='COLOR')
        box.prop(props, "mood_type")
        box.prop(props, "mood_intensity", slider=True)
        # Always show Apply and Reset buttons
        row = box.row(align=True)
        row.operator("procedural_lighting.apply_mood", icon='COLORSET_01_VEC', text="Apply Mood")
        row.operator("procedural_lighting.reset_mood", icon='LOOP_BACK', text="Reset Mood")
        
        # Management
        box = layout.box()
        box.label(text="Management", icon='SETTINGS')
        box.prop(props, "light_group_name")
        box.prop(props, "auto_parent")

class PROCLIGHT_PT_effects_panel(Panel):
    """Rendering effects panel"""
    bl_label = "Rendering Effects"
    bl_idname = "PROCLIGHT_PT_effects_panel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Lighting"
    bl_parent_id = "PROCLIGHT_PT_main_panel"
    
    def draw(self, context):
        layout = self.layout
        props = context.scene.procedural_lighting
        
        # Volumetrics
        box = layout.box()
        box.label(text="Volumetric Lighting", icon='VOLUME_DATA')
        box.prop(props, "use_volumetrics")
        
        if props.use_volumetrics:
            box.prop(props, "volumetric_density")
            box.operator("procedural_lighting.setup_volumetrics", icon='VOLUME_DATA')
        
        # Bloom
        box = layout.box()
        box.label(text="Bloom Effect", icon='LIGHT_SUN')
        box.prop(props, "use_bloom")
        
        if props.use_bloom:
            box.prop(props, "bloom_intensity")
            box.operator("procedural_lighting.setup_bloom", icon='LIGHT_SUN')

class PROCLIGHT_PT_animation_panel(Panel):
    """Animation panel"""
    bl_label = "Animation"
    bl_idname = "PROCLIGHT_PT_animation_panel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Lighting"
    bl_parent_id = "PROCLIGHT_PT_main_panel"
    
    def draw(self, context):
        layout = self.layout
        props = context.scene.procedural_lighting
        
        layout.prop(props, "animate_lights")
        
        if props.animate_lights:
            layout.prop(props, "animation_speed")
            layout.operator("procedural_lighting.animate_lights", icon='PLAY')

class PROCLIGHT_PT_presets_panel(Panel):
    """Presets panel"""
    bl_label = "Presets"
    bl_idname = "PROCLIGHT_PT_presets_panel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Lighting"
    bl_parent_id = "PROCLIGHT_PT_main_panel"
    
    def draw(self, context):
        layout = self.layout
        props = context.scene.procedural_lighting
        
        # Presets list
        row = layout.row()
        row.template_list(
            "PROCLIGHT_UL_presets",
            "",
            props,
            "presets",
            props,
            "active_preset_index",
            rows=3
        )
        
        # Preset buttons
        col = row.column(align=True)
        col.operator("procedural_lighting.save_preset", icon='ADD', text="")
        col.operator("procedural_lighting.remove_preset", icon='REMOVE', text="")
        
        # Load preset
        layout.operator("procedural_lighting.load_preset", icon='IMPORT')

class PROCLIGHT_UL_presets(bpy.types.UIList):
    """UI List for presets"""
    def draw_item(self, context, layout, data, item, icon, active_data, active_propname):
        if self.layout_type in {'DEFAULT', 'COMPACT'}:
            layout.prop(item, "name", text="", emboss=False, icon='LIGHT')
        elif self.layout_type in {'GRID'}:
            layout.alignment = 'CENTER'
            layout.label(text="", icon='LIGHT')

class PROCLIGHT_PT_info_panel(Panel):
    """Information panel"""
    bl_label = "Info & Tips"
    bl_idname = "PROCLIGHT_PT_info_panel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Lighting"
    bl_parent_id = "PROCLIGHT_PT_main_panel"
    bl_options = {'DEFAULT_CLOSED'}
    
    def draw(self, context):
        layout = self.layout
        
        # Tips
        box = layout.box()
        box.label(text="Tips:", icon='INFO')
        box.label(text="• Use Circle for rim lighting")
        box.label(text="• Grid works well for studios")
        box.label(text="• Random creates organic feel")
        box.label(text="• Spiral adds drama")
        box.label(text="• Wave creates movement")
        
        # Requirements
        box = layout.box()
        box.label(text="Requirements:", icon='ERROR')
        box.label(text="• Cycles for volumetrics")
        box.label(text="• Compositor for bloom")
        
        # Performance
        box = layout.box()
        box.label(text="Performance:", icon='TIME')
        box.label(text="• Limit lights for real-time")
        box.label(text="• Use lower density for volumes")

classes = [
    PROCLIGHT_PT_main_panel,
    PROCLIGHT_PT_effects_panel,
    PROCLIGHT_PT_animation_panel,
    PROCLIGHT_PT_presets_panel,
    PROCLIGHT_UL_presets,
    PROCLIGHT_PT_info_panel,
]

def register():
    for cls in classes:
        bpy.utils.register_class(cls)

def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls) 