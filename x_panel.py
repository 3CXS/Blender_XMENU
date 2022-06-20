import bpy
from .hud import redraw_regions
from .functions import tool_grid, tool_bt, funct_bt
from bpy.types import Operator, AddonPreferences
from bl_ui.properties_data_modifier import DATA_PT_modifiers
from bpy.app.translations import contexts as i18n_contexts
from bpy.types import Header, Panel
from .menuitems import *
from .brushtexture import get_brush_mode
from bpy_extras.object_utils import AddObjectHelper, object_data_add

#////////////////////////////////////////////////////////////////////////////////////////////#

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

        #LAYOUT-STRUCTURE/////////////////////////////////////////
        top_row = layout.row()
        top_row.alignment = 'CENTER'

        top_left_outer = top_row.row()
        top_left_outer.ui_units_x = 11.5
        top_left_outer.alignment = 'LEFT'

        top_left = top_row.row()
        top_left.ui_units_x = 12.5
        top_left.alignment = 'RIGHT'

        top_mid = top_row.row()
        top_mid.alignment = 'CENTER'
        top_mid.ui_units_x = 36

        top_right = top_row.row()
        top_right.ui_units_x = 12.5
        top_right.alignment = 'LEFT'

        top_right_outer = top_row.row()
        top_right_outer.ui_units_x = 11.5
        top_right_outer.alignment = 'RIGHT'


        main_row = layout.row()
        main_row.alignment = 'CENTER' 

        main_left = main_row.column()
        main_left.ui_units_x = 24
        #main_left.alignment = 'RIGHT'
        main_mid = main_row.column()
        main_mid.alignment = 'CENTER'
        main_mid.ui_units_x = 36
        main_right = main_row.column()
        main_right.ui_units_x = 24
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

        row = top_left_outer.row()
        row.ui_units_x = 1.5
        row.label(text='')

        row = top_left_outer.row()
        row.ui_units_x = 4
        row.operator("wm.save_mainfile", icon='FILE_TICK', text="SAVE")

        row = top_left_outer.row()
        row.ui_units_x = 1.6
        row.operator("screen.redo_last", text="CMD")



        row = top_right_outer.row(align=True)
        funct_bt(parent=row, cmd='hud', tog=False, w=2, h=1, label='HUD', icon="NONE") 
        funct_bt(parent=row, cmd='pivot', tog=False, w=2, h=1, label='ORIG', icon="NONE")

        row = top_right_outer.row(align=True)
        row.ui_units_x = 3.5
        History(self, context, parent=row)

        col = top_right_outer.column()
        col.ui_units_x = 2
        col.scale_y = 0.7
        col.label(text='')
        col.label(text='')

        #/////////////////////////////////////////////////////////////////////////////#
        #                               OBJECT                                        #
        #/////////////////////////////////////////////////////////////////////////////#
        if bpy.context.mode == 'OBJECT':
            #TOP-ROW//////////////////////////////////////////////////////////////////#
            #TOP-LEFT/////////////////////////////////////////////////////////////////#
            row = top_left.row()
            Normals(self, context, parent=row)

            #row.operator('object.hide_view_set', text='HIDE').unselected=False
            #row.operator('object.hide_view_clear', text='UNHIDE')

            #TOP-MID//////////////////////////////////////////////////////////////////#
            col = top_mid.column()
            col.alignment = 'CENTER'
            col.scale_y = 0.7
            col.label(text="---------")
            col.label(text="")

            #TOP-RIGHT////////////////////////////////////////////////////////////////#

            ToolOptions(self, context, parent=top_right)
            top_right.separator(factor = 2)
            ObjectToolSettings(self, context, parent=top_right)

            #MAIN-ROW/////////////////////////////////////////////////////////////////#
            #MAIN-LEFT////////////////////////////////////////////////////////////////#
            col = main_leftrow.column(align=True)
            SaveScene(self, context, parent=col)
            col = main_leftrow.column(align=True)
            col.menu_contents("VIEW3D_MT_Import")

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

            op = sub.operator("xmenu.override2", text="HIERARCHY")
            op.cmd ='object.select_hierarchy'
            op.prop1 ='direction="CHILD"'
            op.prop2 ='extend=True'

            #MAIN-MID//////////////////////////////////////////////////////////////////#
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
            row.menu("VIEW3D_MT_add", text="Add", text_ctxt=i18n_contexts.operator_default)
            row.operator('mesh.primitive_plane_add', text="", icon='MESH_PLANE')
            row.operator('mesh.primitive_cube_add', text="", icon='MESH_CUBE')
            row.operator('mesh.primitive_uv_sphere_add', text="", icon='MESH_UVSPHERE')
            row.operator('mesh.primitive_cylinder_add', text="", icon='MESH_CYLINDER')
            row.operator('object.empty_add', text="", icon='EMPTY_DATA')
            row.operator('object.gpencil_add', text="", icon='GREASEPENCIL')
            row.operator('curve.primitive_bezier_curve_add', text="", icon='CURVE_DATA')
            row.operator('object.delete', text='DELETE').use_global=False            


            #MAIN-RIGHT///////////////////////////////////////////////////////////////#
            col = main_rightrow.column(align=False)
            Transforms(self, context, parent=col)
            col = main_rightrow.column(align=False)
            col.menu_contents("VIEW3D_MT_Material")
            col = main_rightrow.column(align=False)
            UVTexture(self, context, parent=col)
            col = main_rightrow.column(align=True)
            ViewCam(self, context, parent=col)
            #with context.temp_override(bl_context = "material"):
            #col.popover("DATA_PT_modifiers", text='XX')
            #layout.prop_tabs_enum(view, "context", icon_only=True)
        #/////////////////////////////////////////////////////////////////////////////#
        #                               EDIT                                          #
        #/////////////////////////////////////////////////////////////////////////////#
        if bpy.context.mode == 'EDIT_MESH':
            #TOP-ROW//////////////////////////////////////////////////////////////////#
            #TOP-LEFT/////////////////////////////////////////////////////////////////# 
            col = top_left.column()
            col.label(text="")

            #TOP-MID//////////////////////////////////////////////////////////////////#
            col = top_mid.column()
            col.alignment = 'CENTER'
            col.scale_y = 0.7
            col.label(text="---------")
            col.label(text="")
            #col.menu_contents("OBJECT_MT_edgedata")

            #TOP-RIGHT////////////////////////////////////////////////////////////////#
            col = top_right.column(align=True)
            ToolOptions(self, context, parent=col)

            #MAIN-ROW/////////////////////////////////////////////////////////////////#
            #MAIN-LEFT////////////////////////////////////////////////////////////////#
            col = main_leftrow.column(align=True)
            ViewCam(self, context, parent=col)
            #MAIN-MID/////////////////////////////////////////////////////////////////#
            # MID 1 //////////////////////////////////////////////////////////////////#
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

            # MID 2 //////////////////////////////////////////////////////////////////#
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

            # MID 3 //////////////////////////////////////////////////////////////////#
            col = main_midrow.column(align=False)

            row = col.row(align=True)
            tool_bt(parent=row, cmd=0, w=2, h=1.4, text=False, icon='LARGE')
            tool_bt(parent=row, cmd=1, w=2, h=1.4, text=False, icon='LARGE')
            tool_bt(parent=row, cmd=2, w=2, h=1.4, text=False, icon='LARGE')
            tool_bt(parent=row, cmd=3, w=2, h=1.4, text=False, icon='LARGE')
            tool_bt(parent=row, cmd=4, w=2, h=1.4, text=False, icon='LARGE')

            #MAIN-RIGHT///////////////////////////////////////////////////////////////#

            col = main_rightrow.column(align=False)
            UVTexture(self, context, parent=col)
            #col = main_rightrow.column(align=False)
            #VertexGroups(self, context, parent=col)

            #col = main_rightrow.column(align=False)
            #Materials(self, context, parent=col)


        #/////////////////////////////////////////////////////////////////////////////#
        #                               SCULPT                                        #
        #/////////////////////////////////////////////////////////////////////////////#
        if bpy.context.mode == 'SCULPT':
            #TOP-ROW//////////////////////////////////////////////////////////////////#
            #TOP-LEFT/////////////////////////////////////////////////////////////////#
            col = top_left.column()    
            col.ui_units_x = 4
            col.scale_y = 0.7
            sub = col.column(align=True)
            sub.operator("sculpt.symmetrize", text='SYM')
            col.menu("VIEW3D_MT_sculpt_sym")

            col = top_left.column()
            col.ui_units_x = 8
            col.menu_contents("VIEW3D_MT_TextureMask")

            col = top_left.column()
            col.ui_units_x = 4
            BrushCopy(self, context, parent=col)
            #TOP-MID//////////////////////////////////////////////////////////////////#
            SculptToolSettings(self, context, parent=top_mid)
            top_mid.separator(factor = 0.4)

            SculptBrushSettings(self, context, parent=top_mid)
            top_mid.separator(factor = 0.4)
            SculptMask(self, context, parent=top_mid)
            top_mid.separator(factor = 2)
            #TOP-RIGHT////////////////////////////////////////////////////////////////#
            col = top_right.column(align=True)
            ToolOptions(self, context, parent=col)

            #SculptOverlay(self, context, parent=col)
            #MAIN-ROW/////////////////////////////////////////////////////////////////#
            #MAIN-LEFT////////////////////////////////////////////////////////////////#
            col = main_leftrow.column(align=False)
            col.ui_units_x = 8
            VertexColor(self, context, parent=col)

            #col.popover("VIEW3D_PT_tools_brush_display")

            box = main_leftrow.box()     
            box.ui_units_x = 8
            subrow = box.row()
            subrow.menu_contents("VIEW3D_MT_BrushTexture")

            box = main_leftrow.box()     
            box.ui_units_x = 4
            Stroke(self, context, parent=box)

            #MAIN-MID//////////////////////////////////////////////////////////////////#
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
            tool_bt(parent=subsub, cmd=36, w=2, h=1.4, text=False, icon='LARGE')
            tool_bt(parent=subsub, cmd=37, w=2, h=1.4, text=False, icon='LARGE')
            row.separator(factor = 1)
            tool_grid(parent=row, col=3, align=True, slotmin=19, slotmax=23, w=1.2, h=1, icon='CUSTOM')
            #TRIM
            col.separator(factor = 0.4)
            row = col.row()
            row.separator(factor = 4)
            SculptExtra(self, context, parent=row)
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
            row.separator(factor = 0.4)
            #tool_grid(parent=row, col=1, align=True, slotmin=23, slotmax=25, w=1.2, h=1, icon='CUSTOM')
            sub = row.column()
            #tool_bt(parent=sub, cmd=25, w=1.8, h=1, text=False, icon='OFF')
            sub.menu_contents("VIEW3D_MT_Falloff")
            row.separator(factor = 0.4)
            #tool_grid(parent=row, col=1, align=True, slotmin=26, slotmax=28, w=1.2, h=1, icon='CUSTOM')

            #POLISH//////////// 
            col = main_midrow.column()
            row = col.row()
            tool_bt(parent=row, cmd=9, w=2, h=1.4, text=True, icon='LARGE')
            tool_bt(parent=row, cmd=10, w=2, h=1.4, text=True, icon='LARGE')
            col.separator(factor = 0.4)
            row = col.row()
            tool_bt(parent=row, cmd=11, w=2, h=1.4, text=True, icon='LARGE')
            tool_bt(parent=row, cmd=12, w=2, h=1.4, text=True, icon='LARGE')

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
            tool_bt(parent=grid, cmd=27, w=1.2, h=0.8, text=False, icon='CUSTOM')
            tool_bt(parent=grid, cmd=28, w=1, h=0.8, text=False, icon='CUSTOM')
            tool_bt(parent=grid, cmd=29, w=1.2, h=0.8, text=False, icon='CUSTOM')
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
            tool_bt(parent=grid, cmd=30, w=1.5, h=0.75, text=False, icon='CUSTOM')
            tool_bt(parent=grid, cmd=31, w=1.5, h=0.75, text=False, icon='CUSTOM')
            tool_bt(parent=sub, cmd=32, w=1.2, h=0.5, text=False, icon='OFF')
            #HIDE
            subcol = row.column()
            subcol.ui_units_x = 2.4
            tool_bt(parent=subcol, cmd=15, w=2.4, h=1.4, text=False, icon='LARGE')

            #FACESET INIT//////////////
            col.separator(factor = 0.4)
            row = col.row()
            SculptFaceSet(self, context, parent=row)
            col.separator(factor = 0.4)

            #MAIN-RIGHT///////////////////////////////////////////////////////////////#
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
            tool_bt(parent=sub, cmd=33, w=3, h=1, text=False, icon='OFF')
            sub = col.row()
            tool_bt(parent=sub, cmd=34, w=3, h=1, text=False, icon='OFF')
            sub = col.row()
            tool_bt(parent=sub, cmd=35, w=3, h=1, text=False, icon='OFF')
            col = main_rightrow.column(align=False)
            SculptFilterSettings(self, context, parent=col)

        #/////////////////////////////////////////////////////////////////////////////#
        #                               PAINT_VERTEX                                  #
        #/////////////////////////////////////////////////////////////////////////////#

        if bpy.context.mode == 'PAINT_VERTEX':

            brush = context.tool_settings.vertex_paint.brush
            #TOP-ROW///////////////////////////////////////////////////////////////////#
            #TOP-LEFT////////////////////////////////////////////
            col = top_left.column()
            col.ui_units_x = 8
            col.menu_contents("VIEW3D_MT_TextureMask")
            row = top_left.row()
            row.ui_units_x = 4
            row.operator("object.shade_flat", text="FLAT")
            row.operator("object.shade_smooth", text="SMOOTH")

            #TOP-MID//////////////////////////////////////////////
            col = top_mid.column()
            col.ui_units_x = 4
            col.label(text="")            

            col = top_mid.column()
            col.ui_units_x = 6
            col.prop(brush, "blend", text="")
            col = top_mid.column()
            VertexBrushSettings(self, context, parent=top_mid)

            #TOP-RIGHT////////////////////////////////////////////
            ToolOptions(self, context, parent=top_right)

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

            main_midrow.separator(factor = 1)

            col = main_midrow.column()
            row = col.row()
            tool_bt(parent=row, cmd=0, w=2, h=1.4, text=False, icon='LARGE')
            row.separator(factor = 4)
            sub = row.column()
            sub.ui_units_x = 4         
            BrushCopy(self, context, parent=sub)

            col.separator(factor = 1)
            row = col.row(align=True)
            tool_grid(parent=row, col=5, align=True, slotmin=1, slotmax=4, w=2, h=1.4, text=True, icon='LARGE')
            col.separator(factor = 1)

            main_midrow.separator(factor = 2)
            col = main_midrow.column()
            col.ui_units_x = 8
            col.separator(factor = 8)
            ColorPalette(self, context, parent=col)

            #MAIN-RIGHT/////////////////////////////////////////////////////////////////////////////////////
            col = main_rightrow.column(align=False)
            VertexColor(self, context, parent=col)

        #/////////////////////////////////////////////////////////////////////////////#
        #                               PAINT_TEXTURE                                 #
        #/////////////////////////////////////////////////////////////////////////////#
        if bpy.context.mode == 'PAINT_TEXTURE':

            brush = context.tool_settings.image_paint.brush

            #TOP-ROW////////////////////////////////////////////////////////////////////////////////#
            #TOP-LEFT////////////////////////////////////////////
            col = top_left.column()
            col.ui_units_x = 8
            col.menu_contents("VIEW3D_MT_TextureMask")

            row = top_left.row()
            row.ui_units_x = 4
            row.operator("object.shade_flat", text="FLAT")
            row.operator("object.shade_smooth", text="SMOOTH")

            #TOP-MID//////////////////////////////////////////////
            col = top_mid.column()
            col.ui_units_x = 6
            col.prop(brush, "blend", text="")
            col = top_mid.column()
            TextureBrushSettings(self, context, parent=top_mid)

            #TOP-RIGHT////////////////////////////////////////////
            ToolOptions(self, context, parent=top_right)

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

            main_midrow.separator(factor = 1)

            col = main_midrow.column()
            row = col.row()
            tool_bt(parent=row, cmd=0, w=2, h=1.4, text=False, icon='LARGE')
            row.separator(factor = 4)
            sub = row.column()
            sub.ui_units_x = 4         
            BrushCopy(self, context, parent=sub)
            col.separator(factor = 1)
            row = col.row(align=True)
            tool_grid(parent=row, col=5, align=True, slotmin=1, slotmax=6, w=2, h=1.4, text=True, icon='LARGE')
            col.separator(factor = 1)


            main_midrow.separator(factor = 2)
            col = main_midrow.column()
            col.ui_units_x = 8
            col.separator(factor = 10)
            ColorPalette(self, context, parent=col)

            #MAIN-RIGHT/////////////////////////////////////////////////////////////////////////////////////
            col = main_rightrow.column(align=False)
            TexSlots(self, context, parent=col)

        #/////////////////////////////////////////////////////////////////////////////#
        #                               PAINT_WEIGHT                                  #
        #/////////////////////////////////////////////////////////////////////////////#
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
            col = top_right.column()
            col.label(text="")

            #MAIN-ROW////////////////////////////////////////////////////////////////////////////////#
            #MAIN-LEFT////////////////////////////////////////////           
            box = main_leftrow.box()     
            box.ui_units_x = 4
            Stroke(self, context, parent=box)
            #MAIN-MID//////////////////////////////////////////////
            col = main_midrow.column()
            row = col.row()
            tool_bt(parent=row, cmd=0, w=2, h=1.4, text=False, icon='LARGE')
            row.separator(factor = 8)
            #col.separator(factor = 1)
            row = col.row(align=True)
            tool_grid(parent=row, col=6, align=True, slotmin=1, slotmax=7, w=2, h=1.4, text=True, icon='LARGE')
            main_midrow.separator(factor = 24)
            #MAIN-RIGHT/////////////////////////////////////////////////////////////////////////////////////
            col = main_rightrow.column(align=False)

        #/////////////////////////////////////////////////////////////////////////////#
        #                               PAINT_GPENCIL                                  #
        #/////////////////////////////////////////////////////////////////////////////#
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
            col = top_right.column()
            col.label(text="")

            #MAIN-ROW////////////////////////////////////////////////////////////////////////////////#
            #MAIN-LEFT////////////////////////////////////////////           
            box = main_leftrow.box()     
            box.ui_units_x = 4
            #Stroke(self, context, parent=box)
            #MAIN-MID//////////////////////////////////////////////
            col = main_midrow.column()

            row = col.row()
            tool_bt(parent=row, cmd=0, w=2.4, h=1.4, text=False, icon='OFF')
            tool_bt(parent=row, cmd=1, w=2.4, h=1.4, text=False, icon='OFF')
            tool_bt(parent=row, cmd=2, w=2.4, h=1.4, text=False, icon='OFF')
            tool_bt(parent=row, cmd=3, w=2.4, h=1.4, text=False, icon='OFF')
            tool_bt(parent=row, cmd=4, w=2.4, h=1.4, text=False, icon='OFF')
            tool_bt(parent=row, cmd=5, w=2.4, h=1.4, text=False, icon='OFF')
            tool_bt(parent=row, cmd=6, w=2.4, h=1.4, text=False, icon='OFF')
            tool_bt(parent=row, cmd=7, w=2.4, h=1.4, text=False, icon='OFF')
            col.separator(factor = 2)
            row = col.row(align=True)
            tool_grid(parent=row, col=8, align=True, slotmin=8, slotmax=14, w=2, h=1.4, text=True, icon='LARGE')
            row = col.row(align=True)

            sub = row.column()
            sub.ui_units_x = 4         
            BrushCopy(self, context, parent=sub)
            sub = row.column()
            sub.ui_units_x = 8        
            sub.label(text="")

            #MAIN-RIGHT/////////////////////////////////////////////////////////////////////////////////////
            col = main_rightrow.column(align=False)
            GPLayers(self, context, parent=col)

        #/////////////////////////////////////////////////////////////////////////////#
        #                               EDIT_GPENCIL                                  #
        #/////////////////////////////////////////////////////////////////////////////#
        if bpy.context.mode == 'EDIT_GPENCIL':

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
            col = top_right.column()
            col.label(text="")

            #MAIN-ROW////////////////////////////////////////////////////////////////////////////////#
            #MAIN-LEFT////////////////////////////////////////////           
            box = main_leftrow.box()     
            box.ui_units_x = 4
            #Stroke(self, context, parent=box)
            #MAIN-MID//////////////////////////////////////////////
            col = main_midrow.column()

            row = col.row()
            tool_bt(parent=row, cmd=5, w=2.2, h=1.4, text=True, icon='LARGE')
            tool_bt(parent=row, cmd=6, w=2.2, h=1.4, text=True, icon='LARGE')
            tool_bt(parent=row, cmd=7, w=2.2, h=1.4, text=True, icon='LARGE')
            tool_bt(parent=row, cmd=8, w=2.2, h=1.4, text=True, icon='LARGE')
            row.separator(factor = 1)
            tool_bt(parent=row, cmd=0, w=2.2, h=1.4, text=True, icon='LARGE')
            tool_bt(parent=row, cmd=1, w=2.2, h=1.4, text=True, icon='LARGE')
            tool_bt(parent=row, cmd=2, w=2.2, h=1.4, text=True, icon='LARGE')
            tool_bt(parent=row, cmd=3, w=2.2, h=1.4, text=True, icon='LARGE')
            row.separator(factor = 1)
            tool_bt(parent=row, cmd=4, w=2.2, h=1.4, text=True, icon='LARGE')

            row = col.row()
            tool_bt(parent=row, cmd=9, w=2.2, h=1.4, text=True, icon='LARGE')
            tool_bt(parent=row, cmd=10, w=2.2, h=1.4, text=True, icon='LARGE')
            tool_bt(parent=row, cmd=11, w=2.2, h=1.4, text=True, icon='LARGE')
            tool_bt(parent=row, cmd=12, w=2.2, h=1.4, text=True, icon='LARGE')
            tool_bt(parent=row, cmd=13, w=2.2, h=1.4, text=True, icon='LARGE')
            row.separator(factor = 1)
            tool_bt(parent=row, cmd=13, w=2.2, h=1.4, text=True, icon='LARGE')
            tool_bt(parent=row, cmd=13, w=2.2, h=1.4, text=True, icon='LARGE')

            #MAIN-RIGHT/////////////////////////////////////////////////////////////////////////////////////
            col = main_rightrow.column(align=False)
            GPLayers(self, context, parent=col)

        #/////////////////////////////////////////////////////////////////////////////#
        #                               SCULPT_GPENCIL                                #
        #/////////////////////////////////////////////////////////////////////////////#
        if bpy.context.mode == 'SCULPT_GPENCIL':

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
            col = top_right.column()
            col.label(text="")

            #MAIN-ROW////////////////////////////////////////////////////////////////////////////////#
            #MAIN-LEFT////////////////////////////////////////////           
            box = main_leftrow.box()     
            box.ui_units_x = 4
            #Stroke(self, context, parent=box)
            #MAIN-MID//////////////////////////////////////////////
            col = main_midrow.column()

            row = col.row()
            tool_bt(parent=row, cmd=0, w=2.2, h=1.4, text=True, icon='LARGE')
            tool_bt(parent=row, cmd=1, w=2.2, h=1.4, text=True, icon='LARGE')
            tool_bt(parent=row, cmd=2, w=2.2, h=1.4, text=True, icon='LARGE')
            tool_bt(parent=row, cmd=3, w=2.2, h=1.4, text=True, icon='LARGE')
            row = col.row()
            tool_bt(parent=row, cmd=4, w=2.2, h=1.4, text=True, icon='LARGE')
            tool_bt(parent=row, cmd=5, w=2.2, h=1.4, text=True, icon='LARGE')
            tool_bt(parent=row, cmd=6, w=2.2, h=1.4, text=True, icon='LARGE')
            tool_bt(parent=row, cmd=7, w=2.2, h=1.4, text=True, icon='LARGE')
            row.separator(factor = 1)
            tool_bt(parent=row, cmd=8, w=2.2, h=1.4, text=True, icon='LARGE')

            #MAIN-RIGHT/////////////////////////////////////////////////////////////////////////////////////
            col = main_rightrow.column(align=False)
            GPLayers(self, context, parent=col)

        #/////////////////////////////////////////////////////////////////////////////#
        #                               WEIGHT_GPENCIL                                #
        #/////////////////////////////////////////////////////////////////////////////#
        if bpy.context.mode == 'WEIGHT_GPENCIL':

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
            col = top_right.column()
            col.label(text="")

            #MAIN-ROW////////////////////////////////////////////////////////////////////////////////#
            #MAIN-LEFT////////////////////////////////////////////           
            box = main_leftrow.box()     
            box.ui_units_x = 4
            #Stroke(self, context, parent=box)
            #MAIN-MID//////////////////////////////////////////////
            col = main_midrow.column()

            row = col.row()
            tool_bt(parent=row, cmd=0, w=2.2, h=1.4, text=True, icon='LARGE')
            row.separator(factor = 80)

            #MAIN-RIGHT/////////////////////////////////////////////////////////////////////////////////////
            col = main_rightrow.column(align=False)
            GPLayers(self, context, parent=col)

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
