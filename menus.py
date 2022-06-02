import bpy
from bpy.types import Menu
from .menuitems import ModeSelector, Materials, VertexGroups


class MainMenu(bpy.types.Menu):
    bl_label = "MAIN"
    bl_idname = "OBJECT_MT_main_menu"

    def draw(self, context):
        layout = self.layout
        layout.operator("wm.open_mainfile")
        layout.operator("wm.save_as_mainfile")
        layout.operator("object.select_all")
        col = layout.column()
        #ModeSelector(self, context, col)
        #VertexGroups(self, context, parent=col)

class VIEW3D_MT_PIE_modes(Menu):
    bl_label = "MODES"
    bl_idname = "OBJECT_MT_modes_menu"

    def draw(self, context):
        layout = self.layout

        pie = layout.menu_pie()
        row = pie.column()
        row.scale_y = 1.5
        ModeSelector(self, context, row)


addon_keymaps = []
classes = (MainMenu, VIEW3D_MT_PIE_modes)

def register():
    for cls in classes:
        bpy.utils.register_class(cls)
    
    wm = bpy.context.window_manager
    kc = wm.keyconfigs.addon
    if kc:
        km = wm.keyconfigs.addon.keymaps.new(name='3D View', space_type='VIEW_3D')

        kmi = km.keymap_items.new('wm.call_menu', 'D', 'PRESS', ctrl=False, shift=False, alt=False)
        kmi.properties.name = MainMenu.bl_idname
        addon_keymaps.append((km, kmi))

        kmi = km.keymap_items.new('wm.call_menu_pie', 'TAB', 'PRESS', ctrl=False, shift=False, alt=False)
        kmi.properties.name = VIEW3D_MT_PIE_modes.bl_idname
        addon_keymaps.append((km, kmi))

def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)

    for km, kmi in addon_keymaps:
        km.keymap_items.remove(kmi)
    addon_keymaps.clear()
