import bpy

#object properties
bpy.types.Object.vertex_position_bake = bpy.props.BoolProperty(name="Bake Vertex Position")
bpy.types.Object.material_type = bpy.props.EnumProperty(
        items=[('STO','StampMap', ''),
               ('STV','Vertex Color + StampMap', ''),
               ('DCL','Decals', ''),
               ('FOL','Foliage', ''),
               ('BGD','Background', '')],
        name="Material Type",
        description="choose a material type control panel",
        default=None,
        update=None,
        get=None,
        set=None)

class OdyEnvDevProperties(bpy.types.PropertyGroup):

    def update_unlit2lit(self, context):
        bpy.data.node_groups.get('Unlit2Lit').nodes.get('lit_factor').outputs[0].default_value = self.unlit2lit

    arena_name : bpy.props.StringProperty(name='Arena Name', description='Character name related to this file', default='Arena_Name')
    unlit2lit : bpy.props.IntProperty(name='Unlit to Lit', description='Change the Materials from 0-Unlit to 1-Lit',  default=0, min=0, max=1, step=1, update=update_unlit2lit)
    self_emissive_strenght : bpy.props.FloatProperty(name='Self Emission', description='Change the Materials from 0-Unlit to 1-Lit',  default=0, min=0, max=10, step=1)
    #character_skin : bpy.props.StringProperty(name='Skin', description='Character skin name related to this file',  default='Skin_Name')
    #character_recolor : bpy.props.StringProperty(name='Recolor', description='Character skin recolor name related to this file',  default='Recolor_Name')
    #character_has_recolor : bpy.props.BoolProperty(name='Recolor', description='Character skin recolor name related to this file',  default=False)
    #light_rotation : bpy.props.FloatProperty(name='Light Rotation', description='The main light rotation in the scene',  default=-2, update=update_light_rotation)
    #light_z : bpy.props.FloatProperty(name='Light Z', description='The main light rotation Z in the scene',  default=0.5, update=update_light_z)
    #rim_color : bpy.props.FloatVectorProperty(name = "Rim light color",subtype = "COLOR",size = 4,min = 0.0,max = 1.0,default = (0.287,0.328,1.0,1.0), update=update_rim_light)
    #rim_intensity : bpy.props.FloatProperty(name='Rim Intensity', description='Rim light intensity',  default=0.4, update=update_rim_light)

    #has_diff_root_folder : bpy.props.BoolProperty(name='Change Root Folder', description='Change the character root folder when the name is different',  default=False)
    #root_folder : bpy.props.StringProperty(name='Folder', description='Character root folder name',  default='FolderName')

    set_vertex_code_face : bpy.props.BoolProperty(name='Set Faces Only', description='set only the vertex face instead of the vertice, limiting the color to flood to other faces',  default=True)


class OdyEnvDevVertexColorGroup(bpy.types.PropertyGroup):
    #color_id : bpy.props.StringProperty(name='Color ID', description='Color ID', default='Character_Name')
    color_value : bpy.props.FloatVectorProperty(name = "Color",subtype = "COLOR_GAMMA",size = 4,min = 0.0,max = 1.0,default = (0.287,0.328,1.0,1.0))


#scene properties


def register():
    """
    This function registers the property group class and adds it to the window manager context when the
    addon is enabled.
    """
    bpy.utils.register_class(OdyEnvDevProperties)
    bpy.utils.register_class(OdyEnvDevVertexColorGroup)
    bpy.types.Scene.odyenvdev = bpy.props.PointerProperty(type=OdyEnvDevProperties)
    bpy.types.Scene.OdyEnvDevVertexColorDic = bpy.props.CollectionProperty(type=OdyEnvDevVertexColorGroup)


def unregister():
    """
    This function unregisters the property group class and deletes it from the window manager context when the
    addon is disabled.
    """
    bpy.utils.unregister_class(OdyEnvDevProperties)
    bpy.utils.unregister_class(OdyEnvDevVertexColorGroup)
    del bpy.types.Scene.odyenvdev
    del bpy.types.Scene.OdyEnvDevVertexColorDic