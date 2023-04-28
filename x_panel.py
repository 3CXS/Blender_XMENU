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

        ui_scale = context.preferences.view.ui_scale

        for region in bpy.context.area.regions:
            if region.type == 'WINDOW':
                view_width = region.width/(19.66*ui_scale)

    # LAYOUT-STRUCTURE-----------------------------------------------------------------------------------------
        main_row = layout.row(align=True)
        main_row.ui_units_x = view_width
        main_row.alignment = 'CENTER'
        row = main_row.row(align=True)
        row.alignment = 'CENTER'
    # Top-Row
        top_row = layout.row()
        top_row.alignment = 'CENTER'
        # Left-Outer
        top_left_outer = top_row.row()
        top_left_outer.ui_units_x = 5
        top_left_outer.alignment = 'LEFT'
        # Left
        top_left = top_row.row(align=True)
        top_left.ui_units_x = 19
        top_left.alignment = 'RIGHT'
        # Mid
        top_mid = top_row.row()
        top_mid.alignment = 'LEFT'
        top_mid.ui_units_x = 36
        # Right
        top_right = top_row.row(align=True)
        top_right.ui_units_x = 19
        top_right.alignment = 'LEFT'
        # Right-Outer
        top_right_outer = top_row.row()
        top_right_outer.ui_units_x = 5
        top_right_outer.alignment = 'RIGHT'
    # Main-Row
        main_row = layout.row()
        main_row.alignment = 'CENTER'
        # Left
        main_left = main_row.column()
        main_left.ui_units_x = 24
        main_leftbox = main_left.box()
        main_leftbox.ui_units_y = 0.6
        main_leftrow = main_left.row()
        main_leftrow.alignment = 'RIGHT'
        # Mid
        main_mid = main_row.column()
        main_mid.ui_units_x = 36
        main_midbox = main_mid.box()
        main_midbox.ui_units_y = 0.6
        main_midrow = main_mid.row()
        # Right
        main_right = main_row.column()
        main_right.ui_units_x = 24
        main_rightbox = main_right.box()
        main_rightbox.ui_units_y = 0.6
        main_rightrow = main_right.row()
        main_rightrow.alignment = 'LEFT'
    # End-Row
        end = layout.row()
        end.ui_units_x = 0.2
        end.ui_units_y = 10
        end.label(text="")

    # TOP-LEFT OUTER-----------------------------------------------------------------------------
        col = top_left_outer.column(align=True)
        col.ui_units_x = 0.2
        col.scale_y = 0.7
        col.label(text='')
        col.label(text='')

    # TOP-RIGHT OUTER------------------------------------------------------------------------------
        col = top_right_outer.column(align=True)
        col.ui_units_x = 0.2
        col.scale_y = 0.7
        col.label(text='')
        col.label(text='')

    #OBJECT//////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
        if context.mode == 'OBJECT':
            main_midrow.alignment = 'LEFT'

        #TOP-LEFT---------------------------------------------------------------------------------
            row = top_left.row(align=True)

            #Tools
            tool_bt(layout=row, cmd=6, w=1.2, h=1, text=False, icon='CUSTOM')
            tool_bt(layout=row, cmd=7, w=1.2, h=1, text=False, icon='CUSTOM')
            tool_bt(layout=row, cmd=8, w=1.2, h=1, text=False, icon='CUSTOM')
            tool_bt(layout=row, cmd=9, w=1.2, h=1, text=False, icon='CUSTOM')
            row.separator(factor = 2)
            tool_bt(layout=row, cmd=1, w=1.2, h=1, text=False, icon='CUSTOM')
            tool_bt(layout=row, cmd=2, w=1.2, h=1, text=False, icon='CUSTOM')
            tool_bt(layout=row, cmd=3, w=1.2, h=1, text=False, icon='CUSTOM')
            tool_bt(layout=row, cmd=4, w=1.2, h=1, text=False, icon='CUSTOM')
            tool_bt(layout=row, cmd=5, w=1.2, h=1, text=False, icon='CUSTOM')

        #TOP-MID----------------------------------------------------------------------------------
            row = top_mid.row(align=True)

            #Add-Object
            sub = row.column()
            sub.ui_units_x = 4
            sub.menu("VIEW3D_MT_add", text="OBJECT", text_ctxt=i18n_contexts.operator_default)
            row.operator('mesh.primitive_plane_add', text="", icon='MESH_PLANE')
            row.operator('mesh.primitive_cube_add', text="", icon='MESH_CUBE')
            row.operator('mesh.primitive_uv_sphere_add', text="", icon='MESH_UVSPHERE')
            row.operator('mesh.primitive_cylinder_add', text="", icon='MESH_CYLINDER')
            row.operator('object.empty_add', text="", icon='EMPTY_DATA')
            row.operator('object.gpencil_add', text="", icon='GREASEPENCIL')
            row.separator(factor=1) 

            #Modifiers
            sub = row.column()
            sub.ui_units_x = 4
            sub.operator_menu_enum("object.modifier_add", "type", text="MODIFIER")
            sub = row.row(align=True)
            sub.ui_units_x = 11
            if ob != None:
                if ob.type == 'MESH':
                    sub.operator("object.modifier_add", text="BVL", icon="NONE").type='BEVEL'
                    sub.operator("object.modifier_add", text="SLD", icon="NONE").type='SOLIDIFY'
                    sub.operator("object.modifier_add", text="SUBD", icon="NONE").type='SUBSURF'
                    sub.operator("object.modifier_add", text="SYM", icon="NONE").type='MIRROR'
                    sub.operator("object.modifier_add", text="RMSH", icon="NONE").type='REMESH'
                    sub.operator("object.modifier_add", text="DEC", icon="NONE").type='DECIMATE'
                    row.separator(factor=1)
            #Bool-Operators
                    row.operator('btool.boolean_union', text="", icon='SELECT_EXTEND')
                    row.operator('btool.boolean_diff', text="", icon='SELECT_SUBTRACT')
                    row.operator('btool.boolean_inters', text="", icon='SELECT_INTERSECT')
                    row.operator('btool.boolean_slice', text="", icon='SELECT_DIFFERENCE')
                    row.separator(factor=1)

            else:
                subsub = row.column(align=True)
                subsub.ui_units_x = 1.2
                subsub.label(text=">")

            #Convert
            sub = row.row(align=True)
            sub.ui_units_x = 2
            sub.operator('object.convert', text="CONV", ) #icon='SHADERFX'
            row.separator(factor=1)

            #Merge/Dub
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

            row.separator(factor = 2)

        #TOP-RIGHT-------------------------------------------------------------------------------
            row = top_right.row(align=True)

            #Tool-Options
            sub = row.column()
            sub.ui_units_x = 8.9
            ToolOptions(self, context, layout=sub)
            row.separator(factor = 2)

        #MAIN-LEFT-------------------------------------------------------------------------------
            row = main_leftrow.row()

            #Save-Scene
            sub = row.column(align=True)
            sub.ui_units_x = 4
            SaveScene(self, context, layout=sub)

            #Import
            sub = row.column(align=True)
            sub.ui_units_x = 4
            sub.menu_contents("OBJECT_MT_io_menu")
            InsertSpace(row, space=11)

            #Selection
            sub = row.column(align=True)
            sub.ui_units_x = 4
            op = sub.operator("xm.override2", text="HIERARCHY")
            op.cmd ='object.select_hierarchy'
            op.prop1 ='direction="CHILD"'
            op.prop2 ='extend=True'
            sub.separator(factor = 1)
            subsub = sub.row(align=True)
            subsub.operator('object.select_linked', text='DATA').type='OBDATA'
            subsub.operator('object.select_linked', text='MAT').type='MATERIAL'
            subsub = sub.row(align=True)
            subsub.operator('object.select_linked', text='INST').type='DUPGROUP'
            subsub.operator('object.select_linked', text='LIB').type='LIBRARY_OBDATA'

        #MAIN-MID-------------------------------------------------------------------------------
            row = main_midrow.row()

            #UV
            sub = row.column()
            sub.ui_units_x = 10
            UVTexture(self, context, layout=sub)

            #Vertex-Group
            sub = row.column()
            sub.ui_units_x = 12
            VertexGroups(self, context, layout=sub)

            #Material
            sub = row.column()
            sub.ui_units_x = 14
            sub.menu_contents("VIEW3D_MT_Material")

        #MAIN-RIGHT------------------------------------------------------------------------------
            row = main_rightrow.row()

            #Transform-Matrix
            sub = row.column(align=True)
            sub.ui_units_x = 9
            Transforms(self, context, layout=sub)
            sub = row.column(align=True)
            sub.ui_units_x = 4
            if ob:
                op = sub.operator('object.origin_set', text='COG')
                op.type = 'ORIGIN_GEOMETRY'
                op.center ='MEDIAN'
                sub.operator('xm.floor', text='FLOOR')
                op = sub.operator('object.origin_set', text='CURSOR')
                op.type = 'ORIGIN_CURSOR'
                op.center ='MEDIAN'
            else:
                sub.label(text=">")
            row.separator(factor=1)

            #MOD-Window
            sub = row.column()
            sub.ui_units_x = 10
            ModifierWindow(self, context, layout=sub)

        #EDIT//////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
        if context.mode == 'EDIT_MESH':
            main_midrow.alignment = 'LEFT'

        #TOP-LEFT--------------------------------------------------------------------------------
            row = top_left.row(align=True)

            #Toolset
            tool_bt(layout=row, cmd=6, w=1.2, h=1, text=False, icon='CUSTOM')
            tool_bt(layout=row, cmd=7, w=1.2, h=1, text=False, icon='CUSTOM')
            tool_bt(layout=row, cmd=8, w=1.2, h=1, text=False, icon='CUSTOM')
            tool_bt(layout=row, cmd=9, w=1.2, h=1, text=False, icon='CUSTOM')
            row.separator(factor = 2)
            tool_bt(layout=row, cmd=1, w=1.2, h=1, text=False, icon='CUSTOM')
            tool_bt(layout=row, cmd=2, w=1.2, h=1, text=False, icon='CUSTOM')
            tool_bt(layout=row, cmd=3, w=1.2, h=1, text=False, icon='CUSTOM')
            tool_bt(layout=row, cmd=4, w=1.2, h=1, text=False, icon='CUSTOM')
            tool_bt(layout=row, cmd=5, w=1.2, h=1, text=False, icon='CUSTOM')

            # select contour:
            #row.operator('mesh.region_to_loop', text='', icon='CHECKBOX_DEHLT')
            # quick pivot:
            #row.operator('mesh.quick_pivot', text='', icon='SNAP_FACE_CENTER')

        #TOP-MID---------------------------------------------------------------------------------
            row = top_mid.row(align=True)

            #Add-Mesh
            sub = row.column()
            sub.ui_units_x = 3
            sub.menu("VIEW3D_MT_mesh_add", icon='NONE', text='MESH') 
            row.operator('mesh.primitive_plane_add', text="", icon='MESH_PLANE')
            row.operator('mesh.primitive_cube_add', text="", icon='MESH_CUBE')
            row.operator('mesh.primitive_uv_sphere_add', text="", icon='MESH_UVSPHERE')
            row.operator('mesh.primitive_cylinder_add', text="", icon='MESH_CYLINDER')
            row.separator(factor=1) 

            #Modifiers
            sub = row.column()
            sub.ui_units_x = 4
            sub.scale_y = 1
            sub.operator_menu_enum("object.modifier_add", "type", text='MODIFIER')
            sub = row.row(align=True)
            sub.ui_units_x = 10
            sub.operator("object.modifier_add", text="BVL", icon="NONE").type='BEVEL'
            sub.operator("object.modifier_add", text="SLD", icon="NONE").type='SOLIDIFY'
            sub.operator("object.modifier_add", text="SUBD", icon="NONE").type='SUBSURF'
            sub.operator("object.modifier_add", text="SYM", icon="NONE").type='MIRROR'
            sub.operator("object.modifier_add", text="RMSH", icon="NONE").type='REMESH'
            sub.operator("object.modifier_add", text="DEC", icon="NONE").type='DECIMATE'
            row.separator(factor=1)

            #Mark-Seam
            sub = row.row(align=True)
            sub.ui_units_x = 2.5
            op = sub.operator('mesh.mark_seam', text='SEAM',icon='NONE')
            op = sub.operator('mesh.mark_seam', text='',icon='RADIOBUT_OFF')
            op.clear = True

            #Mark-Sharp
            sub = row.row(align=True)
            sub.ui_units_x = 2.5
            op = sub.operator('mesh.mark_sharp', text='SHRP',icon='NONE')
            op = sub.operator('mesh.mark_sharp', text='',icon='RADIOBUT_OFF')
            op.clear = True
            row.separator(factor=1)

            #Selection
            sub = row.column(align=True)
            sub.ui_units_x = 9
            subsub = sub.row(align=True)
            subsub.scale_x = 2.3
            subsub.operator('mesh.select_all',text='',icon='SHADING_SOLID').action='SELECT'
            subsub.operator('mesh.select_all',text='', icon='IMAGE_ALPHA').action='INVERT'
            subsub.operator('mesh.select_less', icon='REMOVE', text='')
            subsub.operator('mesh.select_more', icon='ADD',text='')

        #TOP-RIGHT-------------------------------------------------------------------------------
            row = top_right.row(align=True)

            #Edge-Tools
            sub = row.row(align=True)
            sub.ui_units_x = 8.3
            sub.operator('transform.edge_bevelweight', text='Bevel')
            sub.operator('transform.edge_crease', text='Crease')


        #MAIN-LEFT-----------------------------------------------------------------------------
            row = main_leftrow.row()

            # UV
            sub = row.column()
            sub.ui_units_x = 10
            UVTexture(self, context, layout=sub)
            row.separator(factor=8)

            #Functions
            col = row.column()
            col.ui_units_x = 11.8
            sub = col.row(align=True)
            sub.operator('mesh.fill_holes', text='FILL-H')
            sub.operator('mesh.edge_face_add', text='FILL')
            sub.operator('mesh.merge', text="MERGE").type='CENTER'
            col.separator(factor=0.5)
            sub = col.row(align=True)
            sub.operator('mesh.flip_normals', text='FLIP')
            sub.operator('mesh.remove_doubles', text='CLEAN')
            sub.operator('mesh.delete_loose', text='LOOSE')
            col.separator(factor=2)
            sub = col.row()
            subsub = sub.column(align=True)
            subsub.operator('mesh.symmetrize', text='SYM')
            op = subsub.operator('transform.mirror', text='MIRROR')
            op.orient_type='GLOBAL'
            op.constraint_axis=(True, False, False)
            subsub = sub.column(align=True)
            subsub.operator('uv.smart_project', text="A-UV")
            subsub.operator('uv.unwrap', text="UNWRP")

        #MAIN-MID-----------------------------------------------------------------------------
            row = main_midrow.row()

            #Tools
            col = row.column(align=True)
            col.ui_units_x = 12

            sub = col.row(align=True)
            tool_bt(layout=sub, cmd=21, w=4, h=1, text=False, icon='OFF')
            sub.separator()
            tool_bt(layout=sub, cmd=20, w=4, h=1, text=False, icon='OFF')
            sub.separator()
            tool_bt(layout=sub, cmd=16, w=4, h=1, text=False, icon='OFF')

            sub = col.row(align=True)
            tool_bt(layout=sub, cmd=23, w=4, h=1, text=False, icon='OFF')
            sub.separator()
            tool_bt(layout=sub, cmd=19, w=4, h=1, text=False, icon='OFF')
            sub.separator()
            tool_bt(layout=sub, cmd=17, w=4, h=1, text=False, icon='OFF')
            col.separator(factor=0.5)

            sub = col.row(align=True)
            tool_bt(layout=sub, cmd=25, w=4, h=1, text=False, icon='OFF')
            sub.separator()
            tool_bt(layout=sub, cmd=30, w=4, h=1, text=False,icon='OFF')
            sub.separator()
            tool_bt(layout=sub, cmd=33, w=4, h=1, text=False, icon='OFF')

            sub = col.row(align=True)
            tool_bt(layout=sub, cmd=35, w=4, h=1, text=False, icon='OFF')
            sub.separator()
            tool_bt(layout=sub, cmd=31, w=4, h=1, text=False, icon='OFF')
            sub.separator()
            tool_bt(layout=sub, cmd=32, w=4, h=1, text=False, icon='OFF')
            col.separator(factor=0.5)

            sub = col.row(align=True)
            sub.scale_y = 0.95
            sub.operator('mesh.split', text='SPLIT', icon='NONE')
            sub.operator('mesh.duplicate_move', text='DUB', icon='NONE')

            #Vertex-Group
            sub = row.column()
            sub.ui_units_x = 14
            VertexGroups(self, context, layout=sub)

            #Selection
            sub = row.column(align=True)
            sub.ui_units_x = 9
            subsub = sub.row(align=True)
            subsub.scale_y = 1.2
            subsub.operator('mesh.select_linked',text='LINK')
            subsub.operator('mesh.shortest_path_select',text='PATH')
            subsub.operator('mesh.faces_select_linked_flat',text='FLAT')
            subsub.operator('mesh.select_mirror',text='MIR')
            subsub = sub.row(align=True)
            subsub.operator_menu_enum("mesh.select_similar", "type", text="SIMILAR")
            subsub.operator_menu_enum("mesh.select_linked", "delimit", text="LINKED")
            subsub = sub.row(align=True)
            subsub .operator('mesh.select_non_manifold',text='BND')
            subsub .operator('mesh.select_loose',text='LSE')
            subsub .operator('mesh.select_interior_faces',text='INT')
            subsub .operator('mesh.select_face_by_sides',text='CNT')
            sub.separator()

            #Separate-Mesh:
            subsub = sub.row(align=True)
            subsub.scale_y = 0.7
            subsub.label(text="Separate:")
            subsub = sub.row(align=True)
            op = subsub.operator('mesh.separate', text='SEL', icon='NONE')
            op.type='SELECTED'
            op = subsub.operator('mesh.separate', text='MAT', icon='NONE')
            op.type='MATERIAL'
            op = subsub.operator('mesh.separate', text='PARTS', icon='NONE')
            op.type='LOOSE'


        #MAIN-RIGHT-----------------------------------------------------------------------------
            row = main_rightrow.row()

            #Material
            sub = row.column()
            sub.ui_units_x = 14
            sub.menu_contents("VIEW3D_MT_Material")

            #MOD-Window
            sub = row.column()
            sub.ui_units_x = 10
            ModifierWindow(self, context, layout=sub)

        #SCULPT//////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
        if context.mode == 'SCULPT':
            main_midrow.alignment = 'CENTER'
            sculpt = context.tool_settings.sculpt

        #TOP-LEFT--------------------------------------------------------------------------------
            row = top_left.row(align=True)

            # BrushTexture-Ramp
            sub = row.column(align=True)
            sub.ui_units_x = 8
            sub.menu_contents("VIEW3D_MT_TextureMask")
            row.separator(factor=2)

            #Brush-Preset
            sub = row.column(align=True) 
            sub.ui_units_x = 5
            BrushCopy(self, context, layout=sub)

        #TOP-MID-------------------------------------------------------------------------------
            row = top_mid.row(align=True)
            row.separator(factor=2)

            #Tool-Settings
            sub = row.column(align=True)
            sub.ui_units_x = 5.4
            SculptToolSettings(self, context, layout=sub)

            row.separator(factor=2)

            #Brush-Settings
            sub = row.column(align=True)
            sub.ui_units_x = 17
            SculptBrushSettings(self, context, layout=sub)

            row.separator(factor=2)

            #Falloff
            sub = row.column(align=True)
            sub.ui_units_x = 2
            sub.scale_y = 1.4
            sub.menu_contents("VIEW3D_MT_Falloff")

            row.separator(factor=3)

            #Mask
            sub = row.column(align=True)
            sub.ui_units_x = 8
            SculptMask(self, context, layout=sub)

        #TOP-RIGHT--------------------------------------------------------------------------------
            row = top_right.row(align=True)

            #Tool-Options
            sub = row.column(align=True)
            ToolOptions(self, context, layout=sub)
            InsertSpace(row, space=2.4)

            #Smooth-Stroke
            sub = row.column(align=True)   
            sub.ui_units_x = 5
            SmoothStroke(self, context, layout=sub)

        #MAIN-LEFT--------------------------------------------------------------------------------

            row = main_leftrow.row(align=True)

            #Vertex-Color
            sub = row.column(align=True)
            sub.ui_units_x = 8
            mesh = context.active_object.data
            subsub = sub.row(align=True)
            subsub.operator("xm.override", icon='ADD', text="VERTEX COLOR").cmd='geometry.color_attribute_add'
            subsub.operator("xm.override", icon='REMOVE', text="").cmd='geometry.color_attribute_remove'
            subsub = sub.column()
            subsub.template_list("MESH_UL_color_attributes", "color_attributes", mesh, "color_attributes", mesh.color_attributes, "active_color_index", rows=2)

            row.separator(factor=2)

            #Brush-Texture
            sub = row.column(align=True)
            sub.ui_units_x = 8
            sub.menu_contents("VIEW3D_MT_BrushTexture")

            row.separator(factor=2)

            #Stroke
            sub = row.column(align=True)   
            sub.ui_units_x = 5
            Stroke(self, context, layout=sub)

        #MAIN-MID--------------------------------------------------------------------------------

            row = main_midrow.row()

            #Paint/Grab
            sub = row.column()
            subsub = sub.row(align=True)
            tool_bt(layout=subsub, cmd=37, w=2, h=1.4, text=True, icon='LARGE')
            tool_bt(layout=subsub, cmd=38, w=2, h=1.4, text=True, icon='LARGE')
            subsub.separator(factor = 1)
            tool_bt(layout=subsub, cmd=1, w=2, h=1.4, text=True, icon='LARGE')
            tool_bt(layout=subsub, cmd=20, w=1.2, h=1.4, text=False, icon='CUSTOM')
            tool_bt(layout=subsub, cmd=22, w=1.2, h=1.4, text=False, icon='CUSTOM')
            sub.separator(factor = 0.4)
            subsub = sub.row()
            subsub.ui_units_x = 6
            ColorPalette(self, context, layout=subsub)

            #Clay
            row.separator(factor = 0.4)
            sub = row.column()
            subsub = sub.row(align=True)
            tool_bt(layout=subsub, cmd=2, w=2, h=1.4, text=True, icon='LARGE')
            tool_bt(layout=subsub, cmd=3, w=2, h=1.4, text=True, icon='LARGE')
            tool_bt(layout=subsub, cmd=4, w=2, h=1.4, text=True, icon='LARGE')
            sub.separator(factor = 0.4)
            subsub = sub.row(align=True)
            tool_bt(layout=subsub, cmd=5, w=2, h=1.4, text=True, icon='LARGE')
            tool_bt(layout=subsub, cmd=6, w=2, h=1.4, text=True, icon='LARGE')
            tool_bt(layout=subsub, cmd=7, w=2, h=1.4, text=True, icon='LARGE')
            sub.separator(factor = 0.4)

            #Extra
            subsub = sub.row(align=True)
            InsertSpace(subsub, space=3)
            tool_bt(layout=subsub, cmd=21, w=1.2, h=1, text=False, icon='CUSTOM')
            tool_bt(layout=subsub, cmd=26, w=1.2, h=1, text=False, icon='CUSTOM')
            tool_bt(layout=subsub, cmd=27, w=1.2, h=1, text=False, icon='CUSTOM')

            #Crease/Transform
            sub = row.column()
            subsub = sub.row(align=True)
            tool_bt(layout=subsub, cmd=8, w=2, h=1.4, text=True, icon='LARGE')
            tool_bt(layout=subsub, cmd=9, w=2, h=1.4, text=True, icon='LARGE')
            sub.separator(factor = 0.4)
            subsub = sub.row(align=True)
            item = subsub.column(align=True)
            item.ui_units_x = 2
            item.scale_y = 0.7
            item.operator('sculpt.set_pivot_position', text='PVT M').mode='UNMASKED'
            item.operator('sculpt.set_pivot_position', text='RESET').mode='ORIGIN'
            tool_bt(layout=subsub, cmd=19, w=2, h=1.4, text=False, icon='LARGE')

            #Polish
            sub = row.column()
            subsub = sub.row(align=True)
            tool_bt(layout=subsub, cmd=10, w=2, h=1.4, text=True, icon='LARGE')
            tool_bt(layout=subsub, cmd=11, w=2, h=1.4, text=True, icon='LARGE')
            sub.separator(factor = 0.4)
            subsub = sub.row(align=True)
            tool_bt(layout=subsub, cmd=12, w=2, h=1.4, text=True, icon='LARGE')
            tool_bt(layout=subsub, cmd=13, w=2, h=1.4, text=True, icon='LARGE')
            row.separator(factor = 0.4)

            #Mask
            sub = row.column()
            subsub = sub.row(align=True)
            tool_bt(layout=subsub, cmd=14, w=2, h=1.4, text=False, icon='LARGE') 
            item = subsub.column()
            item.ui_units_x = 3.4
            label = item.column()
            label.scale_y = 0.5
            label.label(text="MASK")
            grid = item.grid_flow(columns=3, align=True)
            tool_bt(layout=grid, cmd=28, w=1.2, h=0.8, text=False, icon='CUSTOM')
            tool_bt(layout=grid, cmd=29, w=1, h=0.8, text=False, icon='CUSTOM')
            tool_bt(layout=grid, cmd=30, w=1.2, h=0.8, text=False, icon='CUSTOM')

            #Trim
            item = subsub.column()
            item.ui_units_x = 2.4
            label = item.column()
            label.scale_y = 0.5
            label.label(text="TRIM")
            grid = item.grid_flow(columns=2, align=True)
            tool_bt(layout=grid, cmd=17, w=1.2, h=0.8, icon="CUSTOM", text=False)
            tool_bt(layout=grid, cmd=18, w=1.2, h=0.8, icon="CUSTOM", text=False)

            sub.separator(factor = 0.4)

            #Face-Set
            subsub = sub.row(align=True)
            tool_bt(layout=subsub, cmd=15, w=2, h=1.4, text=False, icon='LARGE')
            item = subsub.column()       
            grid = item.grid_flow(columns=2, align=True)
            tool_bt(layout=grid, cmd=31, w=1.5, h=0.75, text=False, icon='CUSTOM')
            tool_bt(layout=grid, cmd=32, w=1.5, h=0.75, text=False, icon='CUSTOM')
            tool_bt(layout=item, cmd=33, w=1.2, h=0.5, text=False, icon='OFF')

            #Hide
            item = subsub.column()
            item.ui_units_x = 2.4
            tool_bt(layout=item, cmd=16, w=2.4, h=1.4, text=False, icon='LARGE')
            sub.separator(factor = 0.4)

            #Face-Set-Init
            subsub = sub.row(align=True)
            SculptFaceSet(self, context, layout=subsub)

        #MAIN-RIGHT--------------------------------------------------------------------------------
            row = main_rightrow.row()

            #Dyntopo
            row.menu_contents("VIEW3D_MT_dynamesh")

            #Remesh
            row.menu_contents("VIEW3D_MT_remesh")

            #Meshfilter
            sub = row.column(align=True)
            sub.ui_units_x = 3
            subsub = sub.row(align=True)
            tool_bt(layout=subsub, cmd=34, w=3, h=1, text=False, icon='OFF')
            subsub = sub.row(align=True)
            tool_bt(layout=subsub, cmd=35, w=3, h=1, text=False, icon='OFF')
            subsub = sub.row(align=True)
            tool_bt(layout=subsub, cmd=36, w=3, h=1, text=False, icon='OFF')
            SculptFilterSettings(self, context, layout=row)

        #PAINT_VERTEX//////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
        if context.mode == 'PAINT_VERTEX':
            brush = context.tool_settings.vertex_paint.brush

        #TOP-LEFT--------------------------------------------------------------------------------
            row = top_left.row(align=True)

            # BrushTexture-Ramp
            sub = row.column(align=True)
            sub.ui_units_x = 8
            sub.menu_contents("VIEW3D_MT_TextureMask")
            row.separator(factor=2)

            #Brush-Preset
            sub = row.column(align=True) 
            sub.ui_units_x = 5
            BrushCopy(self, context, layout=sub)


        #TOP-MID--------------------------------------------------------------------------------

            row = top_mid.row(align=True)

            #Blend
            sub = row.column(align=True)
            sub.ui_units_x = 4.7
            sub.prop(brush, "blend", text="")
            row.separator()

            #Tools:
            tool_bt(layout=row, cmd=1, w=2, h=1.4, text=True, icon='LARGE')
            row.separator()
            tool_bt(layout=row, cmd=2, w=2, h=1.4, text=True, icon='LARGE')
            tool_bt(layout=row, cmd=3, w=2, h=1.4, text=True, icon='LARGE')
            tool_bt(layout=row, cmd=4, w=2, h=1.4, text=True, icon='LARGE')
            row.separator()

            #Falloff
            sub = row.column(align=True)
            sub.ui_units_x = 2
            sub.scale_y = 1.4
            sub.menu_contents("VIEW3D_MT_Falloff")
            row.separator()

            #Brush-Settings
            sub = row.column(align=True)
            sub.ui_units_x = 7
            VertexBrushSettings(self, context, layout=sub)

        #TOP-RIGHT--------------------------------------------------------------------------------
            row = top_right.row(align=True)

            #Smooth-Stroke
            sub = row.column(align=True)   
            sub.ui_units_x = 5
            SmoothStroke(self, context, layout=sub)


        #MAIN-LEFT-------------------------------------------------------------------------------
            row = main_leftrow.row(align=True)

            #Palette
            sub = row.column(align=True)
            sub.ui_units_x = 10
            ColorPalette(self, context, layout=sub)

            #Brush-Tex
            sub = row.column(align=True)
            sub.ui_units_x = 8
            sub.menu_contents("VIEW3D_MT_BrushTexture")
            row.separator(factor=2) 

            #Stroke
            sub = row.column(align=True)   
            sub.ui_units_x = 5
            Stroke(self, context, layout=sub)

        #MAIN-MID-------------------------------------------------------------------------------
            row = main_midrow.row()

            #Color
            sub = row.column(align=True)
            sub.ui_units_x = 3
            Color(self, context, layout=sub)

            #Vertex-Color
            sub = row.column(align=True)
            sub.ui_units_x = 6
            VertexColor(self, context, layout=sub)

            #Vertex-Group
            sub = row.column()
            sub.ui_units_x = 14
            sub.separator()

        #MAIN-RIGHT------------------------------------------------------------------------------
            row = main_rightrow.row()

        #PAINT_TEXTURE//////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
        if context.mode == 'PAINT_TEXTURE':
            brush = context.tool_settings.image_paint.brush

        #TOP-LEFT--------------------------------------------------------------------------------
            row = top_left.row(align=True)

            # BrushTexture-Ramp
            sub = row.column(align=True)
            sub.ui_units_x = 8
            sub.menu_contents("VIEW3D_MT_TextureMask")
            row.separator(factor=2)

            #Brush-Preset
            sub = row.column(align=True) 
            sub.ui_units_x = 5
            BrushCopy(self, context, layout=sub)

        #TOP-MID----------------------------------------------------------------------------------
            row = top_mid.row(align=True)

            #Blend
            sub = row.column(align=True)
            sub.ui_units_x = 4
            sub.prop(brush, "blend", text="")
            row.separator()

            #Tools
            tool_bt(layout=row, cmd=1, w=2, h=1.4, text=True, icon='LARGE')
            row.separator()
            tool_bt(layout=row, cmd=2, w=2, h=1.4, text=True, icon='LARGE')
            tool_bt(layout=row, cmd=3, w=2, h=1.4, text=True, icon='LARGE')
            tool_bt(layout=row, cmd=4, w=2, h=1.4, text=True, icon='LARGE')
            tool_bt(layout=row, cmd=5, w=2, h=1.4, text=True, icon='LARGE')
            tool_bt(layout=row, cmd=6, w=2, h=1.4, text=True, icon='LARGE')
            row.separator()

            #Falloff
            sub = row.column(align=True)
            sub.ui_units_x = 2
            sub.scale_y = 1.4
            sub.menu_contents("VIEW3D_MT_Falloff")
            row.separator()

            #Brush-Settings
            sub = row.column(align=True)
            sub.ui_units_x = 7
            TextureBrushSettings(self, context, layout=sub)
            row.separator()

            #Tool-Options
            sub = row.column(align=True)
            ToolOptions(self, context, layout=sub)

        #TOP-RIGHT-------------------------------------------------------------------------------
            row = top_right.row(align=True)

            #Smooth-Stroke
            sub = row.column(align=True)   
            sub.ui_units_x = 5
            SmoothStroke(self, context, layout=sub)

        #MAIN-LEFT-------------------------------------------------------------------------------
            row = main_leftrow.row(align=True)

            #Palette
            sub = row.column(align=True)
            sub.ui_units_x = 10
            ColorPalette(self, context, layout=sub)

            #Brush-Tex
            sub = row.column(align=True)
            sub.ui_units_x = 8
            sub.menu_contents("VIEW3D_MT_BrushTexture")
            row.separator(factor=2)

            #Stroke
            sub = row.column(align=True)   
            sub.ui_units_x = 5
            Stroke(self, context, layout=sub)

        #MAIN-MID-------------------------------------------------------------------------------
            row = main_midrow.row()

            #Color
            sub = row.column(align=True)
            sub.ui_units_x = 3
            Color(self, context, layout=sub)

            #Texture-Slots
            sub = row.column()
            sub.ui_units_x = 6
            TexSlots(self, context, layout=sub)

            #UV
            sub = row.column()
            sub.ui_units_x = 6
            UVTexture(self, context, layout=sub)

            #Vertex-Group:
            sub = row.column()
            sub.ui_units_x = 6
            VertexGroups(self, context, layout=sub)

        #MAIN-RIGHT------------------------------------------------------------------------------
            row = main_rightrow.row()

            #Material
            sub = row.column()
            sub.ui_units_x = 14
            sub.menu_contents("VIEW3D_MT_Material")

        #PAINT_WEIGHT//////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
        if context.mode == 'PAINT_WEIGHT':
            brush = context.tool_settings.vertex_paint.brush

        #TOP-LEFT--------------------------------------------------------------------------------
            row = top_left.row(align=True)

            # BrushTexture-Ramp
            sub = row.column(align=True)
            sub.ui_units_x = 8
            sub.menu_contents("VIEW3D_MT_TextureMask")
            row.separator(factor=2)

            #Brush-Preset
            sub = row.column(align=True) 
            sub.ui_units_x = 5
            BrushCopy(self, context, layout=sub)

        #TOP-MID---------------------------------------------------------------------------------
            row = top_mid.row(align=True)

            #Tools
            tool_bt(layout=row, cmd=1, w=2, h=1.4, text=True, icon='LARGE')
            row.separator()
            tool_bt(layout=row, cmd=2, w=2, h=1.4, text=True, icon='LARGE')
            tool_bt(layout=row, cmd=3, w=2, h=1.4, text=True, icon='LARGE')
            tool_bt(layout=row, cmd=4, w=2, h=1.4, text=True, icon='LARGE')
            tool_bt(layout=row, cmd=5, w=2, h=1.4, text=True, icon='LARGE')
            tool_bt(layout=row, cmd=6, w=2, h=1.4, text=True, icon='LARGE')
            tool_bt(layout=row, cmd=7, w=2, h=1.4, text=True, icon='LARGE')
            row.separator()

            #Falloff
            sub = row.column()
            sub.ui_units_x = 2
            sub.scale_y = 1.4
            sub.menu_contents("VIEW3D_MT_Falloff")
            row.separator()

            #Brush-Settings
            sub = row.row(align=True)
            sub.ui_units_x = 4
            sub.prop(brush, "use_frontface", text="FRONT", toggle=True)
            sub.prop(brush, "use_accumulate", text="ACCU", toggle=True)
            row.separator(factor=4)

            #Tool-Options
            sub = row.row(align=True)
            sub.ui_units_x = 10
            ts = context.tool_settings
            wp = ts.weight_paint
            sub.prop(ts, "use_auto_normalize", text="NORM", toggle=True)
            sub.prop(ts, "use_lock_relative", text="RELAT", toggle=True)
            sub.prop(ts, "use_multipaint", text="MPAINT", toggle=True)
            sub.prop(wp, "use_group_restrict", text="RESTR", toggle=True)

        #TOP-RIGHT-------------------------------------------------------------------------------
            row = top_right.row(align=True)

            #Smooth-Stroke
            sub = row.column(align=True)   
            sub.ui_units_x = 5
            SmoothStroke(self, context, layout=sub)

        #MAIN-LEFT-------------------------------------------------------------------------------
            row = main_leftrow.row(align=True)

            #Brush-Tex
            sub = row.column(align=True)
            sub.ui_units_x = 8
            sub.menu_contents("VIEW3D_MT_BrushTexture")
            row.separator(factor=2)

            #Stroke
            sub = row.column(align=True)   
            sub.ui_units_x = 5
            Stroke(self, context, layout=sub)


        #MAIN-MID-------------------------------------------------------------------------------
            row = main_midrow.row()

            #Vertex-Group
            sub = row.column()
            sub.ui_units_x = 14
            VertexGroups(self, context, layout=sub)
            InsertSpace(row, space=20)

        #MAIN-RIGHT------------------------------------------------------------------------------
            row = main_rightrow.row()

        #PAINT_GPENCIL//////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
        if context.mode == 'PAINT_GPENCIL':
            brush = context.tool_settings.gpencil_paint.brush
            gp_settings = brush.gpencil_settings

        #TOP-LEFT--------------------------------------------------------------------------------
            row = top_left.row()

            #Cleanup
            sub = row.column()
            sub.ui_units_x = 4
            sub.menu("GPENCIL_MT_cleanup")

            #Init
            sub = row.column()
            sub.ui_units_x = 4
            sub.operator("gpencil.blank_frame_add", text="INIT")

            #Brush-Preset
            sub = row.column(align=True) 
            sub.ui_units_x = 5
            BrushCopy(self, context, layout=sub)

        #TOP-MID--------------------------------------------------------------------------------
            row = top_mid.row(align=True)
            row.alignment = 'CENTER'
            row.separator()

            #Tools
            sub = row.column(align=True)
            tool_bt(layout=sub, cmd=1, w=2.4, h=0.7, text=False, icon='OFF')
            tool_bt(layout=sub, cmd=14, w=2.4, h=0.7, text=False, icon='OFF')
            sub = row.column(align=True)
            tool_bt(layout=sub, cmd=15, w=2.7, h=0.7, text=False, icon='OFF')
            tool_bt(layout=sub, cmd=16, w=2.7, h=0.7, text=False, icon='OFF')
            sub = row.column(align=True)
            tool_bt(layout=sub, cmd=17, w=2.7, h=0.7, text=False, icon='OFF')
            tool_bt(layout=sub, cmd=18, w=2.7, h=0.7, text=False, icon='OFF')
            sub = row.column(align=True)
            tool_bt(layout=sub, cmd=19, w=2.4, h=1.4, text=False, icon='OFF')
            row.separator()
            tool_bt(layout=row, cmd=2, w=2, h=1.4, text=True, icon='LARGE')
            tool_bt(layout=row, cmd=3, w=2, h=1.4, text=True, icon='LARGE')
            tool_bt(layout=row, cmd=4, w=2, h=1.4, text=True, icon='LARGE')
            tool_bt(layout=row, cmd=5, w=2, h=1.4, text=True, icon='LARGE')
            tool_bt(layout=row, cmd=6, w=2, h=1.4, text=True, icon='LARGE')
            row.separator()
            tool_bt(layout=row, cmd=7, w=1.4, h=1.4, text=False, icon='IPO_LINEAR')
            tool_bt(layout=row, cmd=8, w=1.4, h=1.4, text=False, icon='IPO_CONSTANT')
            tool_bt(layout=row, cmd=9, w=1.4, h=1.4, text=False, icon='IPO_EASE_OUT')
            tool_bt(layout=row, cmd=10, w=1.4, h=1.4, text=False, icon='IPO_EASE_IN_OUT')
            tool_bt(layout=row, cmd=11, w=1.4, h=1.4, text=False, icon='MESH_PLANE')
            tool_bt(layout=row, cmd=12, w=1.4, h=1.4, text=False, icon='MESH_CIRCLE')
            row.separator()

            #Smoothstroke
            GPSmoothStroke(self, context, layout=row)

        #TOP-RIGHT-------------------------------------------------------------------------------
            row = top_right.row(align=True)

            #Stroke-Post
            sub = row.column(align=True)
            sub.ui_units_x = 4
            sub.scale_y = 1
            sub.popover("VIEW3D_PT_tools_grease_pencil_brush_post_processing")

            #Stroke-Randomize
            sub = row.column(align=True)
            sub.ui_units_x = 4
            sub.scale_y = 1
            sub.popover("VIEW3D_PT_tools_grease_pencil_brush_random")

            #Stroke-Advanced
            sub = row.column(align=True)
            sub.ui_units_x = 4
            sub.scale_y = 1
            sub.popover("VIEW3D_PT_tools_grease_pencil_brush_advanced")

        #MAIN-LEFT-------------------------------------------------------------------------------
            row = main_leftrow.row()

            #Color-Palette 
            sub = row.column(align=True)
            sub.ui_units_x = 10
            ColorPalette(self, context, layout=sub)


        #MAIN-MID-------------------------------------------------------------------------------
            row = main_midrow.row()

            #Layer
            sub = row.column()
            GPLayersWide(self, context, layout=sub) 
            row.separator(factor=4)

            #Material
            sub = row.column()
            sub.ui_units_x = 8
            sub.menu_contents("VIEW3D_MT_GPMaterial")

        #MAIN-RIGHT------------------------------------------------------------------------------
            row = main_rightrow.row()

            #Mat-Stroke 
            sub = row.column()
            sub.ui_units_x = 6
            sub.menu_contents("VIEW3D_MT_GPStroke")

            #Mat-Fill
            sub = row.column()
            sub.ui_units_x = 6
            sub.menu_contents("VIEW3D_MT_GPFill")

            #Mat-Menu
            sub = row.column()
            sub.ui_units_x = 6
            sub.menu("GPENCIL_MT_material_context_menu")

        #EDIT_GPENCIL//////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
        if context.mode == 'EDIT_GPENCIL':
            brush = context.tool_settings.gpencil_paint.brush

        #TOP-LEFT--------------------------------------------------------------------------------
            row = top_left.row(align=True)

            #Resample
            sub = row.column(align=True)
            sub.ui_units_x = 3.2
            sub.scale_y = 0.7
            sub.operator("gpencil.stroke_simplify", text="SIMPL")
            sub.operator("gpencil.stroke_sample", text="RESAMP")

            #Subdivide/Smooth
            sub = row.column(align=True)
            sub.ui_units_x = 3.2
            sub.scale_y = 0.7
            sub.operator("gpencil.stroke_subdivide", text="SUBDIV").only_selected=True
            sub.operator("gpencil.stroke_smooth", text="SMTH").only_selected=True
            row.separator(factor=2)

            # Close/Trim
            sub = row.column(align=True)
            sub.ui_units_x = 2.4
            sub.scale_y = 0.7
            op = sub.operator("gpencil.stroke_cyclical_set", text="CLOSE")
            op.type='CLOSE'
            op.geometry=True
            sub.operator("gpencil.stroke_trim", text="TRIM")

            # Merge/Join
            sub = row.column(align=True)
            sub.ui_units_x = 2.4
            sub.scale_y = 0.7
            sub.operator("gpencil.stroke_merge", text="MERGE")
            sub.operator("gpencil.stroke_join", text="JOIN")

        #TOP-MID-------------------------------------------------------------------------------
            row = top_mid.row(align=True)
            row.alignment = 'CENTER'

            #Tools
            tool_bt(layout=row, cmd=6, w=1.4, h=1, text=False, icon='CUSTOM')
            tool_bt(layout=row, cmd=7, w=1.4, h=1, text=False, icon='CUSTOM')
            tool_bt(layout=row, cmd=8, w=1.4, h=1, text=False, icon='CUSTOM')
            tool_bt(layout=row, cmd=9, w=1.4, h=1, text=False, icon='CUSTOM')
            row.separator(factor = 2)
            tool_bt(layout=row, cmd=1, w=1.4, h=1, text=False, icon='CUSTOM')
            tool_bt(layout=row, cmd=2, w=1.4, h=1, text=False, icon='CUSTOM')
            tool_bt(layout=row, cmd=3, w=1.4, h=1, text=False, icon='CUSTOM')
            tool_bt(layout=row, cmd=4, w=1.4, h=1, text=False, icon='CUSTOM')
            tool_bt(layout=row, cmd=5, w=1.4, h=1, text=False, icon='CUSTOM')
            row.separator(factor = 2)

            #Tool-Settings
            col = row.column()
            col.ui_units_x = 5
            GPToolSettings(self, context, layout=col)
            row.separator(factor = 2)

            #Functions
            col = row.column(align=True)
            tool_bt(layout=col, cmd=10, w=2, h=0.7, text=False, icon='OFF')
            tool_bt(layout=col, cmd=11, w=2, h=0.7, text=False, icon='OFF')
            col = row.column(align=True)
            tool_bt(layout=col, cmd=12, w=2, h=0.7, text=False, icon='OFF')
            tool_bt(layout=col, cmd=13, w=2, h=0.7, text=False, icon='OFF')
            col = row.column(align=True)
            tool_bt(layout=col, cmd=14, w=2, h=0.7, text=False, icon='OFF')
            col = row.column(align=True)
            tool_bt(layout=col, cmd=15, w=2, h=0.7, text=False, icon='OFF')
            tool_bt(layout=col, cmd=16, w=2, h=0.7, text=False, icon='OFF')

        #TOP-RIGHT-----------------------------------------------------------------------------

            row = top_right.row(align=True)

            InsertSpace(row, space=1)



        #SCULPT_GPENCIL//////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
        if context.mode == 'SCULPT_GPENCIL':
            brush = context.tool_settings.gpencil_paint.brush

        #TOP-LEFT------------------------------------------------------------------------------
            row = top_left.row(align=True)

            #Brush-Preset
            sub = row.column()
            col.ui_units_x = 4
            BrushCopy(self, context, layout=sub)

        #TOP-MID-------------------------------------------------------------------------------
            row = top_mid.row(align=True)

            #Tools
            tool_bt(layout=row, cmd=5, w=2.2, h=1.4, text=False, icon='LARGE')
            tool_bt(layout=row, cmd=6, w=2.2, h=1.4, text=False, icon='LARGE')
            tool_bt(layout=row, cmd=7, w=2.2, h=1.4, text=False, icon='LARGE')
            tool_bt(layout=row, cmd=8, w=2.2, h=1.4, text=False, icon='LARGE')
            tool_bt(layout=row, cmd=9, w=2.2, h=1.4, text=False, icon='LARGE')
            row.separator(factor=1)
            tool_bt(layout=row, cmd=2, w=2.8, h=1, text=False, icon='OFF')
            tool_bt(layout=row, cmd=3, w=2.8, h=1, text=False, icon='OFF')
            tool_bt(layout=row, cmd=1, w=2.8, h=1, text=False, icon='OFF')
            tool_bt(layout=row, cmd=4, w=2.8, h=1, text=False, icon='OFF')
            row.separator(factor=1)

            #Falloff
            sub = row.column()
            sub.ui_units_x = 2
            sub.scale_y = 1.4
            sub.menu_contents("VIEW3D_MT_Falloff")
            row.separator(factor=1)

            #Tool-Settings
            sub = row.column()
            sub.ui_units_x = 6
            GPSculptToolSettings(self, context, layout=sub)

        #TOP-RIGHT-------------------------------------------------------------------------------
            row = top_right.row(align=True)

            InsertSpace(row, space=1)
            '''
            elif tool_mode == 'WEIGHT_GPENCIL':
                col.popover("VIEW3D_PT_tools_grease_pencil_weight_appearance")
            elif tool_mode == 'VERTEX_GPENCIL':
                col.popover("VIEW3D_PT_tools_grease_pencil_vertex_appearance")
            bpy.data.scenes["Scene"].tool_settings.use_gpencil_select_mask_stroke
            bpy.data.scenes["Scene"].tool_settings.use_gpencil_select_mask_point
            '''

        # WEIGHT_GPENCIL //////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
        if context.mode == 'WEIGHT_GPENCIL':
            brush = context.tool_settings.vertex_paint.brush

        #TOP-LEFT--------------------------------------------------------------------------------
            row = top_left.row(align=True)

            InsertSpace(row, space=1)

        #TOP-MID---------------------------------------------------------------------------------
            row = top_mid.row(align=True)

            #Tools
            tool_bt(layout=row, cmd=1, w=2.2, h=1.4, text=False, icon='LARGE')

        #TOP-RIGHT-------------------------------------------------------------------------------
            row = top_right.row(align=True)

            InsertSpace(row, space=1)


        # EDIT_CURVE //////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
        if context.mode == 'EDIT_CURVE':
            main_midrow.alignment = 'LEFT'

        #TOP-LEFT--------------------------------------------------------------------------------
            row = top_left.row(align=True)

            #Toolset
            tool_bt(layout=row, cmd=6, w=1.2, h=1, text=False, icon='CUSTOM')
            tool_bt(layout=row, cmd=7, w=1.2, h=1, text=False, icon='CUSTOM')
            tool_bt(layout=row, cmd=8, w=1.2, h=1, text=False, icon='CUSTOM')
            tool_bt(layout=row, cmd=9, w=1.2, h=1, text=False, icon='CUSTOM')
            row.separator(factor = 2)
            tool_bt(layout=row, cmd=1, w=1.2, h=1, text=False, icon='CUSTOM')
            tool_bt(layout=row, cmd=2, w=1.2, h=1, text=False, icon='CUSTOM')
            tool_bt(layout=row, cmd=3, w=1.2, h=1, text=False, icon='CUSTOM')
            tool_bt(layout=row, cmd=4, w=1.2, h=1, text=False, icon='CUSTOM')
            tool_bt(layout=row, cmd=5, w=1.2, h=1, text=False, icon='CUSTOM')


        redraw_regions()

#-----------------------------------------------------------------------------------------------------------------------

def register() :
    bpy.utils.register_class(XPanel)

def unregister() :
    bpy.utils.unregister_class(XPanel)
