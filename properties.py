import bpy

#object properties
bpy.types.Object.vertex_position_bake = bpy.props.BoolProperty(name="Bake Vertex Position")

class OdyEnvDevProperties(bpy.types.PropertyGroup):
    def update_light_rotation(self, context):
        bpy.data.node_groups.get('Light Direction').nodes.get('LightRotation').outputs[0].default_value = self.light_rotation
    def update_light_z(self, context):
        bpy.data.node_groups.get('Light Direction').nodes.get('LightZ').outputs[0].default_value = self.light_z
    
    def update_rim_light(self, context):
        bpy.data.node_groups.get('Rim Light').nodes.get('RGB').outputs[0].default_value = self.rim_color
        bpy.data.node_groups.get('Rim Light').nodes.get('Intensity').outputs[0].default_value = self.rim_intensity

    character_name : bpy.props.StringProperty(name='Name', description='Character name related to this file', default='Character_Name')
    character_skin : bpy.props.StringProperty(name='Skin', description='Character skin name related to this file',  default='Skin_Name')
    character_recolor : bpy.props.StringProperty(name='Recolor', description='Character skin recolor name related to this file',  default='Recolor_Name')
    character_has_recolor : bpy.props.BoolProperty(name='Recolor', description='Character skin recolor name related to this file',  default=False)
    light_rotation : bpy.props.FloatProperty(name='Light Rotation', description='The main light rotation in the scene',  default=-2, update=update_light_rotation)
    light_z : bpy.props.FloatProperty(name='Light Z', description='The main light rotation Z in the scene',  default=0.5, update=update_light_z)
    rim_color : bpy.props.FloatVectorProperty(name = "Rim light color",subtype = "COLOR",size = 4,min = 0.0,max = 1.0,default = (0.287,0.328,1.0,1.0), update=update_rim_light)
    rim_intensity : bpy.props.FloatProperty(name='Rim Intensity', description='Rim light intensity',  default=0.4, update=update_rim_light)

    has_diff_root_folder : bpy.props.BoolProperty(name='Change Root Folder', description='Change the character root folder when the name is different',  default=False)
    root_folder : bpy.props.StringProperty(name='Folder', description='Character root folder name',  default='FolderName')


    
    

#scene properties


def register():
    """
    This function registers the property group class and adds it to the window manager context when the
    addon is enabled.
    """
    bpy.utils.register_class(OdyEnvDevProperties)
    bpy.types.Scene.odyenvdev = bpy.props.PointerProperty(type=OdyEnvDevProperties)
    


def unregister():
    """
    This function unregisters the property group class and deletes it from the window manager context when the
    addon is disabled.
    """
    bpy.utils.unregister_class(OdyEnvDevProperties)
    del bpy.types.Scene.odylookdev