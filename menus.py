import bpy
from bpy.types import Menu
from .menuitems import ModeSelector, VertexGroups, ShadingMode
from .functions import tool_grid, tool_bt, funct_bt

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


class FloaterPanel(bpy.types.Panel):
    bl_idname = "OBJECT_PT_floater"
    bl_label = "Floaters"
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = "scene"
    bl_order = 1000
    bl_options = {'DEFAULT_CLOSED',}

class ToolMenu(bpy.types.Panel):
    bl_idname = "OBJECT_PT_tool_menu"
    bl_label = ""
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = "scene"
    bl_order = 1000
    bl_options = {'DEFAULT_CLOSED',}

    def draw(self, context):
        layout = self.layout
        layout.use_property_split = False
        layout.use_property_decorate = False

        col = layout.column()


        if context.mode == 'EDIT_MESH':
            sub = col.column()
            #sub.label(text='TOOLS')

            sub = col.row()
            subsub = sub.column()
            subsub.scale_x=2.5
            subsub.template_edit_mode_selection()
            sub.separator(factor=3)
            funct_bt(parent=sub, cmd='xray', tog=True, w=2.4, h=1, label='', icon="XRAY")

            col.separator(factor=1)
            sub = col.column()
            grid = sub.grid_flow(row_major=True, columns=4, align=True)
            grid.ui_units_x = 6
            tool_bt(parent=grid, cmd=0, w=2, h=1.2, text=False, icon='LARGE')
            tool_bt(parent=grid, cmd=1, w=2, h=1.2, text=False, icon='LARGE')
            tool_bt(parent=grid, cmd=2, w=2, h=1.2, text=False, icon='LARGE')
            tool_bt(parent=grid, cmd=3, w=2, h=1.2, text=False, icon='LARGE')

            sub.separator(factor=2)
            grid = sub.grid_flow(row_major=True, columns=4, align=True)
            tool_bt(parent=grid, cmd=20, w=2, h=1.4, text=True, icon='LARGE')
            subsub = grid.column()
            subsub.ui_units_x = 2
            subsub.label(text=' ')
            tool_bt(parent=grid, cmd=24, w=2, h=1.4, text=True, icon='LARGE')
            tool_bt(parent=grid, cmd=22, w=2, h=1.4, text=True, icon='LARGE')

            tool_bt(parent=grid, cmd=19, w=2, h=1.4, text=True, icon='LARGE')
            tool_bt(parent=grid, cmd=18, w=2, h=1.4, text=True, icon='LARGE')
            tool_bt(parent=grid, cmd=15, w=2, h=1.4, text=True, icon='LARGE')
            tool_bt(parent=grid, cmd=16, w=2, h=1.4, text=True, icon='LARGE')
            sub.separator(factor=2)

            grid = sub.grid_flow(row_major=True, columns=4, align=True)
            tool_bt(parent=grid, cmd=29, w=2, h=1, text=False, icon='OFF')
            tool_bt(parent=grid, cmd=30, w=2, h=1, text=False, icon='OFF')
            subsub = grid.column()
            subsub.ui_units_x = 2
            subsub.label(text='X')
            tool_bt(parent=grid, cmd=27, w=2, h=1, text=False, icon='OFF')

            tool_bt(parent=grid, cmd=31, w=2, h=1, text=False, icon='OFF')
            tool_bt(parent=grid, cmd=32, w=2, h=1, text=False, icon='OFF')
            tool_bt(parent=grid, cmd=35, w=2, h=1, text=False, icon='OFF')
            tool_bt(parent=grid, cmd=34, w=2, h=1, text=False, icon='OFF')

            sub = col.column()
            sub.label(text='FUNCTIONS')
            sub = col.row()

            subsub = sub.column(align=True)
            item = subsub.column(align=True)
            op = item.operator('mesh.mark_sharp', text='SHARP')
            op = item.operator('mesh.mark_sharp', text='CLEAR')
            op.clear = True

            subsub = sub.column(align=True)
            item = subsub.column(align=True)
            op = item.operator('mesh.mark_seam', text='SEAM')
            op = item.operator('mesh.mark_seam', text='CLEAR')
            op.clear = True

            subsub = sub.column(align=True)
            item = subsub.column(align=True)
            subsub.operator('mesh.flip_normals', text='FLIP')
            subsub.operator('mesh.select_loose', text='LOOSE')

            col.separator(factor=2)

            sub = col.column()
            subsub = sub.row()
            subsub.operator('mesh.flip_normals', text='FLIP')
            subsub.operator('mesh.select_loose', text='LOOSE')


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

        kmi = km.keymap_items.new('wm.call_panel', 'SPACE', 'PRESS', ctrl=False, shift=False, alt=False)
        kmi.properties.name = ToolMenu.bl_idname
        #kmi.properties.keep_open=True
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

