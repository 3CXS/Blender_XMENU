bl_info = {
    "name": "XMENU",
    "author": "CXS",
    "version": (1, 0),
    "blender": (3, 0, 0),
    "location": "PROPERTIES > Scene > XMENU / Toolheader / Menus",
    "description": "Production Workflow UI",
    "doc_url": "",
    "category": "Interface",
    }
 
modulesNames = ['x_panel', 'x_header', 'x_menus', 'x_toolset', 'hud', 'menuitems', 
                'functions', 'preferences', 'toolsets', 'brushtexture', 'floaters']
 
import sys
import os
import bpy
import importlib
from bpy.types import AddonPreferences

from .import brushtexture as brushtexture
from .brushtexture import register_previews, unregister_previews, clear_brush_textures

from .icons.__init__ import *
from .icons import load_icons, unload_icons

#-----------------------------------------------------------------------------------------------------------------------

modulesFullNames = {}
for currentModuleName in modulesNames:
    modulesFullNames[currentModuleName] = ('{}.{}'.format(__name__, currentModuleName))
 
for currentModuleFullName in modulesFullNames.values():
    if currentModuleFullName in sys.modules:
        importlib.reload(sys.modules[currentModuleFullName])
    else:
        globals()[currentModuleFullName] = importlib.import_module(currentModuleFullName)
        setattr(globals()[currentModuleFullName], 'modulesNames', modulesFullNames)

#-----------------------------------------------------------------------------------------------------------------------

def register():
    for currentModuleName in modulesFullNames.values():
        if currentModuleName in sys.modules:
            if hasattr(sys.modules[currentModuleName], 'register'):
                sys.modules[currentModuleName].register()

    register_previews()
    load_icons()


def unregister():
    for currentModuleName in modulesFullNames.values():
        if currentModuleName in sys.modules:
            if hasattr(sys.modules[currentModuleName], 'unregister'):
                sys.modules[currentModuleName].unregister()

    unload_icons()
    unregister_previews()

