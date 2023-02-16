# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTIBILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.
import bpy
import importlib
from . import operators
from . import properties
from .dependencies import remote_execution
from .UI import viewUI
from .functions import unreal

from bpy.types import (
    Operator,
    Menu,
    AddonPreferences,
)

from bpy.props import (
    StringProperty,
)

bl_info = {
    "name" : "Ody Environment Dev",
    "author" : "Odyssey Interactive",
    "description" : "",
    "blender" : (3, 4, 0),
    "version" : (0, 0, 4),
    "location" : "View3D",
    "warning" : "",
    "category" : "Pipeline"
}

def register():
    ...

def unregister():
    ...



class EnvNodeTemplatePrefs(AddonPreferences):
    bl_idname = __name__

    env_search_path: StringProperty(
        name="Base Env Files",
        subtype='DIR_PATH',
        default="O:\Odyssey\OmegaPerforce\RawContent\Prometheus\Maps\EnvironmentArt\BaseFiles",

    )

    def draw(self, context):
        layout = self.layout
        layout.label(text="Environment")
        layout.prop(self, "env_search_path")


modules = [
    operators,
    remote_execution,
    unreal,
    properties
]

classes = [
    viewUI.ODYENVDEV_PT_view_panel_settings,
    viewUI.ODYENVDEV_PT_view_panel_main_stampmapvertex,
    operators.NODE_OT_env_template_add,
    operators.NODE_MT_env_template_add,
    operators.ODYENVDEV_OT_clean_duplicated_nodes,
    operators.ODYENVDEV_OT_set_vertex_code,
    operators.ODYENVDEV_OT_assign_vertex_to_color_id,
    operators.ODYENVDEV_OT_rename_color_id,
    operators.ODYENVDEV_OT_update_color_ids,
    operators.ODYENVDEV_OT_add_new_color_id,
    operators.ODYENVDEV_OT_color_id_from_stampmap_main,
    operators.ODYENVDEV_OT_generate_uv_maps,
    operators.ODYENVDEV_OT_set_uv_es,
    operators.ODYENVDEV_OT_clear_all_color_ids,
    EnvNodeTemplatePrefs
]



def register():
    """
    This function registers the addon classes when the addon is enabled.
    """
    # reload the submodules
    for module in modules:
        importlib.reload(module)

    # register the properties
    properties.register()

    # register the classes
    for cls in classes:
        bpy.utils.register_class(cls)
    
    bpy.types.NODE_MT_add.append(operators.add_env_node_button)
    


def unregister():
    """
    This function unregisters the addon classes when the addon is disabled.
    """
    # unregister the properties
    properties.unregister()

    for cls in classes:
        bpy.utils.unregister_class(cls)


    bpy.types.NODE_MT_add.remove(operators.add_env_node_button)
