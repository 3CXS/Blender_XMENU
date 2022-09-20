import os
import bpy
from bpy.props import StringProperty, IntProperty, FloatProperty, BoolProperty, EnumProperty

import rna_keymap_ui


#-----------------------------------------------------------------------------------------------------------------------
def centerscreen():
    center_x = bpy.props.FloatProperty(name="center_x", default=1)
    center_y = bpy.props.FloatProperty(name="center_y", default=1)
    for window in bpy.context.window_manager.windows:
        for area in window.screen.areas:
            for region in area.regions:
                if region.type == 'WINDOW':
                    center_x = region.width/2
                    center_y = region.height/2
            return center_x, center_y

class XPrefs(bpy.types.AddonPreferences):
    bl_idname = __package__

    #PROPS---------------------------------------------------------------------------------
 
    hud_01_size: IntProperty(name="Size", default=24)
    hud_01_pos_x: IntProperty(name="Pos X", default=25)
    hud_01_pos_y: IntProperty(name="Pos Y", default=100)

    hud_02_size: IntProperty(name="Size", default=14)
    hud_02_pos_x: IntProperty(name="Pos X", default=32)
    hud_02_pos_y: IntProperty(name="Pos Y", default=780)

    hud_03_size: IntProperty(name="Size", default=20)
    hud_03_pos_x: IntProperty(name="Pos X", default=318)
    hud_03_pos_y: IntProperty(name="Pos Y", default=62)

    tool_icon: BoolProperty(name="TOOL ICON", default=True)
    tool_text: BoolProperty(name="TOOL TEXT", default=True)
    header_inset: FloatProperty(name="Header Inset", default=15)


    tex_path: StringProperty(name="Tex Folder Path",subtype='DIR_PATH',default="")
    file_path: StringProperty(name="File Folder Path",subtype='DIR_PATH',default="")

    floater_01_name : bpy.props.StringProperty(default="1", name="Name",)
    floater_01_type : bpy.props.StringProperty(default='OUTLINER')
    floater_01_size : bpy.props.FloatVectorProperty(name="Size", size=2, default=(300,500),precision=0)
    floater_01_pos  : bpy.props.FloatVectorProperty(name="Pos", size=2, default=(1640,250),precision=0)
    floater_01_alpha: IntProperty(name="FLOAT ALPHA", default=70)

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
    floater_04_alpha: IntProperty(name="FLOAT ALPHA", default=70)

    floater_05_name : bpy.props.StringProperty(default="5", name="Name",)
    floater_05_type : bpy.props.StringProperty(default='UV')
    floater_05_size : bpy.props.FloatVectorProperty(name="Size", size=2, default=(1000,800),precision=0)
    floater_05_pos  : bpy.props.FloatVectorProperty(name="Pos", size=2, default=(200,250),precision=0)
    floater_05_alpha: IntProperty(name="FLOAT ALPHA", default=100)

    floater_06_name : bpy.props.StringProperty(default="6", name="Name",)
    floater_06_type : bpy.props.StringProperty(default='IMAGE_EDITOR')
    floater_06_size : bpy.props.FloatVectorProperty(name="Size", size=2, default=(800,800),precision=0)
    floater_06_pos  : bpy.props.FloatVectorProperty(name="Pos", size=2, default=(200,250),precision=0)
    floater_06_alpha: IntProperty(name="FLOAT ALPHA", default=100)

    floater_07_name : bpy.props.StringProperty(default="7", name="Name",)
    floater_07_type : bpy.props.StringProperty(default='GeometryNodeTree')
    floater_07_size : bpy.props.FloatVectorProperty(name="Size", size=2, default=(900,620),precision=0)
    floater_07_pos  : bpy.props.FloatVectorProperty(name="Pos", size=2, default=(1540,440),precision=0)
    floater_07_alpha: IntProperty(name="FLOAT ALPHA", default=70)

    floater_08_name : bpy.props.StringProperty(default="8", name="Name",)
    floater_08_type : bpy.props.StringProperty(default='VIEW_3D')
    floater_08_size : bpy.props.FloatVectorProperty(name="Size", size=2, default=(900,700),precision=0)
    floater_08_pos  : bpy.props.FloatVectorProperty(name="Pos", size=2, default=(100,300),precision=0)
    floater_08_alpha: IntProperty(name="FLOAT ALPHA", default=100)

    floater_09_name : bpy.props.StringProperty(default="9", name="Name",)
    floater_09_type : bpy.props.StringProperty(default='BakeWrangler_Tree')
    floater_09_size : bpy.props.FloatVectorProperty(name="Size", size=2, default=(800,600),precision=0)
    floater_09_pos  : bpy.props.FloatVectorProperty(name="Pos", size=2, default=(1540,440),precision=0)
    floater_09_alpha: IntProperty(name="FLOAT ALPHA", default=70)

    floater_10_name : bpy.props.StringProperty(default="10", name="Name",)
    floater_10_type : bpy.props.StringProperty(default='CompositorNodeTree')
    floater_10_size : bpy.props.FloatVectorProperty(name="Size", size=2, default=(900,700),precision=0)
    floater_10_pos  : bpy.props.FloatVectorProperty(name="Pos", size=2, default=(100,300),precision=0)
    floater_10_alpha: IntProperty(name="FLOAT ALPHA", default=70)


    key_00: StringProperty(default="TAB")
    key_01: StringProperty(default="SPACE")
    key_02: StringProperty(default="D")
    key_03: StringProperty(default="A")
    key_04: StringProperty(default="FOUR")
    key_05: StringProperty(default="FIVE")
    key_06: StringProperty(default="SIX")
    key_07: StringProperty(default="SEVEN")
    key_08: StringProperty(default="EIGHT")
    key_09: StringProperty(default="NINE")
    key_10: StringProperty(default="ZERO")


    floaters : bpy.props.EnumProperty(default="01",items=[("01","Outliner",""),("02","Properties",""),("03","Modifiers",""),("04","Shader",""),
                                                            ("05","UV",""),("06","Image",""),("07","GeoNode",""),("08","Cam",""),("09","BakeTree",""),
                                                            ("10","Compositor","")])

    hud_items : bpy.props.EnumProperty(default="01",items=[("01","MODE",""),("02","TOOL",""),("03","DATA","")])

    prefs_tabs : EnumProperty(default='info', items=[('info', "Info", "INFO"),('options', "Options", "OPTIONS"),('floaters', "Floaters", "FLOATERS"), ('keymaps', "Keymaps", "KEYMAPS")])


    #MENU---------------------------------------------------------------------------------

    def draw(self, context):
        layout = self.layout
        wm = bpy.context.window_manager
        #layout.use_property_split = True
        row= layout.row(align=True)
        row.prop(self, "prefs_tabs", expand=True)

        if self.prefs_tabs == 'info':
            col = layout.column()
            split = col.split()
            sub = split.column()
            sub.label(text="xyx")
            sub.separator()
            sub.label(text="xxx")

        if self.prefs_tabs == 'options':
            col = layout.column()

            col.label(text="HUD:")
            sub = col.column()
            slots = sub.row()
            slots.scale_y = 1.2
            slots.prop(self,"hud_items", text='ITEMS', expand=True)
            col.separator()

            istr = self.hud_items

            sub = col.column()
            propcol = sub.column()
            propcol.use_property_split = True

            propcol.prop(self,f"hud_{istr}_size",)
            propcol.separator()
            propcol.prop(self,f"hud_{istr}_pos_x",)
            propcol.separator()
            propcol.prop(self,f"hud_{istr}_pos_y",)

            col = layout.column()
            col.label(text="PANEL:")
            col.use_property_split = True
            #col.prop(self, "tool_icon", toggle=False)
            col.prop(self, "tool_text", toggle=False)
            col.prop(self, "header_inset", toggle=False)

            col = layout.column()
            col.label(text="TEXTURE PATH:")
            col.use_property_split = True
            col.prop(self, "tex_path", text="")

            col = layout.column()
            col.label(text="FILE PATH:")
            col.use_property_split = True
            col.prop(self, "file_path", text="")

        if self.prefs_tabs == 'floaters':
            col = layout.column()
            col.label(text="FLOATING EDITORS:")

            sub = col.column()

            slots = sub.row()
            slots.scale_y = 1.2
            slots.prop(self,"floaters", expand=True)
            col.separator()

            istr = self.floaters

            sub = col.column()
            propcol = sub.column()
            propcol.use_property_split = True

            propcol.prop(self,f"floater_{istr}_size",)
            propcol.separator()
            propcol.prop(self,f"floater_{istr}_pos",)
            propcol.separator()
            propcol.prop(self,f"floater_{istr}_alpha",)
            propcol.separator()

        if self.prefs_tabs == 'keymaps':
            col = layout.column()
            col.label(text="KEYMAPS:")

            sub = col.column()

            slots = sub.column()
            slots.scale_y = 1.2
            slots.prop(self,"key_00", text='MODES PIE', expand=True)
            slots.prop(self,"key_01", text='TOOL MENU', expand=True)
            slots.prop(self,"key_02", text='PROP MENU', expand=True)
            slots.prop(self,"key_03", text='TOOLSET', expand=True)
            slots.prop(self,"key_04", text='FLOATER OUTLINER', expand=True)
            slots.prop(self,"key_05", text='FLOATER PROPS', expand=True)
            slots.prop(self,"key_06", text='FLOATER SHADER', expand=True)
            slots.prop(self,"key_07", text='FLOATER UV', expand=True)
            slots.prop(self,"key_08", text='FLOATER IMAGE', expand=True)
            slots.prop(self,"key_09", text='FLOATER GEO', expand=True)
            slots.prop(self,"key_10", text='FLOATER BAKE', expand=True)

#KEY MAPS-----------------------------------------------------------------------------------------------------------------------

def register_keymaps():

    wm = bpy.context.window_manager
    kc = wm.keyconfigs.addon
    if kc:

    # 3D VIEW
        km = wm.keyconfigs.addon.keymaps.new(name='3D View', space_type='VIEW_3D')

        # modes pie
        kmi = km.keymap_items.new('wm.call_menu_pie', bpy.context.preferences.addons[__package__].preferences.key_00, 'PRESS', ctrl=False, shift=False, alt=False)
        kmi.properties.name = "OBJECT_MT_modes_menu"
        addon_keymaps.append((km, kmi))

        # tools panel
        kmi = km.keymap_items.new('wm.call_panel', bpy.context.preferences.addons[__package__].preferences.key_01, 'PRESS', ctrl=False, shift=False, alt=False)
        kmi.properties.name = "OBJECT_PT_tool_menu"
        kmi.properties.keep_open = True
        addon_keymaps.append((km, kmi))

        # toolset hud
        kmi = km.keymap_items.new('xm.toolset', bpy.context.preferences.addons[__package__].preferences.key_03, 'PRESS', ctrl=False, shift=False, alt=False)
        addon_keymaps.append((km, kmi))
        kmi = km.keymap_items.new('xm.dyna', 'ONE', 'PRESS', ctrl=False, shift=False, alt=True)
        addon_keymaps.append((km, kmi))
        kmi = km.keymap_items.new('xm.voxelsize', 'TWO', 'PRESS', ctrl=False, shift=False, alt=True)
        kmi.properties.size = 0.01
        addon_keymaps.append((km, kmi))
        kmi = km.keymap_items.new('xm.voxelsize', 'THREE', 'PRESS', ctrl=False, shift=False, alt=True)
        kmi.properties.size = 0.02
        addon_keymaps.append((km, kmi))
        kmi = km.keymap_items.new('xm.voxelsize', 'FOUR', 'PRESS', ctrl=False, shift=False, alt=True)
        kmi.properties.size = 0.05
        addon_keymaps.append((km, kmi))

        kmi = km.keymap_items.new('xm.settool', 'FIVE', 'PRESS', ctrl=False, shift=False, alt=True)
        kmi.properties.tool_index = 14
        addon_keymaps.append((km, kmi))

    # WINDOW
        km = wm.keyconfigs.addon.keymaps.new(name='Window', space_type='EMPTY')

        # tools panel
        kmi = km.keymap_items.new('wm.call_panel', bpy.context.preferences.addons[__package__].preferences.key_02, 'PRESS', ctrl=False, shift=False, alt=False)
        kmi.properties.name = "OBJECT_PT_prop_menu"
        addon_keymaps.append((km, kmi))

        # floaters
        kmi = km.keymap_items.new('xm.floater_01', bpy.context.preferences.addons[__package__].preferences.key_04, 'PRESS', ctrl=False, shift=False, alt=False)
        addon_keymaps.append((km, kmi))
        kmi = km.keymap_items.new('xm.floater_02', bpy.context.preferences.addons[__package__].preferences.key_05, 'PRESS', ctrl=False, shift=False, alt=False)
        addon_keymaps.append((km, kmi))
        kmi = km.keymap_items.new('xm.floater_03', bpy.context.preferences.addons[__package__].preferences.key_06, 'PRESS', ctrl=False, shift=False, alt=False)
        addon_keymaps.append((km, kmi))
        kmi = km.keymap_items.new('xm.floater_04', bpy.context.preferences.addons[__package__].preferences.key_07, 'PRESS', ctrl=False, shift=False, alt=False)
        addon_keymaps.append((km, kmi))
        kmi = km.keymap_items.new('xm.floater_05', bpy.context.preferences.addons[__package__].preferences.key_08, 'PRESS', ctrl=False, shift=False, alt=False)
        addon_keymaps.append((km, kmi))
        kmi = km.keymap_items.new('xm.floater_06', bpy.context.preferences.addons[__package__].preferences.key_09, 'PRESS', ctrl=False, shift=False, alt=False)
        addon_keymaps.append((km, kmi))
        kmi = km.keymap_items.new('xm.floater_07', bpy.context.preferences.addons[__package__].preferences.key_10, 'PRESS', ctrl=False, shift=False, alt=False)
        addon_keymaps.append((km, kmi))


def unregister_keymaps():

    for km, kmi in addon_keymaps:
        km.keymap_items.remove(kmi)
    addon_keymaps.clear()

#-----------------------------------------------------------------------------------------------------------------------
addon_keymaps = []

def register() :
    bpy.utils.register_class(XPrefs)
    register_keymaps()

def unregister() :
    bpy.utils.unregister_class(XPrefs)
    unregister_keymaps()


