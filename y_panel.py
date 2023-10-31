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

class YPanel(bpy.types.Panel):
    bl_idname = "SCENE_PT_ypanel"
    bl_label = "Y-PANEL"
    bl_space_type = "PROPERTIES"
    bl_region_type = "WINDOW"
    bl_context = "scene"
    bl_order = 2000
    bl_options = {'HIDE_HEADER', 'HEADER_LAYOUT_EXPAND'}

    def draw(self, context):
        layout = self.layout
        ob = context.active_object
        ts = context.tool_settings
        gpd = context.gpencil_data

        # LAYOUT-STRUCTURE -----------------------------------------------------------------------------------------

        main = layout.column(align=True)
        main.alignment = 'CENTER'
        main.ui_units_y = 30

        end = layout.row()
        end.ui_units_x = 0.2
        end.ui_units_y = 3
        end.label(text="")

        # OBJECT /////////////////////////////////////////////////////////////////////////////////////////////
        if context.mode == 'OBJECT':
            row = main.row(align=True)

            # Tools
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
            main.separator(factor=2)

        #--------------------------------------------------------------------------------
            # Tool-Options
            row = main.row(align=True)
            InsertSpace(row, space=2)
            sub = row.column(align=True)
            subsub = sub.row(align=True)
            subsub.scale_y = 0.9
            ToolOptions(self, context, layout=subsub)
            sub.separator(factor = 0.5)

            # Transform-Matrix
            Transforms(self, context, layout=sub)
            sub.separator(factor = 0.5)

            # Pivot
            Pivot(self, context, layout=sub)
            InsertSpace(row, space=2)
            main.separator(factor=2)

        #--------------------------------------------------------------------------------
            # Add-Object
            row = main.row(align=True)
            split = row.split(factor=0.29)
            split.menu("VIEW3D_MT_add", text="OBJECT", text_ctxt=i18n_contexts.operator_default)
            sub = split.row(align=True)
            sub.scale_x = 1.4
            sub.operator('mesh.primitive_plane_add', text="", icon='MESH_PLANE')
            sub.operator('mesh.primitive_cube_add', text="", icon='MESH_CUBE')
            sub.operator('mesh.primitive_uv_sphere_add', text="", icon='MESH_UVSPHERE')
            sub.operator('mesh.primitive_cylinder_add', text="", icon='MESH_CYLINDER')
            sub.operator('object.empty_add', text="", icon='EMPTY_DATA')
            sub.operator('object.gpencil_add', text="", icon='GREASEPENCIL')
            main.separator(factor=1)

            row = main.row(align=True)

        #--------------------------------------------------------------------------------

            # Modifiers
            row = main.row(align=True)

            if ob != None:
                if ob.type == 'MESH':
                    sub = row.row(align=True)
                    sub.operator('btool.boolean_union', text="", icon='SELECT_EXTEND')
                    sub.operator('btool.boolean_diff', text="", icon='SELECT_SUBTRACT')
                    sub.operator('btool.boolean_inters', text="", icon='SELECT_INTERSECT')
                    sub.operator('btool.boolean_slice', text="", icon='SELECT_DIFFERENCE')

            else:
                sub = row.column(align=True)
                sub.ui_units_x = 1.2
                sub.label(text=">")
            row.separator(factor=1)
            # Convert
            row.operator('object.convert', text="CONV", ) #icon='SHADERFX'
            row.separator(factor=1)

            # Merge/Dub
            row.operator('object.join', text='MRG')
            row.operator('object.duplicate_move', text='DUB')

            row.separator(factor=1)

            if ob != None:
                if ob.type == 'MESH':
                    sub = row.column(align=True)
                    sub.ui_units_x = 1.2
                    sub.operator('object.modifier_add', text='', icon='MOD_ARRAY').type='ARRAY'
                else:
                    sub = row.column(align=True)
                    sub.ui_units_x = 1.2
                    sub.label(text="")

            main.separator(factor=1)

        #--------------------------------------------------------------------------------
            # Modifiers
            row = main.row()
            col = row.column(align=True)
            col.ui_units_x = 9
            #sub = col.row(align=True)
            #sub.operator_menu_enum("object.modifier_add", "type", text='MODIFIER')
            sub = col.row(align=True)
            #sub.operator("object.modifier_add", text="BVL", icon="NONE").type='BEVEL'
            #sub.operator("object.modifier_add", text="SLD", icon="NONE").type='SOLIDIFY'
            #sub.operator("object.modifier_add", text="SUBD", icon="NONE").type='SUBSURF'
            sub = col.row(align=True)
            #sub.operator("object.modifier_add", text="SYM", icon="NONE").type='MIRROR'
            #sub.operator("object.modifier_add", text="RMSH", icon="NONE").type='REMESH'
            #sub.operator("object.modifier_add", text="DEC", icon="NONE").type='DECIMATE'

            # MOD-Window
            sub = col.row(align=True)
            ModifierWindow(self, context, layout=sub)

            col = row.column(align=True)
            #Material
            #col.ui_units_x = 14
            col.menu_contents("VIEW3D_MT_Material2")

            main.separator(factor=1)
        #--------------------------------------------------------------------------------
            # CMD
            row = main.row(align=True)
            row.scale_y = 0.7 
            InsertSpace(row, space=12)
            row.operator("screen.redo_last", text=">")

            #row.popover("VIEW3D_PT_ml_modifiers", text='', icon="NONE")
            #bpy.types.VIEW3D_PT_ml_modifiers


        #EDIT//////////////////////////////////////////////////////////////////////////////////////////////////////
        if context.mode == 'EDIT_MESH':
        #--------------------------------------------------------------------------------
            row = main.row(align=True)

            col = row.column(align=True)
            # Component Mode
            sub = col.row(align=True)
            sub.scale_x = 2
            sub.template_edit_mode_selection()

            # X-Ray
            sub = col.row(align=True)
            funct_bt(layout=sub, cmd='xray', tog=True, w=2.4, h=1, label='', icon="XRAY")

            # Automerge
            subsub = sub.row(align=True)
            subsub.scale_x = 1.5
            ts = context.tool_settings
            subsub.prop(ts, "use_mesh_automerge", text="", toggle=True)

            row.separator(factor=1)

            col = row.column(align=True)
            col.scale_x = 2

            #Selection
            sub = col.row(align=True)
            sub.ui_units_x = 1.7
            sub.operator('mesh.select_all',text='',icon='SHADING_SOLID').action='SELECT'
            sub.operator('mesh.select_all',text='', icon='IMAGE_ALPHA').action='INVERT'

            sub = col.row(align=True)
            sub.ui_units_x = 1.7
            sub.operator('mesh.select_less', icon='REMOVE', text='')
            sub.operator('mesh.select_more', icon='ADD',text='')


            row.separator(factor=1.5)

            col = row.column(align=True)
            col.ui_units_x = 5
            sub = col.row(align=True)
            sub.operator('mesh.select_non_manifold',text='BND')
            sub.operator('mesh.select_linked',text='LINK')
            sub.operator('mesh.shortest_path_select',text='PATH')
            sub = col.row(align=True)
            sub.operator('mesh.faces_select_linked_flat',text='FLAT')
            sub.operator('mesh.select_mirror',text='MIR')
            sub.operator('mesh.select_face_by_sides',text='CNT')
            main.separator(factor=1)

        #--------------------------------------------------------------------------------
            row = main.row(align=True)
            # Transform / Selection
            tool_bt(layout=row, cmd=6, w=1.4, h=1, text=False, icon='CUSTOM')
            tool_bt(layout=row, cmd=7, w=1.4, h=1, text=False, icon='CUSTOM')
            tool_bt(layout=row, cmd=8, w=1.4, h=1, text=False, icon='CUSTOM')
            tool_bt(layout=row, cmd=9, w=1.4, h=1, text=False, icon='CUSTOM')
            row.separator(factor = 1)
            tool_bt(layout=row, cmd=1, w=1.4, h=1, text=False, icon='CUSTOM')
            tool_bt(layout=row, cmd=2, w=1.4, h=1, text=False, icon='CUSTOM')
            tool_bt(layout=row, cmd=3, w=1.4, h=1, text=False, icon='CUSTOM')
            tool_bt(layout=row, cmd=4, w=1.4, h=1, text=False, icon='CUSTOM')
            tool_bt(layout=row, cmd=5, w=1.4, h=1, text=False, icon='CUSTOM')
            #row.separator(factor = 1)
            row.operator_menu_enum("mesh.select_similar", "type", text="SIM")
            row.operator_menu_enum("mesh.select_linked", "delimit", text="LINK")

            main.separator(factor=1.5)

        #--------------------------------------------------------------------------------
            row = main.row(align=True)

            # Edge-Tools
            col = row.column(align=True)
            col.ui_units_x = 2.5

            sub = col.row(align=True)
            op = sub.operator('mesh.mark_seam', text='SEAM',icon='NONE')
            op = sub.operator('mesh.mark_seam', text='',icon='RADIOBUT_OFF')
            op.clear = True
            sub = col.row(align=True)
            op = sub.operator('mesh.mark_sharp', text='SHRP',icon='NONE')
            op = sub.operator('mesh.mark_sharp', text='',icon='RADIOBUT_OFF')
            op.clear = True
            sub = col.row(align=True)
            sub.operator('transform.edge_bevelweight', text='Bevel')
            sub = col.row(align=True)
            sub.operator('transform.edge_crease', text='Crease')

            row.separator(factor=1.5)

            # Operators
            col = row.column(align=True)
            col.ui_units_x = 2
            col.operator('mesh.edge_face_add', text='FILL')
            col.operator('mesh.merge', text="MERGE").type='CENTER'
            col.operator('mesh.split', text='SPLIT', icon='NONE')
            col.operator('mesh.duplicate_move', text='DUB', icon='NONE')
            op = col.operator('transform.mirror', text='MIR')
            op.orient_type='GLOBAL'
            op.constraint_axis=(True, False, False)

            row.separator(factor=1.5)

            # Operators
            col = row.column(align=True)
            col.ui_units_x = 5

            # UV
            sub = col.column(align=True)
            UVTexture(self, context, layout=sub)
            sub = col.row(align=True)
            sub.operator('uv.smart_project', text="A-UV")
            sub.operator('uv.unwrap', text="UNWRP")

            row.separator(factor=2)

            # Clean
            col = row.column(align=True)
            col.ui_units_x = 2
            col.operator('mesh.flip_normals', text='FLIP')
            col.operator('mesh.fill_holes', text='FILL-H')
            col.operator('mesh.delete_loose', text='LOOSE')
            col.operator('mesh.remove_doubles', text='CLEAN')
            col.operator('mesh.symmetrize', text='SYM')
            main.separator(factor=1)

        #--------------------------------------------------------------------------------
            row = main.row(align=True)

            col = row.column(align=True)
            tool_bt(layout=col, cmd=21, w=2, h=1, text=False, icon='OFF')
            tool_bt(layout=col, cmd=23, w=2, h=1, text=False, icon='OFF')
            sub = col.row(align=True)
            tool_bt(layout=sub, cmd=16, w=1.2, h=1, text=False, icon='OFF')
            tool_bt(layout=sub, cmd=17, w=0.8, h=1, text=False, icon='OFF')

            tool_bt(layout=col, cmd=20, w=2, h=1, text=False, icon='OFF')
            tool_bt(layout=col, cmd=19, w=2, h=1, text=False, icon='OFF')

            row.separator(factor=1.5)

            col = row.column(align=True)
            tool_bt(layout=col, cmd=25, w=1.5, h=1, text=False, icon='OFF')

            sub = col.row(align=True)
            tool_bt(layout=sub, cmd=31, w=0.9, h=1, text=False, icon='OFF')
            tool_bt(layout=sub, cmd=30, w=0.7, h=1, text=False,icon='OFF')

            tool_bt(layout=col, cmd=32, w=1.5, h=1, text=False, icon='OFF')
            tool_bt(layout=col, cmd=33, w=1.5, h=1, text=False, icon='OFF')
            tool_bt(layout=col, cmd=35, w=1.5, h=1, text=False, icon='OFF')

            row.separator(factor=1.5)

            col = row.column(align=True)
            col.ui_units_x = 6
            #Vertex-Group
            VertexGroups(self, context, layout=col)

            main.separator(factor=1.5) 
        #--------------------------------------------------------------------------------
            # Add-Mesh
            row = main.row(align=True)
            sub = row.row(align=True)
            sub.ui_units_x = 1.2
            sub.menu("VIEW3D_MT_mesh_add", icon='NONE', text='ADD')
            sub = row.row(align=True)
            #sub.ui_units_x = 10
            sub.operator('mesh.primitive_plane_add', text="", icon='MESH_PLANE')
            sub.operator('mesh.primitive_cube_add', text="", icon='MESH_CUBE')
            sub.operator('mesh.primitive_uv_sphere_add', text="", icon='MESH_UVSPHERE')
            sub.operator('mesh.primitive_cylinder_add', text="", icon='MESH_CYLINDER')
            row.separator(factor=1.5) 
            # Separate-Mesh:
            sub = row.row(align=True)
            sub.ui_units_x = 1.2
            op = sub.operator('mesh.separate', text='SEPARATE', icon='NONE')
            op.type='SELECTED'
            sub = row.row(align=True)
            sub.ui_units_x = 1.8
            op = sub.operator('mesh.separate', text='MAT', icon='NONE')
            op.type='MATERIAL'
            op = sub.operator('mesh.separate', text='PARTS', icon='NONE')
            op.type='LOOSE'

            main.separator(factor=1) 

        #--------------------------------------------------------------------------------
            # Modifiers
            row = main.row()
            col = row.column(align=True)
            col.ui_units_x = 9
            #sub = col.row(align=True)
            #sub.operator_menu_enum("object.modifier_add", "type", text='MODIFIER')
            sub = col.row(align=True)
            sub.operator("object.modifier_add", text="BVL", icon="NONE").type='BEVEL'
            sub.operator("object.modifier_add", text="SLD", icon="NONE").type='SOLIDIFY'
            sub.operator("object.modifier_add", text="SUBD", icon="NONE").type='SUBSURF'
            sub = col.row(align=True)
            sub.operator("object.modifier_add", text="SYM", icon="NONE").type='MIRROR'
            sub.operator("object.modifier_add", text="RMSH", icon="NONE").type='REMESH'
            sub.operator("object.modifier_add", text="DEC", icon="NONE").type='DECIMATE'

            # MOD-Window
            sub = col.row(align=True)
            #ModifierWindow(self, context, layout=sub)

            col = row.column(align=True)
            #Material
            #col.ui_units_x = 14
            col.menu_contents("VIEW3D_MT_Material2")

            main.separator(factor=1)

        #--------------------------------------------------------------------------------
            # CMD
            row = main.row(align=True)
            row.scale_y=0.8
            row.label(text='')
            row.label(text='')
            row.operator("screen.redo_last", text="CMD >")

    #SCULPT//////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
        if context.mode == 'SCULPT':
            tool = context.workspace.tools.from_space_view3d_mode(bpy.context.mode).idname
            brush = context.tool_settings.image_paint.brush


        #--------------------------------------------------------------------------------
            row = main.row(align=True)

            #Mask
            SculptMask(self, context, layout=row)
            row.separator(factor=1.5)

            #Face-Set-Init
            col = row.column(align=True)
            col.ui_units_x = 20
            sub = col.row(align=True)
            sub.scale_y = 0.7
            sub.popover("OBJECT_PT_Fset_panel", text='F-SET INIT', icon="NONE")
            sub = col.row(align=True)
            sub.scale_y = 0.7
            sub.operator("sculpt.face_sets_create", text='VIS').mode = 'VISIBLE'
            sub.operator("sculpt.face_sets_create", text='MASK').mode = 'MASKED'

            main.separator(factor=1)


        #--------------------------------------------------------------------------------
            row = main.row(align=True)

            #Mask
            col = row.column()
            sub = col.row(align=True)
            tool_bt(layout=sub, cmd=14, w=2, h=1.4, text=False, icon='LARGE') 

            subsub = sub.column()
            subsub.ui_units_x = 3.4
            label = subsub.column()
            label.scale_y = 0.5
            label.label(text="MASK")
            item = subsub.row(align=True)
            tool_bt(layout=item, cmd=28, w=1.2, h=0.8, text=False, icon='CUSTOM')
            tool_bt(layout=item, cmd=29, w=1, h=0.8, text=False, icon='CUSTOM')
            tool_bt(layout=item, cmd=30, w=1.2, h=0.8, text=False, icon='CUSTOM')

            #Trim
            subsub = sub.column()
            subsub.ui_units_x = 2.4
            label = subsub.column()
            label.scale_y = 0.5
            label.label(text="TRIM")
            item = subsub.row(align=True)
            tool_bt(layout=item, cmd=17, w=1.2, h=0.8, icon="CUSTOM", text=False)
            tool_bt(layout=item, cmd=18, w=1.2, h=0.8, icon="CUSTOM", text=False)

            sub.separator(factor = 1)

            #Face-Set
            tool_bt(layout=sub, cmd=15, w=2, h=1.4, text=False, icon='LARGE')
            subsub = sub.column()
            item = subsub.row(align=True)
            tool_bt(layout=item, cmd=31, w=1.5, h=0.75, text=False, icon='CUSTOM')
            tool_bt(layout=item, cmd=32, w=1.5, h=0.75, text=False, icon='CUSTOM')
            tool_bt(layout=subsub, cmd=33, w=1.2, h=0.5, text=False, icon='OFF')

            #Hide
            subsub = sub.column()
            subsub.ui_units_x = 2.4
            tool_bt(layout=subsub, cmd=16, w=2.4, h=1.4, text=False, icon='LARGE')
        #--------------------------------------------------------------------------------
            row = main.row(align=True)

            sub = row.row(align=True)
            sub.ui_units_x = 2
            BrushCopy(self, context, layout=row)

            #Tool-Settings
            sub = row.column(align=True)
            sub.ui_units_x = 5
            SculptToolSettings(self, context, layout=sub)

            row.separator(factor=1)

            sub = row.row(align=True)

            sub = row.row(align=True)
            sub.ui_units_x = 2.7
            sub.label(text="")

            sub = row.row(align=True)
            sub.scale_y = 1.4
            sub.menu_contents("VIEW3D_MT_Falloff")

            main.separator(factor=0.4)
        #--------------------------------------------------------------------------------

            row = main.row(align=True)
            row.scale_y = 1.2
            SculptBrushSettings(self, context, layout=row)

            main.separator(factor=1)

        #--------------------------------------------------------------------------------
            row = main.row(align=True)
            split = row.split(factor=0.6)
        #-----------------
            col = split.column(align=True)

            # Pivot
            sub = col.row(align=True)
            subsub = sub.column(align=True)
            subsub.ui_units_x = 2
            subsub.scale_y = 0.7
            subsub.operator('sculpt.set_pivot_position', text='PVT M').mode='UNMASKED'
            subsub.operator('sculpt.set_pivot_position', text='RESET').mode='ORIGIN'
            tool_bt(layout=sub, cmd=19, w=2, h=1.4, text=False, icon='LARGE')

            # Grab
            tool_bt(layout=sub, cmd=1, w=2, h=1.4, text=True, icon='LARGE')
            tool_bt(layout=sub, cmd=20, w=1.2, h=1.4, text=False, icon='CUSTOM')
            tool_bt(layout=sub, cmd=22, w=1.2, h=1.4, text=False, icon='CUSTOM')

            col.separator(factor = 0.4)
            sub = col.row(align=True)
            subsub = sub.row(align=True)
            tool_bt(layout=subsub, cmd=2, w=1, h=1.4, text=True, icon='LARGE')
            tool_bt(layout=subsub, cmd=3, w=1, h=1.4, text=True, icon='LARGE')
            tool_bt(layout=subsub, cmd=4, w=1, h=1.4, text=True, icon='LARGE')
            subsub.separator(factor = 1)
            tool_bt(layout=subsub, cmd=8, w=1, h=1.4, text=True, icon='LARGE')

            sub = col.row(align=True)
            subsub = sub.row(align=True)
            tool_bt(layout=subsub, cmd=5, w=1, h=1.4, text=True, icon='LARGE')
            tool_bt(layout=subsub, cmd=6, w=1, h=1.4, text=True, icon='LARGE')
            tool_bt(layout=subsub, cmd=7, w=1, h=1.4, text=True, icon='LARGE')
            subsub.separator(factor = 1)
            tool_bt(layout=subsub, cmd=9, w=1, h=1.4, text=True, icon='LARGE')

            sub = col.row(align=True)
            row.separator(factor = 1)
            subsub = sub.row(align=True)
            tool_bt(layout=subsub, cmd=10, w=1, h=1.4, text=True, icon='LARGE')
            tool_bt(layout=subsub, cmd=11, w=1, h=1.4, text=True, icon='LARGE')
            tool_bt(layout=subsub, cmd=12, w=1, h=1.4, text=True, icon='LARGE')
            subsub.separator(factor = 1)
            tool_bt(layout=subsub, cmd=13, w=1, h=1.4, text=True, icon='LARGE')
            col.separator(factor = 0.4)


            sub = col.row(align=True)
            subsplit = sub.split(factor=0.6)
            #Extra
            subsub = subsplit.row(align=True)
            tool_bt(layout=subsub, cmd=21, w=0.7, h=1, text=False, icon='CUSTOM')
            tool_bt(layout=subsub, cmd=26, w=0.7, h=1, text=False, icon='CUSTOM')
            tool_bt(layout=subsub, cmd=27, w=1.2, h=1, text=False, icon='CUSTOM')

            subsub = subsplit.row(align=True)
            subsubsplit = subsub.split(factor=0.6, align=True)
            subsubsplit.prop(brush, "use_automasking_face_sets", text="F-SET", toggle=True)
            subsubsplit.prop(brush, "use_automasking_boundary_face_sets", text="BND", toggle=True)

            sub = col.row(align=True)
            brush = ts.sculpt.brush
            subsplit = sub.split(factor=0.6)
            subsub = subsplit.row(align=True)
            subsub.prop(brush, "use_automasking_topology", text="TOPO", toggle=True)
            subsub.prop(brush, "use_frontface", text="FRNT", toggle=True)
            subsub.prop(brush, "use_automasking_boundary_edges", text="BND", toggle=True)

            subsplit.prop(brush, "automasking_boundary_edges_propagation_steps", text="",)
        #-----------------
            col = split.column(align=True)
            col.ui_units_x = 5
            sub = col.row(align=True)
            tool_bt(layout=sub, cmd=37, w=1.2, h=1.4, text=True, icon='LARGE')
            tool_bt(layout=sub, cmd=38, w=1.2, h=1.4, text=True, icon='LARGE')
            sub = col.row(align=True)
            sub.ui_units_x = 4
            Color(self, context, layout=sub)
            sub = col.row(align=True)
            sub.ui_units_x = 4
            ColorPalette(self, context, layout=sub)

            main.separator(factor =1)


        #--------------------------------------------------------------------------------
            row = main.row(align=True)

            split = row.split(factor=0.6)

            col = split.column(align=True)
            col.ui_units_x = 5
            col.menu_contents("VIEW3D_MT_TextureMask")
            col.menu_contents("VIEW3D_MT_BrushTexture")

            col = split.column(align=True)
            sub = col.column(align=True)
            sub.ui_units_x = 6
            SmoothStroke(self, context, layout=sub)
            Stroke(self, context, layout=sub)


            main.separator(factor = 1)
        #--------------------------------------------------------------------------------

            row = main.row(align=True)

            #Dyntopo
            row.menu_contents("VIEW3D_MT_dynamesh")
            row.separator(factor = 1.5)
            #Remesh
            row.menu_contents("VIEW3D_MT_remesh")
            row.separator(factor = 1.5)
            #Meshfilter
            sub = row.column(align=True)
            #sub.ui_units_x = 8
            subsub = sub.row(align=True)
            tool_bt(layout=subsub, cmd=34, w=2.5, h=1, text=False, icon='OFF')
            tool_bt(layout=subsub, cmd=35, w=2.5, h=1, text=False, icon='OFF')
            tool_bt(layout=subsub, cmd=36, w=2.5, h=1, text=False, icon='OFF')
            subsub = sub.row(align=True)
            SculptFilterSettings(self, context, layout=subsub)

    #PAINT TEXTURE//////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

        if context.mode == 'PAINT_TEXTURE':
            brush = context.tool_settings.image_paint.brush

            row = main.row(align=True)
            sub = row.column()
            sub.scale_y = 1.4
            sub.ui_units_x = 2
            sub.prop(brush, "blend", text="")
            BrushCopy(self, context, layout=row)
            tool_bt(layout=row, cmd=1, w=4, h=1.4, text=False, icon='LARGE')
            sub = row.column()
            sub.scale_y = 1.4
            sub.ui_units_x = 2
            sub.menu_contents("VIEW3D_MT_Falloff")
            main.separator(factor = 1)

            row = main.row(align=True)
            tool_bt(layout=row, cmd=2, w=2, h=1.4, text=False, icon='LARGE')
            tool_bt(layout=row, cmd=3, w=2, h=1.4, text=False, icon='LARGE')
            tool_bt(layout=row, cmd=4, w=2, h=1.4, text=False, icon='LARGE')
            tool_bt(layout=row, cmd=5, w=2, h=1.4, text=False, icon='LARGE')
            tool_bt(layout=row, cmd=6, w=2, h=1.4, text=False, icon='LARGE')

            main.separator(factor = 1)

            row = main.row(align=True)
            sub = row.column()
            sub.scale_y = 1.4
            sub.ui_units_x = 8
            TextureBrushSettings(self, context, layout=sub)
            ToolOptions(self, context, layout=row)

            main.separator(factor = 1)

            row = main.row()
            #Texture-Slots
            sub = row.column()
            sub.ui_units_x = 12
            TexSlots(self, context, layout=sub)
            Color(self, context, layout=row) 
            main.separator(factor = 1)

            row = main.row(align=True)
            split = row.split(factor=0.6)

            col = split.column(align=True)
            col.ui_units_x = 5
            col.menu_contents("VIEW3D_MT_TextureMask")
            col.menu_contents("VIEW3D_MT_BrushTexture")

            col = split.column(align=True)
            sub = col.column(align=True)
            sub.ui_units_x = 6
            SmoothStroke(self, context, layout=sub)
            Stroke(self, context, layout=sub)
            main.separator(factor = 1)

            row = main.row(align=True)
            #Material
            sub = row.column()
            sub.ui_units_x = 14
            sub.menu_contents("VIEW3D_MT_Material")

            #UV
            sub = row.column()
            sub.ui_units_x = 6
            UVTexture(self, context, layout=sub)

            main.separator(factor = 1)

            row = main.row(align=True)
            ColorPalette(self, context, layout=row)


    #PAINT VERTEX//////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

        if context.mode == 'PAINT_VERTEX':

            brush = context.tool_settings.vertex_paint.brush

            row = main.row(align=True)
            sub = row.column()
            sub.scale_y = 1.4
            sub.ui_units_x = 2
            sub.prop(brush, "blend", text="")
            BrushCopy(self, context, layout=row)
            tool_bt(layout=row, cmd=1, w=4, h=1.4, text=False, icon='LARGE')
            sub = row.column()
            sub.scale_y = 1.4
            sub.ui_units_x = 2
            sub.menu_contents("VIEW3D_MT_Falloff")
            main.separator(factor = 1)

            row = main.row(align=True)
            tool_bt(layout=row, cmd=2, w=2, h=1.4, text=False, icon='LARGE')
            tool_bt(layout=row, cmd=3, w=2, h=1.4, text=False, icon='LARGE')
            tool_bt(layout=row, cmd=4, w=2, h=1.4, text=False, icon='LARGE')
            main.separator(factor = 1)

            row = main.row(align=True)
            sub = row.column()
            sub.scale_y = 1
            sub.ui_units_x = 8
            VertexBrushSettings(self, context, layout=sub)
            main.separator(factor = 1)

            row = main.row()
            #Vertex-Color
            sub = row.column(align=True)
            sub.ui_units_x = 12
            VertexColor(self, context, layout=sub)
            Color(self, context, layout=row)   
            main.separator(factor = 1)

            row = main.row(align=True)
            split = row.split(factor=0.6)
            col = split.column(align=True)
            col.ui_units_x = 5
            col.menu_contents("VIEW3D_MT_TextureMask")
            col.menu_contents("VIEW3D_MT_BrushTexture")
            col = split.column(align=True)
            sub = col.column(align=True)
            sub.ui_units_x = 6
            SmoothStroke(self, context, layout=sub)
            Stroke(self, context, layout=sub)
            main.separator(factor = 1)

            ColorPalette(self, context, layout=main)


    #PAINT WEIGHT//////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

        if context.mode == 'PAINT_WEIGHT':

            brush = context.tool_settings.vertex_paint.brush
            wp = ts.weight_paint

            row = main.row(align=True)
            sub = row.column()
            sub.ui_units_x = 2
            sub.prop(brush, "blend", text="")
            sub = row.column()
            sub.ui_units_x = 2
            sub.menu_contents("VIEW3D_MT_Falloff")

            row= main.row(align=True)
            row.prop(brush, "use_frontface", text="FRONT", toggle=True)
            row.prop(brush, "use_accumulate", text="ACCU", toggle=True)

            main.separator(factor = 1)

            row = main.row(align=True)
            BrushCopy(self, context, layout=row)
            tool_bt(layout=row, cmd=1, w=4, h=1.4, text=False, icon='LARGE')

            main.separator(factor = 1)

            row = main.row(align=True)
            tool_bt(layout=row, cmd=2, w=2, h=1.4, text=False, icon='LARGE')
            tool_bt(layout=row, cmd=3, w=2, h=1.4, text=False, icon='LARGE')
            tool_bt(layout=row, cmd=4, w=2, h=1.4, text=False, icon='LARGE')
            tool_bt(layout=row, cmd=5, w=2, h=1.4, text=False, icon='LARGE')
            tool_bt(layout=row, cmd=6, w=2, h=1.4, text=False, icon='LARGE')
            tool_bt(layout=row, cmd=7, w=2, h=1.4, text=False, icon='LARGE')

            main.separator(factor = 1)

            row = main.row(align=True)
            row.prop(ts, "use_auto_normalize", text="NORM", toggle=True)
            row.prop(ts, "use_lock_relative", text="RELAT", toggle=True)
            row.prop(ts, "use_multipaint", text="MPAINT", toggle=True)
            row.prop(wp, "use_group_restrict", text="RESTR", toggle=True)
            main.separator(factor = 1)

            row = main.row(align=True)
            split = row.split(factor=0.6)

            col = split.column(align=True)
            col.ui_units_x = 5
            col.menu_contents("VIEW3D_MT_TextureMask")
            col.menu_contents("VIEW3D_MT_BrushTexture")

            col = split.column(align=True)
            sub = col.column(align=True)
            sub.ui_units_x = 6
            SmoothStroke(self, context, layout=sub)
            Stroke(self, context, layout=sub)
            main.separator(factor = 1)

            row = main.row()
            VertexGroups(self, context, layout=row)
            main.separator(factor = 1)


    #GP DRAW//////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

        if context.mode == 'PAINT_GPENCIL':

            brush = context.tool_settings.gpencil_paint.brush
            gp_settings = brush.gpencil_settings

            row = main.row()

            sub = row.column(align=True)
            sub.ui_units_x = 4
            BrushCopy(self, context, layout=sub)
            sub.separator()
            subsub = sub.row(align=True)
            subsub.prop(ts, "use_gpencil_draw_onback", text="", icon='MOD_OPACITY', toggle=True)
            subsub.prop(ts, "use_gpencil_automerge_strokes", text="", toggle=True)
            subsub.separator(factor=2)
            subsub.prop(ts, "use_gpencil_weight_data_add", text="", icon='WPAINT_HLT', toggle=True)
            subsub.prop(ts, "use_gpencil_draw_additive", text="", icon='FREEZE', toggle=True)
            subsub.prop(gpd, "use_multiedit", text="", icon='GP_MULTIFRAME_EDITING', toggle=True)

            sub = row.column(align=True)
            sub.ui_units_x = 6
            subsub = sub.row(align=True)
            tool_bt(layout=subsub, cmd=2, w=2.4, h=1.4, text=False, icon='LARGE')
            tool_bt(layout=subsub, cmd=3, w=2.4, h=1.4, text=False, icon='LARGE')
            tool_bt(layout=subsub, cmd=4, w=2.4, h=1.4, text=False, icon='LARGE')
            tool_bt(layout=subsub, cmd=5, w=2.4, h=1.4, text=False, icon='LARGE')
            tool_bt(layout=subsub, cmd=6, w=2.4, h=1.4, text=False, icon='LARGE')
            sub.separator()
            subsub = sub.row(align=True)
            tool_bt(layout=subsub, cmd=7, w=1.2, h=1, text=False, icon='IPO_LINEAR')
            tool_bt(layout=subsub, cmd=8, w=1.2, h=1, text=False, icon='IPO_CONSTANT')
            tool_bt(layout=subsub, cmd=9, w=1.2, h=1, text=False, icon='IPO_EASE_OUT')
            tool_bt(layout=subsub, cmd=10, w=1.2, h=1, text=False, icon='IPO_EASE_IN_OUT')
            tool_bt(layout=subsub, cmd=11, w=1.2, h=1, text=False, icon='MESH_PLANE')
            tool_bt(layout=subsub, cmd=12, w=1.2, h=1, text=False, icon='MESH_CIRCLE')
            main.separator()

            row = main.row(align=True)
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
            GPSmoothStroke(self, context, layout=row)

            row = main.row(align=True)

            main.separator()
            row = main.row(align=True)

            #Layer
            sub = row.column()
            GPLayersWide(self, context, layout=sub) 
            row.separator()
            sub = row.column()
            sub.ui_units_x = 2
            sub.popover("VIEW3D_PT_tools_grease_pencil_brush_post_processing", text="POST")
            sub.popover("VIEW3D_PT_tools_grease_pencil_brush_random", text="RND")
            sub.popover("VIEW3D_PT_tools_grease_pencil_brush_advanced", text="ADV")
            main.separator()
            row = main.row(align=True)
            #Material
            sub = row.column()
            sub.ui_units_x = 14
            subsub = sub.row(align=True)
            subsub.scale_x = 1.6
            subsub.prop_enum(gp_settings, "brush_draw_mode", 'MATERIAL', text="", icon='MATERIAL')
            subsub.prop_enum(gp_settings, "brush_draw_mode", 'VERTEXCOLOR', text="", icon='VPAINT_HLT')
            sub.menu_contents("VIEW3D_MT_GPMaterial")
            row.separator(factor=1)
            #Color
            sub = row.column(align=True)
            sub.ui_units_x = 8
            Color(self, context, layout=sub) 
            ColorPalette(self, context, layout=sub)
            row = main.row(align=True)
            #Mat-Stroke 
            sub = row.column()
            sub.ui_units_x = 6
            sub.menu_contents("VIEW3D_MT_GPStroke")

            #Mat-Fill
            sub = row.column()
            sub.ui_units_x = 6
            sub.menu_contents("VIEW3D_MT_GPFill")
            row = main.row(align=True)


            #Init
            sub = row.column()
            sub.ui_units_x = 4
            sub.operator("gpencil.blank_frame_add", text="INIT")
            #Cleanup
            sub = row.column()
            sub.ui_units_x = 4
            sub.menu("GPENCIL_MT_cleanup")
            #Mat-Menu
            sub = row.column()
            sub.ui_units_x = 6
            sub.menu("GPENCIL_MT_material_context_menu")


    #GP EDIT//////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

        if context.mode == 'EDIT_GPENCIL':
            brush = context.tool_settings.vertex_paint.brush

            row = main.row(align=True)
            row.prop_enum(ts, "gpencil_selectmode_edit", text="POINT", value='POINT', icon='NONE')
            row.prop_enum(ts, "gpencil_selectmode_edit", text="STROKE", value='STROKE', icon='NONE')
            sub = row.row(align=True)
            sub.enabled = not gpd.use_curve_edit
            sub.prop_enum(ts, "gpencil_selectmode_edit", text="SEG", value='SEGMENT')

            main.separator()

            row = main.row(align=True)
            tool_bt(layout=row, cmd=1, w=2, h=1.4, text=False, icon='LARGE')
            tool_bt(layout=row, cmd=2, w=2, h=1.4, text=False, icon='LARGE')
            tool_bt(layout=row, cmd=3, w=2, h=1.4, text=False, icon='LARGE')
            tool_bt(layout=row, cmd=4, w=2, h=1.4, text=False, icon='LARGE')
            tool_bt(layout=row, cmd=5, w=2, h=1.4, text=False, icon='LARGE')

            row = mainl.row(align=True)
            tool_bt(layout=row, cmd=6, w=2, h=1.4, text=False, icon='LARGE')
            tool_bt(layout=row, cmd=7, w=2, h=1.4, text=False, icon='LARGE')
            tool_bt(layout=row, cmd=8, w=2, h=1.4, text=False, icon='LARGE')
            tool_bt(layout=row, cmd=9, w=2, h=1.4, text=False, icon='LARGE')

            main.separator()

            row = main.row(align=True)
            sub = row.column()
            sub.ui_units_x = 4
            GPToolSettings(self, context, layout=sub)
            sub = row.column()
            sub.ui_units_x = 4
            ToolOptions(self, context, layout=sub)

            main.separator()

            row  = main.row(align=True)
            sub = row.column(align=True)
            tool_bt(layout=sub, cmd=10, w=2, h=1, text=True, icon='OFF')
            tool_bt(layout=sub, cmd=11, w=2, h=1, text=True, icon='OFF')

            sub = row.column(align=True)
            tool_bt(layout=sub, cmd=12, w=2, h=1, text=True, icon='OFF')
            tool_bt(layout=sub, cmd=13, w=2, h=1, text=True, icon='OFF')

            sub = row.column(align=True)
            tool_bt(layout=sub, cmd=14, w=2, h=1, text=True, icon='OFF')
            sub.separator(factor=1)

            sub = row.column(align=True)
            tool_bt(layout=sub, cmd=15, w=2, h=1, text=True, icon='OFF')
            tool_bt(layout=sub, cmd=16, w=2, h=1, text=True, icon='OFF')

            main.separator(factor=2)

            InsertLine(main)

            row = main.row(align=True)

            sub = row.column(align=True)
            sub.operator("gpencil.stroke_simplify", text="SIMPLIFY")
            sub.operator("gpencil.stroke_sample", text="RESAMPL")

            sub = row.column(align=True)
            sub.operator("gpencil.stroke_subdivide", text="SUBDIV").only_selected=True
            sub.operator("gpencil.stroke_smooth", text="SMOTH").only_selected=True

            row.separator(factor=2)

            sub = row.column(align=True)
            op = sub.operator("gpencil.stroke_cyclical_set", text="CLOSE")
            op.type='CLOSE'
            op.geometry=True
            sub.operator("gpencil.stroke_trim", text="TRIM")
            sub.separator(factor=2)
            sub.operator("gpencil.stroke_merge", text="MERGE")
            sub.operator("gpencil.stroke_join", text="JOIN")

            InsertLine(main)

            main.separator()

            row = main.row(align=True)
            row.prop(gpd, "use_curve_edit", text="",icon='IPO_BEZIER')
            sub = row.row(align=True)
            sub.active = gpd.use_curve_edit
            sub.popover(panel="VIEW3D_PT_gpencil_curve_edit", text="Curve Editing",)

    #GP SCULPT//////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

        if context.mode == 'SCULPT_GPENCIL':

            brush = context.tool_settings.gpencil_paint.brush

            row = main.row(align=True)
            row.prop(ts, "use_gpencil_select_mask_point", text="POINT")
            row.prop(ts, "use_gpencil_select_mask_stroke", text="STROKE")
            row.prop(ts, "use_gpencil_select_mask_segment", text="SEG")

            InsertLine(main)

            row = main.row(align=True)
            sub = row.column()
            sub.ui_units_x = 4
            BrushCopy(self, context, layout=sub)
            sub = row.column()
            sub.ui_units_x = 4
            sub.menu_contents("VIEW3D_MT_Falloff")

            main.separator()

            row = main.row(align=True)
            tool_bt(layout=row, cmd=5, w=2.2, h=1.4, text=True, icon='LARGE')
            tool_bt(layout=row, cmd=6, w=2.2, h=1.4, text=True, icon='LARGE')
            tool_bt(layout=row, cmd=7, w=2.2, h=1.4, text=True, icon='LARGE')
            tool_bt(layout=row, cmd=8, w=2.2, h=1.4, text=True, icon='LARGE')
            tool_bt(layout=row, cmd=9, w=2.2, h=1.4, text=True, icon='LARGE')

            main.separator()

            row = main.row(align=True)
            tool_bt(layout=row, cmd=1, w=2.8, h=1, text=False, icon='OFF')
            tool_bt(layout=row, cmd=2, w=2.8, h=1, text=False, icon='OFF')
            tool_bt(layout=row, cmd=3, w=2.8, h=1, text=False, icon='OFF')
            tool_bt(layout=row, cmd=4, w=2.8, h=1, text=False, icon='OFF')

            InsertLine(main)

            GPSculptToolSettings(self, context, layout=main)

    # WEIGHT_GPENCIL //////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
        if context.mode == 'WEIGHT_GPENCIL':
            brush = context.tool_settings.vertex_paint.brush
            row = main.row(align=True)
            #Tools
            tool_bt(layout=row, cmd=1, w=2.2, h=1.4, text=False, icon='LARGE')

    # EDIT_CURVE //////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
        if context.mode == 'EDIT_CURVE':

            row = main.row(align=True)

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

'''
#PERSISTENT
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
        #HideObject(self, context, layout=row)

        #row.separator(factor=1)

        # overlay & hud:
        Overlay(self, context, layout=row)
        funct_bt(layout=row, cmd='pivot', tog=True, w=1.2, h=1, label='', icon='ORIENTATION_VIEW')
        funct_bt(layout=row, cmd='hud', tog=True, w=1.2, h=1, label='', icon="INFO") 

        col = top_right_outer.column(align=True)
        col.ui_units_x = 0.2
        col.scale_y = 0.7
        col.label(text='')
        col.label(text='')
'''



#-----------------------------------------------------------------------------------------------------------------------

def register() :
    bpy.utils.register_class(YPanel)

def unregister() :
    bpy.utils.unregister_class(YPanel)
