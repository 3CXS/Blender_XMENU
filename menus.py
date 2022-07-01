import bpy
from bpy.types import Menu
from .menuitems import *
from .functions import tool_bt, funct_bt


class ModesMenu(bpy.types.Menu):
    bl_label = ""
    bl_idname = "OBJECT_MT_modes_menu"

    def draw(self, context):
        layout = self.layout

        pie = layout.menu_pie()

        col = pie.column()
        col.label(text='')

        col = pie.column()
        col.label(text='')

        col = pie.column()
        col.scale_y = 1.5
        ModeSelector(self, context, col)

        col = pie.column()
        ShadingMode(self, context, col)

class FileMenu(bpy.types.Menu):
    bl_label = ""
    bl_idname = "OBJECT_MT_file_menu"

    def draw(self, context):
        layout = self.layout

        pie = layout.menu_pie()

        col = pie.column()
        col.operator("wm.save_mainfile", icon='FILE_TICK', text="SAVE")
        col.operator("wm.save_as_mainfile", text="SAVE AS")

        col = pie.column()
        col.label(text='')
        col.operator("wm.link", text="SCREEN")

        col = pie.column()
        col.popover("OBJECT_PT_import_panel")
        sub = col.row(align=True)
        sub.operator("wm.link", icon='LINK_BLEND', text="LINK")
        sub.operator("wm.append", icon='APPEND_BLEND', text="APND")

        col = pie.column()
        sub = col.row(align=True)
        sub.operator("wm.open_mainfile", text="OPEN")
        sub.menu("TOPBAR_MT_file_open_recent", text="RECENT")

class PropMenu(bpy.types.Panel):
    bl_label = "PROPMENU"
    bl_idname = "OBJECT_PT_main_menu"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'WINDOW'
    bl_context = "scene"
    bl_order = 1000
    bl_options = {'DEFAULT_CLOSED',}

    def draw(self, context):
        layout = self.layout
        if context.mode == 'OBJECT':
            col = layout.column()
            col.menu_contents("VIEW3D_MT_Material")
            UVTexture(self, context, parent=col)
        if context.mode == 'EDIT_MESH':
            col = layout.column()
            VertexGroups(self, context, parent=col)
            col.menu_contents("VIEW3D_MT_Material")
            UVTexture(self, context, parent=col)
        if context.mode == 'PAINT_TEXTURE':
            col = layout.column()
            TexSlots(self, context, parent=col)
            col.menu_contents("VIEW3D_MT_Material")
            UVTexture(self, context, parent=col)
        if context.mode == 'SCULPT':
            col = layout.column()
            col.menu_contents("VIEW3D_MT_dynamesh")
            col.menu_contents("VIEW3D_MT_remesh")

            subrow = col.row(align=False)
            subcol = subrow.column(align=False)
            subcol.ui_units_x = 3
            item = subcol.row()
            item.scale_y = 0.5
            item.label(text='FILTER')
            item = subcol.row()
            tool_bt(parent=item, cmd=33, w=3, h=1, text=False, icon='OFF')
            item = subcol.row()
            tool_bt(parent=item, cmd=34, w=3, h=1, text=False, icon='OFF')
            item = subcol.row()
            tool_bt(parent=item, cmd=35, w=3, h=1, text=False, icon='OFF')

            SculptFilterSettings(self, context, parent=subrow)

            VertexColor(self, context, parent=col)
        if context.mode == 'PAINT_VERTEX':
            col = layout.column()
            VertexColor(self, context, parent=col)

        if context.mode == 'PAINT_WEIGHT':
            col = layout.column()
            VertexGroups(self, context, parent=col)

        if bpy.context.mode == 'PAINT_GPENCIL':
            col = layout.column()
            GPLayers(self, context, parent=col)
            col.menu_contents("VIEW3D_MT_Material")
            col.menu("GPENCIL_MT_material_context_menu")
            col.menu_contents("VIEW3D_MT_GPStroke")
            col.menu_contents("VIEW3D_MT_GPFill")
        if bpy.context.mode == 'EDIT_GPENCIL':
            col = layout.column()
            VertexGroups(self, context, parent=col)
            GPLayers(self, context, parent=col)
            col.menu_contents("VIEW3D_MT_Material")
            col.menu("GPENCIL_MT_material_context_menu")



class ToolMenu(bpy.types.Panel):
    bl_idname = "OBJECT_PT_tool_menu"
    bl_label = "TOOLS"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'WINDOW'
    bl_context = "scene"
    bl_order = 1000
    bl_options = {'DEFAULT_CLOSED',}

    def draw(self, context):
        layout = self.layout

        ts = context.tool_settings
        gpd = context.gpencil_data

        col = layout.column(align=True)

        if context.mode == 'OBJECT':
            sub = col.row(align=True)
            tool_bt(parent=sub, cmd=0, w=2, h=1.4, text=False, icon='LARGE')
            tool_bt(parent=sub, cmd=1, w=2, h=1.4, text=False, icon='LARGE')
            tool_bt(parent=sub, cmd=2, w=2, h=1.4, text=False, icon='LARGE')
            tool_bt(parent=sub, cmd=3, w=2, h=1.4, text=False, icon='LARGE')

            sub = col.row(align=True)
            tool_bt(parent=sub, cmd=5, w=2, h=1.4, text=False, icon='LARGE')
            tool_bt(parent=sub, cmd=6, w=2, h=1.4, text=False, icon='LARGE')
            tool_bt(parent=sub, cmd=7, w=2, h=1.4, text=False, icon='LARGE')
            tool_bt(parent=sub, cmd=8, w=2, h=1.4, text=False, icon='LARGE')

            col.separator(factor=2)
            sub = col.row(align=True)
            subsub = sub.column()
            subsub.ui_units_x = 1.2
            subsub.label(text='')
            subsub = sub.column()
            Transforms(self, context, parent=subsub)
            subsub = sub.column()
            subsub.ui_units_x = 1.2
            subsub.label(text='')

            col.separator(factor=2)

            sub = col.row(align=True)
            subsub = sub.column(align=True)
            #sub.ui_units_x = 4
            subsub.scale_y = 0.8
            subsub.label(text="OBJECT")
            subsub.operator('object.join', text='JOIN')
            subsub.operator('object.duplicate_move', text='DUPLICATE')
            subsub.operator('object.duplicate_move_linked', text='LINKED')
            subsub.operator('object.make_links_data', text='COPY MODS').type='MODIFIERS'

            subsub = sub.column(align=True)
            #sub.ui_units_x = 4
            subsub.scale_y = 0.8
            subsub.label(text="CONVERT")
            #subsub.ui_units_x = 3
            subsub.operator('object.convert', text='MESH').target='MESH'
            subsub.operator('object.convert', text='CURVE').target='CURVE'
            subsub.operator('object.convert', text='GPENCIL').target='GPENCIL'
            subsub.operator('gpencil.trace_image', text='IMG TRACE')

            sub = col.row(align=True)
            sub.alignment = 'CENTER'
            sub.label(text='-----------------------------------------------------')

            col.separator(factor=1)
            sub = col.row(align=True)
            sub.operator('mesh.primitive_plane_add', text="", icon='MESH_PLANE')
            sub.operator('mesh.primitive_cube_add', text="", icon='MESH_CUBE')
            sub.operator('mesh.primitive_uv_sphere_add', text="", icon='MESH_UVSPHERE')
            sub.operator('mesh.primitive_cylinder_add', text="", icon='MESH_CYLINDER')
            sub.operator('object.empty_add', text="", icon='EMPTY_DATA')
            sub.operator('object.gpencil_add', text="", icon='GREASEPENCIL')
            sub.operator('curve.primitive_bezier_curve_add', text="", icon='CURVE_DATA')
            sub.separator(factor=1)
            #sub.operator('object.delete', text='DELETE').use_global=False
            sub.operator("screen.redo_last", text="CMD >")

        if context.mode == 'EDIT_MESH':

            sub = col.row()
            subsub = sub.column()
            subsub.scale_x=2.5
            subsub.template_edit_mode_selection()
            sub.separator(factor=3)
            funct_bt(parent=sub, cmd='xray', tog=True, w=2.4, h=1, label='', icon="XRAY")

            col.separator(factor=1)

            sub = col.column()
            #sub.ui_units_x = 6
            grid = sub.grid_flow(row_major=True, columns=4, align=True)
            tool_bt(parent=grid, cmd=0, w=2, h=1.2, text=False, icon='LARGE')
            tool_bt(parent=grid, cmd=1, w=2, h=1.2, text=False, icon='LARGE')
            tool_bt(parent=grid, cmd=2, w=2, h=1.2, text=False, icon='LARGE')
            tool_bt(parent=grid, cmd=3, w=2, h=1.2, text=False, icon='LARGE')

            col.separator(factor=1)
            sub = col.column()
            grid = sub.grid_flow(row_major=True, columns=4, align=True)
            tool_bt(parent=grid, cmd=20, w=1, h=1.4, text=False, icon='LARGE')
            subsub = grid.column()
            subsub.label(text=' ')
            tool_bt(parent=grid, cmd=24, w=1, h=1.4, text=False, icon='LARGE')
            tool_bt(parent=grid, cmd=22, w=1, h=1.4, text=False, icon='LARGE')

            tool_bt(parent=grid, cmd=19, w=1, h=1.4, text=False, icon='LARGE')
            tool_bt(parent=grid, cmd=18, w=1, h=1.4, text=False, icon='LARGE')
            tool_bt(parent=grid, cmd=15, w=1, h=1.4, text=False, icon='LARGE')
            tool_bt(parent=grid, cmd=16, w=1, h=1.4, text=False, icon='LARGE')

            sub = col.row(align=True)
            sub.alignment = 'CENTER'
            sub.label(text='-----------------------------------------------------')

            split = col.split(factor=0.75)
            sub = split.column(align=True)
            subrow = sub.row(align=True)
            item = subrow.column(align=True)
            tool_bt(parent=item, cmd=29, w=2, h=1, text=False, icon='OFF')
            tool_bt(parent=item, cmd=30, w=2, h=1, text=False, icon='OFF')
            item = subrow.column(align=True)
            tool_bt(parent=item, cmd=32, w=2, h=1, text=False, icon='OFF')
            tool_bt(parent=item, cmd=31, w=2, h=1, text=False, icon='OFF')
            item = subrow.column(align=True)
            tool_bt(parent=item, cmd=35, w=2, h=1, text=False, icon='OFF')
            tool_bt(parent=item, cmd=34, w=2, h=1, text=False, icon='OFF')

            subrow = sub.row(align=True)    
            item = subrow.row(align=True)
            tool_bt(parent=item, cmd=27, w=2, h=1, text=False, icon='OFF')
            item.label(text=' ')


            sub = split.column()
            sub.scale_y=0.8
            item = sub.column(align=True)
            item.operator('mesh.merge', text="MERGE").type='CENTER'
            item.operator('mesh.split', text='SPLIT')
            item.operator('mesh.duplicate_move', text='DUB')
            item.operator('mesh.edge_face_add', text='FILL')
            col.separator(factor=1)

            sub = col.row(align=True)

            subsub = sub.column()
            subsubsub = subsub.row()
            item = subsubsub.column(align=True)
            item.scale_y=0.8
            item.operator('mesh.flip_normals', text='FLIP')
            item.operator('mesh.fill_holes', text='FILL HOLES')

            item = subsubsub.column(align=True)
            item.scale_y=0.8
            item.operator('mesh.remove_doubles', text='CLEAN')
            item.operator('mesh.delete_loose', text='LOOSE')

            subsub.separator(factor=1)
            split = subsub.split(factor=0.25)

            item = split.column(align=True)
            item.scale_y=0.8
            item.operator('mesh.separate', text='SLCT').type='SELECTED'
            item.operator('mesh.separate', text='MAT').type='MATERIAL'
            item.operator('mesh.separate', text='LSE').type='LOOSE'

            subsplit = split.row()
            item = subsplit.column(align=True)
            item.scale_y=0.8
            item.operator('mesh.symmetrize', text='SYM')
            op = item.operator('transform.mirror', text='MIRROR')
            op.orient_type='GLOBAL'
            op.constraint_axis=(True, False, False)

            subsub.separator(factor=0.2)
            item = subsplit.column(align=True)
            item.scale_y=0.8
            item.operator('uv.smart_project', text="A-UV")
            item.operator('uv.unwrap', text="UNWRP")

            sub.separator(factor=2)
            subsub = sub.column(align=True)
            #subsub.ui_units_x = 8
            subsub.operator('mesh.mark_sharp', text='SHARP')
            op = subsub.operator('mesh.mark_sharp', text='CLEAR')
            op.clear = True

            subsub = subsub.column(align=True)
            op = subsub.operator('mesh.mark_seam', text='SEAM')
            op = subsub.operator('mesh.mark_seam', text='CLEAR')
            op.clear = True

            subsub.separator(factor=2)
            subsub.operator("screen.redo_last", text="CMD >")

        if context.mode == 'SCULPT':
            brush = context.tool_settings.image_paint.brush


            sub = col.split(factor=0.4)
            BrushCopy(self, context, parent=sub)
            subsub = sub.split(factor=0.2)
            subsub.scale_y = 1.4
            subsub.label(text='')
            subsub.menu_contents("VIEW3D_MT_Falloff")

            col.separator(factor=2)
            sub = col.row(align=True)
            subsub = sub.column(align=True)
            subsub.ui_units_x = 2
            subsub.scale_y = 0.7
            subsub.operator('xmenu.mask', text='PVT M').cmd='PMASKED'
            subsub.operator('xmenu.mask', text='RESET').cmd='ORIGIN'
            tool_bt(parent=sub, cmd=18, w=2, h=1.4, text=False, icon='LARGE')
            #sub.separator(factor = 1)
            tool_bt(parent=sub, cmd=0, w=2, h=1.4, text=False, icon='LARGE')
            sub.separator(factor = 1)
            subsub = sub.row(align=True)
            tool_bt(parent=subsub, cmd=19, w=1.2, h=1, text=False, icon='CUSTOM')
            tool_bt(parent=subsub, cmd=21, w=1.2, h=1, text=False, icon='CUSTOM')

            col.separator(factor=1)
            sub = col.row(align=True)
            sub.scale_y = 1.4
            SculptBrushSettings1(self, context, parent=sub)

            col.separator(factor=1)
            sub = col.row(align=True)
            tool_grid(parent=sub, col=3, align=True, slotmin=1, slotmax=4, w=2, h=1.4, text=True, icon='LARGE')
            sub.separator(factor = 1)
            tool_bt(parent=sub, cmd=7, w=2, h=1.4, text=True, icon='LARGE')

            sub = col.row(align=True)
            tool_grid(parent=sub, col=3, align=True, slotmin=4, slotmax=7, w=2, h=1.4, text=True, icon='LARGE')
            sub.separator(factor = 1)
            tool_bt(parent=sub, cmd=8, w=2, h=1.4, text=True, icon='LARGE')
            col.separator(factor=1)
            sub = col.row(align=True)
            tool_grid(parent=sub, col=3, align=True, slotmin=9, slotmax=12, w=2, h=1.4, text=True, icon='LARGE')
            sub.separator(factor = 1)
            tool_bt(parent=sub, cmd=12, w=2, h=1.4, text=True, icon='LARGE')

            sub = col.row(align=True)
            sub.alignment = 'CENTER'
            sub.label(text='-----------------------------------------------------')

            tool = context.workspace.tools.from_space_view3d_mode(bpy.context.mode).idname
            if tool == 'builtin_brush.Paint':
                brush = context.tool_settings.sculpt.brush
                subsub = sub.column(align=True)
                subsub.ui_units_x = 4
                subsub.prop(brush, "blend", text="")


            sub = col.row(align=True)
            subsub = sub.column(align=True)
            subsubsub = subsub.row(align=True)
            tool_bt(parent=subsubsub, cmd=36, w=2, h=1.4, text=True, icon='LARGE')
            tool_bt(parent=subsubsub, cmd=37, w=2, h=1.4, text=True, icon='LARGE')
            subsub.separator(factor = 1)
            Color(self, context, parent=subsub)   
            sub.separator(factor = 1)
            Stroke(self, context, parent=sub)

            sub = col.row(align=True)
            sub.alignment = 'CENTER'
            sub.label(text='-----------------------------------------------------')

            col.separator(factor = 1)
            sub = col.row(align=True)
            col.menu_contents("VIEW3D_MT_TextureMask")
            col.separator(factor = 1)
            sub = col.row(align=True)
            sub.menu_contents("VIEW3D_MT_BrushTexture")

            #sub = col.row(align=True)
            #ColorPalette(self, context, parent=sub)

        if context.mode == 'PAINT_TEXTURE':
            brush = context.tool_settings.image_paint.brush

            split = col.split(factor=0.5)
            sub = split.row()
            sub.prop(brush, "blend", text="")
            sub = split.row()
            subsub = sub.column()
            subsub.ui_units_x = 2
            subsub.menu_contents("VIEW3D_MT_Falloff")

            sub = col.row(align=True)

            TextureBrushSettings(self, context, parent=sub)

            sub = col.row(align=True)
            tool_bt(parent=sub, cmd=0, w=2, h=1.4, text=False, icon='LARGE')
            BrushCopy(self, context, parent=sub)
            sub = col.row(align=True)            
            tool_grid(parent=sub, col=5, align=True, slotmin=1, slotmax=6, w=2, h=1.4, text=False, icon='LARGE')
            col.separator(factor = 1)
            sub = col.row(align=True)
            ToolOptions(self, context, parent=sub)
            col.separator(factor = 1)
            sub = col.row(align=True)
            Color(self, context, parent=sub)   
            Stroke(self, context, parent=sub)

            sub = col.row(align=True)
            col.menu_contents("VIEW3D_MT_TextureMask")
            sub = col.row(align=True)
            sub.menu_contents("VIEW3D_MT_BrushTexture")

            sub = col.row(align=True)
            ColorPalette(self, context, parent=sub)

        if context.mode == 'PAINT_VERTEX':
            brush = context.tool_settings.vertex_paint.brush

            split = col.split(factor=0.5)
            sub = split.row()
            sub.prop(brush, "blend", text="")
            sub = split.row()
            subsub = sub.column()
            subsub.ui_units_x = 2
            subsub.menu_contents("VIEW3D_MT_Falloff")
            sub = col.row(align=True)
            VertexBrushSettings(self, context, parent=sub)
            col.separator(factor = 1)
            sub = col.row(align=True)
            tool_bt(parent=sub, cmd=0, w=2, h=1.4, text=False, icon='LARGE')
            BrushCopy(self, context, parent=sub)
            sub = col.row(align=True)            
            tool_grid(parent=sub, col=5, align=True, slotmin=1, slotmax=4, w=2, h=1.4, text=True, icon='LARGE')


            sub = col.row(align=True)
            Color(self, context, parent=sub)   

            Stroke(self, context, parent=sub)

            sub = col.row(align=True)
            col.menu_contents("VIEW3D_MT_TextureMask")
            sub = col.row(align=True)
            sub.menu_contents("VIEW3D_MT_BrushTexture")

            sub = col.row(align=True)
            ColorPalette(self, context, parent=sub)

        if context.mode == 'PAINT_WEIGHT':
            brush = context.tool_settings.vertex_paint.brush

            split = col.split(factor=0.5)
            sub = split.row()
            sub.prop(brush, "blend", text="")
            sub = split.row()
            subsub = sub.column()
            subsub.ui_units_x = 2
            subsub.menu_contents("VIEW3D_MT_Falloff")

            sub = col.row(align=True)

            sub.prop(brush, "use_frontface", text="FRONT", toggle=True)
            sub.prop(brush, "use_accumulate", text="ACCU", toggle=True)

            sub = col.row(align=True)
            ts = context.tool_settings
            wp = ts.weight_paint
            sub.prop(ts, "use_auto_normalize", text="NORM", toggle=True)
            sub.prop(ts, "use_lock_relative", text="RELAT", toggle=True)
            sub.prop(ts, "use_multipaint", text="MPAINT", toggle=True)
            sub.prop(wp, "use_group_restrict", text="RESTR", toggle=True)

            col.separator(factor = 1)
            sub = col.row(align=True)
            tool_bt(parent=sub, cmd=0, w=2, h=1.4, text=False, icon='LARGE')
            BrushCopy(self, context, parent=sub)
            sub = col.row(align=True)            
            tool_grid(parent=sub, col=5, align=True, slotmin=1, slotmax=7, w=2, h=1.4, text=True, icon='LARGE')
            sub = col.row(align=True)
            Stroke(self, context, parent=sub)

        if context.mode == 'PAINT_GPENCIL':
            brush = context.tool_settings.gpencil_paint.brush
            gp_settings = brush.gpencil_settings
            sub = col.row(align=True)
            sub.prop(ts, "use_gpencil_draw_onback", text="BACK", icon='MOD_OPACITY', toggle=True)
            sub.separator(factor=0.4)
            sub.prop(ts, "use_gpencil_automerge_strokes", text="AUTOMERGE", toggle=True)
            sub = col.row(align=True)
            split = sub.split(factor=0.5)         
            BrushCopy(self, context, parent=split)
            col.separator()
            tool_bt(parent=split, cmd=0, w=2.4, h=1.4, text=False, icon='LARGE')
            sub = col.row(align=True)
            tool_bt(parent=sub, cmd=1, w=2.4, h=1.4, text=False, icon='LARGE')
            tool_bt(parent=sub, cmd=2, w=2.4, h=1.4, text=False, icon='LARGE')
            tool_bt(parent=sub, cmd=3, w=2.4, h=1.4, text=False, icon='LARGE')
            tool_bt(parent=sub, cmd=4, w=2.4, h=1.4, text=False, icon='LARGE')
            tool_bt(parent=sub, cmd=5, w=2.4, h=1.4, text=False, icon='LARGE')
            sub = col.row(align=True)
            tool_bt(parent=sub, cmd=6, w=1.2, h=1, text=False, icon='IPO_LINEAR')
            tool_bt(parent=sub, cmd=7, w=1.2, h=1, text=False, icon='IPO_CONSTANT')
            tool_bt(parent=sub, cmd=8, w=1.2, h=1, text=False, icon='IPO_EASE_OUT')
            tool_bt(parent=sub, cmd=9, w=1.2, h=1, text=False, icon='IPO_EASE_IN_OUT')
            tool_bt(parent=sub, cmd=10, w=1.2, h=1, text=False, icon='MESH_PLANE')
            tool_bt(parent=sub, cmd=11, w=1.2, h=1, text=False, icon='MESH_CIRCLE')

            col.separator()
            sub = col.row()
            subsub = sub.column(align=True)
            item = subsub.column(align=True)
            item.prop(gp_settings, "use_settings_stabilizer", text="SMTH", toggle=True)
            item = subsub.column(align=True)
            item.active = gp_settings.use_settings_stabilizer
            item.prop(brush, "smooth_stroke_radius", text="Radius", slider=True)
            item.prop(brush, "smooth_stroke_factor", text="Factor", slider=True)

            col.separator()
            subsub = sub.column(align=True)
            subsub.prop(ts, "use_gpencil_weight_data_add", text="WPAINT", toggle=True)
            subsub.prop(ts, "use_gpencil_draw_additive", text="FREEZE", toggle=True)
            subsub.prop(gpd, "use_multiedit", text="MULTIFRAME", toggle=True)

            col.separator()
            sub = col.row(align=True)
            sub.popover("VIEW3D_PT_tools_grease_pencil_brush_post_processing")
            sub.popover("VIEW3D_PT_tools_grease_pencil_brush_random")
            sub.popover("VIEW3D_PT_tools_grease_pencil_brush_advanced")


        if context.mode == 'EDIT_GPENCIL':
            brush = context.tool_settings.vertex_paint.brush

            sub = col.row(align=True)
            sub.prop_enum(ts, "gpencil_selectmode_edit", text="POINT", value='POINT', icon='NONE')
            sub.prop_enum(ts, "gpencil_selectmode_edit", text="STROKE", value='STROKE', icon='NONE')
            subrow = sub.row(align=True)
            subrow.enabled = not gpd.use_curve_edit
            subrow.prop_enum(ts, "gpencil_selectmode_edit", text="SEG", value='SEGMENT')

            col.separator()
            sub = col.row(align=True)
            tool_bt(parent=sub, cmd=0, w=2, h=1.4, text=False, icon='LARGE')
            tool_bt(parent=sub, cmd=1, w=2, h=1.4, text=False, icon='LARGE')
            tool_bt(parent=sub, cmd=2, w=2, h=1.4, text=False, icon='LARGE')
            tool_bt(parent=sub, cmd=3, w=2, h=1.4, text=False, icon='LARGE')
            tool_bt(parent=sub, cmd=4, w=2, h=1.4, text=False, icon='LARGE')
            sub = col.row(align=True)
            tool_bt(parent=sub, cmd=5, w=2, h=1.4, text=False, icon='LARGE')
            tool_bt(parent=sub, cmd=6, w=2, h=1.4, text=False, icon='LARGE')
            tool_bt(parent=sub, cmd=7, w=2, h=1.4, text=False, icon='LARGE')
            tool_bt(parent=sub, cmd=8, w=2, h=1.4, text=False, icon='LARGE')

            col.separator()
            sub = col.split(factor=0.75)
            GPToolSettings(self, context, parent=sub)
            sub.separator()
            ToolOptions(self, context, parent=sub ) 


            col.separator()
            sub = col.row(align=True)
            subsub = sub.column(align=True)
            tool_bt(parent=subsub, cmd=9, w=2, h=1, text=True, icon='OFF')
            tool_bt(parent=subsub, cmd=10, w=2, h=1, text=True, icon='OFF')
            subsub = sub.column(align=True)
            tool_bt(parent=subsub, cmd=11, w=2, h=1, text=True, icon='OFF')
            tool_bt(parent=subsub, cmd=12, w=2, h=1, text=True, icon='OFF')
            subsub = sub.column(align=True)
            tool_bt(parent=subsub, cmd=13, w=2, h=1, text=True, icon='OFF')
            sub.separator(factor=1)
            subsub = sub.column(align=True)
            tool_bt(parent=subsub, cmd=14, w=2, h=1, text=True, icon='OFF')
            tool_bt(parent=subsub, cmd=15, w=2, h=1, text=True, icon='OFF')

            col.separator(factor=2)
            sub = col.row(align=True)
            sub.alignment = 'CENTER'
            sub.label(text='-----------------------------------------------------')
            sub = col.row(align=True)

            item = sub.column(align=True)
            item.operator("gpencil.stroke_simplify", text="SIMPLIFY")
            item.operator("gpencil.stroke_sample", text="RESAMPL")

            item = sub.column(align=True)
            item.operator("gpencil.stroke_subdivide", text="SUBDIV").only_selected=True
            item.operator("gpencil.stroke_smooth", text="SMOTH").only_selected=True

            sub.separator(factor=2)

            item = sub.column(align=True)
            op = item.operator("gpencil.stroke_cyclical_set", text="CLOSE")
            op.type='CLOSE'
            op.geometry=True
            item.operator("gpencil.stroke_trim", text="TRIM")
            item.separator(factor=2)
            item.operator("gpencil.stroke_merge", text="MERGE")
            item.operator("gpencil.stroke_join", text="JOIN")

            sub = col.row(align=True)
            sub.alignment = 'CENTER'
            sub.label(text='-----------------------------------------------------')
            sub = col.row(align=True)

            col.separator()
            sub = col.row(align=True)
            sub.prop(gpd, "use_curve_edit", text="",icon='IPO_BEZIER')
            subsub = sub.row(align=True)
            subsub.active = gpd.use_curve_edit
            subsub.popover(panel="VIEW3D_PT_gpencil_curve_edit", text="Curve Editing",)


        if context.mode == 'SCULPT_GPENCIL':
            brush = context.tool_settings.gpencil_paint.brush

            sub = col.row(align=True)
            sub.prop(ts, "use_gpencil_select_mask_point", text="POINT")
            sub.prop(ts, "use_gpencil_select_mask_stroke", text="STROKE")
            sub.prop(ts, "use_gpencil_select_mask_segment", text="SEG")

            sub = col.row(align=True)
            sub.alignment = 'CENTER'
            sub.label(text='-----------------------------------------------------')

            sub = col.split(factor=0.4)
            BrushCopy(self, context, parent=sub)
            subsub = sub.split(factor=0.2)
            subsub.scale_y = 1.4
            subsub.label(text='')
            subsub.menu_contents("VIEW3D_MT_Falloff")
            col.separator()
            sub = col.row(align=True)
            tool_bt(parent=sub, cmd=4, w=2.2, h=1.4, text=True, icon='LARGE')
            tool_bt(parent=sub, cmd=5, w=2.2, h=1.4, text=True, icon='LARGE')
            tool_bt(parent=sub, cmd=6, w=2.2, h=1.4, text=True, icon='LARGE')
            tool_bt(parent=sub, cmd=7, w=2.2, h=1.4, text=True, icon='LARGE')
            tool_bt(parent=sub, cmd=8, w=2.2, h=1.4, text=True, icon='LARGE')
            col.separator()
            sub = col.row(align=True)
            tool_bt(parent=sub, cmd=0, w=2.8, h=1, text=False, icon='OFF')
            tool_bt(parent=sub, cmd=1, w=2.8, h=1, text=False, icon='OFF')
            tool_bt(parent=sub, cmd=2, w=2.8, h=1, text=False, icon='OFF')
            tool_bt(parent=sub, cmd=3, w=2.8, h=1, text=False, icon='OFF')
            sub = col.row(align=True)
            sub.alignment = 'CENTER'
            sub.label(text='-----------------------------------------------------')
            sub = col.row(align=True)
            GPSculptToolSettings(self, context, parent=col)

class SelectMenu(bpy.types.Panel):
    bl_label = "SELECTIONS"
    bl_idname = "OBJECT_PT_select_menu"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'WINDOW'
    bl_context = "scene"
    bl_order = 1000
    bl_options = {'DEFAULT_CLOSED',}

    def draw(self, context):
        layout = self.layout

        edit_mode = context.scene.tool_settings.mesh_select_mode
        col = layout.column(align=True)

        if context.mode == 'OBJECT':

            sub = col.column(align=True)
            sub.scale_y = 0.8
            sub.label(text="Linked")
            sub.ui_units_x = 4
            subsub = sub.row(align=True)
            subsub.operator('object.select_linked', text='DATA').type='OBDATA'
            subsub.operator('object.select_linked', text='MAT').type='MATERIAL'
            subsub = sub.row(align=True)
            subsub.operator('object.select_linked', text='INST').type='DUPGROUP'
            subsub.operator('object.select_linked', text='LIB').type='LIBRARY_OBDATA'

            col.separator(factor = 1)
            sub = col.row(align=True)
            op = sub.operator("xmenu.override2", text="HIERARCHY")
            op.cmd ='object.select_hierarchy'
            op.prop1 ='direction="CHILD"'
            op.prop2 ='extend=True'

            sub = col.row()
            subsub = sub.column()
            subsub.label(text='')
            subsub = sub.column()
            subsub.ui_units_x = 4
            subsub.operator("screen.redo_last", text="CMD >>")

        if context.mode == 'EDIT_MESH':
            sub = col.row(align=True)
            sub.scale_y = 1
            #sub.label(text="SELECT")
            sub.ui_units_x = 4
            sub.operator('mesh.select_all',text='ALL').action='SELECT'
            sub.operator('mesh.select_all',text='CLR').action='DESELECT'
            sub.operator('mesh.select_all',text='INV').action='INVERT'

            col.separator(factor = 2)
            sub = col.column(align=True)
            sub.scale_x = 2
            #sub.label(text="SELECT")
            subsub = sub.row(align=True)
            subsub.alignment = 'CENTER'
            subsub.operator('mesh.select_less', icon='REMOVE', text='')
            subsub.operator('mesh.select_more', icon='ADD',text='')

            col.separator(factor = 2)
            sub = col.row(align=True)
            sub.operator('object.vertex_group_assign_new',text='NEW GRP')
            sub.operator('object.vertex_group_assign',text='ADD')

            col.separator(factor = 1)
            sub = col.row(align=True)
            sub.operator_menu_enum("mesh.select_similar", "type")

            col.separator(factor = 2)
            sub = col.row(align=True)
            sub.operator('mesh.select_linked',text='LINKED')
            sub.operator('mesh.shortest_path_select',text='PATH')
            sub.operator('mesh.faces_select_linked_flat',text='FLAT')

            col.separator(factor = 2)
            sub = col.row(align=True)
            sub.scale_y = 1
            sub.label(text="BY TRAIT")
            sub = col.row(align=True)
            subsub = sub.column(align=True)
            subsub.operator('mesh.select_non_manifold',text='OPEN')
            subsub.operator('mesh.select_loose',text='LOOSE')
            subsub = sub.column(align=True)
            subsub.operator('mesh.select_interior_faces',text='INTERIOR')
            subsub.operator('mesh.select_face_by_sides',text='COUNT')

            sub = col.row()
            subsub = sub.column()
            subsub.label(text='')
            subsub = sub.column()
            subsub.ui_units_x = 4
            subsub.operator("screen.redo_last", text="CMD >>")


        if context.mode == 'EDIT_GPENCIL':
            sub = col.row(align=True)
            sub.scale_y = 1
            #sub.label(text="SELECT")
            sub.ui_units_x = 4
            sub.operator('gpencil.select_all',text='ALL').action='SELECT'
            sub.operator('gpencil.select_all',text='CLR').action='DESELECT'
            sub.operator('gpencil.select_all',text='INV').action='INVERT'

            col.separator(factor = 2)
            sub = col.column(align=True)
            sub.scale_x = 2
            #sub.label(text="SELECT")
            subsub = sub.row(align=True)
            subsub.alignment = 'CENTER'
            subsub.operator('gpencil.select_less', icon='REMOVE', text='')
            subsub.operator('gpencil.select_more', icon='ADD',text='')

            col.separator(factor = 2)
            sub = col.row(align=True)
            subsub = sub.column()
            subsub.label(text='')
            subsub = sub.column()
            subsub.operator('object.vertex_group_add',text='NEW GRP')
            subsub = sub.column()
            subsub.label(text='')

            col.separator(factor = 2)
            sub = col.row(align=True)
            sub.operator('gpencil.select_grouped',text='LAYER').type='LAYER'
            sub.operator('gpencil.select_grouped',text='MAT').type='MATERIAL'
            sub.operator('gpencil.select_linked',text='LINKED')

            col.separator(factor = 2)
            sub = col.row()
            subsub = sub.column()
            subsub.label(text='')
            subsub = sub.column()
            subsub.ui_units_x = 4
            subsub.operator("screen.redo_last", text="CMD >>")



        if context.mode == 'SCULPT':
            sub = col.row()
            SculptMask(self, context, parent=sub)

            sub = col.row(align=True)
            op = sub.operator("sculpt.expand", text="EXP NORM")
            op.target='MASK'
            op.falloff_type='NORMALS'
            op.invert=False

            op = sub.operator("sculpt.expand", text="EXP TOPO")
            op.target='MASK'
            op.falloff_type='GEODESIC'
            op.invert=True

            col.separator(factor=1)
            sub = col.row()
            tool_bt(parent=sub, cmd=13, w=2, h=1.4, text=False, icon='LARGE') 
            subsub = sub.column()
            subsub.ui_units_x = 3.4
            item = subsub.column()
            item.scale_y = 0.5
            item.label(text="MASK")
            grid = subsub.grid_flow(columns=3, align=True)
            tool_bt(parent=grid, cmd=27, w=1.2, h=0.8, text=False, icon='CUSTOM')
            tool_bt(parent=grid, cmd=28, w=1, h=0.8, text=False, icon='CUSTOM')
            tool_bt(parent=grid, cmd=29, w=1.2, h=0.8, text=False, icon='CUSTOM')

            subsub = sub.column()
            subsub.ui_units_x = 2.4
            item = subsub.column()
            item.scale_y = 0.5
            item.label(text="TRIM")
            grid = subsub.grid_flow(columns=2, align=True)
            tool_bt(parent=grid, cmd=16, w=1.2, h=0.8, icon="CUSTOM", text=False)
            tool_bt(parent=grid, cmd=17, w=1.2, h=0.8, icon="CUSTOM", text=False)

            sub = col.row(align=True)
            sub.alignment = 'CENTER'
            sub.label(text='-----------------------------------------------------')

            sub = col.row()
            tool_bt(parent=sub, cmd=14, w=2, h=1.4, text=False, icon='LARGE')
            subsub = sub.column()       
            grid = subsub.grid_flow(columns=2, align=True)
            tool_bt(parent=grid, cmd=30, w=1.5, h=0.75, text=False, icon='CUSTOM')
            tool_bt(parent=grid, cmd=31, w=1.5, h=0.75, text=False, icon='CUSTOM')
            tool_bt(parent=subsub, cmd=32, w=1.2, h=0.5, text=False, icon='OFF')
            tool_bt(parent=sub, cmd=15, w=2.4, h=1.4, text=False, icon='LARGE')

            col.separator(factor = 1)
            sub = col.row(align=True)
            op = sub.operator('sculpt.expand',text='EXP ACTIVE')
            op.target='FACE_SETS'
            op.falloff_type='BOUNDARY_FACE_SET'
            op.invert=False
            op.use_modify_active=True

            op = sub.operator('sculpt.expand',text='EXP TOPO')
            op.target='FACE_SETS'
            op.falloff_type='GEODESIC'
            op.invert=False
            op.use_modify_active=False

            sub.operator('sculpt.face_set_edit',text='+').mode='GROW'
            sub.operator('sculpt.face_set_edit',text='-').mode='SHRINK'

            col.separator()
            sub = col.row()
            SculptFaceSet(self, context, parent=sub)
            sub = col.row(align=True)
            sub.alignment = 'CENTER'
            sub.label(text='-----------------------------------------------------')
            sub = col.row(align=True)
            sub.operator('mesh.face_set_extract', text='EXT FSET')
            sub.operator('mesh.paint_mask_extract', text='EXT MASK')



addon_keymaps = []
classes = (PropMenu, ModesMenu, FileMenu, ToolMenu, SelectMenu)

def register():
    for cls in classes:
        bpy.utils.register_class(cls)

    wm = bpy.context.window_manager
    kc = wm.keyconfigs.addon
    if kc:
        km = wm.keyconfigs.addon.keymaps.new(name='3D View', space_type='VIEW_3D')

        kmi = km.keymap_items.new('wm.call_menu_pie', 'TAB', 'PRESS', ctrl=False, shift=False, alt=False)
        kmi.properties.name = ModesMenu.bl_idname
        addon_keymaps.append((km, kmi))

        kmi = km.keymap_items.new('wm.call_panel', 'SPACE', 'PRESS', ctrl=False, shift=False, alt=False)
        kmi.properties.name = ToolMenu.bl_idname
        #kmi.properties.keep_open = True
        addon_keymaps.append((km, kmi))

        kmi = km.keymap_items.new('wm.call_panel', 'A', 'PRESS', ctrl=False, shift=False, alt=False)
        kmi.properties.name = SelectMenu.bl_idname
        addon_keymaps.append((km, kmi))
    
        km = wm.keyconfigs.addon.keymaps.new(name='Window', space_type='EMPTY')

        kmi = km.keymap_items.new('wm.call_menu_pie', 'S', 'PRESS', ctrl=True, shift=False, alt=False)
        kmi.properties.name = FileMenu.bl_idname
        addon_keymaps.append((km, kmi))

        kmi = km.keymap_items.new('wm.call_panel', 'D', 'PRESS', ctrl=False, shift=False, alt=False)
        kmi.properties.name = PropMenu.bl_idname
        addon_keymaps.append((km, kmi))


def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)

    for km, kmi in addon_keymaps:
        km.keymap_items.remove(kmi)
    addon_keymaps.clear()

