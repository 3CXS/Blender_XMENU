bl_info = {
    "name": "XMENU",
    "author": "CXS",
    "version": (1, 0),
    "blender": (3, 0, 0),
    "location": "PROPERTIES > Scene > XMENU",
    "description": "Tool and Function Collection Panel",
    "doc_url": "",
    "category": "Interface",
    }
 
modulesNames = ['x_panel', 'x_header', 'x_menus', 'hud', 'menuitems', 'functions', 'preferences', 'icons', 'toolsets', 'brushtexture', 'editorfloat'] 
 
import sys
import os
import bpy
import importlib
from bpy.types import AddonPreferences

from .icons.icons import clear_icons

from .import brushtexture as brushtexture
from .brushtexture import register_previews, unregister_previews, user_path, clear_brush_textures

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


#KEYMAP-----------------------------------------------------------------------------------------------------------------

keys = {"MENU": [{"label": "1",
                  "region_type": "WINDOW",
                  "map_type": "KEYBOARD",
                  "keymap": "Window",
                  "idname": "xm.floater_01",
                  "type": "FOUR",
                  "ctrl": False,
                  "alt": False,
                  "shift": False,
                  "oskey": False,
                  "value": "PRESS"
                  },
                {"label": "2",
                  "region_type": "WINDOW",
                  "map_type": "KEYBOARD",
                  "keymap": "Window",
                  "idname": "xm.floater_02",
                  "type": "FIVE",
                  "ctrl": False,
                  "alt": False,
                  "shift": False,
                  "oskey": False,
                  "value": "PRESS"
                  },
                {"label": "3",
                  "region_type": "WINDOW",
                  "map_type": "KEYBOARD",
                  "keymap": "Window",
                  "idname": "xm.floater_03",
                  "type": "SIX",
                  "ctrl": False,
                  "alt": False,
                  "shift": False,
                  "oskey": False,
                  "value": "PRESS"
                  },
                {"label": "4",
                  "region_type": "WINDOW",
                  "map_type": "KEYBOARD",
                  "keymap": "Window",
                  "idname": "xm.floater_04",
                  "type": "SEVEN",
                  "ctrl": False,
                  "alt": False,
                  "shift": False,
                  "oskey": False,
                  "value": "PRESS"
                  },
                {"label": "5",
                  "region_type": "WINDOW",
                  "map_type": "KEYBOARD",
                  "keymap": "Window",
                  "idname": "xm.floater_05",
                  "type": "EIGHT",
                  "ctrl": False,
                  "alt": False,
                  "shift": False,
                  "oskey": False,
                  "value": "PRESS"
                  },
                {"label": "6",
                  "region_type": "WINDOW",
                  "map_type": "KEYBOARD",
                  "keymap": "Window",
                  "idname": "xm.floater_06",
                  "type": "NINE",
                  "ctrl": False,
                  "alt": False,
                  "shift": False,
                  "oskey": False,
                  "value": "PRESS"
                  },
                {"label": "7",
                  "region_type": "WINDOW",
                  "map_type": "KEYBOARD",
                  "keymap": "Window",
                  "idname": "xm.floater_07",
                  "type": "ZERO",
                  "ctrl": False,
                  "alt": False,
                  "shift": False,
                  "oskey": False,
                  "value": "PRESS"
                  },
              {"label": "8",
                  "region_type": "WINDOW",
                  "map_type": "KEYBOARD",
                  "keymap": "Window",
                  "idname": "xm.floater_07",
                  "type": "ZERO",
                  "ctrl": False,
                  "alt": True,
                  "shift": False,
                  "oskey": False,
                  "value": "PRESS"
                  }
                  ]}

def get_keys():
    keylists = []
    keylists.append(keys["MENU"])
    return keylists

def register_keymaps(keylists):
    wm = bpy.context.window_manager
    kc = wm.keyconfigs.addon

    keymaps = []

    for keylist in keylists:
        for item in keylist:
            keymap = item.get("keymap")
            space_type = item.get("space_type", "EMPTY")
            region_type = item.get("region_type", "WINDOW")

            if keymap:
                km = kc.keymaps.new(name=keymap, space_type=space_type, region_type=region_type)
                # km = kc.keymaps.new(name=keymap, space_type=space_type)

                if km:
                    idname = item.get("idname")
                    type = item.get("type")
                    value = item.get("value")

                    shift = item.get("shift", False)
                    ctrl = item.get("ctrl", False)
                    alt = item.get("alt", False)
                    oskey = item.get("oskey", False)

                    kmi = km.keymap_items.new(idname, type, value, shift=shift, ctrl=ctrl, alt=alt, oskey=oskey)

                    if kmi:
                        properties = item.get("properties")

                        if properties:
                            for name, value in properties:
                                setattr(kmi.properties, name, value)

                        keymaps.append((km, kmi))
    return keymaps


#-----------------------------------------------------------------------------------------------------------------------

def register():
    for currentModuleName in modulesFullNames.values():
        if currentModuleName in sys.modules:
            if hasattr(sys.modules[currentModuleName], 'register'):
                sys.modules[currentModuleName].register()

    register_previews()

    global keymaps
    keys = get_keys()
    keymaps = register_keymaps(keys)

def unregister():
    for currentModuleName in modulesFullNames.values():
        if currentModuleName in sys.modules:
            if hasattr(sys.modules[currentModuleName], 'unregister'):
                sys.modules[currentModuleName].unregister()
  
    unregister_previews()
    clear_icons()

    global keymaps
    for km, kmi in keymaps:
        km.keymap_items.remove(kmi)