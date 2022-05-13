import bpy
from .hud import redraw_regions
from .functions import tool_grid, tool_bt, funct_bt
from bpy.types import Operator, AddonPreferences
from bl_ui.properties_data_modifier import DATA_PT_modifiers
from bpy.types import Header, Panel
from .menuitems import ViewCam, Color, ToolOptions, BrushCopy, Falloff, SculptBrushSettings, SculptToolSettings, SculptMask, SculptFaceSet, SculptTrim, Stroke, SmoothStroke
#////////////////////////////////////////////////////////////////////////////////////////////#

class XPanel(bpy.types.Panel):
    bl_idname = "SCENE_PT_xpanel"
    bl_label = "X-PANEL"
    bl_space_type = "PROPERTIES"
    bl_region_type = "WINDOW"
    bl_context = "scene"
    bl_order = 2000
    #bl_options = {'HIDE_HEADER','DEFAULT_CLOSED'}

    def draw(self, context):
        
        layout = self.layout
        layout.use_property_split = False
        layout.use_property_decorate = False

        ts = context.tool_settings
        scene = context.scene
        view = context.space_data
        wm = context.window_manager
        ups = ts.unified_paint_settings
        ptr = ups if ups.use_unified_color else ts.image_paint.brush
        tool_mode = context.mode
        #mesh = context.active_object.data
        brush = context.tool_settings.sculpt.brush
        settings = context.tool_settings.sculpt

        #LAYOUT-STRUCTURE/////////////////////////////////////////
        top_row = layout.row()
        top_left = top_row.row()
        top_left.ui_units_x = 20
        top_left.alignment = 'RIGHT'
        top_mid = top_row.row()
        top_mid.alignment = 'CENTER'
        top_right = top_row.row()
        top_right.ui_units_x = 20
        top_right.alignment = 'LEFT'

        main_row = layout.row()   
        main_left = main_row.column()
        main_left.ui_units_x = 20
        main_left.alignment = 'RIGHT'
        main_mid = main_row.column()
        main_mid.alignment = 'CENTER'
        main_right = main_row.column()
        main_right.ui_units_x = 20
        main_right.alignment = 'LEFT'

        #TOP-ROW////////////////////////////////////////////////////////////////////////////////#
        #TOP-LEFT//////////////////////////////////////////// 
        row = top_left.row()
        row.ui_units_x = 5

        if bpy.context.mode == 'EDIT_MESH': 
            row.template_edit_mode_selection()
        else:      
            row.operator("object.shade_flat")
            row.operator("object.shade_smooth")

        top_left.separator(factor = 6)  
              
        #TOP-MID//////////////////////////////////////////////
        SculptMask(self, context, parent=top_left)
        top_mid.separator(factor = 1)

        if bpy.context.mode == 'SCULPT': 
            SculptBrushSettings(self, context, parent=top_mid)
        top_mid.separator(factor = 1)

        col = top_right.column(align=True)
        SculptFaceSet(self, context, parent=col)
        #TOP-RIGHT////////////////////////////////////////////
        top_right.separator(factor = 6)
        col = top_right.column(align=True)
        ToolOptions(self, context, parent=col)

        top_right.separator(factor = 2)  
        funct_bt(parent=top_right, cmd='hud', tog=False, w=2, h=1, label='HUD', icon="NONE") 
        #MAIN-ROW////////////////////////////////////////////////////////////////////////////////#
        #MAIN-LEFT////////////////////////////////////////////      
        main_leftbox = main_left.box()
        main_leftbox.ui_units_y = 0.6
        main_leftrow = main_left.row()
        main_leftrow.alignment = 'LEFT'

        col = main_leftrow.column(align=True)
        ViewCam(self, context, parent=col)
        col.separator(factor = 1)
        
        #Color(self, context, parent=col)

        col = main_leftrow.column()
        col.ui_units_x = 4
        col.popover("VIEW3D_PT_tools_brush_display")
        BrushCopy(self, context, parent=col)

        box = main_leftrow.box()     
        box.ui_units_x = 8
        subrow = box.row()
        subrow.menu_contents("VIEW3D_MT_BrushTexture")

        box = main_leftrow.box()     
        box.ui_units_x = 4
        Stroke(self, context, parent=box)

    
        #MAIN-MID//////////////////////////////////////////////
        main_midbox = main_mid.box()
        main_midbox.ui_units_y = 1
        main_midrow = main_mid.row()
        main_midrow.alignment = 'CENTER'

        #GRAB/////////////////
        col = main_midrow.column()
        col.alignment = 'LEFT'
        row = col.row(align=True)
        sub = row.column(align=True)
        sub.ui_units_x = 2
        sub.scale_y = 0.7
        sub.operator('xmenu.mask', text='PVT M').cmd='PMASKED'
        sub.operator('xmenu.mask', text='RESET').cmd='ORIGIN'
        tool_bt(parent=row, cmd=18, w=2, h=1.4, text=False, icon='LARGE')
        row.separator(factor = 1)
        tool_bt(parent=row, cmd=0, w=2, h=1.4, text=False, icon='LARGE')
        #EXTRA/////////////////
        col.separator(factor = 0.4)
        row = col.row()
        row.separator(factor = 11)
        tool_grid(parent=row, col=3, align=True, slotmin=19, slotmax=23, w=1.2, h=1, icon='CUSTOM')
        #TRIM
        col.separator(factor = 0.4)
        row = col.row()
        row.separator(factor = 4)
        SculptTrim(self, context, parent=row)
        #CLAY////////////////
        main_midrow.separator(factor = 0.4)
        col = main_midrow.column()
        row = col.row(align=True)
        tool_grid(parent=row, col=3, align=True, slotmin=1, slotmax=4, w=2, h=1.4, text=True, icon='LARGE')
        col.separator(factor = 0.4)
        row = col.row(align=True)
        tool_grid(parent=row, col=3, align=True, slotmin=4, slotmax=7, w=2, h=1.4, text=True, icon='LARGE')
        row = col.row(align=True)

        #CREASE///////////////
        col = main_midrow.column()
        row = col.row()
        row.separator(factor = 0.4)
        tool_grid(parent=row, col=2, align=True, slotmin=7, slotmax=9, w=2, h=1.4, text=True, icon='LARGE')
        row.separator(factor = 0.4)
        col.separator(factor = 0.4)
        row = col.row()
        tool_grid(parent=row, col=1, align=True, slotmin=23, slotmax=25, w=1.2, h=1, icon='CUSTOM')
        sub = row.column()
        tool_bt(parent=sub, cmd=25, w=1.8, h=1, text=False, icon='OFF')
        sub.menu_contents("VIEW3D_MT_Falloff")
        tool_grid(parent=row, col=1, align=True, slotmin=26, slotmax=28, w=1.2, h=1, icon='CUSTOM')

        #POLISH//////////// 
        col = main_midrow.column()
        row = col.row()
        tool_grid(parent=row, col=2, align=True, slotmin=9, slotmax=11, w=2, h=1.4, text=True, icon='LARGE')
        col.separator(factor = 0.4)
        row = col.row()
        tool_grid(parent=row, col=2, align=True, slotmin=11, slotmax=13, w=2, h=1.4, text=True, icon='LARGE')    
        #MASK//////////// 
        main_midrow.separator(factor = 0.4)
        col = main_midrow.column()
        row = col.row()
        tool_bt(parent=row, cmd=13, w=2, h=1.4, text=False, icon='LARGE') 
        sub = row.column()
        sub.ui_units_x = 3.4
        subsub = sub.column()
        subsub.scale_y = 0.5
        subsub.label(text="MASK")
        grid = sub.grid_flow(columns=3, align=True)
        tool_bt(parent=grid, cmd=28, w=1.2, h=0.8, text=False, icon='CUSTOM')
        tool_bt(parent=grid, cmd=29, w=1, h=0.8, text=False, icon='CUSTOM')
        tool_bt(parent=grid, cmd=30, w=1.2, h=0.8, text=False, icon='CUSTOM')
        #TRIM//////////////// 
        sub = row.column()
        sub.ui_units_x = 2.4
        subsub = sub.column()
        subsub.scale_y = 0.5
        subsub.label(text="TRIM")
        grid = sub.grid_flow(columns=2, align=True)
        tool_bt(parent=grid, cmd=16, w=1.2, h=0.8, icon="CUSTOM", text=False)
        tool_bt(parent=grid, cmd=17, w=1.2, h=0.8, icon="CUSTOM", text=False)
        #FSETS//////////////
        col.separator(factor = 0.4)
        row = col.row()
        tool_bt(parent=row, cmd=14, w=2, h=1.4, text=False, icon='LARGE')
        sub = row.column()       
        grid = sub.grid_flow(columns=2, align=True)
        tool_bt(parent=grid, cmd=31, w=1.5, h=0.75, text=False, icon='CUSTOM')
        tool_bt(parent=grid, cmd=32, w=1.5, h=0.75, text=False, icon='CUSTOM')
        tool_bt(parent=sub, cmd=33, w=1.2, h=0.5, text=False, icon='OFF')
        #HIDE
        subcol = row.column()
        subcol.ui_units_x = 2.4
        tool_bt(parent=subcol, cmd=15, w=2.4, h=1.4, text=False, icon='LARGE')

        #FILTER//////////////
        col.separator(factor = 0.4)
        row = col.row()
        tool_bt(parent=row, cmd=34, w=2, h=1.4, text=False, icon='OFF')
        SculptToolSettings(self, context, parent=row)

        #MAIN-RIGHT/////////////////////////////////////////////////////////////////////////////////////
        main_rightbox = main_right.box()
        main_rightbox.ui_units_y = 0.6
        main_rightrow = main_right.row()
        main_rightrow.alignment = 'RIGHT'

        if bpy.context.mode == 'SCULPT': 
            col = main_rightrow.column(align=False)
            col.menu_contents("VIEW3D_MT_sculpt_sym")
            col = main_rightrow.column(align=False)
            col.menu_contents("VIEW3D_MT_dynamesh")
            col = main_rightrow.column(align=False)
            col.menu_contents("VIEW3D_MT_remesh")

        end = main_rightrow.row()
        end.ui_units_x = 0.2
        end.ui_units_y = 7.6
        end.label(text="")
        #//////////////////////////////////////////////////////////////////////////////////#

        redraw_regions()

        box = layout.box()
        box.ui_units_y = 12

#////////////////////////////////////////////////////////////////////////////////////////////#

def register() :
    bpy.utils.register_class(XPanel)

def unregister() :
    bpy.utils.unregister_class(XPanel)
