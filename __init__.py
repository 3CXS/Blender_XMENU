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
 
modulesNames = ['x_panel', 'menus', 'hud', 'functions', 'preferences', 'icons', 'toolsets']
 
import sys
import os
import importlib
from .icons.icons import xmenu_clear_icons



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
 
def unregister():
    xmenu_clear_icons()
    for currentModuleName in modulesFullNames.values():
        if currentModuleName in sys.modules:
            if hasattr(sys.modules[currentModuleName], 'unregister'):
                sys.modules[currentModuleName].unregister()
