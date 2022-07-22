import bpy

from bpy.types import Operator, Header, Panel, AddonPreferences

from bpy.app.translations import contexts as i18n_contexts
from bpy_extras.object_utils import AddObjectHelper, object_data_add
from bl_ui.properties_data_modifier import DATA_PT_modifiers

from .menuitems import *
from .functions import tool_bt, funct_bt, redraw_regions, update_normaldisp
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

        ob = context.active_object

        layout = self.layout


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
        top_mid.alignment = 'LEFT'
        top_mid.ui_units_x = 36

        top_right = top_row.row(align=True)
        top_right.ui_units_x = 16
        top_right.alignment = 'LEFT'

        top_right_outer = top_row.row()
        top_right_outer.ui_units_x = 8
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

        col = top_left_outer.column(align=True)
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

        # object visibility:
        HideObject(self, context, layout=row)

        row.separator(factor=1)

        # overlay & hud:
        Overlay(self, context, layout=row)
        funct_bt(layout=row, cmd='pivot', tog=True, w=1.2, h=1, label='', icon='ORIENTATION_VIEW')
        funct_bt(layout=row, cmd='hud', tog=True, w=1.2, h=1, label='', icon="INFO") 

        col = top_right_outer.column(align=True)
        col.ui_units_x = 0.2
        col.scale_y = 0.7
        col.label(text='')
        col.label(text='')


#OBJECT-----------------------------------------------------------------------------------------------  

        if context.mode == 'OBJECT':

            main_midrow.alignment = 'LEFT'

    #TOP-LEFT---------------------------------------------------------------------------------

            row = top_left.row(align=True)

            # toolset:
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

    #TOP-MID----------------------------------------------------------------------------------

            row = top_mid.row(align=True)

            # object injection:
            row.operator('mesh.primitive_plane_add', text="", icon='MESH_PLANE')
            row.operator('mesh.primitive_cube_add', text="", icon='MESH_CUBE')
            row.operator('mesh.primitive_uv_sphere_add', text="", icon='MESH_UVSPHERE')
            row.operator('mesh.primitive_cylinder_add', text="", icon='MESH_CYLINDER')
            row.operator('object.empty_add', text="", icon='EMPTY_DATA')
            row.operator('object.gpencil_add', text="", icon='GREASEPENCIL')

            sub = row.column()
            sub.ui_units_x = 4
            sub.menu("VIEW3D_MT_add", text="OBJECT", text_ctxt=i18n_contexts.operator_default)

            row.separator(factor=2) 

            # bool operators:
            row.operator('btool.boolean_union', text="", icon='SELECT_EXTEND')
            row.operator('btool.boolean_diff', text="", icon='SELECT_SUBTRACT')
            row.operator('btool.boolean_inters', text="", icon='SELECT_INTERSECT')
            row.operator('btool.boolean_slice', text="", icon='SELECT_DIFFERENCE')

            # list modifiers:
            sub = row.column()
            sub.ui_units_x = 5
            sub.operator_menu_enum("object.modifier_add", "type", text="MODIFIER")

            row.separator(factor=2)

            # merge/clone/array:
            row.operator('object.convert', text="", icon='SHADERFX')

            row.separator(factor=1)

            sub = row.row(align=True)
            sub.ui_units_x = 4
            sub.operator('object.join', text='MRG')
            sub.operator('object.duplicate_move', text='DUB')

            if ob != None:
                if ob.type == 'MESH':
                    subsub = row.column(align=True)
                    subsub.ui_units_x = 1.2
                    subsub.operator('object.modifier_add', text='', icon='MOD_ARRAY').type='ARRAY'
                else:
                    subsub = row.column(align=True)
                    subsub.ui_units_x = 1.2
                    subsub.label(text="")

            row.separator(factor = 1)

            # tool settings:
            ObjectToolSettings(self, context, layout=row)

            row.separator(factor = 1)

            # normal shading:
            Normals(self, context, layout=row)

    #TOP-RIGHT-------------------------------------------------------------------------------

            row = top_right.row(align=True)

            # tool options:
            sub = row.column()
            sub.ui_units_x = 8
            ToolOptions(self, context, layout=sub)

            empty = row.column()
            empty.ui_units_x = 4
            empty.separator()

            # annotate & measure:
            tool_bt(layout=row, cmd=9, w=1.2, h=1, text=False, icon='OUTLINER_DATA_GP_LAYER')
            tool_bt(layout=row, cmd=12, w=1.2, h=1, text=False, icon='OUTLINER_DATA_LIGHTPROBE')
            tool_bt(layout=row, cmd=13, w=1.2, h=1, text=False, icon='DRIVER_ROTATIONAL_DIFFERENCE')

    #MAIN-LEFT-------------------------------------------------------------------------------

            row = main_leftrow.row()

            # save scene:
            sub = row.column(align=True)
            sub.ui_units_x = 4
            SaveScene(self, context, layout=sub)

            # import:
            sub = row.column(align=True)
            sub.ui_units_x = 4
            sub.menu_contents("OBJECT_MT_import_menu")

            # empty:
            empty = row.column(align=True)
            empty.ui_units_x = 16
            empty.separator()

    #MAIN-MID-------------------------------------------------------------------------------

            row = main_midrow.row()

            # uv-window
            sub = row.column()
            sub.ui_units_x = 8

            subsub = sub.row(align=True)
            subsub.scale_y = 1.2
            subsub.operator("xm.override", icon='ADD', text="").cmd='mesh.uv_texture_add'
            subsub.operator("xm.override", icon='REMOVE', text="").cmd='mesh.uv_texture_remove'
            empty = subsub.column()
            empty.ui_units_x = 3
            empty.separator()

            subsub.operator("xm.override", text="NEW").cmd='material.new'
            subsub.menu("MATERIAL_MT_context_menu", text="",icon='DOWNARROW_HLT')

            UVTexture(self, context, layout=sub)

            # MAT-window:
            sub = row.column()
            sub.ui_units_x = 14
            sub.menu_contents("VIEW3D_MT_Material")

            # vertex group:
            sub = row.column()
            sub.ui_units_x = 10

            subsub = sub.row(align=True)
            subsub.scale_y = 1.2
            subsub.operator('xm.override', text='Vertex Group').cmd='object.vertex_group_add'
            subsub.operator('xm.override',text='',icon='ADD').cmd='object.vertex_group_add'
            subsub.operator('xm.override',text='',icon='REMOVE').cmd='object.vertex_group_remove'

            subsub = sub.row(align=True)

            if ob != None:
                group = ob.vertex_groups.active
                subsub.template_list("MESH_UL_vgroups", "", ob, "vertex_groups", ob.vertex_groups, "active_index", rows=2)

    #MAIN-RIGHT------------------------------------------------------------------------------

            row = main_rightrow.row()

            # XYZ Matrix:
            sub = row.column()
            sub.ui_units_x = 8
            Transforms(self, context, layout=sub)

            # MOD Window:
            sub = row.column()
            sub.ui_units_x = 13
            sub.scale_y = 1.22

            if ob != None:
                ml_props = bpy.context.window_manager.modifier_list
                active_mod_index = ob.ml_modifier_active_index
                sub.template_list("OBJECT_UL_ml_modifier_list", "", ob, "modifiers", ml_props, "active_object_modifier_active_index", rows=3)

#EDIT------------------------------------------------------------------------------------------------

        if context.mode == 'EDIT_MESH':

            main_midrow.alignment = 'LEFT'

    #TOP-LEFT--------------------------------------------------------------------------------

            row = top_left.row(align=True)

            # toolset:
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

    #TOP-MID---------------------------------------------------------------------------------

            row = top_mid.row(align=True)

            # add meshes:
            row.operator('mesh.primitive_plane_add', text="", icon='MESH_PLANE')
            row.operator('mesh.primitive_cube_add', text="", icon='MESH_CUBE')
            row.operator('mesh.primitive_uv_sphere_add', text="", icon='MESH_UVSPHERE')
            row.operator('mesh.primitive_cylinder_add', text="", icon='MESH_CYLINDER')

            sub = row.column()
            sub.ui_units_x = 4
            sub.menu("VIEW3D_MT_mesh_add", icon='NONE', text='MESH') 

            row.separator(factor=1) 

            '''
            # list MACHIN3:
            row.menu('MACHIN3_MT_mesh_machine', text=' Machine')

            # list HOPS: use only one choice of menus
            row.menu('HOPS_MT_ObjectsOperatorsSubmenu', text='Hard.OPs')  
            row.menu('HOPS_MT_BoolSumbenu', text='Hard.OPs')
            row.menu('HOPS_MT_ST3MeshToolsSubmenu', text='Hard.OPs')
            row.menu('HOPS_MT_ObjectToolsSubmenu', text='Hard.OPs')

            # list Quick:
            row.menu('SCREEN_MT_user_menu', text=' Quick')
            '''
            # mesh functions:
            sub = row.column()
            sub.ui_units_x = 4
            sub.menu('VIEW3D_MT_edit_mesh_edges', text='Edge Tool')

            row.separator(factor=1)

            # contour select:
            row.operator('mesh.region_to_loop', text='', icon='CHECKBOX_DEHLT')

            row.separator(factor=1)

            # list modifiers:
            sub = row.column()
            sub.ui_units_x = 4
            sub.scale_y = 1
            sub.operator_menu_enum("object.modifier_add", "type", text='Modifiers')

            # add MOD Bevel :
            row.operator("object.modifier_add", text="", icon="MOD_BEVEL").type='BEVEL'

            row.separator(factor=1)

            # mark seams:
            op = row.operator('mesh.mark_seam', text='',icon='RADIOBUT_ON')
            op = row.operator('mesh.mark_seam', text='',icon='RADIOBUT_OFF')
            op.clear = True

            row.separator(factor=1)

            # mark sharp:
            op = row.operator('mesh.mark_sharp', text='',icon='RADIOBUT_ON')
            op = row.operator('mesh.mark_sharp', text='',icon='RADIOBUT_OFF')
            op.clear = True

    #TOP-RIGHT-------------------------------------------------------------------------------

            row = top_right.row(align=True)

            # normal shading:
            Normals(self, context, layout=row)

            empty = row.column()
            empty.ui_units_x = 6
            empty.separator()

            # annotate & measure:
            tool_bt(layout=row, cmd=9, w=1.2, h=1, text=False, icon='OUTLINER_DATA_GP_LAYER')
            tool_bt(layout=row, cmd=10, w=1.2, h=1, text=False, icon='OUTLINER_DATA_LIGHTPROBE')
            tool_bt(layout=row, cmd=11, w=1.2, h=1, text=False, icon='DRIVER_ROTATIONAL_DIFFERENCE')

    #MAIN-LEFT-----------------------------------------------------------------------------

            row = main_leftrow.row()

            empty = row.column()
            empty.separator()

    #MAIN-MID-----------------------------------------------------------------------------

            row = main_midrow.row()

            # uv-window
            sub = row.column()
            sub.ui_units_x = 8

            subsub = sub.row(align=True)
            subsub.scale_y = 1.2
            subsub.operator("xm.override", icon='ADD', text="").cmd='mesh.uv_texture_add'
            subsub.operator("xm.override", icon='REMOVE', text="").cmd='mesh.uv_texture_remove'
            empty = subsub.column()
            empty.ui_units_x = 3
            empty.separator()

            subsub.operator("xm.override", text="NEW").cmd='material.new'
            subsub.menu("MATERIAL_MT_context_menu", text="",icon='DOWNARROW_HLT')

            UVTexture(self, context, layout=sub)

            # MAT-window:
            sub = row.column()
            sub.ui_units_x = 14
            sub.menu_contents("VIEW3D_MT_Material")

            # vertex group:
            sub = row.column()
            sub.ui_units_x = 10

            subsub = sub.row(align=True)
            subsub.scale_y = 1.2

            subsub.operator('xm.override', text=' Vertex Group ').cmd='object.vertex_group_assign_new'
            subsub.operator('xm.override',text='',icon='X').cmd='object.vertex_group_remove'
            subsub.operator('xm.override',text='',icon='CHECKMARK').cmd='object.vertex_group_assign'
            subsub.operator('xm.override',text='',icon='REMOVE').cmd='object.vertex_group_remove_from'
            subsub.separator(factor = 1)
            subsub.operator('xm.override',text='',icon='RADIOBUT_ON').cmd='object.vertex_group_select'
            subsub.operator('xm.override',text='',icon='RADIOBUT_OFF').cmd='object.vertex_group_deselect'

            subsub = sub.row(align=True)

            if ob != None:
                group = ob.vertex_groups.active
                subsub.template_list("MESH_UL_vgroups", "", ob, "vertex_groups", ob.vertex_groups, "active_index", rows=2)


    #MAIN-RIGHT-----------------------------------------------------------------------------

            row = main_rightrow.row()

            # MOD Window:
            sub = row.column()
            sub.ui_units_x = 13
            sub.scale_y = 1.22

            if ob != None:
                ml_props = bpy.context.window_manager.modifier_list
                active_mod_index = ob.ml_modifier_active_index
                sub.template_list("OBJECT_UL_ml_modifier_list", "", ob, "modifiers", ml_props, "active_object_modifier_active_index", rows=3)

#SCULPT----------------------------------------------------------------------------------------------

        if context.mode == 'SCULPT':

            sculpt = context.tool_settings.sculpt

            main_midrow.alignment = 'CENTER'

    #TOP-LEFT--------------------------------------------------------------------------------

            row = top_left.row(align=True)

            # optimize:
            sub = row.column(align=True)
            sub.ui_units_x = 1.2
            sub.operator('sculpt.optimize', text="" ,icon='SOLO_ON')

            row.separator(factor=2)


            # normal shading:
            sub = row.column(align=True)
            sub.ui_units_x = 2
            sub.operator("xm.normalshading", text="SMTH", depress=update_normaldisp(self, context))

            row.separator(factor=2)

            # symmetrie:
            sub = row.column(align=True) 
            sub.ui_units_x = 2
            sub.scale_y = 1
            sub.operator("sculpt.symmetrize", text='SYM')
            sub = row.column(align=True) 
            sub.ui_units_x = 2
            sub.menu("VIEW3D_MT_sculpt_sym", icon='PREFERENCES')

            row.separator(factor=2)

            # brush preset:
            sub = row.column(align=True) 
            sub.ui_units_x = 4
            BrushCopy(self, context, layout=sub)

    #TOP-MID-------------------------------------------------------------------------------

            row = top_mid.row(align=True)

            row.separator(factor=2)

            # brush settings:
            sub = row.column(align=True)
            sub.ui_units_x = 17
            SculptBrushSettings(self, context, layout=sub)

            row.separator(factor=2)

            # falloff:
            sub = row.column(align=True)
            sub.ui_units_x = 2
            sub.scale_y = 1.4
            sub.menu_contents("VIEW3D_MT_Falloff")

            row.separator(factor=2)

            # toolsettings:
            sub = row.column(align=True)
            sub.ui_units_x = 6
            SculptToolSettings(self, context, layout=sub)

            row.separator(factor=2)

            # mask:
            sub = row.column(align=True)
            sub.ui_units_x = 8
            SculptMask(self, context, layout=sub)

            #TOP-RIGHT--------------------------------------------------------------------------------

            row = top_right.row(align=True)

            # tooloptions:
            sub = row.column(align=True)
            ToolOptions(self, context, layout=sub)

            #MAIN-LEFT--------------------------------------------------------------------------------

            row = main_leftrow.row(align=True)

            # vertex color:
            sub = row.column(align=True)
            sub.ui_units_x = 8
            VertexColor(self, context, layout=sub)

            row.separator(factor=2)

            # brush tex:
            sub = row.column(align=True)
            sub.ui_units_x = 8
            sub.menu_contents("VIEW3D_MT_TextureMask")
            sub.menu_contents("VIEW3D_MT_BrushTexture")

            row.separator(factor=2)

            # stroke:
            sub = row.column(align=True)   
            sub.ui_units_x = 4
            SmoothStroke(self, context, layout=sub)
            Stroke(self, context, layout=sub)

    #MAIN-MID--------------------------------------------------------------------------------

            row = main_midrow.row()

            # paint / grab
            sub = row.column()
            subsub = sub.row(align=True)
            tool_bt(layout=subsub, cmd=36, w=2, h=1.4, text=False, icon='LARGE')
            tool_bt(layout=subsub, cmd=37, w=2, h=1.4, text=False, icon='LARGE')
            subsub.separator(factor = 1)
            tool_bt(layout=subsub, cmd=0, w=2, h=1.4, text=False, icon='LARGE')
            tool_bt(layout=subsub, cmd=19, w=1.2, h=1.4, text=False, icon='CUSTOM')
            tool_bt(layout=subsub, cmd=21, w=1.2, h=1.4, text=False, icon='CUSTOM')
            sub.separator(factor = 0.4)
            subsub = sub.row()
            subsub.ui_units_x = 6
            ColorPalette(self, context, layout=subsub)

            # clay
            row.separator(factor = 0.4)
            sub = row.column()
            subsub = sub.row(align=True)
            tool_bt(layout=subsub, cmd=1, w=2, h=1.4, text=False, icon='LARGE')
            tool_bt(layout=subsub, cmd=2, w=2, h=1.4, text=False, icon='LARGE')
            tool_bt(layout=subsub, cmd=3, w=2, h=1.4, text=False, icon='LARGE')
            sub.separator(factor = 0.4)
            subsub = sub.row(align=True)
            tool_bt(layout=subsub, cmd=4, w=2, h=1.4, text=False, icon='LARGE')
            tool_bt(layout=subsub, cmd=5, w=2, h=1.4, text=False, icon='LARGE')
            tool_bt(layout=subsub, cmd=6, w=2, h=1.4, text=False, icon='LARGE')
            sub.separator(factor = 0.4)

            # extra
            subsub = sub.row(align=True)
            empty = subsub.column()
            empty.ui_units_x = 3.5
            empty.separator()
            tool_bt(layout=subsub, cmd=20, w=1.2, h=1, text=False, icon='CUSTOM')
            tool_bt(layout=subsub, cmd=25, w=1.2, h=1, text=False, icon='CUSTOM')
            tool_bt(layout=subsub, cmd=26, w=1.2, h=1, text=False, icon='CUSTOM')

            # crease & transform
            sub = row.column()
            subsub = sub.row(align=True)
            tool_bt(layout=subsub, cmd=7, w=2, h=1.4, text=False, icon='LARGE')
            tool_bt(layout=subsub, cmd=8, w=2, h=1.4, text=False, icon='LARGE')

            sub.separator(factor = 0.4)

            subsub = sub.row(align=True)
            item = subsub.column(align=True)
            item.ui_units_x = 2
            item.scale_y = 0.7
            item.operator('sculpt.set_pivot_position', text='PVT M').mode='UNMASKED'
            item.operator('sculpt.set_pivot_position', text='RESET').mode='ORIGIN'
            tool_bt(layout=subsub, cmd=18, w=2, h=1.4, text=False, icon='LARGE')

            # polish
            sub = row.column()
            subsub = sub.row(align=True)
            tool_bt(layout=subsub, cmd=9, w=2, h=1.4, text=True, icon='LARGE')
            tool_bt(layout=subsub, cmd=10, w=2, h=1.4, text=True, icon='LARGE')
            sub.separator(factor = 0.4)
            subsub = sub.row(align=True)
            tool_bt(layout=subsub, cmd=11, w=2, h=1.4, text=True, icon='LARGE')
            tool_bt(layout=subsub, cmd=12, w=2, h=1.4, text=True, icon='LARGE')

            row.separator(factor = 0.4)

            # mask
            sub = row.column()
            subsub = sub.row(align=True)
            tool_bt(layout=subsub, cmd=13, w=2, h=1.4, text=False, icon='LARGE') 
            item = subsub.column()
            item.ui_units_x = 3.4
            label = item.column()
            label.scale_y = 0.5
            label.label(text="MASK")
            grid = item.grid_flow(columns=3, align=True)
            tool_bt(layout=grid, cmd=27, w=1.2, h=0.8, text=False, icon='CUSTOM')
            tool_bt(layout=grid, cmd=28, w=1, h=0.8, text=False, icon='CUSTOM')
            tool_bt(layout=grid, cmd=29, w=1.2, h=0.8, text=False, icon='CUSTOM')

            # trim
            item = subsub.column()
            item.ui_units_x = 2.4
            label = item.column()
            label.scale_y = 0.5
            label.label(text="TRIM")
            grid = item.grid_flow(columns=2, align=True)
            tool_bt(layout=grid, cmd=16, w=1.2, h=0.8, icon="CUSTOM", text=False)
            tool_bt(layout=grid, cmd=17, w=1.2, h=0.8, icon="CUSTOM", text=False)

            sub.separator(factor = 0.4)

            # face sets
            subsub = sub.row(align=True)
            tool_bt(layout=subsub, cmd=14, w=2, h=1.4, text=False, icon='LARGE')
            item = subsub.column()       
            grid = item.grid_flow(columns=2, align=True)
            tool_bt(layout=grid, cmd=30, w=1.5, h=0.75, text=False, icon='CUSTOM')
            tool_bt(layout=grid, cmd=31, w=1.5, h=0.75, text=False, icon='CUSTOM')
            tool_bt(layout=item, cmd=32, w=1.2, h=0.5, text=False, icon='OFF')

            # hide
            item = subsub.column()
            item.ui_units_x = 2.4
            tool_bt(layout=item, cmd=15, w=2.4, h=1.4, text=False, icon='LARGE')

            sub.separator(factor = 0.4)

            # face set init
            subsub = sub.row(align=True)
            SculptFaceSet(self, context, layout=subsub)


    #MAIN-RIGHT--------------------------------------------------------------------------------

            row = main_rightrow.row()

            # dyntopo
            row.menu_contents("VIEW3D_MT_dynamesh")

            # remesh
            row.menu_contents("VIEW3D_MT_remesh")

            # meshfilter
            sub = row.column(align=False)
            sub.ui_units_x = 3
            subsub = sub.row()
            subsub.scale_y = 0.5
            subsub.label(text='FILTER')
            subsub = sub.row()
            tool_bt(layout=subsub, cmd=33, w=3, h=1, text=False, icon='OFF')
            subsub = sub.row()
            tool_bt(layout=subsub, cmd=34, w=3, h=1, text=False, icon='OFF')
            subsub = sub.row()
            tool_bt(layout=subsub, cmd=35, w=3, h=1, text=False, icon='OFF')

            SculptFilterSettings(self, context, layout=row)


#PAINT_VERTEX----------------------------------------------------------------------------------------

        if context.mode == 'PAINT_VERTEX':

            brush = context.tool_settings.vertex_paint.brush

    #TOP-LEFT--------------------------------------------------------------------------------

            row = top_left.row()

            # normal shading:
            sub = row.column()
            sub.ui_units_x = 2
            sub.operator("xm.normalshading", text="SMTH", depress=update_normaldisp(self, context))

            # brush preset:
            sub = row.column()
            sub.ui_units_x = 4 
            BrushCopy(self, context, layout=sub)

    #TOP-MID--------------------------------------------------------------------------------

            row = top_mid.row(align=True)

            # blend:
            sub = row.column(align=True)
            sub.ui_units_x = 4
            sub.prop(brush, "blend", text="")
            row.separator()

            # toolset:
            tool_bt(layout=row, cmd=0, w=2, h=1.4, text=False, icon='LARGE')
            row.separator()
            tool_bt(layout=row, cmd=1, w=2, h=1.4, text=False, icon='LARGE')
            tool_bt(layout=row, cmd=2, w=2, h=1.4, text=False, icon='LARGE')
            tool_bt(layout=row, cmd=3, w=2, h=1.4, text=False, icon='LARGE')
            row.separator()

            # falloff:
            sub = row.column(align=True)
            sub.ui_units_x = 2
            sub.scale_y = 1.4
            sub.menu_contents("VIEW3D_MT_Falloff")
            row.separator()

            # brushsettings:
            sub = row.column(align=True)
            sub.ui_units_x = 6
            VertexBrushSettings(self, context, layout=sub)
            row.separator()

            # smoothstroke:
            SmoothStroke(self, context, row)

    #TOP-RIGHT--------------------------------------------------------------------------------

            row = top_right.row(align=True)

            empty = row.column()
            empty.separator()


#PAINT_TEXTURE----------------------------------------------------------------------------------------

        if context.mode == 'PAINT_TEXTURE':

            brush = context.tool_settings.image_paint.brush

    #TOP-LEFT---------------------------------------------------------------------------------

            row = top_left.row()

            # normal shading:
            sub = row.column()
            sub.ui_units_x = 2
            sub.operator("xm.normalshading", text="SMTH", depress=update_normaldisp(self, context))

            # brush preset:
            sub = row.column()
            sub.ui_units_x = 4 
            BrushCopy(self, context, layout=sub)

    #TOP-MID----------------------------------------------------------------------------------

            row = top_mid.row(align=True)

            # blend:
            sub = row.column(align=True)
            sub.ui_units_x = 4
            sub.prop(brush, "blend", text="")
            row.separator()

            # toolset:
            tool_bt(layout=row, cmd=0, w=2, h=1.4, text=False, icon='LARGE')
            row.separator()
            tool_bt(layout=row, cmd=1, w=2, h=1.4, text=False, icon='LARGE')
            tool_bt(layout=row, cmd=2, w=2, h=1.4, text=False, icon='LARGE')
            tool_bt(layout=row, cmd=3, w=2, h=1.4, text=False, icon='LARGE')
            tool_bt(layout=row, cmd=4, w=2, h=1.4, text=False, icon='LARGE')
            tool_bt(layout=row, cmd=5, w=2, h=1.4, text=False, icon='LARGE')
            row.separator()

            # falloff:
            sub = row.column(align=True)
            sub.ui_units_x = 2
            sub.scale_y = 1.4
            sub.menu_contents("VIEW3D_MT_Falloff")
            row.separator()

            # brushsettings:
            sub = row.column(align=True)
            TextureBrushSettings(self, context, layout=sub)
            row.separator()

            # smoothstroke:
            SmoothStroke(self, context, row)

    #TOP-RIGHT-------------------------------------------------------------------------------

            row = top_right.row(align=True)

            # tooloptions:
            ToolOptions(self, context, layout=row)



#PAINT_WEIGHT----------------------------------------------------------------------------------------

        if context.mode == 'PAINT_WEIGHT':

            brush = context.tool_settings.vertex_paint.brush

    #TOP-LEFT--------------------------------------------------------------------------------

            row = top_left.row()

            # brush preset:
            sub = row.column()
            sub.ui_units_x = 4 
            BrushCopy(self, context, layout=sub)

    #TOP-MID---------------------------------------------------------------------------------
            
            row = top_mid.row(align=True)

            # toolset:
            tool_bt(layout=row, cmd=0, w=2, h=1.4, text=False, icon='LARGE')
            row.separator()
            tool_bt(layout=row, cmd=1, w=2, h=1.4, text=False, icon='LARGE')
            tool_bt(layout=row, cmd=2, w=2, h=1.4, text=False, icon='LARGE')
            tool_bt(layout=row, cmd=3, w=2, h=1.4, text=False, icon='LARGE')
            tool_bt(layout=row, cmd=4, w=2, h=1.4, text=False, icon='LARGE')
            tool_bt(layout=row, cmd=5, w=2, h=1.4, text=False, icon='LARGE')
            tool_bt(layout=row, cmd=6, w=2, h=1.4, text=False, icon='LARGE')
            row.separator()

            # falloff:
            sub = row.column()
            sub.ui_units_x = 2
            sub.scale_y = 1.4
            sub.menu_contents("VIEW3D_MT_Falloff")
            row.separator()

            # brushsettings:
            sub = row.row(align=True)
            sub.ui_units_x = 4
            sub.prop(brush, "use_frontface", text="FRONT", toggle=True)
            sub.prop(brush, "use_accumulate", text="ACCU", toggle=True)
            row.separator()

            # smoothstroke:
            SmoothStroke(self, context, row)

    #TOP-RIGHT-------------------------------------------------------------------------------

            row = top_right.row(align=True)

            # tooloptions:
            sub = row.row(align=True)
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

            # clean up:
            sub = row.column()
            sub.ui_units_x = 4
            sub.menu("GPENCIL_MT_cleanup")

            # init:
            sub = row.column()
            sub.ui_units_x = 4
            sub.operator("gpencil.blank_frame_add", text="INIT")

    #TOP-MID--------------------------------------------------------------------------------

            row = top_mid.row(align=True)
            row.alignment = 'CENTER'

            # brush preset:
            sub = row.column()
            sub.ui_units_x = 4         
            BrushCopy(self, context, layout=sub)

            row.separator()

            # toolset:
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

            # smoothstroke:
            GPSmoothStroke(self, context, layout=row)

    #TOP-RIGHT-------------------------------------------------------------------------------

            row = top_right.row(align=True)

            # stroke post:
            sub = row.column(align=True)
            sub.ui_units_x = 4
            sub.scale_y = 1
            sub.popover("VIEW3D_PT_tools_grease_pencil_brush_post_processing")

            # stroke randomize:
            sub = row.column(align=True)
            sub.ui_units_x = 4
            sub.scale_y = 1
            sub.popover("VIEW3D_PT_tools_grease_pencil_brush_random")

            # advanced:
            sub = row.column(align=True)
            sub.ui_units_x = 4
            sub.scale_y = 1
            sub.popover("VIEW3D_PT_tools_grease_pencil_brush_advanced")


#EDIT_GPENCIL----------------------------------------------------------------------------------------

        if context.mode == 'EDIT_GPENCIL':

            brush = context.tool_settings.gpencil_paint.brush

    #TOP-LEFT--------------------------------------------------------------------------------

            row = top_left.row(align=True)

            # resample:
            sub = row.column(align=True)
            sub.ui_units_x = 3.2
            sub.scale_y = 0.7
            sub.operator("gpencil.stroke_simplify", text="SIMPL")
            sub.operator("gpencil.stroke_sample", text="RESAMP")

            # subdivide/smooth:
            sub = row.column(align=True)
            sub.ui_units_x = 3.2
            sub.scale_y = 0.7
            sub.operator("gpencil.stroke_subdivide", text="SUBDIV").only_selected=True
            sub.operator("gpencil.stroke_smooth", text="SMTH").only_selected=True

            row.separator(factor=2)

            # close/trim:
            sub = row.column(align=True)
            sub.ui_units_x = 2.4
            sub.scale_y = 0.7
            op = sub.operator("gpencil.stroke_cyclical_set", text="CLOSE")
            op.type='CLOSE'
            op.geometry=True
            sub.operator("gpencil.stroke_trim", text="TRIM")

            # merge/join:
            sub = row.column(align=True)
            sub.ui_units_x = 2.4
            sub.scale_y = 0.7
            sub.operator("gpencil.stroke_merge", text="MERGE")
            sub.operator("gpencil.stroke_join", text="JOIN")

    #TOP-MID-------------------------------------------------------------------------------

            row = top_mid.row(align=True)
            row.alignment = 'CENTER'

            # toolset:
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

            # toolsettings
            col = row.column()
            col.ui_units_x = 5
            GPToolSettings(self, context, layout=col)

            row.separator(factor = 2)

            # functions
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

            row = top_right.row(align=True)

            empty = row.column()
            empty.separator()



#SCULPT_GPENCIL------------------------------------------------------------------------------------

        if context.mode == 'SCULPT_GPENCIL':

            brush = context.tool_settings.gpencil_paint.brush


    #TOP-LEFT------------------------------------------------------------------------------

            row = top_left.row(align=True)

            # brush preset:
            sub = row.column()
            col.ui_units_x = 4
            BrushCopy(self, context, layout=sub)

    #TOP-MID-------------------------------------------------------------------------------

            row = top_mid.row(align=True)

            # toolset:
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

            # falloff:
            sub = row.column()
            sub.ui_units_x = 2
            sub.scale_y = 1.4
            sub.menu_contents("VIEW3D_MT_Falloff")

            row.separator(factor=1)

            # toolsettings:
            sub = row.column()
            sub.ui_units_x = 6
            GPSculptToolSettings(self, context, layout=sub)

    #TOP-RIGHT-------------------------------------------------------------------------------


            row = top_right.row(align=True)

            empty = row.column()
            empty.separator()

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

            row = top_left.row(align=True)

            empty = row.column()
            empty.separator()

    #TOP-MID---------------------------------------------------------------------------------
            row = top_mid.row(align=True)

            # toolset:
            tool_bt(layout=row, cmd=0, w=2.2, h=1.4, text=False, icon='LARGE')

    #TOP-RIGHT-------------------------------------------------------------------------------

            row = top_right.row(align=True)

            empty = row.column()
            empty.separator()


        redraw_regions()

#-----------------------------------------------------------------------------------------------------------------------

def register() :
    bpy.utils.register_class(XPanel)

def unregister() :
    bpy.utils.unregister_class(XPanel)
