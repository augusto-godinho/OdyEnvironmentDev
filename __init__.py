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
    "version" : (0, 0, 1),
    "location" : "View3D",
    "warning" : "",
    "category" : "Pipeline"
}

def register():
    ...

def unregister():
    ...

def node_search_path(context):
    preferences = context.preferences
    addon_prefs = preferences.addons["OdyEnvDev"].preferences
    dirpath = addon_prefs.search_path
    return dirpath


class NodeTemplatePrefs(AddonPreferences):
    bl_idname = __name__

    search_path: StringProperty(
        name="Base Files",
        subtype='DIR_PATH',
        default="O:\Odyssey\OmegaPerforce\RawContent\Prometheus\Maps\BaseFiles",

    )

    def draw(self, context):
        layout = self.layout
        layout.prop(self, "search_path")


modules = [
    operators,
    remote_execution,
    unreal,
    properties
]

classes = [
    viewUI.ODYENVDEV_PT_view_panel_settings
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
    
    bpy.types.NODE_MT_add.append(operators.add_node_button)
    


def unregister():
    """
    This function unregisters the addon classes when the addon is disabled.
    """
    # unregister the properties
    properties.unregister()

    for cls in classes:
        bpy.utils.unregister_class(cls)


    bpy.types.NODE_MT_add.remove(operators.add_node_button)
