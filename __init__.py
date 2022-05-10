bl_info = {
    "name": "XMENU",
    "author": "cxs",
    "version": (1, 0),
    "blender": (3, 0, 0),
    "location": "PROPERTIES > Scene > XMENU",
    "description": "Tool and Function Collection Panel",
    "doc_url": "",
    "category": "Interface",
}
 
modulesNames = ['x_panel', 'x_header', 'hud', 'menus', 'menuitems', 'functions', 'preferences', 'icons', 'toolsets', 'brushtexture', 'properties'] 
 
import sys
import os
import bpy
import importlib
from .icons.icons import xmenu_clear_icons
from .import properties
from .import brushtexture as brushtexture
from .functions import clear_brush_textures
from .brushtexture import register_previews, unregister_previews, user_path
from .import menuitems

modulesFullNames = {}
for currentModuleName in modulesNames:
    modulesFullNames[currentModuleName] = ('{}.{}'.format(__name__, currentModuleName))
 
for currentModuleFullName in modulesFullNames.values():
    if currentModuleFullName in sys.modules:
        importlib.reload(sys.modules[currentModuleFullName])
    else:
        globals()[currentModuleFullName] = importlib.import_module(currentModuleFullName)
        setattr(globals()[currentModuleFullName], 'modulesNames', modulesFullNames)

def register():
    for currentModuleName in modulesFullNames.values():
        if currentModuleName in sys.modules:
            if hasattr(sys.modules[currentModuleName], 'register'):
                sys.modules[currentModuleName].register()

    menuitems.register_previews()
    register_previews()

def unregister():
    for currentModuleName in modulesFullNames.values():
        if currentModuleName in sys.modules:
            if hasattr(sys.modules[currentModuleName], 'unregister'):
                sys.modules[currentModuleName].unregister()

    unregister_previews()
    menuitems.unregister_previews()

    xmenu_clear_icons()