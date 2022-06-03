import os
import bpy
from ..toolsets import Tools_Sculpt
 
xm_icon_collections = {}
xm_icons_loaded = False
 
def load_icons():
    global xm_icon_collections
    global xm_icons_loaded
 
    if xm_icons_loaded: return xm_icon_collections["main"]
 
    custom_icons = bpy.utils.previews.new()
 
    icons_dir = os.path.join(os.path.dirname(__file__))
    
    list = Tools_Sculpt
    NTools = len(list)

    for i in range(NTools):
        if Tools_Sculpt[i][4] != '':
            Toolname = str(Tools_Sculpt[i][4])
            Imagename = str(Tools_Sculpt[i][4]) 
            Imagename +='.png'
            custom_icons.load(Toolname, os.path.join(icons_dir, Imagename), 'IMAGE')

    xm_icon_collections["main"] = custom_icons
    xm_icons_loaded = True
 
    return xm_icon_collections["main"]


def xmenu_clear_icons():
    global xm_icons_loaded
    for icon in xm_icon_collections.values():
        bpy.utils.previews.remove(icon)
    xm_icon_collections.clear()
    xm_icons_loaded = False