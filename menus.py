import bpy
from bpy.types import Menu
from .menuitems import ModeSelector, VertexGroups, ShadingMode

class ModesMenu(Menu):
    bl_label = "MODES-MENU"
    bl_idname = "XM_MT_modes_menu"

    def draw(self, context):
        layout = self.layout

        pie = layout.menu_pie()
        row = pie.column()
        row.scale_y = 1.5

        ModeSelector(self, context, row)
        row = pie.column()
        ShadingMode(self, context, row)

class MainMenu(bpy.types.Menu):
    bl_label = "MAIN-MENU"
    bl_idname = "XM_MT_main_menu"

    def draw(self, context):
        layout = self.layout

        col = layout.column()
        col.operator("script.reload", icon='FILE_REFRESH', text="SCRIPT RELOAD")

class ToolMenu(Menu):
    bl_label = "TOOL-MENU"
    bl_idname = "XM_MT_tool_menu"

    def draw(self, context):
        layout = self.layout

        col = layout.column()
        col.label(text='TOOLS')

class SelectMenu(Menu):
    bl_label = "SELECT-MENU"
    bl_idname = "XM_MT_select_menu"

    def draw(self, context):
        layout = self.layout

        col = layout.column()
        col.label(text='SELECTION')

classes = (MainMenu, ModesMenu, ToolMenu, SelectMenu)

def register():
    for cls in classes:
        bpy.utils.register_class(cls)
    
def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)


