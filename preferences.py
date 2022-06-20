import os
import bpy
from bpy.props import StringProperty, IntProperty, BoolProperty
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


    #///////////////////////////MENU/////////////////////////////////#

    def draw(self, context):
        layout = self.layout

        col = layout.column()
        col.use_property_split = True

        col.label(text="HUD:")
        sub = col.column()
        slots = sub.row()
        slots.scale_y = 1.2
        slots.prop(self,"hud_items", text='ITEMS', expand=True)
        col.separator()

        istr = self.hud_items

        box = col.box()
        propcol = box.column()
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

        col = layout.column()
        col.label(text="FLOATING EDITORS:")

        sub = col.column()

        slots = sub.row()
        slots.scale_y = 1.2
        slots.prop(self,"floaters", expand=True)
        col.separator()

        istr = self.floaters

        box = col.box()
        propcol = box.column()
        propcol.use_property_split = True

        propcol.prop(self,f"floater_{istr}_size",)
        propcol.separator()
        propcol.prop(self,f"floater_{istr}_pos",)
        propcol.separator()
        propcol.prop(self,f"floater_{istr}_alpha",)
        propcol.separator()

#////////////////////////////////////////////////////////////////////////////////////////////#

def register() :
    bpy.utils.register_class(XPrefs)

def unregister() :
    bpy.utils.unregister_class(XPrefs) 


