import os
import bpy
from bpy.props import StringProperty, IntProperty, BoolProperty, EnumProperty

import rna_keymap_ui
keymaps_items_dict = {
                      "ModesMenu":['wm.call_menu_pie', 'XM_MT_modes_menu', '3D View '
                                      'Generic', 'VIEW_3D', 'WINDOW',
                                      'TAB', 'PRESS', False, False, False
                                      ],
                      "MainMenu":['wm.call_menu', 'XM_MT_main_menu', '3D View '
                                      'Generic', 'VIEW_3D', 'WINDOW',
                                      'D', 'PRESS', False, False, False
                                      ],
                      "ToolMenu":['wm.call_menu', 'XM_MT_tool_menu', '3D View '
                                      'Generic', 'VIEW_3D', 'WINDOW',
                                      'SPACE', 'PRESS', False, False, False
                                      ],
                      "SelectMenu":['wm.call_menu', 'XM_MT_select_menu', '3D View '
                                      'Generic', 'VIEW_3D', 'WINDOW',
                                      'A', 'PRESS', False, False, False
                                      ],
                      "Floater01":['xmenu.floater_01', None, 'Window'
                                      '', 'EMPTY', 'WINDOW',
                                      'FOUR', 'PRESS', False, False, False
                                      ],
                      "Floater02":['xmenu.floater_02', None, 'Window'
                                      '', 'EMPTY', 'WINDOW',
                                      'FIVE', 'PRESS', False, False, False
                                      ],
                      "Floater03":['xmenu.floater_03', None, 'Window'
                                      '', 'EMPTY', 'WINDOW',
                                      'SIX', 'PRESS', False, False, False
                                      ],
                      "Floater04":['xmenu.floater_04', None, 'Window'
                                      '', 'EMPTY', 'WINDOW',
                                      'SEVEN', 'PRESS', False, False, False
                                      ],
                      "Floater05":['xmenu.floater_05', None, 'Window'
                                      '', 'EMPTY', 'WINDOW',
                                      'EIGHT', 'PRESS', False, False, False
                                      ],
                      "Floater06":['xmenu.floater_06', None, 'Window'
                                      '', 'EMPTY', 'WINDOW',
                                      'NINE', 'PRESS', False, False, False
                                      ],
                      "Floater07":['xmenu.floater_07', None, 'Window'
                                      '', 'EMPTY', 'WINDOW',
                                      'ZERO', 'PRESS', False, False, False
                                      ],
                     }

#////////////////////////////////////////////////////////////////////////////////////////////#
#////////////////////////////////////////////////////////////////////////////////////////////#
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

    #///////////////////////////ITEMS////////////////////////////////#
 
    hud_01_size: IntProperty(name="Size", default=24)
    hud_01_pos_x: IntProperty(name="Pos X", default=25)
    hud_01_pos_y: IntProperty(name="Pos Y", default=100)

    hud_02_size: IntProperty(name="Size", default=14)
    hud_02_pos_x: IntProperty(name="Pos X", default=35)
    hud_02_pos_y: IntProperty(name="Pos Y", default=800)

    hud_03_size: IntProperty(name="Size", default=20)
    hud_03_pos_x: IntProperty(name="Pos X", default=460)
    hud_03_pos_y: IntProperty(name="Pos Y", default=55)

    tool_icon: BoolProperty(name="TOOL ICON", default=True)
    tool_text: BoolProperty(name="TOOL TEXT", default=True)
    tex_path: StringProperty(name="Tex Folder Path",subtype='DIR_PATH',default="")

    file_path: StringProperty(name="File Folder Path",subtype='DIR_PATH',default="")

    floater_01_name : bpy.props.StringProperty(default="1", name="Name",)
    floater_01_type : bpy.props.StringProperty(default='OUTLINER')
    floater_01_size : bpy.props.FloatVectorProperty(name="Size", size=2, default=(300,500),precision=0)
    floater_01_pos  : bpy.props.FloatVectorProperty(name="Pos", size=2, default=centerscreen(),precision=0)
    floater_01_alpha: IntProperty(name="FLOAT ALPHA", default=100)

    floater_02_name : bpy.props.StringProperty(default="2", name="Name",)
    floater_02_type : bpy.props.StringProperty(default='PROPERTIES')
    floater_02_size : bpy.props.FloatVectorProperty(name="Size", size=2, default=(500,800),precision=0)
    floater_02_pos  : bpy.props.FloatVectorProperty(name="Pos", size=2, default=centerscreen(),precision=0)
    floater_02_alpha: IntProperty(name="FLOAT ALPHA", default=100)

    floater_03_name : bpy.props.StringProperty(default="3", name="Name",)
    floater_03_type : bpy.props.StringProperty(default='PROPERTIES')
    floater_03_size : bpy.props.FloatVectorProperty(name="Size", size=2, default=(500,800),precision=0)
    floater_03_pos  : bpy.props.FloatVectorProperty(name="Pos", size=2, default=centerscreen(),precision=0)
    floater_03_alpha: IntProperty(name="FLOAT ALPHA", default=100)

    floater_04_name : bpy.props.StringProperty(default="4", name="Name",)
    floater_04_type : bpy.props.StringProperty(default='ShaderNodeTree')
    floater_04_size : bpy.props.FloatVectorProperty(name="Size", size=2, default=(800,600),precision=0)
    floater_04_pos  : bpy.props.FloatVectorProperty(name="Pos", size=2, default=centerscreen(),precision=0)
    floater_04_alpha: IntProperty(name="FLOAT ALPHA", default=68)

    floater_05_name : bpy.props.StringProperty(default="5", name="Name",)
    floater_05_type : bpy.props.StringProperty(default='UV')
    floater_05_size : bpy.props.FloatVectorProperty(name="Size", size=2, default=(1000,800),precision=0)
    floater_05_pos  : bpy.props.FloatVectorProperty(name="Pos", size=2, default=centerscreen(),precision=0)
    floater_05_alpha: IntProperty(name="FLOAT ALPHA", default=100)

    floater_06_name : bpy.props.StringProperty(default="6", name="Name",)
    floater_06_type : bpy.props.StringProperty(default='IMAGE_EDITOR')
    floater_06_size : bpy.props.FloatVectorProperty(name="Size", size=2, default=(800,800),precision=0)
    floater_06_pos  : bpy.props.FloatVectorProperty(name="Pos", size=2, default=centerscreen(),precision=0)
    floater_06_alpha: IntProperty(name="FLOAT ALPHA", default=100)

    floater_07_name : bpy.props.StringProperty(default="7", name="Name",)
    floater_07_type : bpy.props.StringProperty(default='GeometryNodeTree')
    floater_07_size : bpy.props.FloatVectorProperty(name="Size", size=2, default=(800,600),precision=0)
    floater_07_pos  : bpy.props.FloatVectorProperty(name="Pos", size=2, default=centerscreen(),precision=0)
    floater_07_alpha: IntProperty(name="FLOAT ALPHA", default=68)

    floater_08_name : bpy.props.StringProperty(default="8", name="Name",)
    floater_08_type : bpy.props.StringProperty(default='VIEW_3D')
    floater_08_size : bpy.props.FloatVectorProperty(name="Size", size=2, default=(600,400),precision=0)
    floater_08_pos  : bpy.props.FloatVectorProperty(name="Pos", size=2, default=centerscreen(),precision=0)
    floater_08_alpha: IntProperty(name="FLOAT ALPHA", default=100)

    floaters : bpy.props.EnumProperty(default="01",items=[("01","Outliner",""),("02","Properties",""),("03","Modifiers",""),("04","Shader",""),("05","UV",""),("06","Image",""),("07","GeoNode",""),("08","Cam","")])

    hud_items : bpy.props.EnumProperty(default="01",items=[("01","MODE",""),("02","TOOL",""),("03","DATA","")])
    prefs_tabs : EnumProperty(default='info', items=[('info', "Info", "INFO"),('options', "Options", "OPTIONS"),('floaters', "Floaters", "FLOATERS"),('keymap', "Keymap", "KEYMAP")])

    #///////////////////////////MENU/////////////////////////////////#

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
            col.prop(self, "tool_icon", toggle=False)
            col.prop(self, "tool_text", toggle=False)

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

        if self.prefs_tabs == 'keymap':
            col = layout.column()
            col.label(text="KEYMAP:")

            sub = col.column()
            draw_keymap_items(wm, sub)


#////////////////////////////////////////////////////////////////////////////////////////////#
#////////////////////////////////////////////////////////////////////////////////////////////#

addon_keymaps = []

def draw_keymap_items(wm, layout):
    kc = wm.keyconfigs.user

    for name, items in keymaps_items_dict.items():
        kmi_name, kmi_value, km_name = items[:3]
        box = layout.box()
        split = box.split()
        col = split.column()
        col.label(text=name)
        col.separator()
        km = kc.keymaps[km_name]
        get_hotkey_entry_item(kc, km, kmi_name, kmi_value, col)


def get_hotkey_entry_item(kc, km, kmi_name, kmi_value, col):

    # for menus and pie_menu
    if kmi_value:
        for km_item in km.keymap_items:
            if km_item.idname == kmi_name and km_item.properties.name == kmi_value:
                col.context_pointer_set('keymap', km)
                rna_keymap_ui.draw_kmi([], kc, km, km_item, col, 0)
                return

        col.label(text = "No hotkey entry found for {}".format(kmi_value))
        col.operator(AddHotkey.bl_idname, icon='NONE')

    # for operators
    else:
        if km.keymap_items.get(kmi_name):
            col.context_pointer_set('keymap', km)
            rna_keymap_ui.draw_kmi(
                    [], kc, km, km.keymap_items[kmi_name], col, 0)
        else:
            col.label(text = "No hotkey entry found for {}".format(kmi_name))
            col.operator(AddHotkey.bl_idname, icon='NONE')


class AddHotkey(bpy.types.Operator):
    bl_idname = "xm.add_hotkey"
    bl_label = "Add Hotkeys"
    bl_options = {'REGISTER', 'INTERNAL'}

    def execute(self, context):
        add_hotkey()

        self.report({'INFO'},
                    "Hotkey added in User Preferences -> Input -> Screen -> Screen (Global)")
        return {'FINISHED'}

def add_hotkey():
    wm = bpy.context.window_manager
    kc = wm.keyconfigs.addon

    if not kc:
        return

    for items in keymaps_items_dict.values():
        kmi_name, kmi_value, km_name, space_type, region_type = items[:5]
        eventType, eventValue, ctrl, shift, alt = items[5:]
        km = kc.keymaps.new(name = km_name, space_type = space_type,
                            region_type=region_type)

        kmi = km.keymap_items.new(kmi_name, eventType,
                                  eventValue, ctrl = ctrl, shift = shift,
                                  alt = alt

                                  )
        if kmi_value:
            kmi.properties.name = kmi_value

        kmi.active = True

    addon_keymaps.append((km, kmi))


def remove_hotkey():
    kmi_values = [item[1] for item in keymaps_items_dict.values() if item]
    kmi_names = [item[0] for item in keymaps_items_dict.values() if item not in ['wm.call_menu', 'wm.call_menu_pie']]

    for km, kmi in addon_keymaps:
        # remove addon keymap for menu and pie menu
        if hasattr(kmi.properties, 'name'):
            if kmi_values:
                if kmi.properties.name in kmi_values:
                    km.keymap_items.remove(kmi)

        # remove addon_keymap for operators
        else:
            if kmi_names:
                if kmi.name in kmi_names:
                    km.keymap_items.remove(kmi)

    addon_keymaps.clear()


#////////////////////////////////////////////////////////////////////////////////////////////#
#////////////////////////////////////////////////////////////////////////////////////////////#
classes = (XPrefs, AddHotkey)


def register() :
    for cls in classes:
        bpy.utils.register_class(cls)
    add_hotkey()


def unregister() :
    for cls in classes:
        bpy.utils.unregister_class(cls)
    remove_hotkey()

