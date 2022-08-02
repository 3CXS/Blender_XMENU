import bpy
from bpy.types import Menu
from .menuitems import *
from .functions import tool_bt, funct_bt

from .icons import get_icon_id

#-----------------------------------------------------------------------------------------------------------------------
# PIE-MODES:

class ModesMenu(bpy.types.Menu):
    bl_label = ""
    bl_idname = "OBJECT_MT_modes_menu"

    def draw(self, context):
        layout = self.layout

        pie = layout.menu_pie()

        #empty
        col = pie.column()
        col.label(text='')
        col.label(text='')
        col.label(text='')

        #file save / open
        col.operator("wm.save_mainfile", icon='FILE_TICK', text="SAVE")
        col.operator("wm.save_as_mainfile", text="SAVE AS")

        sub = col.row(align=True)
        sub.operator("wm.open_mainfile", text="OPEN")
        sub.menu("TOPBAR_MT_file_open_recent", text="RECENT")

        #I-O
        col.popover("OBJECT_PT_import_panel", text="IMPORT / EXPORT")
        sub = col.row(align=True)
        sub.operator("wm.link", icon='LINK_BLEND', text="LINK")
        sub.operator("wm.append", icon='APPEND_BLEND', text="APND")

        #shading
        col = pie.column()
        col.label(text='')
        col.scale_y = 1.2
        ShadingMode(self, context, col)
        col.label(text='')
        col.operator("screen.screenshot_area", text="SCREEN")

        #empty
        col = pie.column()
        col.label(text='')

        #modes
        col = pie.column()
        col.scale_y = 1.3
        ModeSelector(self, context, col)


#-----------------------------------------------------------------------------------------------------------------------
#PANEL-X1:

class ToolMenu(bpy.types.Panel):
    bl_label = "X-1"
    bl_idname = "OBJECT_PT_tool_menu"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'WINDOW'
    bl_context = "scene"

    def draw(self, context):
        layout = self.layout

        ts = context.tool_settings
        gpd = context.gpencil_data

        col = layout.column(align=True)
        col.alignment = 'LEFT'

    #OBJECT-----------------------------------------------------------------------------------------------

        if context.mode == 'OBJECT':

            row = col.row(align=True)

            # toolset:
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

            col.separator(factor=2)

            # transform-matrix:
            row = col.row(align=True)
            Transforms(self, context, layout=row)
            row = col.row(align=True)
            Pivot(self, context, layout=row)

            col.separator(factor=2)

            # add modifiers:
            row =col.row(align=True)
            ob = context.active_object
            if  ob:
                if ob.type == "MESH" and "CURVE" and "SURFACE" and "TEXT":
                    row.operator("object.modifier_add", text="", icon="MOD_BEVEL").type='BEVEL'
                    row.operator("object.modifier_add", text="", icon="MOD_SOLIDIFY").type='SOLIDIFY'
                    row.operator("object.modifier_add", text="", icon="MOD_SUBSURF").type='SUBSURF'
                    row.operator("object.modifier_add", text="", icon="MOD_MIRROR").type='MIRROR'
                    row.operator("object.modifier_add", text="", icon="MOD_REMESH").type='REMESH'
                    row.operator("object.modifier_add", text="", icon="MOD_DECIM").type='DECIMATE'
                    row.operator_menu_enum("object.modifier_add", "type", text='ADD MOD')
                elif ob.type == "GPENCIL":
                    split = row.split(factor=0.62)
                    split.label(text="")
                    split.operator_menu_enum("object.gpencil_modifier_add", "type", text='ADD MOD')
                elif ob.type == "ARMATURE":
                    row.label(text=">") 
                else:
                    row.label(text=">")

            col.separator(factor=1)

            # add objects:
            row = col.row(align=True)
            row.operator('mesh.primitive_plane_add', text="", icon='MESH_PLANE')
            row.operator('mesh.primitive_cube_add', text="", icon='MESH_CUBE')
            row.operator('mesh.primitive_uv_sphere_add', text="", icon='MESH_UVSPHERE')
            row.operator('mesh.primitive_cylinder_add', text="", icon='MESH_CYLINDER')
            row.operator('object.empty_add', text="", icon='EMPTY_DATA')
            row.operator('object.gpencil_add', text="", icon='GREASEPENCIL').type='EMPTY'
            row.menu("VIEW3D_MT_add", text="ADD OBJ", text_ctxt=i18n_contexts.operator_default)

            col.separator(factor=0.2)

            # bool operators:
            row = col.row(align=True)
            row.operator('btool.boolean_union', text="", icon='SELECT_EXTEND')
            row.operator('btool.boolean_diff', text="", icon='SELECT_SUBTRACT')
            row.operator('btool.boolean_inters', text="", icon='SELECT_INTERSECT')
            row.operator('btool.boolean_slice', text="", icon='SELECT_DIFFERENCE')
            row.operator('object.convert', text="CONV",)

            # merge/clone:
            row.operator('object.join', text='MRG')
            row.operator('object.duplicate_move', text='DUB')
            #sub.operator('object.make_links_data', text='COPY MODS').type='MODIFIERS'

            col.separator(factor=1)

            row = col.row(align=True)
            row.scale_y = 0.7 
            row.label(text="")
            row.label(text="")
            row.label(text="")
            row.label(text="")
            row.operator("screen.redo_last", text=">")

    #EDIT-----------------------------------------------------------------------------------------------

        if context.mode == 'EDIT_MESH':

            row = col.row(align=True)

            sub = row.column( )
            sub.scale_x = 2.5
            sub.template_edit_mode_selection()

            row.separator(factor=2)
            funct_bt(layout=row, cmd='xray', tog=True, w=2.4, h=1, label='', icon="XRAY")

            row.separator(factor=2)

            # automerge:
            ts = context.tool_settings
            sub = row.row(align=True)
            sub.scale_x = 2.5
            sub.prop(ts, "use_mesh_automerge", text="", toggle=True)

            # stitch-tools:
            sub = row.row(align=True)
            sub.scale_x = 2.5    
            sub.operator('mesh.target_weld_toggle', text='', icon='CON_TRACKTO') #target_weld

            col.separator(factor=1)

            # toolset:
            row = col.row(align=True)
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

            insert_line(col)

            # mark seams:
            row = col.row(align=True)
            op = row.operator('mesh.mark_seam', text='',icon='ADD')
            op = row.operator('mesh.mark_seam', text='',icon='REMOVE')
            op.clear = True
            row.separator(factor = 1)

            insert_space(row, space=6)

            # mark sharp:
            op = row.operator('mesh.mark_sharp', text='',icon='ADD')
            op = row.operator('mesh.mark_sharp', text='',icon='REMOVE')
            op.clear = True

            col.separator(factor = 1)

            # Edge Tools:
            row = col.row(align=True)
            row.operator('transform.edge_bevelweight', text='Bevel')
            row.operator('transform.edge_crease', text='Crease')

            # modifiers ON/OFF:
            # row.operator("view3d.ml_toggle_all_modifiers", icon="CANCEL", text="")

            # select contour:
            row.operator('mesh.region_to_loop', text='', icon='CHECKBOX_DEHLT')

            # quick pivot:
            row.operator('mesh.quick_pivot', text='', icon='SNAP_FACE_CENTER')

            col.separator(factor = 2.5)

            # add mesh:
            row = col.row(align=True)
            row.menu("VIEW3D_MT_mesh_add",text='ADD MSH')
            row.separator(factor = 1)
            sub = row.row(align=True)
            sub.scale_x = 2.5
            sub.operator('mesh.intersect_boolean', text='', icon='MOD_BOOLEAN')
            sub = row.row(align=True)
            sub.scale_x = 2.5
            sub.operator('mesh.intersect', text='', icon='FCURVE')

            col.separator(factor = 1)

            # separate mesh:
            row = col.row(align=True)
            row.operator_menu_enum("mesh.separate", "type")
            row.separator(factor = 1)
            sub = row.row(align=True)
            sub.scale_x = 2.5
            sub .operator('mesh.split', text='', icon='MOD_BOOLEAN')
            sub = row.row(align=True)
            sub.scale_x = 2.5
            sub.operator('mesh.duplicate_move', text='', icon='XRAY')

            col.separator(factor=1)

            # tools:
            row = col.row(align=True)
            tool_bt(layout=row, cmd=21, w=1.2, h=1, text=False, icon='MOD_LINEART')

            insert_space(row, space=1.2)

            row.separator()

            tool_bt(layout=row, cmd=30, w=1.2, h=1, text=False, icon='UV_EDGESEL')
            tool_bt(layout=row, cmd=33, w=1.2, h=1, text=False, icon='EXPORT')
            row.separator()
            tool_bt(layout=row, cmd=35, w=1.2, h=1, text=False, icon='CURVE_NCIRCLE')
            row.separator()
            tool_bt(layout=row, cmd=19, w=1.2, h=1, text=False, icon='MOD_MESHDEFORM')
            tool_bt(layout=row, cmd=20, w=1.2, h=1, text=False, icon='MOD_BEVEL')

            row = col.row(align=True)
            tool_bt(layout=row, cmd=23, w=1.2, h=1, text=False, icon='SNAP_MIDPOINT')
            tool_bt(layout=row, cmd=25, w=1.2, h=1, text=False, icon='MOD_DATA_TRANSFER')
            row.separator()
            tool_bt(layout=row, cmd=31, w=1.2, h=1, text=False, icon='UV_VERTEXSEL')
            tool_bt(layout=row, cmd=32, w=1.2, h=1, text=False, icon='IMPORT')
            row.separator()
            tool_bt(layout=row, cmd=36, w=1.2, h=1, text=False, icon='TRANSFORM_ORIGINS')
            row.separator()
            tool_bt(layout=row, cmd=17, w=1.2, h=1, text=False, icon='MOD_EXPLODE')
            tool_bt(layout=row, cmd=16, w=1.2, h=1, text=False, icon='MOD_SOLIDIFY')

            col.separator(factor=1)

            # functions:
            row = col.row(align=True)

            sub = row.column(align=True)
            sub.scale_y=0.8
            sub.operator('mesh.flip_normals', text='FLIP')
            sub.operator('mesh.fill_holes', text='FILL HOLES')

            sub = row.column(align=True)
            sub.scale_y=0.8
            sub.operator('mesh.remove_doubles', text='CLEAN')
            sub.operator('mesh.delete_loose', text='LOOSE')

            row.separator(factor=2)

            sub = row.column(align=True)
            sub.scale_y=0.8
            sub.operator('mesh.merge', text="MERGE").type='CENTER'
            sub.operator('mesh.edge_face_add', text='FILL')

            col.separator(factor=1)

            row = col.row(align=True)

            sub = row.column(align=True)
            sub.scale_y=0.8
            sub.operator('mesh.symmetrize', text='SYM')
            op = sub.operator('transform.mirror', text='MIRROR')
            op.orient_type='GLOBAL'
            op.constraint_axis=(True, False, False)

            sub = row.column(align=True)
            sub.scale_y=0.8
            sub.operator('uv.smart_project', text="A-UV")
            sub.operator('uv.unwrap', text="UNWRP")

            row.separator(factor=2)

            # redo last:
            sub = row.column(align=True)
            sub.scale_y=0.8
            sub.label(text='')
            sub.operator("screen.redo_last", text="CMD >")

    #SCULPT-----------------------------------------------------------------------------------------------

        if context.mode == 'SCULPT':

            tool = context.workspace.tools.from_space_view3d_mode(bpy.context.mode).idname
            brush = context.tool_settings.image_paint.brush

            row = col.row()
            BrushCopy(self, context, layout=row)

            sub = row.column()
            sub.scale_y = 1.4
            sub.ui_units_x = 2
            if tool == 'builtin_brush.Paint':
                brush = context.tool_settings.sculpt.brush
                sub.prop(brush, "blend", text="")
            else:
                sub.label(text='')

            sub = row.column()
            sub.ui_units_x = 2
            sub.scale_y = 1.4
            sub.menu_contents("VIEW3D_MT_Falloff")

            col.separator(factor=1)

            row = col.row(align=True)
            row.scale_y = 1.2
            SculptBrushSettings(self, context, layout=row)

            insert_line(col)

            row = col.row(align=True)
            sub = row.column(align=True)
            subsub = sub.row(align=True)
            tool_bt(layout=subsub, cmd=37, w=2, h=1.4, text=True, icon='LARGE')
            tool_bt(layout=subsub, cmd=38, w=2, h=1.4, text=True, icon='LARGE')

            Color(self, context, layout=sub)   
            sub.separator(factor = 1)

            sub = row.column(align=True)
            SmoothStroke(self, context, layout=sub)
            Stroke(self, context, layout=sub)

            insert_line(col)

            col.menu_contents("VIEW3D_MT_TextureMask")
            col.menu_contents("VIEW3D_MT_BrushTexture")
            #ColorPalette(self, context, layout=col)


    #PAINT TEXTURE -----------------------------------------------------------------------------------------------

        if context.mode == 'PAINT_TEXTURE':
            brush = context.tool_settings.image_paint.brush

            row = col.row(align=True)

            sub = row.column()
            sub.ui_units_x = 2
            sub.prop(brush, "blend", text="")
            sub = row.column()
            sub.ui_units_x = 2
            sub.menu_contents("VIEW3D_MT_Falloff")

            TextureBrushSettings(self, context, layout=col)

            col.separator(factor = 1)

            row = col.row(align=True)
            BrushCopy(self, context, layout=row)
            tool_bt(layout=row, cmd=1, w=4, h=1.4, text=False, icon='LARGE')

            col.separator(factor = 1)

            row = col.row(align=True)
            tool_bt(layout=row, cmd=2, w=2, h=1.4, text=False, icon='LARGE')
            tool_bt(layout=row, cmd=3, w=2, h=1.4, text=False, icon='LARGE')
            tool_bt(layout=row, cmd=4, w=2, h=1.4, text=False, icon='LARGE')
            tool_bt(layout=row, cmd=5, w=2, h=1.4, text=False, icon='LARGE')
            tool_bt(layout=row, cmd=6, w=2, h=1.4, text=False, icon='LARGE')

            col.separator(factor = 1)

            ToolOptions(self, context, layout=col)

            col.separator(factor = 1)

            row = col.row()
            Color(self, context, layout=row) 
            sub = row.column(align=True)
            SmoothStroke(self, context, layout=sub)
            Stroke(self, context, layout=sub)
            col.separator(factor = 1)

            col.menu_contents("VIEW3D_MT_TextureMask")
            col.menu_contents("VIEW3D_MT_BrushTexture")

            col.separator(factor = 1)

            ColorPalette(self, context, layout=col)


    #PAINT VERTEX -----------------------------------------------------------------------------------------------

        if context.mode == 'PAINT_VERTEX':

            brush = context.tool_settings.vertex_paint.brush

            row = col.row(align=True)
            sub = row.column()
            sub.ui_units_x = 2
            sub.prop(brush, "blend", text="")
            sub = row.column()
            sub.ui_units_x = 2
            sub.menu_contents("VIEW3D_MT_Falloff")

            VertexBrushSettings(self, context, layout=col)

            col.separator(factor = 1)

            row = col.row(align=True)
            BrushCopy(self, context, layout=row)
            tool_bt(layout=row, cmd=1, w=4, h=1.4, text=False, icon='LARGE')

            col.separator(factor = 1)

            row = col.row(align=True)
            tool_bt(layout=row, cmd=2, w=2, h=1.4, text=False, icon='LARGE')
            tool_bt(layout=row, cmd=3, w=2, h=1.4, text=False, icon='LARGE')
            tool_bt(layout=row, cmd=4, w=2, h=1.4, text=False, icon='LARGE')

            col.separator(factor = 1)

            row = col.row()
            Color(self, context, layout=row)   

            sub = row.column(align=True)
            SmoothStroke(self, context, layout=sub)
            Stroke(self, context, layout=sub)

            col.separator(factor = 1)

            col.menu_contents("VIEW3D_MT_TextureMask")
            col.menu_contents("VIEW3D_MT_BrushTexture")

            col.separator(factor = 1)

            ColorPalette(self, context, layout=col)


    #PAINT WEIGHT-----------------------------------------------------------------------------------------------

        if context.mode == 'PAINT_WEIGHT':

            brush = context.tool_settings.vertex_paint.brush
            wp = ts.weight_paint

            row = col.row(align=True)
            sub = row.column()
            sub.ui_units_x = 2
            sub.prop(brush, "blend", text="")
            sub = row.column()
            sub.ui_units_x = 2
            sub.menu_contents("VIEW3D_MT_Falloff")

            row= col.row(align=True)
            row.prop(brush, "use_frontface", text="FRONT", toggle=True)
            row.prop(brush, "use_accumulate", text="ACCU", toggle=True)

            col.separator(factor = 1)

            row = col.row(align=True)
            BrushCopy(self, context, layout=row)
            tool_bt(layout=row, cmd=1, w=4, h=1.4, text=False, icon='LARGE')

            col.separator(factor = 1)

            row = col.row(align=True)
            tool_bt(layout=row, cmd=2, w=2, h=1.4, text=False, icon='LARGE')
            tool_bt(layout=row, cmd=3, w=2, h=1.4, text=False, icon='LARGE')
            tool_bt(layout=row, cmd=4, w=2, h=1.4, text=False, icon='LARGE')
            tool_bt(layout=row, cmd=5, w=2, h=1.4, text=False, icon='LARGE')
            tool_bt(layout=row, cmd=6, w=2, h=1.4, text=False, icon='LARGE')
            tool_bt(layout=row, cmd=7, w=2, h=1.4, text=False, icon='LARGE')

            col.separator(factor = 1)

            row = col.row()
            sub = row.column(align=True)
            sub.ui_units_x = 4

            sub.prop(ts, "use_auto_normalize", text="NORM", toggle=True)
            sub.prop(ts, "use_lock_relative", text="RELAT", toggle=True)
            sub.prop(ts, "use_multipaint", text="MPAINT", toggle=True)
            sub.prop(wp, "use_group_restrict", text="RESTR", toggle=True)

            sub = row.column(align=True)
            sub.ui_units_x = 4
            SmoothStroke(self, context, layout=sub)
            Stroke(self, context, layout=sub)

            col.separator(factor = 1)


    #GP DRAW-----------------------------------------------------------------------------------------------

        if context.mode == 'PAINT_GPENCIL':

            brush = context.tool_settings.gpencil_paint.brush
            gp_settings = brush.gpencil_settings

            row = col.row(align=True)
            sub = row.column()
            sub.ui_units_x = 4
            BrushCopy(self, context, layout=sub)
            sub = row.column()
            sub.ui_units_x = 4
            tool_bt(layout=sub, cmd=1, w=2.4, h=1.4, text=False, icon='LARGE')
 
            col.separator()

            row = col.row(align=True)
            tool_bt(layout=row, cmd=2, w=2.4, h=1.4, text=False, icon='LARGE')
            tool_bt(layout=row, cmd=3, w=2.4, h=1.4, text=False, icon='LARGE')
            tool_bt(layout=row, cmd=4, w=2.4, h=1.4, text=False, icon='LARGE')
            tool_bt(layout=row, cmd=5, w=2.4, h=1.4, text=False, icon='LARGE')
            tool_bt(layout=row, cmd=6, w=2.4, h=1.4, text=False, icon='LARGE')

            row = col.row(align=True)
            tool_bt(layout=row, cmd=7, w=1.2, h=1, text=False, icon='IPO_LINEAR')
            tool_bt(layout=row, cmd=8, w=1.2, h=1, text=False, icon='IPO_CONSTANT')
            tool_bt(layout=row, cmd=9, w=1.2, h=1, text=False, icon='IPO_EASE_OUT')
            tool_bt(layout=row, cmd=10, w=1.2, h=1, text=False, icon='IPO_EASE_IN_OUT')
            tool_bt(layout=row, cmd=11, w=1.2, h=1, text=False, icon='MESH_PLANE')
            tool_bt(layout=row, cmd=12, w=1.2, h=1, text=False, icon='MESH_CIRCLE')

            col.separator()

            row = col.row()
            sub = row.column(align=True)
            GPSmoothStroke(self, context, layout=sub)

            sub = row.column(align=True)

            subsub = sub.row(align=True)
            subsub.prop(ts, "use_gpencil_draw_onback", text="", icon='MOD_OPACITY', toggle=True)
            subsub.separator(factor=0.4)
            subsub.prop(ts, "use_gpencil_automerge_strokes", text="", toggle=True)

            subsub = sub.row(align=True)
            subsub.prop(ts, "use_gpencil_weight_data_add", text="", icon='WPAINT_HLT', toggle=True)
            subsub.prop(ts, "use_gpencil_draw_additive", text="", icon='FREEZE', toggle=True)
            subsub.prop(gpd, "use_multiedit", text="", icon='GP_MULTIFRAME_EDITING', toggle=True)

            col.separator()

            row = col.row(align=True)
            row.popover("VIEW3D_PT_tools_grease_pencil_brush_post_processing")
            row.popover("VIEW3D_PT_tools_grease_pencil_brush_random")
            row.popover("VIEW3D_PT_tools_grease_pencil_brush_advanced")

    #GP EDIT -----------------------------------------------------------------------------------------------

        if context.mode == 'EDIT_GPENCIL':
            brush = context.tool_settings.vertex_paint.brush

            row = col.row(align=True)
            row.prop_enum(ts, "gpencil_selectmode_edit", text="POINT", value='POINT', icon='NONE')
            row.prop_enum(ts, "gpencil_selectmode_edit", text="STROKE", value='STROKE', icon='NONE')
            sub = row.row(align=True)
            sub.enabled = not gpd.use_curve_edit
            sub.prop_enum(ts, "gpencil_selectmode_edit", text="SEG", value='SEGMENT')

            col.separator()

            row = col.row(align=True)
            tool_bt(layout=row, cmd=1, w=2, h=1.4, text=False, icon='LARGE')
            tool_bt(layout=row, cmd=2, w=2, h=1.4, text=False, icon='LARGE')
            tool_bt(layout=row, cmd=3, w=2, h=1.4, text=False, icon='LARGE')
            tool_bt(layout=row, cmd=4, w=2, h=1.4, text=False, icon='LARGE')
            tool_bt(layout=row, cmd=5, w=2, h=1.4, text=False, icon='LARGE')

            row = col.row(align=True)
            tool_bt(layout=row, cmd=6, w=2, h=1.4, text=False, icon='LARGE')
            tool_bt(layout=row, cmd=7, w=2, h=1.4, text=False, icon='LARGE')
            tool_bt(layout=row, cmd=8, w=2, h=1.4, text=False, icon='LARGE')
            tool_bt(layout=row, cmd=9, w=2, h=1.4, text=False, icon='LARGE')

            col.separator()

            row = col.row(align=True)
            sub = row.column()
            sub.ui_units_x = 4
            GPToolSettings(self, context, layout=sub)
            sub = row.column()
            sub.ui_units_x = 4
            ToolOptions(self, context, layout=sub)

            col.separator()

            row  = col.row(align=True)
            sub = row .column(align=True)
            tool_bt(layout=sub, cmd=10, w=2, h=1, text=True, icon='OFF')
            tool_bt(layout=sub, cmd=11, w=2, h=1, text=True, icon='OFF')

            sub = row .column(align=True)
            tool_bt(layout=sub, cmd=12, w=2, h=1, text=True, icon='OFF')
            tool_bt(layout=sub, cmd=13, w=2, h=1, text=True, icon='OFF')

            sub = row .column(align=True)
            tool_bt(layout=sub, cmd=14, w=2, h=1, text=True, icon='OFF')
            sub.separator(factor=1)

            sub = row .column(align=True)
            tool_bt(layout=sub, cmd=15, w=2, h=1, text=True, icon='OFF')
            tool_bt(layout=sub, cmd=16, w=2, h=1, text=True, icon='OFF')

            col.separator(factor=2)

            insert_line(col)

            row = col.row(align=True)

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

            insert_line(col)

            col.separator()

            row = col.row(align=True)
            row.prop(gpd, "use_curve_edit", text="",icon='IPO_BEZIER')
            sub = row.row(align=True)
            sub.active = gpd.use_curve_edit
            sub.popover(panel="VIEW3D_PT_gpencil_curve_edit", text="Curve Editing",)

    #GP SCULPT-----------------------------------------------------------------------------------------------

        if context.mode == 'SCULPT_GPENCIL':

            brush = context.tool_settings.gpencil_paint.brush

            row = col.row(align=True)
            row.prop(ts, "use_gpencil_select_mask_point", text="POINT")
            row.prop(ts, "use_gpencil_select_mask_stroke", text="STROKE")
            row.prop(ts, "use_gpencil_select_mask_segment", text="SEG")

            insert_line(col)

            row = col.row(align=True)
            sub = row.column()
            sub.ui_units_x = 4
            BrushCopy(self, context, layout=sub)
            sub = row.column()
            sub.ui_units_x = 4
            sub.menu_contents("VIEW3D_MT_Falloff")

            col.separator()

            row = col.row(align=True)
            tool_bt(layout=row, cmd=5, w=2.2, h=1.4, text=True, icon='LARGE')
            tool_bt(layout=row, cmd=6, w=2.2, h=1.4, text=True, icon='LARGE')
            tool_bt(layout=row, cmd=7, w=2.2, h=1.4, text=True, icon='LARGE')
            tool_bt(layout=row, cmd=8, w=2.2, h=1.4, text=True, icon='LARGE')
            tool_bt(layout=row, cmd=9, w=2.2, h=1.4, text=True, icon='LARGE')

            col.separator()

            row = col.row(align=True)
            tool_bt(layout=row, cmd=1, w=2.8, h=1, text=False, icon='OFF')
            tool_bt(layout=row, cmd=2, w=2.8, h=1, text=False, icon='OFF')
            tool_bt(layout=row, cmd=3, w=2.8, h=1, text=False, icon='OFF')
            tool_bt(layout=row, cmd=4, w=2.8, h=1, text=False, icon='OFF')

            insert_line(col)

            GPSculptToolSettings(self, context, layout=col)


#-----------------------------------------------------------------------------------------------------------------------
#PANEL-X2:


class PropMenu(bpy.types.Panel):
    bl_label = "X-2"
    bl_idname = "OBJECT_PT_prop_menu"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'WINDOW'
    bl_context = "scene"

    def draw(self, context):

        layout = self.layout
        col = layout.column()

    #OBJECT-----------------------------------------------------------------------------------------------

        if context.mode == 'OBJECT':

            col.menu_contents("VIEW3D_MT_Material")
            UVTexture(self, context, layout=col)


    #EDIT-----------------------------------------------------------------------------------------------

        if context.mode == 'EDIT_MESH':

            ob = context.active_object
            group = ob.vertex_groups.active
            mat = ob.active_material
            slot = ob.material_slots
            space = context.space_data

            # vertex group:
            row = col.row(align=True)
            row.operator('object.vertex_group_assign_new', text='Vertex Group   ')
            row.operator('object.vertex_group_remove',text='',icon='BLANK1')
            row.operator('object.vertex_group_assign',text='',icon='ADD')
            row.operator('object.vertex_group_remove_from',text='',icon='REMOVE')
            row.separator(factor = 1)
            row.operator('object.vertex_group_select',text='',icon='RADIOBUT_ON')
            row.operator('object.vertex_group_deselect',text='',icon='RADIOBUT_OFF')

            col.template_list("MESH_UL_vgroups", "", ob, "vertex_groups", ob.vertex_groups, "active_index", rows=1)

            col.separator(factor = 2.5)

            # materials:
            row = col.row(align=True)
            row.menu("MATERIAL_MT_context_menu", text="Material")
            row.operator('object.material_slot_assign',text='',icon='BLANK1')
            row.operator('object.material_slot_add',text='',icon='ADD')
            row.operator('object.material_slot_remove',text='',icon='REMOVE')
            row.separator(factor = 1)
            row.operator('object.material_slot_select',text='',icon='RADIOBUT_ON')
            row.operator('object.material_slot_deselect',text='',icon='RADIOBUT_OFF')

            col.template_list("MATERIAL_UL_matslots", "", ob, "material_slots", ob, "active_material_index", rows=1)

            col.separator(factor = 1)

            col.template_ID(ob, "active_material")
            col.operator("xm.override", icon='ADD', text="NEW").cmd='material.new'


    #SCULPT-----------------------------------------------------------------------------------------------

        if context.mode == 'SCULPT':

            row = col.row()
            row.menu_contents("VIEW3D_MT_dynamesh")

            row.menu_contents("VIEW3D_MT_remesh")

            insert_line(col)

            row = col.row(align=True)
            op = row.operator('sculpt.expand',text='ACTIVE>')
            op.target='FACE_SETS'
            op.falloff_type='BOUNDARY_FACE_SET'
            op.invert=False
            op.use_modify_active=True

            op = row.operator('sculpt.expand',text='TOPO>')
            op.target='FACE_SETS'
            op.falloff_type='GEODESIC'
            op.invert=False
            op.use_modify_active=False

            sub = row.row(align=True)
            sub.scale_y = 1
            sub.scale_x = 1.4
            sub.operator('sculpt.face_set_edit',text='', icon='REMOVE').mode='SHRINK'
            sub.operator('sculpt.face_set_edit',text='', icon='ADD').mode='GROW'

            SculptFaceSet(self, context, layout=col)

            row = col.row(align=True)
            row.operator('mesh.face_set_extract', text='EXT FSET')
            row.operator('mesh.paint_mask_extract', text='EXT MASK')

            insert_line(col)

            col.separator(factor = 1)

            row = col.row(align=False)
            sub = row.column(align=False)
            sub.ui_units_x = 3
            subsub = sub.row()
            subsub.scale_y = 0.5
            subsub.label(text='FILTER')
            subsub = sub.row(align=True)
            tool_bt(layout=subsub, cmd=34, w=1, h=1, text=False, icon='OFF')
            tool_bt(layout=subsub, cmd=35, w=1, h=1, text=False, icon='OFF')
            tool_bt(layout=subsub, cmd=36, w=1, h=1, text=False, icon='OFF')

            col.separator(factor = 1)

            SculptFilterSettings(self, context, layout=col)

            col.separator(factor = 1)

            VertexColor(self, context, layout=col)

    #PAINT TEXTURE-----------------------------------------------------------------------------------------------

        if context.mode == 'PAINT_TEXTURE':

            TexSlots(self, context, layout=col)
            col.menu_contents("VIEW3D_MT_Material")
            UVTexture(self, context, layout=col)

    #PAINT VERTEX-----------------------------------------------------------------------------------------------

        if context.mode == 'PAINT_VERTEX':

            VertexColor(self, context, layout=col)

    #PAINT WEIGHT-----------------------------------------------------------------------------------------------

        if context.mode == 'PAINT_WEIGHT':

            VertexGroups(self, context, layout=col)

    #PAINT GPENCIL-----------------------------------------------------------------------------------------------

        if bpy.context.mode == 'PAINT_GPENCIL':

            GPLayers(self, context, layout=col)
            col.menu_contents("VIEW3D_MT_Material")
            col.menu("GPENCIL_MT_material_context_menu")
            col.menu_contents("VIEW3D_MT_GPStroke")
            col.menu_contents("VIEW3D_MT_GPFill")

    #EDIT GPENCIL-----------------------------------------------------------------------------------------------

        if bpy.context.mode == 'EDIT_GPENCIL':

            VertexGroups(self, context, layout=col)
            GPLayers(self, context, layout=col)
            col.menu_contents("VIEW3D_MT_Material")
            col.menu("GPENCIL_MT_material_context_menu")



#-----------------------------------------------------------------------------------------------------------------------
#PANEL-X3:

class SelectMenu(bpy.types.Panel):
    bl_label = "X-3"
    bl_idname = "OBJECT_PT_select_menu"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'WINDOW'
    bl_context = "scene"

    def draw(self, context):

        layout = self.layout
        col = layout.column(align=True)

        edit_mode = context.scene.tool_settings.mesh_select_mode

    #OBJECT-----------------------------------------------------------------------------------------------

        if context.mode == 'OBJECT':

            sub = col.column(align=True)
            sub.ui_units_x = 4
            subsub = sub.row(align=True)
            subsub.operator('object.select_linked', text='DATA').type='OBDATA'
            subsub.operator('object.select_linked', text='MAT').type='MATERIAL'
            subsub = sub.row(align=True)
            subsub.operator('object.select_linked', text='INST').type='DUPGROUP'
            subsub.operator('object.select_linked', text='LIB').type='LIBRARY_OBDATA'

            col.separator(factor = 1)

            row = col.row(align=True)
            op = row.operator("xm.override2", text="HIERARCHY")
            op.cmd ='object.select_hierarchy'
            op.prop1 ='direction="CHILD"'
            op.prop2 ='extend=True'

            col.separator(factor = 2)

            row = col.row()
            sub = row.column()
            sub.label(text='')
            sub = row.column()
            sub.ui_units_x = 4
            sub.operator("screen.redo_last", text="CMD >>")

    #EDIT-----------------------------------------------------------------------------------------------

        if context.mode == 'EDIT_MESH':

            row = col.row(align=True)
            row.scale_x = 2
            row.operator('mesh.select_all',text='',icon='SHADING_SOLID').action='SELECT'
            row.operator('mesh.select_all',text='', icon='IMAGE_ALPHA').action='INVERT'

            row.separator(factor = 4)

            row.operator('mesh.select_less', icon='REMOVE', text='')
            row.operator('mesh.select_more', icon='ADD',text='')

            col.separator(factor = 2)

            row = col.row(align=True)
            row.operator('object.vertex_group_assign_new',text='VERTEX GRP')
            sub = row.row(align=True)
            sub.scale_x = 1.2
            sub.operator('object.vertex_group_assign',text='',icon='CHECKMARK')

            col.separator(factor = 2)

            row = col.row(align=True)
            row.operator('mesh.select_linked',text='LINKED')
            row.operator('mesh.shortest_path_select',text='PATH')
            row.operator('mesh.faces_select_linked_flat',text='FLAT')
            row.separator(factor = 2)
            row.operator('mesh.select_mirror',text='MIRROR')

            col.separator(factor = 2)

            row = col.row(align=True)
            row.operator_menu_enum("mesh.select_similar", "type")
            row.operator_menu_enum("mesh.select_linked", "delimit")

            col.separator(factor = 2)

            row = col.row(align=True)
            row.operator('mesh.select_non_manifold',text='OPEN')
            row.operator('mesh.select_loose',text='LOOSE')
            row.operator('mesh.select_interior_faces',text='INTERIOR')
            row.operator('mesh.select_face_by_sides',text='COUNT')

            col.separator(factor = 2)

            row = col.row()
            sub = row.column()
            sub.label(text='')
            sub = row.column()
            sub.ui_units_x = 4
            sub.operator("screen.redo_last", text="CMD >>")

    #GP EDIT-----------------------------------------------------------------------------------------------

        if context.mode == 'EDIT_GPENCIL':

            row = col.row(align=True)
            row.ui_units_x = 4
            row.operator('gpencil.select_all',text='ALL').action='SELECT'
            row.operator('gpencil.select_all',text='CLR').action='DESELECT'
            row.operator('gpencil.select_all',text='INV').action='INVERT'

            col.separator(factor = 2)

            row = col.row(align=True)
            row.scale_x = 2
            row.alignment = 'CENTER'
            row.operator('gpencil.select_less', icon='REMOVE', text='')
            row.operator('gpencil.select_more', icon='ADD',text='')

            col.separator(factor = 2)

            row = col.row(align=True)
            row.label(text='')
            row.operator('object.vertex_group_add',text='NEW GRP')
            row.label(text='')

            col.separator(factor = 2)

            row = col.row(align=True)
            row.operator('gpencil.select_grouped',text='LAYER').type='LAYER'
            row.operator('gpencil.select_grouped',text='MAT').type='MATERIAL'
            row.operator('gpencil.select_linked',text='LINKED')

            col.separator(factor = 2)

            row= col.row()
            sub = row.column()
            sub.label(text='')
            sub = row.column()
            sub.ui_units_x = 4
            sub.operator("screen.redo_last", text="CMD >>")


    #SCULPT-----------------------------------------------------------------------------------------------
        if context.mode == 'SCULPT':

            SculptMask(self, context, layout=col)

            row = col.row(align=True)
            op = row.operator("sculpt.expand", text="NORM>")
            op.target='MASK'
            op.falloff_type='NORMALS'
            op.invert=False
            op = row.operator("sculpt.expand", text="TOPO>")
            op.target='MASK'
            op.falloff_type='GEODESIC'
            op.invert=True
            row.operator('sculpt.dirty_mask', text='CURV')

            col.separator(factor=1)

            row = col.row()
            tool_bt(layout=row, cmd=14, w=2, h=1.4, text=False, icon='LARGE') 
            sub = row.column()
            sub.ui_units_x = 3.4
            subsub = sub.column()
            subsub.scale_y = 0.5
            subsub.label(text="MASK")
            grid = sub.grid_flow(columns=3, align=True)
            tool_bt(layout=grid, cmd=28, w=1.2, h=0.8, text=False, icon='CUSTOM')
            tool_bt(layout=grid, cmd=29, w=1, h=0.8, text=False, icon='CUSTOM')
            tool_bt(layout=grid, cmd=30, w=1.2, h=0.8, text=False, icon='CUSTOM')

            sub = row.column()
            sub.ui_units_x = 2.4
            subsub = sub.column()
            subsub.scale_y = 0.5
            subsub.label(text="TRIM")
            grid = sub.grid_flow(columns=2, align=True)
            tool_bt(layout=grid, cmd=17, w=1.2, h=0.8, icon="CUSTOM", text=False)
            tool_bt(layout=grid, cmd=18, w=1.2, h=0.8, icon="CUSTOM", text=False)

            insert_line(col)

            row = col.row()
            tool_bt(layout=row, cmd=15, w=2, h=1.4, text=False, icon='LARGE')
            sub = row.column()       
            grid = sub.grid_flow(columns=2, align=True)
            tool_bt(layout=grid, cmd=31, w=1.5, h=0.75, text=False, icon='CUSTOM')
            tool_bt(layout=grid, cmd=32, w=1.5, h=0.75, text=False, icon='CUSTOM')
            tool_bt(layout=grid, cmd=33, w=1.2, h=0.5, text=False, icon='OFF')
            tool_bt(layout=grid, cmd=16, w=2.4, h=1.4, text=False, icon='LARGE')

            col.separator(factor = 1)

            row = col.row(align=True)
            op = row.operator('sculpt.expand',text='ACTIVE>')
            op.target='FACE_SETS'
            op.falloff_type='BOUNDARY_FACE_SET'
            op.invert=False
            op.use_modify_active=True

            op = row.operator('sculpt.expand',text='TOPO>')
            op.target='FACE_SETS'
            op.falloff_type='GEODESIC'
            op.invert=False
            op.use_modify_active=False

            sub = row.row(align=True)
            sub.scale_y = 1
            sub.scale_x = 1.4
            sub.operator('sculpt.face_set_edit',text='', icon='REMOVE').mode='SHRINK'
            sub.operator('sculpt.face_set_edit',text='', icon='ADD').mode='GROW'

            col.separator()

            row = col.row()
            SculptFaceSet(self, context, layout=row )

            insert_line(col)

            row  = col.row(align=True)
            row .operator('mesh.face_set_extract', text='EXT FSET')
            row .operator('mesh.paint_mask_extract', text='EXT MASK')


#-----------------------------------------------------------------------------------------------------------------------

addon_keymaps = []
classes = (PropMenu, ModesMenu, ToolMenu, SelectMenu)

def register():
    for cls in classes:
        bpy.utils.register_class(cls)

def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)

