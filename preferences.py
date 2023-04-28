import os
import bpy
from bpy.props import StringProperty, IntProperty, FloatProperty, BoolProperty, EnumProperty
import rna_keymap_ui
from .menuitems import InsertSpace
from .functions import tool_bt, funct_bt

#-----------------------------------------------------------------------------------------------------------#

class XPrefs(bpy.types.AddonPreferences):
    bl_idname = __package__

    # PROPERTIES ---------------------------------------------------------------------------------------------#
 
    hud_01_size: IntProperty(name="Size", default=14)
    hud_01_pos_x: IntProperty(name="Pos X", default=450)
    hud_01_pos_y: IntProperty(name="Pos Y", default=32)

    hud_02_size: IntProperty(name="Size", default=14)
    hud_02_pos_x: IntProperty(name="Pos X", default=915)
    hud_02_pos_y: IntProperty(name="Pos Y", default=32)

    hud_03_size: IntProperty(name="Size", default=20)
    hud_03_pos_x: IntProperty(name="Pos X", default=450)
    hud_03_pos_y: IntProperty(name="Pos Y", default=110)

    tool_text: BoolProperty(name="TOOL TEXT", default=False)

    tex_path: StringProperty(name="Tex Folder Path",subtype='DIR_PATH',default="")
    file_path: StringProperty(name="File Folder Path",subtype='DIR_PATH',default="")

    floater_00_name : bpy.props.StringProperty(default="0", name="Name",)
    floater_00_type : bpy.props.StringProperty(default='PROPERTIES')
    floater_00_size : bpy.props.FloatVectorProperty(name="Size", size=2, default=(300,500),precision=0)
    floater_00_pos  : bpy.props.FloatVectorProperty(name="Pos", size=2, default=(1640,250),precision=0)
    floater_00_alpha: IntProperty(name="FLOAT ALPHA", default=100)

    floater_01_name : bpy.props.StringProperty(default="1", name="Name",)
    floater_01_type : bpy.props.StringProperty(default='OUTLINER')
    floater_01_size : bpy.props.FloatVectorProperty(name="Size", size=2, default=(300,500),precision=0)
    floater_01_pos  : bpy.props.FloatVectorProperty(name="Pos", size=2, default=(1640,250),precision=0)
    floater_01_alpha: IntProperty(name="FLOAT ALPHA", default=100)

    floater_02_name : bpy.props.StringProperty(default="2", name="Name",)
    floater_02_type : bpy.props.StringProperty(default='PROPERTIES')
    floater_02_size : bpy.props.FloatVectorProperty(name="Size", size=2, default=(500,800),precision=0)
    floater_02_pos  : bpy.props.FloatVectorProperty(name="Pos", size=2, default=(1960,250),precision=0)
    floater_02_alpha: IntProperty(name="FLOAT ALPHA", default=100)

    floater_03_name : bpy.props.StringProperty(default="3", name="Name",)
    floater_03_type : bpy.props.StringProperty(default='PROPERTIES')
    floater_03_size : bpy.props.FloatVectorProperty(name="Size", size=2, default=(500,800),precision=0)
    floater_03_pos  : bpy.props.FloatVectorProperty(name="Pos", size=2, default=(1960,250),precision=0)
    floater_03_alpha: IntProperty(name="FLOAT ALPHA", default=100)

    floater_04_name : bpy.props.StringProperty(default="4", name="Name",)
    floater_04_type : bpy.props.StringProperty(default='ShaderNodeTree')
    floater_04_size : bpy.props.FloatVectorProperty(name="Size", size=2, default=(900,620),precision=0)
    floater_04_pos  : bpy.props.FloatVectorProperty(name="Pos", size=2, default=(1540,440),precision=0)
    floater_04_alpha: IntProperty(name="FLOAT ALPHA", default=100)

    floater_05_name : bpy.props.StringProperty(default="6", name="Name",)
    floater_05_type : bpy.props.StringProperty(default='IMAGE_EDITOR')
    floater_05_size : bpy.props.FloatVectorProperty(name="Size", size=2, default=(800,800),precision=0)
    floater_05_pos  : bpy.props.FloatVectorProperty(name="Pos", size=2, default=(200,250),precision=0)
    floater_05_alpha: IntProperty(name="FLOAT ALPHA", default=100)

    floater_06_name : bpy.props.StringProperty(default="8", name="Name",)
    floater_06_type : bpy.props.StringProperty(default='VIEW_3D')
    floater_06_size : bpy.props.FloatVectorProperty(name="Size", size=2, default=(900,700),precision=0)
    floater_06_pos  : bpy.props.FloatVectorProperty(name="Pos", size=2, default=(100,300),precision=0)
    floater_06_alpha: IntProperty(name="FLOAT ALPHA", default=100)

    floaters_item : bpy.props.EnumProperty(default="01",items=[("00","ToolMenu",""),("01","Outliner",""),("02","Properties",""),("03","Modifiers",""),("04","NodeTree","")
                                                            ,("05","Image","")])

    info: BoolProperty(name="info", description="Info", default=False)
    options: BoolProperty(name="options", description="Options", default=False)
    floaters: BoolProperty(name="floaters", description="Floaters", default=False)
    keymaps: BoolProperty(name="keymaps", description="Keymaps", default=False)

    # MENU ------------------------------------------------------------------------------------------------------------------ #

    def draw(self, context):
        layout = self.layout
        wm = bpy.context.window_manager

        # Info
        layout.prop(self, "info", text="Info",
                icon='DISCLOSURE_TRI_DOWN' if self.info
                else 'DISCLOSURE_TRI_RIGHT')
        if self.info:
            col = layout.column()
            split = col.split()
            sub = split.column()
            sub.label(text="X-MENU")
            sub.separator()
            sub.label(text="ARTISTIC PRODUCTION INTERFACE")
            sub.separator()
            sub.label(text="CXS/2023")

        # Options
        layout.prop(self, "options", text="Options",
                icon='DISCLOSURE_TRI_DOWN' if self.options
                else 'DISCLOSURE_TRI_RIGHT')
        if self.options:
            col = layout.column(align=True)

            row = col.row()
            sub = row.column(align=True)
            sub.ui_units_x = 2
            sub.separator()
            # Hud
            sub = row.column()
            sub.ui_units_x = 2
            sub.label(text="HUD:")

            # Mode
            sub = row.column(align=True)
            sub.ui_units_x = 3
            sub.label(text="Mode")
            sub.prop(self, "hud_01_size")
            sub.prop(self, "hud_01_pos_x")
            sub.prop(self, "hud_01_pos_y")
            # Tool
            sub = row.column(align=True)
            sub.ui_units_x = 3
            sub.label(text="Tool")
            sub.prop(self, "hud_02_size")
            sub.prop(self, "hud_02_pos_x")
            sub.prop(self, "hud_02_pos_y")
            # Data
            sub = row.column(align=True)
            sub.ui_units_x = 3
            sub.label(text="Data")
            sub.prop(self, "hud_03_size")
            sub.prop(self, "hud_03_pos_x")
            sub.prop(self, "hud_03_pos_y")

            sub = row.column(align=True)
            sub.ui_units_x = 2
            sub.separator()

            col.separator()


            # UI
            row = col.row()
            sub = row.column(align=True)
            sub.ui_units_x = 2
            sub.separator()
            sub = row.column()
            sub.ui_units_x = 2
            sub.label(text="UI:")

            sub = row.row()
            funct_bt(layout=sub, cmd='togxheader',tog=True, w=4.5, h=1, label='CUSTOM HEADER', icon="NONE")
            subsub = sub.column()
            subsub.ui_units_x = 4.5
            subsub.prop(self, "tool_text", toggle=True)

            sub = row.column(align=True)
            sub.ui_units_x = 2
            sub.separator()

            col.separator()

            # Img Path
            row = col.row()
            sub = row.column(align=True)
            sub.ui_units_x = 2
            sub.separator()
            sub = row.column()
            sub.ui_units_x = 2
            sub.label(text="IMG PATH:")

            sub = row.column(align=True)
            sub.ui_units_x = 9.4
            sub.prop(self, "tex_path", text="")

            sub = row.column(align=True)
            sub.ui_units_x = 2
            sub.separator()

            col.separator()

        # Floaters

        layout.prop(self, "floaters", text="Floaters",
                icon='DISCLOSURE_TRI_DOWN' if self.floaters
                else 'DISCLOSURE_TRI_RIGHT')
        if self.floaters:
            col = layout.column(align=True)
            row = col.row()

            sub = row.column(align=True)
            sub.ui_units_x = 2
            sub.separator()

            sub = row.column()
            sub.ui_units_x = 3
            sub.prop(self,"floaters_item", expand=True)
            sub = row.column(align=True)
            sub.ui_units_x = 1
            sub.label(text='>>')

            istr = self.floaters_item
            sub = row.column(align=True)
            sub.ui_units_x = 2
            sub.label(text='Width')
            sub.label(text='Height')
            sub.label(text='Pos X')
            sub.label(text='Pos Y')
            sub.label(text='Alpha')
            sub = row.column(align=True)
            sub.prop(self,f"floater_{istr}_size", text="")
            sub.prop(self,f"floater_{istr}_pos", text="")
            sub.prop(self,f"floater_{istr}_alpha", text="")

            sub = row.column(align=True)
            sub.ui_units_x = 2
            sub.separator()

            col.separator()

            row = col.row()

            sub = row.column(align=True)
            sub.ui_units_x = 2
            sub.separator()

            sub = row.column(align=True)
            sub.ui_units_x = 2.2
            sub.operator('xm.clearscreens', text='CLR SCREENS')
            sub = row.column(align=True)
            sub.label(text="Remove temp screens. Close all windows. File > Clean Up > Unused Data Blocks")

            sub = row.column(align=True)
            sub.ui_units_x = 2
            sub.separator()

        # Keymaps
        layout.prop(self, "keymaps", text="Keymaps",
                icon='DISCLOSURE_TRI_DOWN' if self.keymaps
                else 'DISCLOSURE_TRI_RIGHT')
        if self.keymaps:
            col = layout.column()

            box=col.box()
            kc = wm.keyconfigs.addon
            km = kc.keymaps['3D View Generic']
            kmi = get_menu_hotkey_entry_item(km, 'wm.call_menu_pie', 'OBJECT_MT_modes_menu')
            if kmi:
                box.context_pointer_set("keymap", km)
                rna_keymap_ui.draw_kmi([], kc, km, kmi, box, 0)
            else:
                box.label(text="No hotkey entry found")
                op = box.operator(Template_Add_Hotkey.bl_idname, text = "Add hotkey entry", icon = 'NONE')
                op.cmd = 'modes_pie'

            box = col.box()
            kc = wm.keyconfigs.addon
            km = kc.keymaps['Window']
            kmi = get_hotkey_entry_item(km, 'xm.floater_00')
            if kmi:
                box.context_pointer_set("keymap", km)
                rna_keymap_ui.draw_kmi([], kc, km, kmi, box, 0)
            else:
                box.label(text="No hotkey entry found")
                op = box.operator(Template_Add_Hotkey.bl_idname, text = "Add hotkey entry", icon = 'NONE')
                op.cmd = 'floater_00'

            box = col.box()
            kc = wm.keyconfigs.addon
            km = kc.keymaps['Window']
            kmi = get_hotkey_entry_item(km, 'xm.floater_01')
            if kmi:
                box.context_pointer_set("keymap", km)
                rna_keymap_ui.draw_kmi([], kc, km, kmi, box, 0)
            else:
                box.label(text="No hotkey entry found")
                op = box.operator(Template_Add_Hotkey.bl_idname, text = "Add hotkey entry", icon = 'NONE')
                op.cmd = 'floater_01'

            box = col.box()
            kc = wm.keyconfigs.addon
            km = kc.keymaps['Window']
            kmi = get_hotkey_entry_item(km, 'xm.floater_02')
            if kmi:
                box.context_pointer_set("keymap", km)
                rna_keymap_ui.draw_kmi([], kc, km, kmi, box, 0)
            else:
                box.label(text="No hotkey entry found")
                op = box.operator(Template_Add_Hotkey.bl_idname, text = "Add hotkey entry", icon = 'NONE')
                op.cmd = 'floater_02'

            box = col.box()
            kc = wm.keyconfigs.addon
            km = kc.keymaps['Window']
            kmi = get_hotkey_entry_item(km, 'xm.floater_03')
            if kmi:
                box.context_pointer_set("keymap", km)
                rna_keymap_ui.draw_kmi([], kc, km, kmi, box, 0)
            else:
                box.label(text="No hotkey entry found")
                op = box.operator(Template_Add_Hotkey.bl_idname, text = "Add hotkey entry", icon = 'NONE')
                op.cmd = 'floater_03'

            box = col.box()
            kc = wm.keyconfigs.addon
            km = kc.keymaps['Window']
            kmi = get_hotkey_entry_item(km, 'xm.floater_04')
            if kmi:
                box.context_pointer_set("keymap", km)
                rna_keymap_ui.draw_kmi([], kc, km, kmi, box, 0)
            else:
                box.label(text="No hotkey entry found")
                op = box.operator(Template_Add_Hotkey.bl_idname, text = "Add hotkey entry", icon = 'NONE')
                op.cmd = 'floater_04'

            box = col.box()
            kc = wm.keyconfigs.addon
            km = kc.keymaps['Window']
            kmi = get_hotkey_entry_item(km, 'xm.floater_05')
            if kmi:
                box.context_pointer_set("keymap", km)
                rna_keymap_ui.draw_kmi([], kc, km, kmi, box, 0)
            else:
                box.label(text="No hotkey entry found")
                op = box.operator(Template_Add_Hotkey.bl_idname, text = "Add hotkey entry", icon = 'NONE')
                op.cmd = 'floater_05'


# KEY-MAPS ----------------------------------------------------------------------------------------------------------------------- #

addon_keymaps = [] 
         
def get_menu_hotkey_entry_item(km, kmi_name, kmi_value):
    for i, km_item in enumerate(km.keymap_items):
        if km.keymap_items.keys()[i] == kmi_name:
            if km.keymap_items[i].properties.name == kmi_value:
                return km_item
    return None 

def get_hotkey_entry_item(km, kmi_name):
    for km_item in km.keymap_items:
        if km_item.idname == kmi_name:
            return km_item
    return None

def add_hotkey(cmd):
    wm = bpy.context.window_manager
    kc = wm.keyconfigs.addon

    if kc:
        if cmd == 'modes_pie':
            km = wm.keyconfigs.addon.keymaps.new(name='3D View Generic', space_type='VIEW_3D', region_type='WINDOW')
            kmi = km.keymap_items.new('wm.call_menu_pie', 'TAB', 'PRESS', ctrl=False, shift=False, alt=False)
            kmi.properties.name = "OBJECT_MT_modes_menu"
            kmi.active = True
            addon_keymaps.append((km, kmi))
        if cmd == 'floater_00':
            km = wm.keyconfigs.addon.keymaps.new(name='Window', space_type='EMPTY')
            kmi = km.keymap_items.new('xm.floater_00', 'SPACE', 'PRESS', ctrl=False, shift=False, alt=False)
            kmi.active = True
            addon_keymaps.append((km, kmi))
        if cmd == 'floater_01':
            km = wm.keyconfigs.addon.keymaps.new(name='Window', space_type='EMPTY')
            kmi = km.keymap_items.new('xm.floater_01', 'SIX', 'PRESS', ctrl=False, shift=False, alt=False)
            kmi.active = True
            addon_keymaps.append((km, kmi))
        if cmd == 'floater_02':
            km = wm.keyconfigs.addon.keymaps.new(name='Window', space_type='EMPTY')
            kmi = km.keymap_items.new('xm.floater_02', 'SEVEN', 'PRESS', ctrl=False, shift=False, alt=False)
            kmi.active = True
            addon_keymaps.append((km, kmi))
        if cmd == 'floater_03':
            km = wm.keyconfigs.addon.keymaps.new(name='Window', space_type='EMPTY')
            kmi = km.keymap_items.new('xm.floater_03', 'EIGHT', 'PRESS', ctrl=False, shift=False, alt=False)
            kmi.active = True
            addon_keymaps.append((km, kmi))
        if cmd == 'floater_04':
            km = wm.keyconfigs.addon.keymaps.new(name='Window', space_type='EMPTY')
            kmi = km.keymap_items.new('xm.floater_04', 'NINE', 'PRESS', ctrl=False, shift=False, alt=False)
            kmi.active = True
            addon_keymaps.append((km, kmi))
        if cmd == 'floater_05':
            km = wm.keyconfigs.addon.keymaps.new(name='Window', space_type='EMPTY')
            kmi = km.keymap_items.new('xm.floater_05', 'ZERO', 'PRESS', ctrl=False, shift=False, alt=False)
            kmi.active = True
            addon_keymaps.append((km, kmi))

        #Menu
        #kmi = km.keymap_items.new('wm.call_panel', 'SPACE', 'PRESS', ctrl=True, shift=False, alt=False)
        #kmi.properties.name = "OBJECT_PT_***_menu"
        #kmi.properties.keep_open = True


class Template_Add_Hotkey(bpy.types.Operator):
    bl_idname = "template.add_hotkey"
    bl_label = "Addon Preferences Example"
    bl_options = {'REGISTER', 'INTERNAL'}

    cmd: bpy.props.StringProperty()

    def execute(self, context):
        add_hotkey(cmd=self.cmd)
        self.report({'INFO'}, "Hotkey added")
        return {'FINISHED'}

def unregister_keymaps():
	for km, kmi in addon_keymaps:
		km.keymap_items.remove(kmi)
	addon_keymaps.clear()

def remove_hotkey():
    wm = bpy.context.window_manager
    kc = wm.keyconfigs.addon
    km = kc.keymaps['3D View Generic']
    
    for km, kmi in addon_keymaps:
        km.keymap_items.remove(kmi)
        wm.keyconfigs.addon.keymaps.remove(km)
    addon_keymaps.clear()


# ----------------------------------------------------------------------------------------------------------------------- #
addon_keymaps = []

classes = (XPrefs, Template_Add_Hotkey)

def register():
    for cls in classes:
        bpy.utils.register_class(cls)

    add_hotkey(cmd='modes_pie')
    add_hotkey(cmd='floater_00')
    add_hotkey(cmd='floater_01')
    add_hotkey(cmd='floater_02')
    add_hotkey(cmd='floater_03')
    add_hotkey(cmd='floater_04')
    add_hotkey(cmd='floater_05')
    add_hotkey(cmd='floater_06')

def unregister() :
    for cls in classes:
        bpy.utils.unregister_class(cls)

    unregister_keymaps()