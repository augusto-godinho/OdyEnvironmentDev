
from asyncio.windows_events import NULL
from pickle import TRUE
import bpy
import json
import os
from pathlib import Path
from mathutils import Vector, Color
from .functions import unreal

from bpy.types import (
    Operator,
    Menu,
    AddonPreferences,
    StringProperty
)

from bpy.props import (
    StringProperty,
)

from bpy.types import (
    NodeSocketShader,
    NodeSocketVirtual,
    NodeSocketVector,
    NodeSocketVectorDirection,
    NodeSocketVectorXYZ,
    NodeSocketVectorTranslation,
    NodeSocketVectorEuler,
    NodeSocketColor,

    NodeReroute,

    Object,
    Image,
    ImageUser,
    Text,
    ParticleSystem,
    CurveMapping,
    ColorRamp,

    ShaderNodeTree,
)

ody_nodes = [
                'Character Full',
                'Character Main',
                'Character Face',
                'Character Transparent',
                'Character Glass',
                'Character Hair'
]

ody_nodes_all = [
                'Character Full',
                'Character Main',
                'Character Face',
                'Character Transparent',
                'Character Glass',
                'Character Hair',
                'Face Shadows',
                'Outline',
                'Hair',
                'Light Direction',
                'Main Shadow',
                'Rim Light',
                'Speculars'
]

ody_materials = {
    'Character Full' : "/Game/Prometheus/Commons/Rendering/Materials/Defaults/MI_Character_SSE",
    'Character Main': "/Game/Prometheus/Commons/Rendering/Materials/Defaults/MI_Character_SSE",
    'Character Face': "/Game/Prometheus/Commons/Rendering/Materials/Defaults/MI_Character_Face",
    'Character Transparent': "/Game/Prometheus/Commons/Rendering/Materials/Defaults/MI_Character_Transparent",
    'Character Glass': "/Game/Prometheus/Commons/Rendering/Materials/Defaults/MI_Character_Glass",
    'Character Hair': "/Game/Prometheus/Commons/Rendering/Materials/Defaults/MI_Character_Hair",
    'Emission': "/Game/Prometheus/Commons/Rendering/Materials/Defaults/MI_Character_Unlit"
}

def value_from_socket(socket):
    """
    Returns the evaluated value of a node socket's default value
    """
    # A Shader socket (green dot) doesn't have a default value :
    if isinstance(socket, (NodeSocketShader, NodeSocketVirtual)):
        return NULL
    elif isinstance(socket, (
            NodeSocketVector,
            NodeSocketVectorXYZ,
            NodeSocketVectorTranslation,
            NodeSocketVectorEuler,
            NodeSocketVectorDirection)):
        return f"{[socket.default_value[i] for i in range(3)]}"
    elif isinstance(socket, NodeSocketColor):
        return f"{[socket.default_value[i] for i in range(4)]}"
    else:
        return socket.default_value.__str__()
    

#Object
class ODYLOOKDEV_OT_export_materials(bpy.types.Operator):
    bl_idname = "odylookdev.export_materials"
    bl_label = "Export Materials"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):

        odylookdev = bpy.context.scene.odylookdev
        character_name = odylookdev.character_name
        character_skin = odylookdev.character_skin
        character_recolor = odylookdev.character_recolor
        has_recolor = odylookdev.character_has_recolor

        character_folder = odylookdev.character_name
        if odylookdev.has_diff_root_folder:
            character_folder = odylookdev.root_folder


        meshes_dir = bpy.path.abspath("//")
        materials_dir = os.path.abspath(os.path.join(meshes_dir, os.pardir)) + '\Materials'

        materials_data ={}
        materials_data['Materials'] = []

        id = 0
        for material in bpy.data.materials:
            if material.node_tree:
                master_node = NULL
                have_master_node = False
                #finding master_node
                for link in material.node_tree.links: #checking all links
                    have_master_node = False
                    parent_name = 'Character Full'
                    if link.to_socket.name == 'Surface': #checking if something is connected to surface output
                        master_node = link.from_node

                        if(master_node.type == 'GROUP'): #checking if is a group node
                            if (master_node.node_tree.name in ody_nodes): #checking if it is a valid prometheus character material
                                print(material.name +'-->'+master_node.node_tree.name)
                                parent_name = master_node.node_tree.name
                                have_master_node = True
                                
                        if (master_node.name == 'Emission'): #checking if it is a emissive material
                            print(material.name +'-->'+master_node.name)
                            parent_name = master_node.name
                            have_master_node = True
                                
                    
                    if have_master_node:
                        materials_data['Materials'].append({})
                        materials_data['Materials'][id]['Name'] = material.name
                        materials_data['Materials'][id]['Parent'] = ody_materials[parent_name]
                        print(parent_name)
                        materials_data['Materials'][id]['Vectors'] = {}
                        materials_data['Materials'][id]['Scalars'] = {}
                        materials_data['Materials'][id]['Textures'] = {}
                        
                        for socket in master_node.inputs:
                            name = socket.name
                            if socket.type == 'VALUE':
                                if name == 'Specular Intensity':
                                    name = 'Intensity'
                                if name == 'Glossines':
                                    name = 'Glossiness'
                                if name == 'Use Matcap':
                                    if socket.default_value == 1:
                                        materials_data['Materials'][id]['Parent'] = ody_materials[parent_name]+"_Matcap"
                                materials_data['Materials'][id]['Scalars'][name] = socket.default_value                                
                            if socket.type == 'RGBA':
                                if name == 'Hair Details Color':
                                    name = 'Hair Detail Color'
                                materials_data['Materials'][id]['Vectors'][name] = {'R':socket.default_value[0],'G':socket.default_value[1],'B':socket.default_value[2],'A':socket.default_value[3],}


                            for link in material.node_tree.links:
                                if link.to_socket == socket:
                                    if link.from_node.type == "TEX_IMAGE":
                                        if parent_name == 'Character Glass':
                                            materials_data['Materials'][id]['Parent'] = ody_materials[parent_name]+"_Texture"
                                        if link.from_node.image:
                                            name = socket.name
                                            if name == "Base Color":
                                                name = "Base Color Texture"
                                            if name == "Color":
                                                name = "Base Color Texture"
                                            if name == "Opacity":
                                                name = "Opacity Texture"
                                            if link.from_node.image.name == 'T_Matcap_Base.png':
                                                img_path = "/Game/Prometheus/Characters/Commons/Textures/T_Matcap_Base.png.T_Matcap_Base.png"
                                            else:
                                                if has_recolor and character_recolor in link.from_node.image.name.split('.')[0]: 
                                                    img_path = f"/Game/Prometheus/Characters/{character_folder}/{character_skin}/Textures/{character_recolor}/{link.from_node.image.name.split('.')[0]}"
                                                else:
                                                    img_path = f"/Game/Prometheus/Characters/{character_folder}/{character_skin}/Textures/{link.from_node.image.name.split('.')[0]}"

                                            materials_data['Materials'][id]['Textures'][name] = img_path
                                

                                    if link.from_node.type == "SEPARATE_COLOR":
                                        for l in material.node_tree.links:
                                            if l.to_node == link.from_node:
                                                if l.from_node.type == "TEX_IMAGE":
                                                    if parent_name == 'Character Glass':
                                                        materials_data['Materials'][id]['Parent'] = ody_materials[parent_name]+"_Texture_Opacity"
                                                    if l.from_node.image:
                                                        name = 'SSE Texture'
                                                        if socket.name == "Opacity":
                                                            name = "Opacity Texture"
                                                            print('Glass Opacity Tex')
                                                        if l.from_node.image.name == 'T_Matcap_Base.png':
                                                            img_path = "/Game/Prometheus/Characters/Commons/Textures/T_Matcap_Base.png.T_Matcap_Base"
                                                        else:
                                                            if has_recolor and character_recolor in l.from_node.image.name.split('.')[0]:
                                                                img_path = f"/Game/Prometheus/Characters/{character_folder}/{character_skin}/Textures/{character_recolor}/{l.from_node.image.name.split('.')[0]}"
                                                            else:
                                                                img_path = f"/Game/Prometheus/Characters/{character_folder}/{character_skin}/Textures/{l.from_node.image.name.split('.')[0]}"
                                                        
                                                        materials_data['Materials'][id]['Textures'][name] = img_path 
                            
                        id = id+1
                            
        #print(materials_data)
        file_dir = f"{meshes_dir}\{character_name}_{character_skin}_{character_recolor}.json"
        f = open(file_dir, 'w')
        json.dump(materials_data, f)
        unreal.export_materials(materials_data)
        return {'FINISHED'}

class ODYLOOKDEV_OT_clean_duplicated_nodes(bpy.types.Operator):
    bl_idname = "odylookdev.clean_duplicated_nodes"
    bl_label = "Update Materials"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):

        node_groups = bpy.data.node_groups


        dirpath = node_search_path(context)
        filepath = os.path.join(dirpath, "Character_Material_Base.blend")
        nodes_to_link = []
        with bpy.data.libraries.load(filepath, link=True) as (data_from, data_to):
            for group_name in data_from.node_groups:
                if group_name in ody_nodes_all:
                    nodes_to_link.append({'name': group_name})

        filepath = os.path.join(dirpath, "Character_Material_Base.blend/NodeTree/")
        bpy.ops.wm.link(directory=filepath, files=nodes_to_link)


        for node in bpy.data.node_groups:
            if node.library == None:
                if (node.name.split('.')[0] in ody_nodes_all):
                    node.name =node.name.split('.')[0]+".replace"
        
        for material in bpy.data.materials:
            if material.use_nodes:
                for node in material.node_tree.nodes:
                    if node.type == 'GROUP':
                        if node.node_tree != None:
                            if node.node_tree.name.split('.')[0] in ody_nodes_all:
                                node.node_tree = bpy.data.node_groups.get(node.node_tree.name.split('.')[0])
        
        for node in bpy.data.node_groups:
            if node.library == None:
                if (node.name.split('.')[0] in ody_nodes_all):
                    bpy.data.node_groups.remove(node)

        return {'FINISHED'}

class ODYLOOKDEV_OT_add_outline(bpy.types.Operator):
    bl_idname = "odylookdev.add_outline"
    bl_label = "Add Outline"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):

        bpy.ops.view3d.snap_cursor_to_center()
        dirpath = node_search_path(context)
        filepath = os.path.join(dirpath, "Character_Material_Base.blend")
        nodes_to_link = [{"name":"Outline"}]

        filepath = os.path.join(dirpath, "Character_Material_Base.blend/NodeTree/")
        bpy.ops.wm.link(directory=filepath, files=nodes_to_link)
        
        filepath = os.path.join(dirpath, "Character_Material_Base.blend/Material/")
        bpy.ops.wm.link(directory=filepath, files=nodes_to_link)

        bpy.ops.mesh.primitive_monkey_add()
        outline = bpy.context.active_object
        outline.name = "Outline"
        modifier = outline.modifiers.new("Oultline", "NODES")
        replacement = bpy.data.node_groups["Outline"]
        modifier.node_group = replacement

        if  "Outline" in bpy.data.collections:
            coll = bpy.data.collections["Outline"]
        else:
            coll = bpy.data.collections.new("Outline")
            bpy.context.scene.collection.children.link(coll)

        coll.objects.link(outline)
        bpy.context.scene.collection.objects.unlink(outline)
        
        bpy.context.object.modifiers["Oultline"]["Input_0"] = bpy.data.collections["Character"]
        if "Outline" in bpy.data.materials:
            bpy.context.object.modifiers["Oultline"]["Input_3"] = bpy.data.materials["Outline"]
        else:
            mat = bpy.data.materials.new("Outline")
            mat.context.object.active_material.use_nodes = True
            bpy.context.object.active_material.use_backface_culling = True
            bpy.context.object.modifiers["Oultline"]["Input_3"] = mat

        return {'FINISHED'}

class ODYLOOKDEV_OT_light_rotation(bpy.types.Operator):
    bl_idname = "odylookdev.clean_duplicated_nodes"
    bl_label = "Update Materials"
    bl_options = {'REGISTER', 'UNDO'}



    def execute(self, context):
        return {'FINISHED'}

#----Nodes Sync-----------
#-------------------------



# -----------------------------------------------------------------------------
# Node Adding Operator


def node_center(context):
    from mathutils import Vector
    loc = Vector((0.0, 0.0))
    node_selected = context.selected_nodes
    if node_selected:
        for node in node_selected:
            loc += node.location
        loc /= len(node_selected)
    return loc


def node_template_add(context, filepath, node_group, ungroup, report):
    """ Main function
    """

    space = context.space_data
    node_tree = space.node_tree
    node_active = context.active_node
    node_selected = context.selected_nodes

    if node_tree is None:
        report({'ERROR'}, "No node tree available")
        return

    with bpy.data.libraries.load(filepath, link=True) as (data_from, data_to):
        assert(node_group in data_from.node_groups)
        data_to.node_groups = [node_group]
    node_group = data_to.node_groups[0]

    # add node!
    center = node_center(context)

    for node in node_tree.nodes:
        node.select = False

    node_type_string = {
        "ShaderNodeTree": "ShaderNodeGroup",
        "CompositorNodeTree": "CompositorNodeGroup",
        "TextureNodeTree": "TextureNodeGroup",
        "GeometryNodeTree": "GeometryNodeGroup",
    }[type(node_tree).__name__]

    node = node_tree.nodes.new(type=node_type_string)
    node.node_tree = node_group

    is_fail = (node.node_tree is None)
    if is_fail:
        report({'WARNING'}, "Incompatible node type")

    node.select = True
    node_tree.nodes.active = node
    node.location = center

    if is_fail:
        node_tree.nodes.remove(node)
    else:
        if ungroup:
            bpy.ops.node.group_ungroup()

    # node_group.user_clear()
    # bpy.data.node_groups.remove(node_group)


# -----------------------------------------------------------------------------
# Node Template Prefs

def node_search_path(context):
    preferences = context.preferences
    addon_prefs = preferences.addons["OdyLookDev"].preferences
    dirpath = addon_prefs.search_path
    return dirpath


class NodeTemplatePrefs(AddonPreferences):
    bl_idname = __name__

    search_path: StringProperty(
        name="Directory of blend files with node-groups",
        subtype='DIR_PATH',
    )

    def draw(self, context):
        layout = self.layout
        layout.prop(self, "search_path")


class NODE_OT_template_add(Operator):
    """Add a node template"""
    bl_idname = "node.template_add"
    bl_label = "Add node group template"
    bl_description = "Add node group template"
    bl_options = {'REGISTER', 'UNDO'}

    filepath: StringProperty(
        subtype='FILE_PATH',
    )
    group_name: StringProperty()

    def execute(self, context):
        node_template_add(context, self.filepath, self.group_name, True, self.report)

        return {'FINISHED'}

    def invoke(self, context, event):
        node_template_add(context, self.filepath, self.group_name, event.shift, self.report)

        return {'FINISHED'}


# -----------------------------------------------------------------------------
# Node menu list

def node_template_cache(context, *, reload=False):
    dirpath = node_search_path(context)

    if node_template_cache._node_cache_path != dirpath:
        reload = True

    node_cache = node_template_cache._node_cache
    if reload:
        node_cache = []
    if node_cache:
        return node_cache

    filepath = os.path.join(dirpath, "Character_Material_Base.blend")
    with bpy.data.libraries.load(filepath, link=True) as (data_from, data_to):
        for group_name in data_from.node_groups:
            if not group_name.startswith("_"):
                node_cache.append((filepath, group_name))

    node_template_cache._node_cache = node_cache
    node_template_cache._node_cache_path = dirpath

    return node_cache


node_template_cache._node_cache = []
node_template_cache._node_cache_path = ""


class NODE_MT_template_add(Menu):
    bl_label = "Node Template"

    def draw(self, context):
        layout = self.layout

        dirpath = node_search_path(context)
        if dirpath == "":
            layout.label(text="Set search dir in the addon-prefs")
            return

        try:
            node_items = node_template_cache(context)
        except Exception as ex:
            node_items = ()
            layout.label(text=repr(ex), icon='ERROR')

        for filepath, group_name in node_items:
            props = layout.operator(
                NODE_OT_template_add.bl_idname,
                text=group_name,
            )
            props.filepath = filepath
            props.group_name = group_name


def add_node_button(self, context):
    self.layout.menu(
        NODE_MT_template_add.__name__,
        text="Ody Shaders",
        icon='PLUGIN',
    )



#------------------------------------------------------------
#-----Vertex Paint-------------------------------------------

def GetColor(col, flow):
    final_col = (col[0], col[1], col[2], col[3])
    if flow == "ADD":
        final_col = (col[0], col[1], col[2], 1)

    if flow == "REMOVE":
        final_col = (col[0], col[1], col[2], 0)
    return final_col

def GetThickness(thc, flow):
    final_col = (thc[0], thc[1], thc[2], thc[3])
    if flow == "ADD":
        final_col = (1, thc[1], thc[2], thc[3])

    if flow == "REMOVE":
        final_col = (0, thc[1], thc[2], thc[3])
    return final_col

def Recolor(flow):
    D =  bpy.data
    C =  bpy.context
    S =  bpy.context.scene

    objects = bpy.context.selected_objects
    o_id=0
    for obj in objects:
        if obj.mode == 'EDIT':
            bpy.ops.object.editmode_toggle()

        mesh = obj.data
        if not mesh.vertex_colors:
            mesh.vertex_colors.new()

        if "Col" in mesh.vertex_colors:
            color_layer = mesh.vertex_colors["Col"]
        else:
            thickness_layer = mesh.vertex_colors.new(name="Col")

        if "Thickness" in mesh.vertex_colors:
            thickness_layer = mesh.vertex_colors["Thickness"]
        else:
            thickness_layer = mesh.vertex_colors.new(name="Thickness")
        
        i=0
        for poly in mesh.polygons:
            for idx in poly.loop_indices:
                id = mesh.loops[i].vertex_index
                col = color_layer.data[i].color
                thc = thickness_layer.data[i].color

                if mesh.vertices[id].select == True:
                    color_layer.data[i].color = GetColor(col, flow)
                    thickness_layer.data[i].color = GetThickness(thc, flow)

                i+=1
        
        o_id += 1


class ODYLOOKDEV_OT_set_vertex_alpha(bpy.types.Operator):
    bl_label = "Vertex"
    bl_idname = "odylookdev.vertex_aplha"
    bl_options = {'REGISTER', 'UNDO'}

    flow : bpy.props.StringProperty(default="NEUTRAL")
    
    def execute(self, context):
        print("Flow = "+ self.flow)
        Recolor(self.flow)
        return {'FINISHED'}


#---------Export Outline----------->
def ExportOutline():
    D =  bpy.data
    C =  bpy.context
    S =  bpy.context.scene

    objects = D.collections['Character'].all_objects
    d_objects = []
    armature = objects[0]

    for obj in objects:
        obj.select_set(True)
        if obj.type == 'ARMATURE':
            armature = obj
        if obj.type == 'MESH':
            o = obj.copy()
            o.data = obj.data.copy()
            o.animation_data_clear()
            C.collection.objects.link(o)
            d_objects.append(o)
            obj.select_set(False)
    
    for obj in d_objects:
        obj.select_set(True)

    outline = d_objects[0]
    C.view_layer.objects.active = outline
    bpy.ops.object.join()
    outline.name = "OutlineToExport"
    outline.data.materials.clear()
    outline.data.materials.append(D.materials['Outline'])

    bpy.ops.object.editmode_toggle()
    bpy.ops.mesh.reveal()
    bpy.ops.mesh.select_all(action='SELECT')
    bpy.ops.mesh.flip_normals()
    bpy.ops.object.editmode_toggle()

    odylookdev = bpy.context.scene.odylookdev
    character_name = odylookdev.character_name
    character_skin = odylookdev.character_skin
    outline_name = 'SK_'+character_name +'_'+character_skin+'_Outline.fbx'

    meshes_dir = bpy.path.abspath("//")
    path = os.path.join(meshes_dir, outline_name)
    print(str(path))
    #Exporting the outline
    bpy.ops.export_scene.fbx(filepath=str(path), 
        check_existing=True,
        filter_glob='*.fbx',
        use_selection=True,
        use_visible=False,
        use_active_collection=False,
        global_scale=1.0, 
        apply_unit_scale=True,
        apply_scale_options='FBX_SCALE_NONE',
        use_space_transform=True,
        bake_space_transform=False, 
        object_types={'ARMATURE', 'EMPTY', 'MESH'},
        use_mesh_modifiers=True, use_mesh_modifiers_render=True, mesh_smooth_type='OFF',
        use_subsurf=False, use_mesh_edges=False, use_tspace=False, use_triangles=False,
        use_custom_props=False,
        add_leaf_bones=False,
        primary_bone_axis='Y', secondary_bone_axis='X',
        use_armature_deform_only=False,
        armature_nodetype='NULL',
        bake_anim=True,
        bake_anim_use_all_bones=True,
        bake_anim_use_nla_strips=True,
        bake_anim_use_all_actions=True,
        bake_anim_force_startend_keying=True,
        bake_anim_step=1.0,
        bake_anim_simplify_factor=1.0,
        path_mode='AUTO',
        embed_textures=False,
        batch_mode='OFF',
        use_batch_own_dir=True,
        use_metadata=True,
        axis_forward='-Z', axis_up='Y')
    
    for obj in objects:
        obj.select_set(False)
    
    outline.select_set(True)
    C.view_layer.objects.active = outline

    bpy.ops.object.delete()

class ODYLOOKDEV_OT_export_as_outline(bpy.types.Operator):
    bl_idname = "odylookdev.export_as_outline"
    bl_label = "Export as Outline"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        ExportOutline()
        return {'FINISHED'}


#------->Export Main-------------

def ExportMain():
    D =  bpy.data
    C =  bpy.context
    S =  bpy.context.scene

    objects = D.objects
    d_objects = []
    armature = objects[0]
    excluded_objects = []

    for obj in objects:
        obj.select_set(True)

        if obj.type == 'ARMATURE':
            armature = obj
        if obj.type == 'MESH':
            if 'Outline' in obj.name:
                excluded_objects.append(obj)
            else:
                o = obj.copy()
                o.data = obj.data.copy()
                o.animation_data_clear()
                o.select_set(False)
                d_objects.append(o)
                C.collection.objects.link(o)
                obj.select_set(False)
                excluded_objects.append(obj)
        
    for obj in excluded_objects:
        obj.select_set(False)

    bpy.ops.object.editmode_toggle()
    bpy.ops.mesh.reveal()
    bpy.ops.mesh.select_all(action='SELECT')
    MarkVertex()

    odylookdev = bpy.context.scene.odylookdev
    character_name = odylookdev.character_name
    character_skin = odylookdev.character_skin
    outline_name = 'SK_'+character_name +'_'+character_skin+'.fbx'

    meshes_dir = bpy.path.abspath("//")
    path = os.path.join(meshes_dir, outline_name)
    print(str(path))
    
    #Exporting the main mesh
    bpy.ops.export_scene.fbx(filepath=str(path), 
        check_existing=True,
        filter_glob='*.fbx',
        use_selection=True,
        use_visible=False,
        use_active_collection=False,
        global_scale=1.0, 
        apply_unit_scale=True,
        apply_scale_options='FBX_SCALE_NONE',
        use_space_transform=True,
        bake_space_transform=False, 
        object_types={'ARMATURE', 'EMPTY', 'MESH'},
        use_mesh_modifiers=True, use_mesh_modifiers_render=True, mesh_smooth_type='OFF',
        use_subsurf=False, use_mesh_edges=False, use_tspace=False, use_triangles=False,
        use_custom_props=False,
        add_leaf_bones=False,
        primary_bone_axis='Y', secondary_bone_axis='X',
        use_armature_deform_only=False,
        armature_nodetype='NULL',
        bake_anim=True,
        bake_anim_use_all_bones=True,
        bake_anim_use_nla_strips=True,
        bake_anim_use_all_actions=True,
        bake_anim_force_startend_keying=True,
        bake_anim_step=1.0,
        bake_anim_simplify_factor=1.0,
        path_mode='AUTO',
        embed_textures=False,
        batch_mode='OFF',
        use_batch_own_dir=True,
        use_metadata=True,
        axis_forward='-Z', axis_up='Y')
    
    for obj in objects:
        obj.select_set(False)
    
    for obj in d_objects:
        obj.select_set(True)

    bpy.ops.object.delete()

def MarkVertex():
    D =  bpy.data
    C =  bpy.context
    S =  bpy.context.scene

    objects = bpy.context.selected_objects
    o_id=0
    for obj in objects:
        if obj.type == "MESH":
            if True:
                if obj.mode == 'EDIT':
                    bpy.ops.object.editmode_toggle()

                mesh = obj.data
                
                vcolor_names = []
                for vcolor in mesh.vertex_colors:
                    vcolor_names.append(vcolor.name)
                
                for vname in vcolor_names:
                    mesh.vertex_colors.remove(mesh.vertex_colors[vname])

                if not mesh.vertex_colors:
                    mesh.vertex_colors.new(name='Col', do_init=True)

                if "Col" in mesh.vertex_colors:
                    color_layer = mesh.vertex_colors["Col"]
                else:
                    color_layer = mesh.vertex_colors.new(name="Col")
                
                bpy.ops.geometry.color_attribute_render_set(name="Col")
                
                i=0
                for poly in mesh.polygons:
                    for idx in poly.loop_indices:
                        id = mesh.loops[i].vertex_index
                        col = color_layer.data[i].color

                        if mesh.vertices[id].select == True:
                            pos = 1
                            if mesh.vertices[id].co[0] <= 0:
                                pos = 0
                            
                            color_layer.data[i].color = [pos,0,0,0]
                        i+=1
                
                o_id += 1


class ODYLOOKDEV_OT_export_main(bpy.types.Operator):
    bl_idname = "odylookdev.export_main"
    bl_label = "Export Main"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        ExportMain()
        return {'FINISHED'}