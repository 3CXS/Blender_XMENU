import bpy

from bpy.types import Operator, Header, Panel, AddonPreferences

from bpy.app.translations import contexts as i18n_contexts
from bpy_extras.object_utils import AddObjectHelper, object_data_add
from bl_ui.properties_data_modifier import DATA_PT_modifiers

from .menuitems import *
from .functions import tool_grid, tool_bt, funct_bt, redraw_regions, update_normaldisp
from .brushtexture import get_brush_mode, preview_collections

from .icons import get_icon_id



#-----------------------------------------------------------------------------------------------------------------------

class XPanel(bpy.types.Panel):
    bl_idname = "SCENE_PT_xpanel"
    bl_label = "X-PANEL"
    bl_space_type = "PROPERTIES"
    bl_region_type = "WINDOW"
    bl_context = "scene"
    bl_order = 2000
    bl_options = {'DEFAULT_CLOSED',}

    def draw(self, context):



        layout = self.layout

        #layout.label(text="Blender SE", icon_value=get_icon_id("TWEAK"))



#LAYOUT-STRUCTURE-----------------------------------------------------------------------------------------

        top_row = layout.row()
        top_row.alignment = 'CENTER'

        top_left_outer = top_row.row()
        top_left_outer.ui_units_x = 8
        top_left_outer.alignment = 'LEFT'

        top_left = top_row.row(align=True)
        top_left.ui_units_x = 16
        top_left.alignment = 'RIGHT'

        top_mid = top_row.row()
        top_mid.alignment = 'CENTER'
        top_mid.ui_units_x = 36

        top_right = top_row.row()
        top_right.ui_units_x = 12
        top_right.alignment = 'LEFT'

        top_right_outer = top_row.row()
        top_right_outer.ui_units_x = 12
        top_right_outer.alignment = 'RIGHT'


        main_row = layout.row()
        main_row.alignment = 'CENTER' 

        main_left = main_row.column()
        main_left.ui_units_x = 24

        main_mid = main_row.column()
        main_mid.ui_units_x = 36

        main_right = main_row.column()
        main_right.ui_units_x = 24

        main_leftbox = main_left.box()
        main_leftbox.ui_units_y = 0.6
        main_leftrow = main_left.row()
        main_leftrow.alignment = 'RIGHT'

        main_midbox = main_mid.box()
        main_midbox.ui_units_y = 0.8
        main_midrow = main_mid.row()


        main_rightbox = main_right.box()
        main_rightbox.ui_units_y = 0.6
        main_rightrow = main_right.row()
        main_rightrow.alignment = 'LEFT'

        end = layout.row()
        end.ui_units_x = 0.2
        end.ui_units_y = 10
        end.label(text="")

        #TOP-LEFT OUTER-----------------------------------------------------------------------------

        col = top_left_outer.column()
        col.ui_units_x = 0.2
        col.scale_y = 0.7
        col.label(text='')
        col.label(text='')

        row = top_left_outer.row()
        row.ui_units_x = 4
        row.operator("wm.save_mainfile", icon='FILE_TICK', text="SAVE")

        top_left_outer.separator(factor=2)

        row = top_left_outer.row()
        row.scale_x = 1.2
        row.operator("script.reload", icon='FILE_REFRESH', text="")

        #TOP-RIGHT OUTER------------------------------------------------------------------------------

        row = top_right_outer.row(align=True)
        Overlay(self, context, layout=row)
        funct_bt(layout=row, cmd='hud', tog=True, w=2, h=1.4, label='INFO', icon="NONE") 
        funct_bt(layout=row, cmd='pivot', tog=True, w=1.2, h=1.4, label='ORIG', icon="OUTLINER_DATA_EMPTY")

        col = top_right_outer.column()
        col.ui_units_x = 0.2
        col.scale_y = 0.7
        col.label(text='')
        col.label(text='')


#OBJECT-----------------------------------------------------------------------------------------------  

        if context.mode == 'OBJECT':

            main_midrow.alignment = 'LEFT'

            #TOP-LEFT---------------------------------------------------------------------------------

            row = top_left.row()
            HideObject(self, context, layout=row)
            row.separator()
            Normals(self, context, layout=row)

            #TOP-MID----------------------------------------------------------------------------------

            col = top_mid.column()
            row = col.row(align=True)
            #row.scale_y = 0.7

            tool_bt(layout=row, cmd=5, w=1.4, h=1, text=False, icon='CUSTOM')
            tool_bt(layout=row, cmd=6, w=1.4, h=1, text=False, icon='CUSTOM')
            tool_bt(layout=row, cmd=7, w=1.4, h=1, text=False, icon='CUSTOM')
            tool_bt(layout=row, cmd=8, w=1.4, h=1, text=False, icon='CUSTOM')
            row.separator(factor = 2)
            tool_bt(layout=row, cmd=0, w=1.4, h=1, text=False, icon='CUSTOM')
            tool_bt(layout=row, cmd=1, w=1.4, h=1, text=False, icon='CUSTOM')
            tool_bt(layout=row, cmd=2, w=1.4, h=1, text=False, icon='CUSTOM')
            tool_bt(layout=row, cmd=3, w=1.4, h=1, text=False, icon='CUSTOM')
            tool_bt(layout=row, cmd=4, w=1.4, h=1, text=False, icon='CUSTOM')

            row.separator(factor = 2)
            col = row.column()
            col.ui_units_x = 5
            ObjectToolSettings(self, context, layout=col)

            row.separator(factor = 2)
            tool_bt(layout=row, cmd=9, w=2, h=1.4, text=False, icon='LARGE')
            tool_bt(layout=row, cmd=12, w=2, h=1.4, text=False, icon='LARGE')
            tool_bt(layout=row, cmd=13, w=2, h=1.4, text=False, icon='LARGE')
            row.separator(factor = 1)
            #tool_bt(layout=row, cmd=14, w=2, h=1.4, text=False, icon='LARGE')

            sub = row.column()
            sub.ui_units_x = 3
            sub.menu("VIEW3D_MT_add", text="ADD", text_ctxt=i18n_contexts.operator_default)

            #TOP-RIGHT-------------------------------------------------------------------------------

            ToolOptions(self, context, layout=top_right)
            top_right.separator(factor = 2)

            #MAIN-LEFT-------------------------------------------------------------------------------

            box = main_leftrow.box()
            box.ui_units_x = 4
            SaveScene(self, context, layout=box)

            box = main_leftrow.box()
            box.ui_units_x = 4
            box.menu_contents("OBJECT_MT_import_menu")

            box = main_leftrow.box()
            box.ui_units_x = 4
            col = box.column(align=True)
            col.scale_y = 0.8

            col.operator('object.join', text='JOIN')
            col.operator('object.duplicate_move', text='DUPLICATE')
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
            col.ui_units_x = 4
            sub = col.row(align=True)
            sub.operator('object.select_linked', text='DATA').type='OBDATA'
            sub.operator('object.select_linked', text='MAT').type='MATERIAL'
            sub = col.row(align=True)
            sub.operator('object.select_linked', text='INST').type='DUPGROUP'
            sub.operator('object.select_linked', text='LIB').type='LIBRARY_OBDATA'
            col.separator(factor = 2)
            sub = col.row(align=True)

            op = sub.operator("xm.override2", text="HIERARCHY")
            op.cmd ='object.select_hierarchy'
            op.prop1 ='direction="CHILD"'
            op.prop2 ='extend=True'

            #MAIN-MID-------------------------------------------------------------------------------

            col = main_midrow.column(align=False)
            col.ui_units_x= 12
            col.separator(factor = 1)

            row = col.row(align=False)
            row.ui_units_x = 4
            row.operator('mesh.primitive_plane_add', text="", icon='MESH_PLANE')
            row.operator('mesh.primitive_cube_add', text="", icon='MESH_CUBE')
            row.operator('mesh.primitive_uv_sphere_add', text="", icon='MESH_UVSPHERE')
            row.operator('mesh.primitive_cylinder_add', text="", icon='MESH_CYLINDER')
            row.operator('object.empty_add', text="", icon='EMPTY_DATA')
            row.operator('object.gpencil_add', text="", icon='GREASEPENCIL')
            row.operator('curve.primitive_bezier_curve_add', text="", icon='CURVE_DATA')
            row.operator('object.delete', text='DELETE').use_global=False            

            #MAIN-RIGHT------------------------------------------------------------------------------
            box = main_rightrow.box()
            box.ui_units_x = 8
            Transforms(self, context, layout=box)

            box = main_rightrow.box()
            box.ui_units_x = 8
            box.menu_contents("VIEW3D_MT_Material")

            box = main_rightrow.box()
            box.ui_units_x = 8
            UVTexture(self, context, layout=box)


#EDIT------------------------------------------------------------------------------------------------

        if context.mode == 'EDIT_MESH':

            #TOP-LEFT--------------------------------------------------------------------------------

            row = top_left.row()
            Normals(self, context, layout=row)

            #TOP-MID---------------------------------------------------------------------------------

            col = top_mid.column(align=False)
            col.alignment = 'CENTER'

            row = col.row(align=True)
            tool_bt(layout=row, cmd=5, w=1.4, h=1, text=False, icon='CUSTOM')
            tool_bt(layout=row, cmd=6, w=1.4, h=1, text=False, icon='CUSTOM')
            tool_bt(layout=row, cmd=7, w=1.4, h=1, text=False, icon='CUSTOM')
            tool_bt(layout=row, cmd=8, w=1.4, h=1, text=False, icon='CUSTOM')
            row.separator(factor = 2)
            tool_bt(layout=row, cmd=0, w=1.4, h=1, text=False, icon='CUSTOM')
            tool_bt(layout=row, cmd=1, w=1.4, h=1, text=False, icon='CUSTOM')
            tool_bt(layout=row, cmd=2, w=1.4, h=1, text=False, icon='CUSTOM')
            tool_bt(layout=row, cmd=3, w=1.4, h=1, text=False, icon='CUSTOM')
            tool_bt(layout=row, cmd=4, w=1.4, h=1, text=False, icon='CUSTOM')

            row.separator(factor = 2)
            col = row.column()
            col.ui_units_x = 5
            ObjectToolSettings(self, context, layout=col)

            row.separator(factor = 2)
            tool_bt(layout=row, cmd=9, w=2, h=1.4, text=False, icon='LARGE')
            tool_bt(layout=row, cmd=10, w=2, h=1.4, text=False, icon='LARGE')
            tool_bt(layout=row, cmd=11, w=2, h=1.4, text=False, icon='LARGE')
            row.separator(factor = 1)
            #tool_bt(layout=row, cmd=12, w=2, h=1.4, text=False, icon='LARGE')
            sub = row.column()
            sub.ui_units_x = 3
            sub.menu("VIEW3D_MT_mesh_add",text='ADD')

            #col.menu_contents("OBJECT_MT_edgedata")

            #TOP-RIGHT-------------------------------------------------------------------------------

            col = top_right.column(align=True)
            ToolOptions(self, context, layout=col)

            '''
            col.ui_units_x = 5
            col.operator('uv.smart_project', text="AUTO UV")
            col.operator('uv.unwrap', text="UNWRAP")
            col.operator('uv.follow_active_quads', text="FOLLOW Q")
            op = col.operator('uv.project_from_view', text="FROM VIEW")
            op.scale_to_bounds = True
            col.operator('uv.reset', text="RESET")
            col = main_leftrow.column(align=True)
            UVTexture(self, context, layout=col)
            '''

#SCULPT----------------------------------------------------------------------------------------------

        if context.mode == 'SCULPT':

            sculpt = context.tool_settings.sculpt

            main_midrow.alignment = 'CENTER'

            #TOP-LEFT--------------------------------------------------------------------------------

            col = top_left.column(align=True)
            col.ui_units_x = 1.2
            col.operator('sculpt.optimize', text="" ,icon='SOLO_ON')

            top_left.separator(factor=2)

            col = top_left.column(align=True)
            col.ui_units_x = 2
            col.operator("xm.normalshading", text="SMTH", depress=update_normaldisp(self, context))

            top_left.separator(factor=2)

            col = top_left.column(align=True)    
            col.ui_units_x = 2
            col.scale_y = 1
            col.operator("sculpt.symmetrize", text='SYM')
            col = top_left.column()
            col.ui_units_x = 2
            col.menu("VIEW3D_MT_sculpt_sym", icon='PREFERENCES')

            top_left.separator(factor=2)

            col = top_left.column()
            col.ui_units_x = 4
            BrushCopy(self, context, layout=col)

            #TOP-MID-------------------------------------------------------------------------------

            col = top_mid.column()
            col.ui_units_x = 6
            SculptToolSettings(self, context, layout=col)

            col = top_mid.column()
            col.ui_units_x = 17
            SculptBrushSettings1(self, context, layout=col)
            SculptBrushSettings2(self, context, layout=col)
            col = top_mid.column()
            col.ui_units_x = 2
            col.scale_y = 1.4
            col.menu_contents("VIEW3D_MT_Falloff")


            col = top_mid.column()
            col.ui_units_x = 4
            SculptMask(self, context, layout=top_mid)

            #TOP-RIGHT--------------------------------------------------------------------------------

            col = top_right.column(align=True)
            ToolOptions(self, context, layout=col)

            #MAIN-LEFT--------------------------------------------------------------------------------

            col = main_leftrow.column(align=False)
            col.ui_units_x = 8
            VertexColor(self, context, layout=col)
            ColorPalette(self, context, layout=col)

            box = main_leftrow.box()     
            box.ui_units_x = 8
            subrow = box.row()
            subrow.menu_contents("VIEW3D_MT_TextureMask")
            subrow = box.row()
            subrow.menu_contents("VIEW3D_MT_BrushTexture")

            box = main_leftrow.box()     
            box.ui_units_x = 4
            Stroke(self, context, layout=box)

            #MAIN-MID--------------------------------------------------------------------------------

            #GRAB/////////////////
            col = main_midrow.column()
            col.alignment = 'LEFT'
            row = col.row(align=True)
            sub = row.column(align=True)
            sub.ui_units_x = 2
            sub.scale_y = 0.7
            sub.operator('xm.mask', text='PVT M').cmd='PMASKED'
            sub.operator('xm.mask', text='RESET').cmd='ORIGIN'
            tool_bt(layout=row, cmd=18, w=2, h=1.4, text=False, icon='LARGE')
            row.separator(factor = 1)
            tool_bt(layout=row, cmd=0, w=2, h=1.4, text=False, icon='LARGE')
            row.separator(factor = 2)
            #EXTRA/////////////////
            col.separator(factor = 0.4)
            row = col.row(align=True)
            sub = row.column(align=True)
            subsub = sub.row(align=True)
            subsub.scale_y = 0.7
            subsub.ui_units_x = 4
            subsub.label(text='PAINT')
            subsub = sub.row(align=True)
            #subsub.ui_units_x = 2
            tool_bt(layout=subsub, cmd=36, w=2, h=1.4, text=False, icon='LARGE')
            tool_bt(layout=subsub, cmd=37, w=2, h=1.4, text=False, icon='LARGE')
            row.separator(factor = 1)
            tool_grid(layout=row, col=3, align=True, slotmin=19, slotmax=23, w=1.2, h=1, icon='CUSTOM')

            #CLAY////////////////
            main_midrow.separator(factor = 0.4)
            col = main_midrow.column()
            row = col.row(align=True)
            tool_grid(layout=row, col=3, align=False, slotmin=1, slotmax=4, w=2, h=1.4, text=True, icon='LARGE')
            col.separator(factor = 0.4)
            row = col.row(align=True)
            tool_grid(layout=row, col=3, align=False, slotmin=4, slotmax=7, w=2, h=1.4, text=True, icon='LARGE')
            col.separator(factor = 0.4)

            #CREASE///////////////
            col = main_midrow.column()
            row = col.row()
            row.separator(factor = 0.4)
            tool_grid(layout=row, col=2, align=False, slotmin=7, slotmax=9, w=2, h=1.4, text=True, icon='LARGE')
            row.separator(factor = 0.4)
            col.separator(factor = 0.4)
            row = col.row()
            row.separator(factor = 0.4)
            #tool_grid(layout=row, col=1, align=True, slotmin=23, slotmax=25, w=1.2, h=1, icon='LARGE')
            sub = row.column()
            #tool_bt(layout=sub, cmd=25, w=1.8, h=1, text=False, icon='OFF')
            #tool_grid(layout=row, col=1, align=True, slotmin=26, slotmax=28, w=1.2, h=1, icon='LARGE')

            #POLISH//////////// 
            col = main_midrow.column()
            row = col.row()
            tool_bt(layout=row, cmd=9, w=2, h=1.4, text=True, icon='LARGE')
            tool_bt(layout=row, cmd=10, w=2, h=1.4, text=True, icon='LARGE')
            col.separator(factor = 0.4)
            row = col.row()
            tool_bt(layout=row, cmd=11, w=2, h=1.4, text=True, icon='LARGE')
            tool_bt(layout=row, cmd=12, w=2, h=1.4, text=True, icon='LARGE')

            #MASK//////////// 
            main_midrow.separator(factor = 0.4)
            col = main_midrow.column()
            row = col.row()
            tool_bt(layout=row, cmd=13, w=2, h=1.4, text=False, icon='LARGE') 
            sub = row.column()
            sub.ui_units_x = 3.4
            subsub = sub.column()
            subsub.scale_y = 0.5
            subsub.label(text="MASK")
            grid = sub.grid_flow(columns=3, align=True)
            tool_bt(layout=grid, cmd=27, w=1.2, h=0.8, text=False, icon='CUSTOM')
            tool_bt(layout=grid, cmd=28, w=1, h=0.8, text=False, icon='CUSTOM')
            tool_bt(layout=grid, cmd=29, w=1.2, h=0.8, text=False, icon='CUSTOM')
            #TRIM//////////////// 
            sub = row.column()
            sub.ui_units_x = 2.4
            subsub = sub.column()
            subsub.scale_y = 0.5
            subsub.label(text="TRIM")
            grid = sub.grid_flow(columns=2, align=True)
            tool_bt(layout=grid, cmd=16, w=1.2, h=0.8, icon="CUSTOM", text=False)
            tool_bt(layout=grid, cmd=17, w=1.2, h=0.8, icon="CUSTOM", text=False)
            #FSETS//////////////
            col.separator(factor = 0.4)
            row = col.row()
            tool_bt(layout=row, cmd=14, w=2, h=1.4, text=False, icon='LARGE')
            sub = row.column()       
            grid = sub.grid_flow(columns=2, align=True)
            tool_bt(layout=grid, cmd=30, w=1.5, h=0.75, text=False, icon='CUSTOM')
            tool_bt(layout=grid, cmd=31, w=1.5, h=0.75, text=False, icon='CUSTOM')
            tool_bt(layout=sub, cmd=32, w=1.2, h=0.5, text=False, icon='OFF')
            #HIDE
            subcol = row.column()
            subcol.ui_units_x = 2.4
            tool_bt(layout=subcol, cmd=15, w=2.4, h=1.4, text=False, icon='LARGE')

            #FACESET INIT//////////////
            col.separator(factor = 0.4)
            row = col.row()
            SculptFaceSet(self, context, layout=row)
            col.separator(factor = 0.4)

            #MAIN-RIGHT--------------------------------------------------------------------------------

            col = main_rightrow.column(align=False)
            col.menu_contents("VIEW3D_MT_dynamesh")
            col = main_rightrow.column(align=False)
            col.menu_contents("VIEW3D_MT_remesh")
            col = main_rightrow.column(align=False)
            col.ui_units_x = 3
            sub = col.row()
            sub.scale_y = 0.5
            sub.label(text='FILTER')
            sub = col.row()
            tool_bt(layout=sub, cmd=33, w=3, h=1, text=False, icon='OFF')
            sub = col.row()
            tool_bt(layout=sub, cmd=34, w=3, h=1, text=False, icon='OFF')
            sub = col.row()
            tool_bt(layout=sub, cmd=35, w=3, h=1, text=False, icon='OFF')
            col = main_rightrow.column(align=False)
            SculptFilterSettings(self, context, layout=col)



#PAINT_VERTEX----------------------------------------------------------------------------------------

        if context.mode == 'PAINT_VERTEX':

            brush = context.tool_settings.vertex_paint.brush

            #TOP-LEFT--------------------------------------------------------------------------------

            col = top_left.column()
            col.ui_units_x = 2
            col.operator("xm.normalshading", text="SMTH", depress=update_normaldisp(self, context))
            row = top_left.row()
            row.ui_units_x = 4       
            BrushCopy(self, context, layout=row )

            #TOP-MID--------------------------------------------------------------------------------

            col = top_mid.column()
            col.ui_units_x = 4
            col.prop(brush, "blend", text="")
            row = top_mid.row()
            tool_bt(layout=row, cmd=0, w=2, h=1.4, text=False, icon='LARGE')
            tool_grid(layout=row, col=5, align=True, slotmin=1, slotmax=4, w=2, h=1.4, text=False, icon='LARGE')

            col = top_mid.column()
            col.ui_units_x = 2
            col.scale_y = 1.4
            col.menu_contents("VIEW3D_MT_Falloff")

            col = top_mid.column()
            col.ui_units_x = 6
            VertexBrushSettings(self, context, layout=col)

            #TOP-RIGHT--------------------------------------------------------------------------------

            top_right.label(text='')




#PAINT_TEXTURE----------------------------------------------------------------------------------------

        if context.mode == 'PAINT_TEXTURE':

            brush = context.tool_settings.image_paint.brush

            #TOP-LEFT---------------------------------------------------------------------------------

            col = top_left.column()
            col.ui_units_x = 2
            col.operator("xm.normalshading", text="SMTH", depress=update_normaldisp(self, context))

            row = top_left.row()
            row.ui_units_x = 4      
            BrushCopy(self, context, layout=row )

            #TOP-MID----------------------------------------------------------------------------------

            col = top_mid.column()
            col.ui_units_x = 4
            col.prop(brush, "blend", text="")
            row = top_mid.row()
            tool_bt(layout=row, cmd=0, w=2, h=1.4, text=False, icon='LARGE')
            tool_grid(layout=row, col=5, align=True, slotmin=1, slotmax=6, w=2, h=1.4, text=False, icon='LARGE')

            col = top_mid.column()
            col.ui_units_x = 2
            col.scale_y = 1.4
            col.menu_contents("VIEW3D_MT_Falloff")

            col = top_mid.column()
            TextureBrushSettings(self, context, layout=top_mid)



            #TOP-RIGHT-------------------------------------------------------------------------------

            ToolOptions(self, context, layout=top_right)

#PAINT_WEIGHT----------------------------------------------------------------------------------------

        if context.mode == 'PAINT_WEIGHT':

            brush = context.tool_settings.vertex_paint.brush


            #TOP-LEFT--------------------------------------------------------------------------------
            row = top_left.row()
            row.ui_units_x = 4      
            BrushCopy(self, context, layout=row )

            #TOP-MID---------------------------------------------------------------------------------
            col = top_mid.column()
            row = col.row()
            tool_bt(layout=row, cmd=0, w=2, h=1.4, text=False, icon='LARGE')
            tool_grid(layout=row, col=6, align=True, slotmin=1, slotmax=7, w=2, h=1.4, text=False, icon='LARGE')


            sub = top_mid.row(align=True)
            sub.ui_units_x = 4
            sub.prop(brush, "use_frontface", text="FRONT", toggle=True)
            sub.prop(brush, "use_accumulate", text="ACCU", toggle=True)

            #TOP-RIGHT-------------------------------------------------------------------------------


            sub = top_right.row(align=True)
            sub.ui_units_x = 10
            ts = context.tool_settings
            wp = ts.weight_paint
            sub.prop(ts, "use_auto_normalize", text="NORM", toggle=True)
            sub.prop(ts, "use_lock_relative", text="RELAT", toggle=True)
            sub.prop(ts, "use_multipaint", text="MPAINT", toggle=True)
            sub.prop(wp, "use_group_restrict", text="RESTR", toggle=True)

#PAINT_GPENCIL---------------------------------------------------------------------------------------

        if context.mode == 'PAINT_GPENCIL':

            brush = context.tool_settings.gpencil_paint.brush
            gp_settings = brush.gpencil_settings

            #TOP-LEFT--------------------------------------------------------------------------------

            row = top_left.row()
            sub = row.column()
            sub.ui_units_x = 4
            sub.menu("GPENCIL_MT_cleanup")

            sub = row.column()
            sub.ui_units_x = 4
            sub.operator("gpencil.blank_frame_add", text="INIT")

            #TOP-MID--------------------------------------------------------------------------------

            row = top_mid.row(align=True)
            row.alignment = 'CENTER'
            sub = row.column()
            sub.ui_units_x = 4         
            BrushCopy(self, context, layout=sub)
            row.separator()
            tool_bt(layout=row, cmd=0, w=2.4, h=1.4, text=False, icon='LARGE')
            row.separator()
            tool_bt(layout=row, cmd=1, w=2.4, h=1.4, text=False, icon='LARGE')
            tool_bt(layout=row, cmd=2, w=2.4, h=1.4, text=False, icon='LARGE')
            tool_bt(layout=row, cmd=3, w=2.4, h=1.4, text=False, icon='LARGE')
            tool_bt(layout=row, cmd=4, w=2.4, h=1.4, text=False, icon='LARGE')
            tool_bt(layout=row, cmd=5, w=2.4, h=1.4, text=False, icon='LARGE')
            row.separator()
            tool_bt(layout=row, cmd=6, w=1.2, h=1, text=False, icon='IPO_LINEAR')
            tool_bt(layout=row, cmd=7, w=1.2, h=1, text=False, icon='IPO_CONSTANT')
            tool_bt(layout=row, cmd=8, w=1.2, h=1, text=False, icon='IPO_EASE_OUT')
            tool_bt(layout=row, cmd=9, w=1.2, h=1, text=False, icon='IPO_EASE_IN_OUT')
            tool_bt(layout=row, cmd=10, w=1.2, h=1, text=False, icon='MESH_PLANE')
            tool_bt(layout=row, cmd=11, w=1.2, h=1, text=False, icon='MESH_CIRCLE')

            row.separator()
            sub = row.column(align=True)
            sub.ui_units_x = 2
            sub.scale_y = 1.4
            sub.prop(gp_settings, "use_settings_stabilizer", text="SMTH", toggle=True)
            sub = row.column(align=True)
            sub.ui_units_x = 4
            sub.scale_y = 0.7
            sub.active = gp_settings.use_settings_stabilizer
            sub.prop(brush, "smooth_stroke_radius", text="Radius", slider=True)
            sub.prop(brush, "smooth_stroke_factor", text="Factor", slider=True)

            #TOP-RIGHT-------------------------------------------------------------------------------

            row = top_right.row(align=True)

            sub = row.column(align=True)
            sub.ui_units_x = 4
            sub.scale_y = 1
            sub.popover("VIEW3D_PT_tools_grease_pencil_brush_post_processing")
            sub = row.column(align=True)
            sub.ui_units_x = 4
            sub.scale_y = 1
            sub.popover("VIEW3D_PT_tools_grease_pencil_brush_random")
            sub = row.column(align=True)
            sub.ui_units_x = 4
            sub.scale_y = 1
            sub.popover("VIEW3D_PT_tools_grease_pencil_brush_advanced")


#EDIT_GPENCIL----------------------------------------------------------------------------------------

        if context.mode == 'EDIT_GPENCIL':

            brush = context.tool_settings.gpencil_paint.brush

            #TOP-LEFT--------------------------------------------------------------------------------

            row = top_left.row(align=True)

            sub = row.column(align=True)
            sub.ui_units_x = 3.2
            sub.scale_y = 0.7
            sub.operator("gpencil.stroke_simplify", text="SIMPLIFY")
            sub.operator("gpencil.stroke_sample", text="RESAMPL")

            sub = row.column(align=True)
            sub.ui_units_x = 3.2
            sub.scale_y = 0.7
            sub.operator("gpencil.stroke_subdivide", text="SUBDIV").only_selected=True
            sub.operator("gpencil.stroke_smooth", text="SMOTH").only_selected=True

            row.separator(factor=2)

            sub = row.column(align=True)
            sub.ui_units_x = 2.4
            sub.scale_y = 0.7
            op = sub.operator("gpencil.stroke_cyclical_set", text="CLOSE")
            op.type='CLOSE'
            op.geometry=True
            sub.operator("gpencil.stroke_trim", text="TRIM")

            sub = row.column(align=True)
            sub.ui_units_x = 2.4
            sub.scale_y = 0.7
            sub.operator("gpencil.stroke_merge", text="MERGE")
            sub.operator("gpencil.stroke_join", text="JOIN")

            #TOP-MID-------------------------------------------------------------------------------

            col = top_mid.column(align=False)
            col.alignment = 'CENTER'

            row = col.row(align=True)
            tool_bt(layout=row, cmd=5, w=1.4, h=1, text=False, icon='TWEAK')
            tool_bt(layout=row, cmd=6, w=1.4, h=1, text=False, icon='TWEAK')
            tool_bt(layout=row, cmd=7, w=1.4, h=1, text=False, icon='TWEAK')
            tool_bt(layout=row, cmd=8, w=1.4, h=1, text=False, icon='TWEAK')

            row.separator(factor = 2)
            tool_bt(layout=row, cmd=0, w=1.4, h=1, text=False, icon='TWEAK')
            tool_bt(layout=row, cmd=1, w=1.4, h=1, text=False, icon='TWEAK')
            tool_bt(layout=row, cmd=2, w=1.4, h=1, text=False, icon='TWEAK')
            tool_bt(layout=row, cmd=3, w=1.4, h=1, text=False, icon='TWEAK')
            tool_bt(layout=row, cmd=4, w=1.4, h=1, text=False, icon='TWEAK')

            row.separator(factor = 2)
            col = row.column()
            col.ui_units_x = 5
            GPToolSettings(self, context, layout=col)
            row.separator(factor = 2)
            col = row.column(align=True)
            tool_bt(layout=col, cmd=9, w=2, h=0.7, text=True, icon='OFF')
            tool_bt(layout=col, cmd=10, w=2, h=0.7, text=True, icon='OFF')
            col = row.column(align=True)
            tool_bt(layout=col, cmd=11, w=2, h=0.7, text=True, icon='OFF')
            tool_bt(layout=col, cmd=12, w=2, h=0.7, text=True, icon='OFF')
            col = row.column(align=True)
            tool_bt(layout=col, cmd=13, w=2, h=0.7, text=True, icon='OFF')
            col = row.column(align=True)
            tool_bt(layout=col, cmd=14, w=2, h=0.7, text=True, icon='OFF')
            tool_bt(layout=col, cmd=15, w=2, h=0.7, text=True, icon='OFF')

            #TOP-RIGHT-----------------------------------------------------------------------------

            col = top_right.column()
            ToolOptions(self, context, layout=col)



#SCULPT_GPENCIL------------------------------------------------------------------------------------

        if context.mode == 'SCULPT_GPENCIL':

            brush = context.tool_settings.gpencil_paint.brush


            #TOP-LEFT------------------------------------------------------------------------------

            col = top_left.column()
            col.ui_units_x = 4
            BrushCopy(self, context, layout=col)

            #TOP-MID-------------------------------------------------------------------------------

            col = top_mid.column()
            col.alignment = 'CENTER'
            row = col.row(align=True)
            tool_bt(layout=row, cmd=4, w=2.2, h=1.4, text=False, icon='LARGE')
            tool_bt(layout=row, cmd=5, w=2.2, h=1.4, text=False, icon='LARGE')
            tool_bt(layout=row, cmd=6, w=2.2, h=1.4, text=False, icon='LARGE')
            tool_bt(layout=row, cmd=7, w=2.2, h=1.4, text=False, icon='LARGE')
            tool_bt(layout=row, cmd=8, w=2.2, h=1.4, text=False, icon='LARGE')
            row.separator(factor=1)
            tool_bt(layout=row, cmd=1, w=2.8, h=1, text=False, icon='OFF')
            tool_bt(layout=row, cmd=2, w=2.8, h=1, text=False, icon='OFF')
            tool_bt(layout=row, cmd=0, w=2.8, h=1, text=False, icon='OFF')
            tool_bt(layout=row, cmd=3, w=2.8, h=1, text=False, icon='OFF')

            row.separator(factor=1)
            col = top_mid.column()
            col.ui_units_x = 2
            col.scale_y = 1.4
            col.menu_contents("VIEW3D_MT_Falloff")

            row.separator(factor=1)
            col = top_mid.column()
            col.ui_units_x = 6
            GPSculptToolSettings(self, context, layout=col)

            #TOP-RIGHT-------------------------------------------------------------------------------

            col = top_right.column()
            col.label(text="")

            '''
            elif tool_mode == 'WEIGHT_GPENCIL':
                col.popover("VIEW3D_PT_tools_grease_pencil_weight_appearance")
            elif tool_mode == 'VERTEX_GPENCIL':
                col.popover("VIEW3D_PT_tools_grease_pencil_vertex_appearance")


            bpy.data.scenes["Scene"].tool_settings.use_gpencil_select_mask_stroke
            bpy.data.scenes["Scene"].tool_settings.use_gpencil_select_mask_point
            '''


#WEIGHT_GPENCIL--------------------------------------------------------------------------------------

        if context.mode == 'WEIGHT_GPENCIL':

            brush = context.tool_settings.vertex_paint.brush

            #TOP-LEFT--------------------------------------------------------------------------------

            row = top_left.row()
            row.ui_units_x = 6
            row.label(text="")

            #TOP-MID---------------------------------------------------------------------------------

            col = top_mid.column()
            col.alignment = 'CENTER'
            tool_bt(layout=col, cmd=0, w=2.2, h=1.4, text=False, icon='LARGE')

            #TOP-RIGHT-------------------------------------------------------------------------------

            col = top_right.column()
            col.label(text="")


        redraw_regions()

#-----------------------------------------------------------------------------------------------------------------------

def register() :
    bpy.utils.register_class(XPanel)

def unregister() :
    bpy.utils.unregister_class(XPanel)
