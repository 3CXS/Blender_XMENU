import bpy
from bpy.types import Menu
from .menuitems import ModeSelector, VertexGroups, ShadingMode

class ModesMenu(bpy.types.Menu):
    bl_label = "MODES-MENU"
    bl_idname = "OBJECT_MT_modes_menu"

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
    bl_idname = "OBJECT_MT_main_menu"

    def draw(self, context):
        layout = self.layout

        col = layout.column()
        col.operator("script.reload", icon='FILE_REFRESH', text="SCRIPT RELOAD")

class ToolMenu(bpy.types.Menu):
    bl_label = "TOOL-MENU"
    bl_idname = "OBJECT_MT_tool_menu"

    def draw(self, context):
        layout = self.layout

        col = layout.column()
        col.label(text='TOOLS')

class SelectMenu(bpy.types.Menu):
    bl_label = "SELECT-MENU"
    bl_idname = "OBJECT_MT_select_menu"

    def draw(self, context):
        layout = self.layout

        col = layout.column()
        col.label(text='SELECTION')

addon_keymaps = []
classes = (MainMenu, ModesMenu, ToolMenu, SelectMenu)

def register():
    for cls in classes:
        bpy.utils.register_class(cls)

    wm = bpy.context.window_manager
    kc = wm.keyconfigs.addon
    if kc:
        km = wm.keyconfigs.addon.keymaps.new(name='3D View', space_type='VIEW_3D')

        kmi = km.keymap_items.new('wm.call_menu_pie', 'TAB', 'PRESS', ctrl=False, shift=False, alt=False)
        kmi.properties.name = ModesMenu.bl_idname
        addon_keymaps.append((km, kmi))

        kmi = km.keymap_items.new('wm.call_menu', 'D', 'PRESS', ctrl=False, shift=False, alt=False)
        kmi.properties.name = MainMenu.bl_idname
        addon_keymaps.append((km, kmi))

        kmi = km.keymap_items.new('wm.call_menu', 'SPACE', 'PRESS', ctrl=False, shift=False, alt=False)
        kmi.properties.name = ToolMenu.bl_idname
        addon_keymaps.append((km, kmi))

        kmi = km.keymap_items.new('wm.call_menu', 'A', 'PRESS', ctrl=False, shift=False, alt=False)
        kmi.properties.name = SelectMenu.bl_idname
        addon_keymaps.append((km, kmi))
    
def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)

    for km, kmi in addon_keymaps:
        km.keymap_items.remove(kmi)
    addon_keymaps.clear()

