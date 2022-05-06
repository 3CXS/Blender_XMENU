import bpy
from .hud import redraw_regions
from .functions import tool_grid, tool_bt, funct_bt
from bpy.types import Operator, AddonPreferences
from bl_ui.properties_data_modifier import DATA_PT_modifiers
from bpy.types import Header, Panel
from .menuitems import SculptBrushSettings, ViewCam, Color, ToolOptions, TopoRake, BrushCopy
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
        top_row = layout.row(align=False)
        top_left = top_row.row(align=False)
        top_left.ui_units_x = 20
        top_left.alignment = 'LEFT'
        top_mid = top_row.row(align=False)
        top_mid.alignment = 'CENTER'
        top_right = top_row.row(align=False)
        top_right.ui_units_x = 20
        top_right.alignment = 'RIGHT'

        main_row = layout.row()   
        main_left = main_row.column()
        main_left.ui_units_x = 20
        main_left.alignment = 'LEFT'
        main_mid = main_row.column()
        main_mid.alignment = 'CENTER'
        main_right = main_row.column()
        main_right.ui_units_x = 20
        main_right.alignment = 'RIGHT'

        #TOP-ROW////////////////////////////////////////////////////////////////////////////////#
        SculptBrushSettings(self, context, parent=top_mid)

        #TOP-LEFT//////////////////////////////////////////// 
        shades = top_left.row()
        shades.ui_units_x = 5
        if bpy.context.mode == 'EDIT_MESH': 
            shades.template_edit_mode_selection()
        else:      
            shades.operator("object.shade_flat")
            shades.operator("object.shade_smooth")
        top_left.separator(factor = 4)  

        top_left.operator('xmenu.mask', text='FILL').cmd='FILL'
        top_left.operator('xmenu.mask', text='CLEAR').cmd='CLEAR'
        top_left.operator('xmenu.mask', text='INV').cmd='INVERT'
        top_left.operator('xmenu.mask', text='-').cmd='SHRINK'
        top_left.operator('xmenu.mask', text='+').cmd='GROW'
        top_left.operator('xmenu.mask', text='SHARP').cmd='SHARPEN'
        top_left.operator('xmenu.mask', text='SMOOTH').cmd='SMOOTH'
        #TOP-MID//////////////////////////////////////////////


        #TOP-RIGHT////////////////////////////////////////////

        opt = top_right.column(align=True)
        ToolOptions(self, context, parent=opt)
        top_right.separator(factor = 1)  
        funct_bt(parent=top_right, cmd='hud', tog=False, w=2, h=1, label='HUD', icon="NONE") 
        top_right.separator(factor = 4)


        #MAIN-ROW////////////////////////////////////////////////////////////////////////////////#
        #MAIN-LEFT////////////////////////////////////////////      
        main_leftbox = main_left.box()
        main_leftbox.ui_units_y = 0.6
        main_leftrow = main_left.row()
        main_leftrow.alignment = 'LEFT'

        cam = main_leftrow.column(align=True)
        ViewCam(self, context, parent=cam)


        #color = main_leftrow.column()
        #Color(self, context, parent=color)

        col = main_leftrow.column()
        col.ui_units_x = 4
        col.popover("VIEW3D_PT_tools_brush_texture")
        col.popover("VIEW3D_PT_tools_brush_stroke")
        col.popover("VIEW3D_PT_tools_brush_falloff")   
        
        #col = main_leftrow.column()
        #col.ui_units_x = 4
        subrow = col.row()
        subrow.scale_y = 0.3
        BrushCopy(self, context, parent=subrow)

        col = main_leftrow.column()
        col.ui_units_x = 10
        subrow = col.row()
        subrow.scale_y = 1
        subrow.menu_contents("VIEW3D_MT_BrushTexture")


        #main_leftrow.popover("VIEW3D_PT_tools_brush_display")

        #MAIN-MID//////////////////////////////////////////////
        main_midbox = main_mid.box()
        main_midbox.ui_units_y = 1
        main_midrow = main_mid.row()
        main_midrow.alignment = 'CENTER'

        midsubcol1 = main_midrow.column()
        midsubcol1.alignment = 'LEFT'
        midrow1_1 = midsubcol1.row()
        midrow1_1.ui_units_y = 1.7
        midrow1_1.alignment = 'LEFT' 
        midrow1_2 = midsubcol1.row()
        midrow1_2.alignment = 'LEFT' 
        midrow1_2.ui_units_y = 2.4
        midrow1_3 = midsubcol1.row()
        midrow1_3.alignment = 'LEFT'
        midrow1_3.ui_units_y = 3

        midsubcol2 = main_midrow.column()
        midsubcol2.alignment = 'CENTER'
        midrow2_1 = midsubcol2.row()
        midrow2_1.ui_units_y = 2.4
        midrow2_1.alignment = 'CENTER' 
        midrow2_2 = midsubcol2.row()
        midrow2_2.alignment = 'CENTER' 
        midrow2_2.ui_units_y = 2.4
        midrow2_3 = midsubcol2.row()
        midrow2_3.alignment = 'CENTER'
        midrow2_3.ui_units_y = 3

        midsubcol3 = main_midrow.column()
        midsubcol3.alignment = 'RIGHT'
        midrow3_1 = midsubcol3.row()
        midrow3_1.ui_units_y = 1.7
        midrow3_1.alignment = 'RIGHT' 
        midrow3_2 = midsubcol3.row()
        midrow3_2.alignment = 'RIGHT' 
        midrow3_2.ui_units_y = 2.4
        midrow3_3 = midsubcol3.row()
        midrow3_3.alignment = 'RIGHT'
        midrow3_3.ui_units_y = 3

        #GRAB/////////////////
        tool_bt(parent=midrow1_1, cmd=18, w=2, h=1.4, text=False, icon='LARGE')
        tool_bt(parent=midrow1_1, cmd=0, w=2, h=1.4, text=False, icon='LARGE')
        midrow1_1.separator(factor = 0.2)
        midrow1_2.separator(factor = 4)
        #EXTRA3/////////////////
        tool_grid(parent=midrow1_2, col=3, align=True, slotmin=19, slotmax=23, w=1.2, h=1, icon='CUSTOM')
        midrow1_2.separator(factor = 0.2)
        #CLAY////////////////
        tool_grid(parent=midrow2_1, col=3, align=True, slotmin=1, slotmax=4, w=2, h=1.4, text=True, icon='LARGE')
        midrow2_1.separator(factor = 0.2)
        tool_grid(parent=midrow2_2, col=3, align=True, slotmin=4, slotmax=7, w=2, h=1.4, text=True, icon='LARGE')
        #EXTRA2/////////////////
        tool_grid(parent=midrow2_2, col=1, align=True, slotmin=23, slotmax=25, w=1.2, h=1, icon='CUSTOM')
        #SMOOTH/////////////////
        tool_bt(parent=midrow2_2, cmd=25, w=2.2, h=1, text=False, icon='OFF')
        #EXTRA3/////////////////
        tool_grid(parent=midrow2_2, col=1, align=True, slotmin=26, slotmax=28, w=1.2, h=1, icon='CUSTOM')
        #CREASE//////////////     
        tool_grid(parent=midrow2_1, col=2, align=True, slotmin=7, slotmax=9, w=2, h=1.4, text=True, icon='LARGE')
        midrow2_1.separator(factor = 0.2)
        #POLISH////////////     
        tool_grid(parent=midrow2_1, col=2, align=True, slotmin=9, slotmax=11, w=2, h=1.4, text=True, icon='LARGE')
        midrow2_1.separator(factor = 0.2)
        tool_grid(parent=midrow2_2, col=2, align=True, slotmin=11, slotmax=13, w=2, h=1.4, text=True, icon='LARGE')    
        midrow2_2.separator(factor = 0.2)
        #MASK//////////// 
        tool_grid(parent=midrow3_1, col=2, align=True, slotmin=13, slotmax=14, w=2, h=1.4, icon='LARGE', text=False)
        mask_col = midrow3_1.column()
        mask_col.ui_units_x = 3.4
        mask_label_col = mask_col.column()
        mask_label_col.scale_y = 0.5
        mask_label_col.label(text="MASK")
        mask_grid = mask_col.grid_flow(columns=3, align=True)
        tool_bt(parent=mask_grid, cmd=28, w=1.2, h=0.8, text=False, icon='CUSTOM')
        tool_bt(parent=mask_grid, cmd=29, w=1, h=0.8, text=False, icon='CUSTOM')
        tool_bt(parent=mask_grid, cmd=30, w=1.2, h=0.8, text=False, icon='CUSTOM')
        #HIDE
        tool_bt(parent=midrow3_1, cmd=15, w=2.4, h=1.4, text=False, icon='LARGE')
        #FSETS//////////////
        tool_bt(parent=midrow3_2, cmd=14, w=2, h=1.4, text=False, icon='LARGE')
        fset_col = midrow3_2.column()        
        fset_grid_grid = fset_col.grid_flow(columns=2, align=True)
        tool_bt(parent=fset_grid_grid, cmd=31, w=1.5, h=0.75, text=False, icon='CUSTOM')
        tool_bt(parent=fset_grid_grid, cmd=32, w=1.5, h=0.75, text=False, icon='CUSTOM')
        tool_bt(parent=fset_col, cmd=33, w=1.2, h=0.5, text=False, icon='OFF')
        #RAKE////////////////
        TopoRake(self, context, parent=midrow3_3)


        #TRIM//////////////// 
        trim_col = midrow3_2.column()
        trim_col.ui_units_x = 2.4
        trim_label_col = trim_col.column()
        trim_label_col.scale_y = 0.5
        trim_label_col.label(text="TRIM")
        trim_grid = trim_col.grid_flow(columns=2, align=True)
        tool_bt(parent=trim_grid, cmd=16, w=1.2, h=0.8, icon="CUSTOM", text=False)
        tool_bt(parent=trim_grid, cmd=17, w=1.2, h=0.8, icon="CUSTOM", text=False)
        #MAIN-RIGHT/////////////////////////////////////////////////////////////////////////////////////
        main_rightbox = main_right.box()
        main_rightbox.ui_units_y = 0.6
        main_rightrow = main_right.row()
        main_rightrow.alignment = 'RIGHT'

        if bpy.context.mode == 'SCULPT': 
            sym = main_rightrow.column(align=False)
            sym.menu_contents("VIEW3D_MT_sculpt_sym")
            dyna = main_rightrow.column(align=False)
            dyna.menu_contents("VIEW3D_MT_dynamesh")
            remesh = main_rightrow.column(align=False)
            remesh.menu_contents("VIEW3D_MT_remesh")


        
        #//////////////////////////////////////////////////////////////////////////////////#
        redraw_regions()

        box = layout.box()
        box.ui_units_y = 12

#////////////////////////////////////////////////////////////////////////////////////////////#

def register() :
    bpy.utils.register_class(XPanel)

def unregister() :
    bpy.utils.unregister_class(XPanel)
