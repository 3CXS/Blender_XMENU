import os
import bpy
from bpy.props import StringProperty, IntProperty, BoolProperty
#////////////////////////////////////////////////////////////////////////////////////////////#
editors_items = [
    ('VIEW_3D','3D Viewport','','VIEW3D',1),
    ('IMAGE_EDITOR','Image Editor','','IMAGE',2),
    ('UV','Uv Editor','','UV',3),
    ('ShaderNodeTree','Shader Editor','','NODE_MATERIAL',4),
    ('GeometryNodeTree','Geonode Editor','','NODETREE',5),
    ('CompositorNodeTree','Compositor','','NODE_COMPOSITING',6),
    ('TextureNodeTree','Texture Editor','','NODE_TEXTURE',7),
    ('SEQUENCE_EDITOR','Video Sequencer','','SEQUENCE',8),
    ('CLIP_EDITOR','Movie Clip Editor','','TRACKER',9),
    ('DOPESHEET','Dope Sheet','','ACTION',10),
    ('TIMELINE','Timeline','','TIME',11),
    ('FCURVES','Graph Editor','','GRAPH',12),
    ('DRIVERS','Drivers','','TRACKING',13),
    ('NLA_EDITOR','Non-Linear','','NLA',14),
    ('TEXT_EDITOR','Text Editor','','TEXT',15),
    ('CONSOLE','Python Console','','CONSOLE',16),
    ('INFO','Info','','INFO',17),
    ('OUTLINER','Outliner','','OUTLINER',18),
    ('PROPERTIES','Properties','','PROPERTIES',19),
    ('FILES','File Browser','','FILEBROWSER',20),
    ('ASSETS','Asset Browser','','ASSET_MANAGER',21),
    ('PREFERENCES','Preferences','','PREFERENCES',22),
    ]

def centerscreen():
    center_x = bpy.props.FloatProperty(name="center_x", default=1)
    center_y = bpy.props.FloatProperty(name="center_y", default=1)
    for window in bpy.context.window_manager.windows:
        for area in window.screen.areas:
            for region in area.regions:
                if region.type == 'WINDOW':
                    center_x = region.width/2+200
                    center_y = region.height/2-300
            return center_x, center_y

class XPrefs(bpy.types.AddonPreferences):
    bl_idname = __package__

    #///////////////////////////ITEMS////////////////////////////////#
    
    hud_activate: BoolProperty(name="HUD", default=True)
    hud_dpi: IntProperty(name="DPI", default=72)
    tool_icon: BoolProperty(name="TOOL ICON", default=True)
    tool_text: BoolProperty(name="TOOL TEXT", default=True)
    tex_path: StringProperty(name="Folder Path",subtype='DIR_PATH',default="")

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


    #///////////////////////////MENU/////////////////////////////////#

    def draw(self, context):
        layout = self.layout

        box = layout.box()

        box.prop(self, "hud_activate", toggle=False)
        box.prop(self, "hud_dpi", toggle=False)
        box.prop(self, "tool_icon", toggle=False)
        box.prop(self, "tool_text", toggle=False)
        box.prop(self, "tex_path", text="")

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
        propcol.prop(self,f"floater_{istr}_key",)
        propcol.separator()
        #propcol.prop(self,f"float_{istr}_name",)
        #propcol.separator()
        #propcol.prop(self,f"float_{istr}_type",)
        #propcol.separator()




#////////////////////////////////////////////////////////////////////////////////////////////#

def register() :
    bpy.utils.register_class(XPrefs)


def unregister() :
    bpy.utils.unregister_class(XPrefs) 


