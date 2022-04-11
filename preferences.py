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

    #///////////////////////////MENU/////////////////////////////////#

    def draw(self, context):
        layout = self.layout
        box = layout.box()
        box.prop(self, "hud_activate", toggle=False)
        box.prop(self, "hud_dpi", toggle=False)
        box.prop(self, "tool_icon", toggle=False)
        box.prop(self, "tool_text", toggle=False)

#////////////////////////////////////////////////////////////////////////////////////////////#

def register() :
    bpy.utils.register_class(XPrefs)
    
def unregister() :
    bpy.utils.unregister_class(XPrefs) 