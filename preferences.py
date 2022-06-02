import os
import bpy
from bpy.props import StringProperty, IntProperty, BoolProperty

#////////////////////////////////////////////////////////////////////////////////////////////#

class XPrefs(bpy.types.AddonPreferences):
    bl_idname = __package__

    #///////////////////////////ITEMS////////////////////////////////#
    
    hud_activate: BoolProperty(name="HUD", default=True)
    hud_dpi: IntProperty(name="DPI", default=72)
    tool_icon: BoolProperty(name="TOOL ICON", default=True)
    tool_text: BoolProperty(name="TOOL TEXT", default=True)
    tex_path: StringProperty(name="Folder Path",subtype='DIR_PATH',default="")
    float_alpha: IntProperty(name="FLOAT ALPHA", default=100)
    #///////////////////////////MENU/////////////////////////////////#

    def draw(self, context):

        wm = context.window_manager
        layout = self.layout
        box = layout.box()
        box.prop(self, "hud_activate", toggle=False)
        box.prop(self, "hud_dpi", toggle=False)
        box.prop(self, "tool_icon", toggle=False)
        box.prop(self, "tool_text", toggle=False)
        box.prop(self, "tex_path", text="")
        box.prop(self, "float_alpha")
#////////////////////////////////////////////////////////////////////////////////////////////#

def register() :
    bpy.utils.register_class(XPrefs)


def unregister() :
    bpy.utils.unregister_class(XPrefs) 


