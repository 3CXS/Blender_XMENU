import bpy
from .hud import redraw_regions
from .functions import tool_grid, tool_bt, funct_bt
from bpy.types import Operator, AddonPreferences
from bl_ui.properties_data_modifier import DATA_PT_modifiers
from bpy.app.translations import contexts as i18n_contexts
from bpy.types import Header, Panel
from .menuitems import *
from .brushtexture import get_brush_mode
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

        #LAYOUT-STRUCTURE/////////////////////////////////////////
        top_row = layout.row()
        top_row.alignment = 'CENTER'
        top_left = top_row.row()
        top_left.ui_units_x = 22
        top_left.alignment = 'RIGHT'
        top_mid = top_row.row()
        top_mid.alignment = 'CENTER'
        top_mid.ui_units_x = 34
        top_right = top_row.row()
        top_right.ui_units_x = 22
        top_right.alignment = 'LEFT'

        main_row = layout.row()
        main_row.alignment = 'CENTER'  
        main_left = main_row.column()
        main_left.ui_units_x = 22
        #main_left.alignment = 'RIGHT'
        main_mid = main_row.column()
        main_mid.alignment = 'CENTER'
        main_mid.ui_units_x = 34
        main_right = main_row.column()
        main_right.ui_units_x = 22
        #main_right.alignment = 'LEFT'

        main_leftbox = main_left.box()
        main_leftbox.ui_units_y = 0.6
        main_leftrow = main_left.row()
        main_leftrow.alignment = 'RIGHT'

        main_midbox = main_mid.box()
        main_midbox.ui_units_y = 1
        main_midrow = main_mid.row()
        main_midrow.alignment = 'CENTER'

        main_rightbox = main_right.box()
        main_rightbox.ui_units_y = 0.6
        main_rightrow = main_right.row()
        main_rightrow.alignment = 'LEFT'

        if bpy.context.mode == 'OBJECT':
            #TOP-ROW////////////////////////////////////////////////////////////////////////////////#
            #TOP-LEFT//////////////////////////////////////////// 
            row = top_left.row()
            row.ui_units_x = 6
            row.operator("object.shade_flat", text="FLAT")
            row.operator("object.shade_smooth", text="SMOOTH")
            
            row = top_left.row()
            row.ui_units_x = 6
            row.operator('object.hide_view_set', text='HIDE').unselected=False
            row.operator('object.hide_view_clear', text='UNHIDE')

            #TOP-MID//////////////////////////////////////////////
            col = top_mid.column()
            col.alignment = 'CENTER'
            col.scale_y = 0.7
            col.label(text="---------")
            col.label(text="")

            #TOP-RIGHT////////////////////////////////////////////

            ToolOptions(self, context, parent=top_right)
            top_right.separator(factor = 2)
            ObjectToolSettings(self, context, parent=top_right)
            top_right.separator(factor = 2)  
            funct_bt(parent=top_right, cmd='hud', tog=False, w=2, h=1, label='HUD', icon="NONE")
            #MAIN-ROW////////////////////////////////////////////////////////////////////////////////#
            #MAIN-LEFT////////////////////////////////////////////
            col = main_leftrow.column(align=True)
            ViewCam(self, context, parent=col)

            box = main_leftrow.box()
            box.ui_units_x = 4
            col = box.column(align=True)
            col.scale_y = 0.8
            col.operator('object.join', text='JOIN')
            col.operator('object.duplicate_move', text='DUBLICATE')
            col.operator('object.duplicate_move_linked', text='LINKED')
            col.separator(factor = 2)
            col.operator('object.make_links_data', text='COPY MODS').type='MODIFIERS'

            box = main_leftrow.box()
            col = box.column(align=True)
            col.scale_y = 0.8
            col.label(text="CONVERT")
            col.ui_units_x = 3
            col.operator('object.convert', text='MESH').target='MESH'
            col.operator('object.convert', text='CURVE').target='CURVE'
            col.operator('object.convert', text='GPENCIL').target='GPENCIL'
            col.operator('gpencil.trace_image', text='IMG TRACE')

            box = main_leftrow.box()
            col = box.column(align=True)
            col.scale_y = 0.8
            col.label(text="Linked")
            col.ui_units_x = 5
            sub = col.row(align=True)
            sub.operator('object.select_linked', text='DATA').type='OBDATA'
            sub.operator('object.select_linked', text='MAT').type='MATERIAL'
            sub = col.row(align=True)
            sub.operator('object.select_linked', text='INST').type='DUPGROUP'
            sub.operator('object.select_linked', text='LIB').type='LIBRARY_OBDATA'
            col.separator(factor = 2)
            sub = col.row(align=True)
            sub.operator('xmenu.sel_parent', text='PARENT').direction='PARENT'
            sub.operator('xmenu.sel_parent', text='CHILD').direction='CHILD'

            #MAIN-MID//////////////////////////////////////////////
            col = main_midrow.column(align=False)
            row = col.row(align=True)
            row.ui_units_x = 18
            tool_bt(parent=row, cmd=5, w=2, h=1.4, text=False, icon='LARGE')
            tool_bt(parent=row, cmd=6, w=2, h=1.4, text=False, icon='LARGE')
            tool_bt(parent=row, cmd=7, w=2, h=1.4, text=False, icon='LARGE')
            tool_bt(parent=row, cmd=8, w=2, h=1.4, text=False, icon='LARGE')
            row.separator(factor = 2)
            tool_bt(parent=row, cmd=0, w=2, h=1.4, text=False, icon='LARGE')
            tool_bt(parent=row, cmd=1, w=2, h=1.4, text=False, icon='LARGE')
            tool_bt(parent=row, cmd=2, w=2, h=1.4, text=False, icon='LARGE')
            tool_bt(parent=row, cmd=3, w=2, h=1.4, text=False, icon='LARGE')
            tool_bt(parent=row, cmd=4, w=2, h=1.4, text=False, icon='LARGE')
            col.separator(factor = 1)
            row = col.row(align=True)
            row.ui_units_x = 18
            tool_bt(parent=row, cmd=9, w=2, h=1.4, text=False, icon='LARGE')
            tool_bt(parent=row, cmd=10, w=2, h=1.4, text=False, icon='LARGE')
            tool_bt(parent=row, cmd=11, w=2, h=1.4, text=False, icon='LARGE')
            tool_bt(parent=row, cmd=12, w=2, h=1.4, text=False, icon='LARGE')
            row.separator(factor = 4)
            tool_bt(parent=row, cmd=13, w=2, h=1.4, text=False, icon='LARGE')
            row.separator(factor = 2)
            tool_bt(parent=row, cmd=14, w=2, h=1.4, text=False, icon='LARGE')
            col.separator(factor = 1)
            row = col.row(align=False)
            row.ui_units_x = 4
            row.operator('object.delete', text='DELETE').use_global=False
            row.menu("VIEW3D_MT_add", text="Add", text_ctxt=i18n_contexts.operator_default)

            #MAIN-RIGHT/////////////////////////////////////////////////////////////////////////////////////
            col = main_rightrow.column(align=False)
            SetPivot(self, context, parent=col)
            col = main_rightrow.column(align=False)
            Transforms(self, context, parent=col)

        if bpy.context.mode == 'EDIT_MESH':
            #TOP-ROW////////////////////////////////////////////////////////////////////////////////#
            #TOP-LEFT//////////////////////////////////////////// 
            top_left.separator(factor = 6)
            row = top_left.row()
            row.ui_units_x = 6
            row.template_edit_mode_selection()

            #TOP-MID//////////////////////////////////////////////
            col = top_mid.column()
            col.alignment = 'CENTER'
            col.scale_y = 0.7
            col.label(text="---------")
            col.label(text="")

            #TOP-RIGHT////////////////////////////////////////////
            col = top_right.column(align=True)
            ToolOptions(self, context, parent=col)
            top_right.separator(factor = 2)
            top_left.separator(factor = 6)
            funct_bt(parent=top_right, cmd='hud', tog=False, w=2, h=1, label='HUD', icon="NONE")
            #MAIN-ROW////////////////////////////////////////////////////////////////////////////////#
            #MAIN-LEFT////////////////////////////////////////////      
            col = main_leftrow.column(align=True)
            ViewCam(self, context, parent=col)
            #MAIN-MID//////////////////////////////////////////////
            # MID 1 //////////////////////////////////////////////
            col = main_midrow.column(align=False)

            row = col.row(align=True)
            tool_bt(parent=row, cmd=5, w=2, h=1.4, text=False, icon='LARGE')
            tool_bt(parent=row, cmd=6, w=2, h=1.4, text=False, icon='LARGE')
            tool_bt(parent=row, cmd=7, w=2, h=1.4, text=False, icon='LARGE')
            tool_bt(parent=row, cmd=8, w=2, h=1.4, text=False, icon='LARGE')

            col.separator(factor = 1)
            row = col.row(align=True)
            tool_bt(parent=row, cmd=9, w=2, h=1.4, text=False, icon='LARGE')
            tool_bt(parent=row, cmd=10, w=2, h=1.4, text=False, icon='LARGE')
            tool_bt(parent=row, cmd=11, w=2, h=1.4, text=False, icon='LARGE')
            tool_bt(parent=row, cmd=12, w=2, h=1.4, text=False, icon='LARGE')

            # MID 2 //////////////////////////////////////////////
            col = main_midrow.column(align=False)

            row = col.row(align=True)
            tool_bt(parent=row, cmd=13, w=2, h=1.4, text=True, icon='LARGE')
            tool_bt(parent=row, cmd=14, w=2, h=1.4, text=True, icon='LARGE')
            tool_bt(parent=row, cmd=15, w=2, h=1.4, text=True, icon='LARGE')
            tool_bt(parent=row, cmd=16, w=2, h=1.4, text=True, icon='LARGE')
            tool_bt(parent=row, cmd=17, w=2, h=1.4, text=True, icon='LARGE')
            row.separator(factor = 2)
            tool_bt(parent=row, cmd=18, w=2, h=1.4, text=True, icon='LARGE')
            row.separator(factor = 2)
            tool_bt(parent=row, cmd=19, w=2, h=1.4, text=True, icon='LARGE')

            #col.separator(factor = 1)
            row = col.row(align=True)
            tool_bt(parent=row, cmd=20, w=2, h=1.4, text=True, icon='LARGE')
            tool_bt(parent=row, cmd=21, w=2, h=1.4, text=True, icon='LARGE')
            row.separator(factor = 2)
            tool_bt(parent=row, cmd=22, w=2, h=1.4, text=True, icon='LARGE')
            tool_bt(parent=row, cmd=23, w=2, h=1.4, text=True, icon='LARGE')
            row.separator(factor = 2)
            tool_bt(parent=row, cmd=24, w=2, h=1.4, text=True, icon='LARGE')
            row.separator(factor = 2)
            tool_bt(parent=row, cmd=25, w=2, h=1.4, text=True, icon='LARGE')
            tool_bt(parent=row, cmd=26, w=2, h=1.4, text=True, icon='LARGE')

            #col.separator(factor = 1)
            row = col.row(align=True)
            tool_bt(parent=row, cmd=27, w=2, h=1.4, text=True, icon='LARGE')
            tool_bt(parent=row, cmd=28, w=2, h=1.4, text=True, icon='LARGE')
            row.separator(factor = 2)
            tool_bt(parent=row, cmd=29, w=2, h=1.4, text=True, icon='LARGE')
            tool_bt(parent=row, cmd=30, w=2, h=1.4, text=True, icon='LARGE')
            row.separator(factor = 2)
            tool_bt(parent=row, cmd=31, w=2, h=1.4, text=True, icon='LARGE')
            tool_bt(parent=row, cmd=32, w=2, h=1.4, text=True, icon='LARGE')
            row.separator(factor = 2)
            tool_bt(parent=row, cmd=33, w=2, h=1.4, text=True, icon='LARGE')
            tool_bt(parent=row, cmd=34, w=2, h=1.4, text=True, icon='LARGE')
            row.separator(factor = 2)
            tool_bt(parent=row, cmd=35, w=2, h=1.4, text=True, icon='LARGE')
            tool_bt(parent=row, cmd=36, w=2, h=1.4, text=True, icon='LARGE')

            # MID 3 //////////////////////////////////////////////
            col = main_midrow.column(align=False)

            row = col.row(align=True)
            tool_bt(parent=row, cmd=0, w=2, h=1.4, text=False, icon='LARGE')
            tool_bt(parent=row, cmd=1, w=2, h=1.4, text=False, icon='LARGE')
            tool_bt(parent=row, cmd=2, w=2, h=1.4, text=False, icon='LARGE')
            tool_bt(parent=row, cmd=3, w=2, h=1.4, text=False, icon='LARGE')
            tool_bt(parent=row, cmd=4, w=2, h=1.4, text=False, icon='LARGE')

            #MAIN-RIGHT/////////////////////////////////////////////////////////////////////////////////////
            col = main_rightrow.column(align=False)
            row = col.row(align=True)
            Normals(self, context, parent=row)



        if bpy.context.mode == 'SCULPT':
            #TOP-ROW////////////////////////////////////////////////////////////////////////////////#
            #TOP-LEFT//////////////////////////////////////////// 

            #TOP-MID//////////////////////////////////////////////
            SculptMask(self, context, parent=top_left)
            top_mid.separator(factor = 1)

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
            col = main_leftrow.column(align=True)
            ViewCam(self, context, parent=col)
            col.separator(factor = 1)
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
            col.separator(factor = 0.4)
            row = col.row(align=True)
            SculptRake(self, context, parent=row)
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
            col = main_rightrow.column(align=False)
            col.menu_contents("VIEW3D_MT_sculpt_sym")
            col = main_rightrow.column(align=False)
            col.menu_contents("VIEW3D_MT_dynamesh")
            col = main_rightrow.column(align=False)
            col.menu_contents("VIEW3D_MT_remesh")
        '''
        if bpy.context.mode == 'PAINT_GPENCIL':
            gpd = context.gpencil
            #gpl = context.gpencil.layers.active
            sub = layout.row()
            sub.ui_units_x = 8
            sub.template_list("GPENCIL_UL_layer", "", gpd, "layers", gpd.layers, "active_index",
            rows=layer_rows, sort_reverse=True, sort_lock=True)
        '''
        if bpy.context.mode == 'PAINT_VERTEX':

            brush = context.tool_settings.vertex_paint.brush

            #TOP-ROW////////////////////////////////////////////////////////////////////////////////#
            #TOP-LEFT//////////////////////////////////////////// 
            row = top_left.row()
            row.ui_units_x = 6
            row.operator("object.shade_flat", text="FLAT")
            row.operator("object.shade_smooth", text="SMOOTH")

            #TOP-MID//////////////////////////////////////////////
            col = top_mid.column()
            col.alignment = 'CENTER'
            col.scale_y = 0.7
            col.label(text="---------")
            col.label(text="")
            col = top_mid.column()
            col.prop(brush, "blend", text="")
            #TOP-RIGHT////////////////////////////////////////////
            top_right.separator(factor = 2)  
            funct_bt(parent=top_right, cmd='hud', tog=False, w=2, h=1, label='HUD', icon="NONE")
            #ToolOptions(self, context, parent=top_right)
            top_right.separator(factor = 2)

            #MAIN-ROW////////////////////////////////////////////////////////////////////////////////#
            #MAIN-LEFT////////////////////////////////////////////
            box = main_leftrow.box()     
            box.ui_units_x = 8
            subrow = box.row()
            subrow.menu_contents("VIEW3D_MT_BrushTexture")

            box = main_leftrow.box()     
            box.ui_units_x = 4
            Stroke(self, context, parent=box)

            #MAIN-MID//////////////////////////////////////////////
            col = main_midrow.column()
            col.ui_units_x = 4
            Color(self, context, parent=col)

            col = main_midrow.column()
            col.ui_units_x = 4
            col.popover("VIEW3D_PT_tools_brush_display")
            BrushCopy(self, context, parent=col)

            main_midrow.separator(factor = 20)

            col = main_midrow.column()
            row = col.row()
            #row.ui_units_x = 18
            tool_bt(parent=row, cmd=0, w=2, h=1.4, text=False, icon='LARGE')
            row.separator(factor = 8)
            col.separator(factor = 1)
            row = col.row(align=True)
            tool_grid(parent=row, col=5, align=True, slotmin=1, slotmax=4, w=2, h=1.4, text=True, icon='LARGE')
            main_midrow.separator(factor = 20)
            #MAIN-RIGHT/////////////////////////////////////////////////////////////////////////////////////
            col = main_rightrow.column(align=False)
            VertexColor(self, context, parent=col)


        if bpy.context.mode == 'PAINT_TEXTURE':

            brush = context.tool_settings.image_paint.brush

            #TOP-ROW////////////////////////////////////////////////////////////////////////////////#
            #TOP-LEFT//////////////////////////////////////////// 
            row = top_left.row()
            row.ui_units_x = 6
            row.operator("object.shade_flat", text="FLAT")
            row.operator("object.shade_smooth", text="SMOOTH")

            #TOP-MID//////////////////////////////////////////////
            col = top_mid.column()
            col.alignment = 'CENTER'
            col.scale_y = 0.7
            col.label(text="---------")
            col.label(text="")
            col = top_mid.column()
            col.prop(brush, "blend", text="")
            #TOP-RIGHT////////////////////////////////////////////
            top_right.separator(factor = 2)  
            funct_bt(parent=top_right, cmd='hud', tog=False, w=2, h=1, label='HUD', icon="NONE")
            #ToolOptions(self, context, parent=top_right)
            top_right.separator(factor = 2)

            #MAIN-ROW////////////////////////////////////////////////////////////////////////////////#
            #MAIN-LEFT////////////////////////////////////////////           
            box = main_leftrow.box()     
            box.ui_units_x = 8
            subrow = box.row()
            subrow.menu_contents("VIEW3D_MT_BrushTexture")

            box = main_leftrow.box()     
            box.ui_units_x = 4
            Stroke(self, context, parent=box)

            #MAIN-MID//////////////////////////////////////////////
            col = main_midrow.column()
            col.ui_units_x = 4
            Color(self, context, parent=col)

            col = main_midrow.column()
            col.ui_units_x = 4
            col.popover("VIEW3D_PT_tools_brush_display")
            BrushCopy(self, context, parent=col)

            main_midrow.separator(factor = 20)
            col = main_midrow.column()
            row = col.row()
            #row.ui_units_x = 18
            tool_bt(parent=row, cmd=0, w=2, h=1.4, text=False, icon='LARGE')
            row.separator(factor = 8)
            col.separator(factor = 1)
            row = col.row(align=True)
            tool_grid(parent=row, col=5, align=True, slotmin=1, slotmax=6, w=2, h=1.4, text=True, icon='LARGE')
            main_midrow.separator(factor = 24)
            #MAIN-RIGHT/////////////////////////////////////////////////////////////////////////////////////
            col = main_rightrow.column(align=False)

        if bpy.context.mode == 'PAINT_WEIGHT':

            brush = context.tool_settings.vertex_paint.brush

            #TOP-ROW////////////////////////////////////////////////////////////////////////////////#
            #TOP-LEFT//////////////////////////////////////////// 
            row = top_left.row()
            row.ui_units_x = 6
            row.operator("object.shade_flat", text="FLAT")
            row.operator("object.shade_smooth", text="SMOOTH")

            #TOP-MID//////////////////////////////////////////////
            col = top_mid.column()
            col.alignment = 'CENTER'
            col.scale_y = 0.7
            col.label(text="---------")
            col.label(text="")

            #TOP-RIGHT////////////////////////////////////////////
            top_right.separator(factor = 2)  
            funct_bt(parent=top_right, cmd='hud', tog=False, w=2, h=1, label='HUD', icon="NONE")
            #ToolOptions(self, context, parent=top_right)
            top_right.separator(factor = 2)

            #MAIN-ROW////////////////////////////////////////////////////////////////////////////////#
            #MAIN-LEFT////////////////////////////////////////////           

            #MAIN-MID//////////////////////////////////////////////

            col = main_midrow.column()
            row = col.row()
            #row.ui_units_x = 18
            tool_bt(parent=row, cmd=0, w=2, h=1.4, text=False, icon='LARGE')
            row.separator(factor = 8)
            col.separator(factor = 1)
            row = col.row(align=True)
            tool_grid(parent=row, col=5, align=True, slotmin=1, slotmax=7, w=2, h=1.4, text=True, icon='LARGE')
            main_midrow.separator(factor = 24)
            #MAIN-RIGHT/////////////////////////////////////////////////////////////////////////////////////
            col = main_rightrow.column(align=False)

        if bpy.context.mode == 'PAINT_GPENCIL':

            brush = context.tool_settings.vertex_paint.brush

            #TOP-ROW////////////////////////////////////////////////////////////////////////////////#
            #TOP-LEFT//////////////////////////////////////////// 
            row = top_left.row()
            row.ui_units_x = 6
            row.operator("object.shade_flat", text="FLAT")
            row.operator("object.shade_smooth", text="SMOOTH")

            #TOP-MID//////////////////////////////////////////////
            col = top_mid.column()
            col.alignment = 'CENTER'
            col.scale_y = 0.7
            col.label(text="---------")
            col.label(text="")

            #TOP-RIGHT////////////////////////////////////////////
            top_right.separator(factor = 2)  
            funct_bt(parent=top_right, cmd='hud', tog=False, w=2, h=1, label='HUD', icon="NONE")
            #ToolOptions(self, context, parent=top_right)
            top_right.separator(factor = 2)

            #MAIN-ROW////////////////////////////////////////////////////////////////////////////////#
            #MAIN-LEFT////////////////////////////////////////////           

            #MAIN-MID//////////////////////////////////////////////

            col = main_midrow.column()
            row = col.row()
            #row.ui_units_x = 18
            tool_bt(parent=row, cmd=0, w=2, h=1.4, text=False, icon='LARGE')
            row.separator(factor = 8)
            col.separator(factor = 1)
            row = col.row(align=True)
            tool_grid(parent=row, col=5, align=True, slotmin=1, slotmax=7, w=2, h=1.4, text=True, icon='LARGE')
            main_midrow.separator(factor = 24)
            #MAIN-RIGHT/////////////////////////////////////////////////////////////////////////////////////
            col = main_rightrow.column(align=False)



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