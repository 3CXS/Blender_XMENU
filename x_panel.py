import bpy
from .hud import redraw_regions
from .functions import tool_grid, tool_bt, funct_bt
from bpy.types import Operator, AddonPreferences

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
        ts = context.tool_settings
        scene = context.scene
        view = context.space_data
        wm = context.window_manager
        ups = ts.unified_paint_settings
        ptr = ups if ups.use_unified_color else ts.image_paint.brush
        tool_mode = context.mode

        #LAYOUT-STRUCTURE/////////////////////////////////////////
        top_row = layout.row(align=False)
        top_left = top_row.row()
        top_left.ui_units_x = 16
        top_mid = top_row.row()
        top_right = top_row.row()
        top_right.ui_units_x = 16

        main_row = layout.row()   
        main_left = main_row.column()
        main_left.ui_units_x = 16
        main_mid = main_row.column()
        main_right = main_row.column()
        main_right.ui_units_x = 16

        #TOP-ROW/////////////////////////////////////////////////////////////
        #TOP-LEFT//////////////////////////////////////////// 
        topsubrow = top_left.row()
        topsubrow.ui_units_x = 5
        if bpy.context.mode == 'EDIT_MESH': 
            topsubrow.template_edit_mode_selection()
        else:      
            topsubrow.operator("object.shade_flat")
            topsubrow.operator("object.shade_smooth")
                
        top_left.prop(ts, "use_snap")
        top_left.prop(ts, "use_transform_data_origin")

        #TOP-MID//////////////////////////////////////////////
        grid = top_mid.grid_flow(columns=12, align=True)
        for i in range(12):
            grid.template_icon(i+24)
        #TOP-RIGHT////////////////////////////////////////////

        top_right.prop(ts, "use_mesh_automerge", text="Auto Merge")
        funct_bt(parent=top_right, cmd='overlay', tog=True, w=2, h=1, label='WIRE', icon="NONE")
        funct_bt(parent=top_right, cmd='xray', tog=True, w=2, h=1, label='XRAY', icon="NONE")

        
        #MAIN-ROW/////////////////////////////////////////////////////////////
        #MAIN-LEFT////////////////////////////////////////////      
        leftbox = main_left.box()
        leftbox.ui_units_y = 0.6  
        #col.scale_y = 0.8 
        funct_bt(parent=main_left, cmd='persp', tog=True, w=2, h=1, label='PERSP', icon="NONE")
        #main_left.separator()
        box = main_left.box()
        leftsubrow = box.row()
        funct_bt(parent=leftsubrow, cmd='frames', w=2, h=1, label='FRAME', icon="NONE")
        funct_bt(parent=leftsubrow, cmd='framea', w=2, h=1, label='ALL', icon="NONE")
   
        #MAIN-MID//////////////////////////////////////////////
        midbox = main_mid.box()
        midbox.ui_units_y = 0.6
        midrow = main_mid.row()

        midsubcol1 = midrow.column()
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

        midsubcol2 = midrow.column()
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

        midsubcol3 = midrow.column()
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
        tool_grid(parent=midrow2_2, col=1
        , align=True, slotmin=26, slotmax=28, w=1.2, h=1, icon='CUSTOM')
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
        #TRIM//////////////// 
        trim_col = midrow3_2.column()
        trim_col.ui_units_x = 2.4
        trim_label_col = trim_col.column()
        trim_label_col.scale_y = 0.5
        trim_label_col.label(text="TRIM")
        trim_grid = trim_col.grid_flow(columns=2, align=True)
        tool_bt(parent=trim_grid, cmd=16, w=1.2, h=0.8, icon="CUSTOM", text=False)
        tool_bt(parent=trim_grid, cmd=17, w=1.2, h=0.8, icon="CUSTOM", text=False)

        #MAIN-RIGHT///////////////////////////////////////////////////
        rightbox = main_right.box()
        rightbox.ui_units_y = 0.6
        row = main_right.row()
        sub = row.column()
        sub.scale_y = 0.7 
        sub.ui_units_x = 4
        sub.template_color_picker(ptr, 'color', value_slider=True)
        subsub = sub.row(align=True)
        subsub.prop(ptr, 'color', text="")
        subsub.prop(ptr, 'secondary_color', text="")
        sub = row.column()     
        sub = row.column()
        sub.scale_x = 0.6
        sub.label(text="ICECREAM:")
        funct_bt(parent=sub, cmd='viewcam', tog=True, w=2, h=1, label='VIEW CAM', icon="NONE")
        funct_bt(parent=sub, cmd='lockcam', tog=True, w=2, h=1, label='LOCK', icon="NONE")
        box = sub.box()
        box.operator("object.select_all")

        box.operator("xmenu.hud", icon="XRAY", depress=wm.hud_state)

        #///////////////////////////////////////////////////////////////
        redraw_regions()

        box = layout.box()
        box.ui_units_y = 12

#////////////////////////////////////////////////////////////////////////////////////////////#

def register() :
    bpy.utils.register_class(XPanel)

def unregister() :
    bpy.utils.unregister_class(XPanel)
