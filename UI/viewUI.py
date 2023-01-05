import bpy

class ODYENVDEV_PT_view_panel_settings(bpy.types.Panel):
    """Creates a Panel in the view 3d properties window"""
    bl_label = "Environmen Settings"
    bl_idname = "view_panel_env_settings"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Odyssey'

    def draw(self, context):
        layout = self.layout

        scene = context.scene
        odyenvdev = scene.odyenvdev
        
        panel = layout.column()
        
        panel.label(text="Environment")