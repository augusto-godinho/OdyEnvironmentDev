import bpy

class ODYENVDEV_PT_view_panel_settings(bpy.types.Panel):
    """Creates a Panel in the view 3d properties window"""
    bl_label = "Environmen Settings"
    bl_idname = "view_panel_env_settings"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Ody Environment'

    def draw(self, context):
        layout = self.layout

        scene = context.scene
        odyenvdev = scene.odyenvdev

        obj = context.object
        
        panel = layout.column()
        
        col = panel.column()
        col.prop(odyenvdev,'arena_name')
        col.prop(obj,'material_type')

        col.separator()
    
        box = col.box()
        boxcol = box.column()
        boxcol.label(text="Tools:")
        if obj.material_type == 'STV':
            boxcol.operator("odyenvironmentdev.color_id_from_stampmap_main", text="Convert from main")
            boxcol.operator("odyenvironmentdev.generate_uv_maps", text="Generate UV Maps")


class ODYENVDEV_PT_view_panel_actions(bpy.types.Panel):
    """Creates a Panel in the view 3d properties window"""
    bl_label = "Environment Operations"
    bl_idname = "view_panel_actions"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Odyssey'

    def draw(self, context):
        layout = self.layout

        scene = context.scene
        odyenvdev = scene.odyenvironmentdev
        
        panel = layout.column()
        panel.label(text="Clean up")
        box = layout.column()
        clean_panel = box.box()
        clean_panel.operator("odyenvironmentdev.clean_duplicated_nodes")

#>>>------STAMP MAP PANELS------->
class ODYENVDEV_PT_view_panel_main_stampmapvertex(bpy.types.Panel):
    bl_label = "Materials Controls"
    bl_idname = "view_panel_main_stampmapvertex"
    bl_space_type = "VIEW_3D"
    bl_region_type = 'UI'
    bl_category = "Ody Environment"
    
    flow : bpy.props.StringProperty(default="0.02;r")

    def draw(self, context):
        scene = context.scene
        odyenvdev = scene.odyenvdev
        vertexcolors = scene.OdyEnvDevVertexColorDic
        obj = context.object

        if obj.material_type == 'STO':
            drawStampMapMenu(self, odyenvdev, vertexcolors)

        if obj.material_type == 'STV':
            drawVertexStampMapMenu(self, odyenvdev, vertexcolors)

            
def drawStampMapMenu(self, odyenvdev, vertexcolors):
    layout = self.layout
    col = layout.column()

    col.label(text="Main")
    col.prop(odyenvdev,'set_vertex_code_face')
    col.operator("odyenvironmentdev.set_vertex_code", text="Base").flow = "0.02;r"
    col.operator("odyenvironmentdev.set_vertex_code", text="Secondary").flow = "0.125;r"
    col.operator("odyenvironmentdev.set_vertex_code", text="Accent").flow = "0.250;r"
    col.operator("odyenvironmentdev.set_vertex_code", text="Floor Base").flow = "0.375;r"
    col.operator("odyenvironmentdev.set_vertex_code", text="Floor Accent").flow = "0.750;r"
    col.operator("odyenvironmentdev.set_vertex_code", text="Team 1").flow = "0.500;r"
    col.operator("odyenvironmentdev.set_vertex_code", text="Team 2").flow = "0.625;r"
    col.operator("odyenvironmentdev.set_vertex_code", text="Secondary Accent 1").flow = "0.875;r"
    col.operator("odyenvironmentdev.set_vertex_code", text="Secondary Accent 2").flow = "1.0;r"
    
    col.separator()
    col.label(text="Emissive")
    col.operator("odyenvironmentdev.set_vertex_code", text="Off").flow = "0.1;g"
    col.operator("odyenvironmentdev.set_vertex_code", text="Default").flow = "0.250;g"
    col.operator("odyenvironmentdev.set_vertex_code", text="Team1").flow = "0.500;g"
    col.operator("odyenvironmentdev.set_vertex_code", text="Team2").flow = "0.750;g"
    col.operator("odyenvironmentdev.set_vertex_code", text="Accent").flow = "1;g"

    col.separator()
    col.label(text="Surface")
    col.operator("odyenvironmentdev.set_vertex_code", text="Surface A").flow = "0.250;b"
    col.operator("odyenvironmentdev.set_vertex_code", text="Surface B").flow = "0.500;b"
    col.operator("odyenvironmentdev.set_vertex_code", text="Surface C").flow = "0.750;b"
    col.operator("odyenvironmentdev.set_vertex_code", text="Surface D").flow = "0.900;b"

        
def drawVertexStampMapMenu(self, odyenvdev, vertexcolors):        
    layout = self.layout
    col = layout.column()
    vertex_box = col.box()
    vertex_box.label(text="Dictionary:")
    for cg in vertexcolors:
        row = vertex_box.row()
        crow = row.row()
        crow.operator("odyenvironmentdev.assign_vertex_to_color_id", text="", icon='MOD_LINEART').color_id = text=cg.name
        crow.prop(cg, "color_value", text=cg.name)
        oprow = row.row()
        oprow.operator("odyenvironmentdev.update_color_ids", text="", icon='FILE_REFRESH').color_id = text=cg.name
        oprow.operator("odyenvironmentdev.rename_color_id", text="", icon='SORTALPHA').color_id = text=cg.name
    vertex_box.separator()

    col.operator("odyenvironmentdev.update_color_ids", text="Update Colors").color_id = 'UPDATE_ALL'
    col.operator("odyenvironmentdev.add_new_color_id", text="Add Color ID")
    col.operator("odyenvironmentdev.assign_vertex_to_color_id", text="Remove from ID").color_id = 'FREE'
    col.operator("odyenvironmentdev.clear_all_color_ids", text="Clear all color Ids")
    
    col.separator()
    col.label(text="Emissive")
    col.operator("odyenvironmentdev.set_uv_es", text="Off").flow = "0.1;u"
    col.operator("odyenvironmentdev.set_uv_es", text="Default").flow = "0.250;u"
    col.operator("odyenvironmentdev.set_uv_es", text="Team1").flow = "0.500;u"
    col.operator("odyenvironmentdev.set_uv_es", text="Team2").flow = "0.750;u"
    col.operator("odyenvironmentdev.set_uv_es", text="Accent").flow = "0.9;u"
    col.operator("odyenvironmentdev.set_uv_es", text="From Main").flow = "1.0;u"

    col.separator()
    col.label(text="Surface")
    col.operator("odyenvironmentdev.set_uv_es", text="Surface A").flow = "0.250;v"
    col.operator("odyenvironmentdev.set_uv_es", text="Surface B").flow = "0.500;v"
    col.operator("odyenvironmentdev.set_uv_es", text="Surface C").flow = "0.750;v"
    col.operator("odyenvironmentdev.set_uv_es", text="Surface D").flow = "0.900;v"



class ODYENVDEV_PT_view_panel_emissive_stampmapvertex(bpy.types.Panel):
    bl_label = "Emissive"
    bl_idname = "view_panel_emissive_stampmapvertex"
    bl_space_type = "VIEW_3D"
    bl_region_type = 'UI'
    bl_category = "Stamp Map"
    
    flow : bpy.props.StringProperty(default="0.1;g")
    def draw(self, context):

        scene = context.scene
        odyenvdev = scene.odyenvdev

        layout = self.layout
        col = layout.column()
        col.prop(odyenvdev,'set_vertex_code_face')
        col.operator("odyenvironmentdev.set_vertex_code", text="Off").flow = "0.1;g"
        col.operator("odyenvironmentdev.set_vertex_code", text="Default").flow = "0.250;g"
        col.operator("odyenvironmentdev.set_vertex_code", text="Team1").flow = "0.500;g"
        col.operator("odyenvironmentdev.set_vertex_code", text="Team2").flow = "0.750;g"
        col.operator("odyenvironmentdev.set_vertex_code", text="Accent").flow = "1;g"

class ODYENVDEV_PT_view_panel_patterns_stampmapvertex(bpy.types.Panel):
    bl_label = "Surface Patterns"
    bl_idname = "view_panel_patterns_stampmapvertex"
    bl_space_type = "VIEW_3D"
    bl_region_type = 'UI'
    bl_category = "Stamp Map"
    
    flow : bpy.props.StringProperty(default="0.1;g")
    def draw(self, context):

        scene = context.scene
        odyenvdev = scene.odyenvdev

        layout = self.layout
        col = layout.column()
        col.prop(odyenvdev,'set_vertex_code_face')
        col.operator("odyenvironmentdev.set_vertex_code", text="Surface A").flow = "0.250;b"
        col.operator("odyenvironmentdev.set_vertex_code", text="Surface B").flow = "0.500;b"
        col.operator("odyenvironmentdev.set_vertex_code", text="Surface C").flow = "0.750;b"
        col.operator("odyenvironmentdev.set_vertex_code", text="Surface D").flow = "0.900;b"
    
    
class ODYENVDEV_PT_view_panel_surface_stampmapvertex(bpy.types.Panel):
    bl_label = "Surface"
    bl_idname = "view_panel_surface_stampmapvertex"
    bl_space_type = "VIEW_3D"
    bl_region_type = 'UI'
    bl_category = "Stamp Map"
    
    flow : bpy.props.StringProperty(default="0.1;g")
    def draw(self, context):

        scene = context.scene
        odyenvdev = scene.odyenvdev

        layout = self.layout
        col = layout.column()
        col.prop(odyenvdev,'set_vertex_code_face')
        col.operator("odyenvironmentdev.set_vertex_code", text="Rough").flow = "0.0 ;a"
        col.operator("odyenvironmentdev.set_vertex_code", text="Plastic").flow = "0.250;a"
        col.operator("odyenvironmentdev.set_vertex_code", text="Metal").flow = "0.500;a"
        col.operator("odyenvironmentdev.set_vertex_code", text="Reflective").flow = "0.750;a"

class ODYENVDEV_PT_view_panel_foliage_vertex(bpy.types.Panel):
    bl_label = "Foliage"
    bl_idname = "view_panel_foliage_vertex"
    bl_space_type = "VIEW_3D"
    bl_region_type = 'UI'
    bl_category = "Stamp Map"
    
    flow : bpy.props.StringProperty(default="0.1;g")
    def draw(self, context):

        scene = context.scene
        odyenvdev = scene.odyenvdev

        layout = self.layout
        col = layout.column()
        col.prop(odyenvdev,'set_vertex_code_face')
        col.operator("odyenvironmentdev.set_vertex_code", text="Base").flow = "0.0 ;r"
        col.operator("odyenvironmentdev.set_vertex_code", text="Secondary").flow = "0.250;r"
        col.operator("odyenvironmentdev.set_vertex_code", text="Accent").flow = "0.500;r"
        col.operator("odyenvironmentdev.set_vertex_code", text="Bark").flow = "0.750;r"
        col.operator("odyenvironmentdev.set_vertex_code", text="Rock").flow = "1.0;r"
