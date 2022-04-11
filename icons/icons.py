import os
import bpy
from ..toolsets import Tools_Sculpt
 
epm_icon_collections = {}
epm_icons_loaded = False
 
def load_icons():
    global epm_icon_collections
    global epm_icons_loaded
 
    if epm_icons_loaded: return epm_icon_collections["main"]
 
    custom_icons = bpy.utils.previews.new()
 
    icons_dir = os.path.join(os.path.dirname(__file__))
    
    list = Tools_Sculpt
    NTools = len(list)

    for i in range(NTools):
        if Tools_Sculpt[i][3] != '':
            Toolname = str(Tools_Sculpt[i][3])
            Imagename = str(Tools_Sculpt[i][3]) 
            Imagename +='.png'
            custom_icons.load(Toolname, os.path.join(icons_dir, Imagename), 'IMAGE')

    epm_icon_collections["main"] = custom_icons
    epm_icons_loaded = True
 
    return epm_icon_collections["main"]


def xmenu_clear_icons():
    global epm_icons_loaded
    for icon in epm_icon_collections.values():
        bpy.utils.previews.remove(icon)
    epm_icon_collections.clear()
    epm_icons_loaded = False