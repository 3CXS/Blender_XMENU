import bpy

class MainMenu(bpy.types.Menu):
    bl_label = "xmenu.main_menu"
    bl_idname = "OBJECT_MT_main_menu"

    def draw(self, context):
        layout = self.layout
        layout.operator("wm.open_mainfile")
        layout.operator("wm.save_as_mainfile")
        layout.operator("object.select_all")

addon_keymaps = []

def register():
    bpy.utils.register_class(MainMenu)
    
    wm = bpy.context.window_manager
    kc = wm.keyconfigs.addon
    if kc:
        km = wm.keyconfigs.addon.keymaps.new(name='3D View', space_type='VIEW_3D')
        kmi = km.keymap_items.new('wm.call_menu', 'D', 'PRESS', ctrl=False, shift=False, alt=False)
        kmi.properties.name =  MainMenu.bl_idname
        addon_keymaps.append((km, kmi))

def unregister():
    bpy.utils.unregister_class(MainMenu)
    for km, kmi in addon_keymaps:
        km.keymap_items.remove(kmi)
    addon_keymaps.clear()
