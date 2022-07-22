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

        col = pie.column()
        col.label(text='')

        col = pie.column()
        col.scale_y = 1.2
        ShadingMode(self, context, col)

        col = pie.column()
        col.label(text='')

        col = pie.column()
        col.scale_y = 1.3
        ModeSelector(self, context, col)

#-----------------------------------------------------------------------------------------------------------------------
#PIE-FILE:

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
        col.operator("screen.screenshot_area", text="SCREEN")

        col = pie.column()
        col.popover("OBJECT_PT_import_panel")
        sub = col.row(align=True)
        sub.operator("wm.link", icon='LINK_BLEND', text="LINK")
        sub.operator("wm.append", icon='APPEND_BLEND', text="APND")

        col = pie.column()
        sub = col.row(align=True)
        sub.operator("wm.open_mainfile", text="OPEN")
        sub.menu("TOPBAR_MT_file_open_recent", text="RECENT")

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

            col.separator(factor=2)

#           transform-matrix:
            sub = col.row(align=True)
            Transforms(self, context, layout=sub)
            sub = col.row(align=True)
            Pivot(self, context, layout=sub)

            col.separator(factor=2)

#           add modifiers:
            sub=col.row(align=True)
            ob = context.active_object
            if  ob:
                if ob.type == "MESH" and "CURVE" and "SURFACE" and "TEXT":
                    sub.operator("object.modifier_add", text="", icon="MOD_BEVEL").type='BEVEL'
                    sub.operator("object.modifier_add", text="", icon="MOD_SOLIDIFY").type='SOLIDIFY'
                    sub.operator("object.modifier_add", text="", icon="MOD_SUBSURF").type='SUBSURF'
                    sub.operator("object.modifier_add", text="", icon="MOD_MIRROR").type='MIRROR'
                    sub.operator("object.modifier_add", text="", icon="MOD_REMESH").type='REMESH'
                    sub.operator("object.modifier_add", text="", icon="MOD_DECIM").type='DECIMATE'
                    #sub.separator(factor=1.2)
                    sub.operator_menu_enum("object.modifier_add", "type", text='ADD MOD')
                elif ob.type == "GPENCIL":
                    split = sub.split(factor=0.62)
                    split.label(text="")
                    #sub.separator(factor=1.2)
                    split.operator_menu_enum("object.gpencil_modifier_add", "type", text='ADD MOD')
                elif ob.type == "ARMATURE":
                    sub.label(text=">") 
                else:
                    sub.label(text=">")


            col.separator(factor=1)

#           add objects:
            sub = col.row(align=True)
            sub.operator('mesh.primitive_plane_add', text="", icon='MESH_PLANE')
            sub.operator('mesh.primitive_cube_add', text="", icon='MESH_CUBE')
            sub.operator('mesh.primitive_uv_sphere_add', text="", icon='MESH_UVSPHERE')
            sub.operator('mesh.primitive_cylinder_add', text="", icon='MESH_CYLINDER')
            sub.operator('object.empty_add', text="", icon='EMPTY_DATA')
            sub.operator('object.gpencil_add', text="", icon='GREASEPENCIL').type='EMPTY'
            #sub.separator(factor=1.2)
            sub.menu("VIEW3D_MT_add", text="ADD OBJ", text_ctxt=i18n_contexts.operator_default)

            col.separator(factor=0.2)

#           bool operators:
            sub = col.row(align=True)
            sub.operator('btool.boolean_union', text="", icon='SELECT_EXTEND')
            sub.operator('btool.boolean_diff', text="", icon='SELECT_SUBTRACT')
            sub.operator('btool.boolean_inters', text="", icon='SELECT_INTERSECT')
            sub.operator('btool.boolean_slice', text="", icon='SELECT_DIFFERENCE')
            sub.operator('object.convert', text="CONV",)


#           merge/clone:
            #sub.separator(factor=1)
            sub.operator('object.join', text='MRG')
            sub.operator('object.duplicate_move', text='DUB')
            #sub.operator('object.make_links_data', text='COPY MODS').type='MODIFIERS'

            col.separator(factor=1)

            sub = col.row(align=True)
            sub.scale_y = 0.7 
            sub.label(text="")
            sub.label(text="")
            sub.label(text="")
            sub.label(text="")
            sub.operator("screen.redo_last", text=">")

    #EDIT-----------------------------------------------------------------------------------------------

        if context.mode == 'EDIT_MESH':

            sub = col.row(align=True)

            item = sub.column( )
            item.scale_x = 2.5
            item.template_edit_mode_selection()

            sub.separator(factor=2)
            funct_bt(layout=sub, cmd='xray', tog=True, w=2.4, h=1, label='', icon="XRAY")
            sub.separator(factor=2)

#           automerge:
            ts = context.tool_settings
            item = sub.row(align=True)
            item.scale_x = 2.5
            item.prop(ts, "use_mesh_automerge", text="", toggle=True)
#           stitch-tools:
            item = sub.row(align=True)
            item.scale_x = 2.5    
            item.operator('mesh.target_weld_toggle', text='', icon='CON_TRACKTO') #target_weld



            col.separator(factor=1)

            sub = col.column()
            #sub.ui_units_x = 6
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

            sub = col.row(align=True)
            sub.alignment = 'CENTER'
            sub.label(text='-----------------------------------------------------')

            #---------------------------------------------------------------------

#           mark seams:
            sub = col.row(align=True)
            op = sub.operator('mesh.mark_seam', text='',icon='ADD')
            op = sub.operator('mesh.mark_seam', text='',icon='REMOVE')
            op.clear = True
            sub.separator(factor = 1)

            empty = sub.column()
            empty.ui_units_x = 4
            empty.label(text='')

#           mark sharp:
            op = sub.operator('mesh.mark_sharp', text='',icon='ADD')
            op = sub.operator('mesh.mark_sharp', text='',icon='REMOVE')
            op.clear = True


            col.separator(factor = 1)

#           Edge Tools:
            sub = col.row(align=True)
            sub.ui_units_x = 8
            sub.operator('transform.edge_bevelweight', text='Bevel')
            sub.operator('transform.edge_crease', text='Crease')



#           modifiers ON/OFF:
#           sub.operator("view3d.ml_toggle_all_modifiers", icon="CANCEL", text="")

#           select contour:
            sub.operator('mesh.region_to_loop', text='', icon='CHECKBOX_DEHLT')

#           quick pivot:
            sub.operator('mesh.quick_pivot', text='', icon='SNAP_FACE_CENTER')

            col.separator(factor = 2.5)




#           add mesh:
            sub = col.row(align=True)
            sub.menu("VIEW3D_MT_mesh_add",text='ADD MSH')
            sub.separator(factor = 1)
            item = sub.row(align=True)
            item.scale_x = 2.5
            item.operator('mesh.intersect_boolean', text='', icon='MOD_BOOLEAN')
            item = sub.row(align=True)
            item.scale_x = 2.5
            item.operator('mesh.intersect', text='', icon='FCURVE')

            col.separator(factor = 1)

#           separate mesh:
            sub = col.row(align=True)
            sub.operator_menu_enum("mesh.separate", "type")
            sub.separator(factor = 1)
            item = sub.row(align=True)
            item.scale_x = 2.5
            item .operator('mesh.split', text='', icon='MOD_BOOLEAN')
            item = sub.row(align=True)
            item.scale_x = 2.5
            item .operator('mesh.duplicate_move', text='', icon='XRAY')

            col.separator(factor=1)

#           tools:
            sub = col.row(align=True)
            tool_bt(layout=sub, cmd=20, w=1.2, h=1, text=False, icon='MOD_LINEART')
            empty = sub.column()
            empty.ui_units_x = 1.2
            empty.label(text='')
            sub.separator()
            tool_bt(layout=sub, cmd=29, w=1.2, h=1, text=False, icon='UV_EDGESEL')
            tool_bt(layout=sub, cmd=32, w=1.2, h=1, text=False, icon='EXPORT')
            sub.separator()
            tool_bt(layout=sub, cmd=34, w=1.2, h=1, text=False, icon='CURVE_NCIRCLE')
            sub.separator()
            tool_bt(layout=sub, cmd=18, w=1.2, h=1, text=False, icon='MOD_MESHDEFORM')
            tool_bt(layout=sub, cmd=19, w=1.2, h=1, text=False, icon='MOD_BEVEL')

            sub = col.row(align=True)
            tool_bt(layout=sub, cmd=22, w=1.2, h=1, text=False, icon='SNAP_MIDPOINT')
            tool_bt(layout=sub, cmd=24, w=1.2, h=1, text=False, icon='MOD_DATA_TRANSFER')
            sub.separator()
            tool_bt(layout=sub, cmd=30, w=1.2, h=1, text=False, icon='UV_VERTEXSEL')
            tool_bt(layout=sub, cmd=31, w=1.2, h=1, text=False, icon='IMPORT')
            sub.separator()
            tool_bt(layout=sub, cmd=35, w=1.2, h=1, text=False, icon='TRANSFORM_ORIGINS')
            sub.separator()
            tool_bt(layout=sub, cmd=16, w=1.2, h=1, text=False, icon='MOD_EXPLODE')
            tool_bt(layout=sub, cmd=15, w=1.2, h=1, text=False, icon='MOD_SOLIDIFY')

            col.separator(factor=1)

#           functions:
            sub = col.row(align=True)

            item = sub.column(align=True)
            item.scale_y=0.8
            item.operator('mesh.flip_normals', text='FLIP')
            item.operator('mesh.fill_holes', text='FILL HOLES')

            item = sub.column(align=True)
            item.scale_y=0.8
            item.operator('mesh.remove_doubles', text='CLEAN')
            item.operator('mesh.delete_loose', text='LOOSE')

            sub.separator(factor=2)

            item = sub.column(align=True)
            item.scale_y=0.8
            item.operator('mesh.merge', text="MERGE").type='CENTER'
            item.operator('mesh.edge_face_add', text='FILL')

            col.separator(factor=1)

            sub = col.row(align=True)

            item = sub.column(align=True)
            item.scale_y=0.8
            item.operator('mesh.symmetrize', text='SYM')
            op = item.operator('transform.mirror', text='MIRROR')
            op.orient_type='GLOBAL'
            op.constraint_axis=(True, False, False)

            item = sub.column(align=True)
            item.scale_y=0.8
            item.operator('uv.smart_project', text="A-UV")
            item.operator('uv.unwrap', text="UNWRP")

            sub.separator(factor=2)

#           redo last:
            item = sub.column(align=True)
            item.scale_y=0.8
            item.label(text='')
            item.operator("screen.redo_last", text="CMD >")

    #SCULPT-----------------------------------------------------------------------------------------------

        if context.mode == 'SCULPT':
            brush = context.tool_settings.image_paint.brush

            sub = col.row()
            BrushCopy(self, context, layout=sub)
            tool = context.workspace.tools.from_space_view3d_mode(bpy.context.mode).idname
            subsub = sub.column()
            subsub.scale_y = 1.4
            subsub.ui_units_x = 2
            if tool == 'builtin_brush.Paint':
                brush = context.tool_settings.sculpt.brush
                subsub.prop(brush, "blend", text="")
            else:
                subsub.label(text='')

            subsub = sub.column()
            subsub.ui_units_x = 2
            subsub.scale_y = 1.4
            subsub.menu_contents("VIEW3D_MT_Falloff")

            col.separator(factor=2)
            sub = col.row(align=True)
            subsub = sub.column(align=True)
            subsub.ui_units_x = 2
            subsub.scale_y = 0.7
            subsub.operator('sculpt.set_pivot_position', text='PVT M').mode='UNMASKED'
            subsub.operator('sculpt.set_pivot_position', text='RESET').mode='ORIGIN'
            tool_bt(layout=sub, cmd=18, w=2, h=1.4, text=False, icon='LARGE')
            tool_bt(layout=sub, cmd=0, w=2, h=1.4, text=False, icon='LARGE')
            sub.separator(factor = 1)
            subsub = sub.row(align=True)
            tool_bt(layout=subsub, cmd=19, w=1.2, h=1, text=False, icon='CUSTOM')
            tool_bt(layout=subsub, cmd=21, w=1.2, h=1, text=False, icon='CUSTOM')

            col.separator(factor=1)
            sub = col.row(align=True)
            sub.scale_y = 1.2
            SculptBrushSettings(self, context, layout=sub)

            col.separator(factor=1)
            sub = col.row(align=True)
            tool_bt(layout=sub, cmd=1, w=2, h=1.4, text=False, icon='LARGE')
            tool_bt(layout=sub, cmd=2, w=2, h=1.4, text=False, icon='LARGE')
            tool_bt(layout=sub, cmd=3, w=2, h=1.4, text=False, icon='LARGE')

            sub.separator(factor = 1)
            tool_bt(layout=sub, cmd=7, w=2, h=1.4, text=True, icon='LARGE')

            sub = col.row(align=True)
            tool_bt(layout=sub, cmd=4, w=2, h=1.4, text=False, icon='LARGE')
            tool_bt(layout=sub, cmd=5, w=2, h=1.4, text=False, icon='LARGE')
            tool_bt(layout=sub, cmd=6, w=2, h=1.4, text=False, icon='LARGE')

            sub.separator(factor = 1)
            tool_bt(layout=sub, cmd=8, w=2, h=1.4, text=True, icon='LARGE')

            sub = col.row(align=True)
            tool_bt(layout=sub, cmd=9, w=2, h=1.4, text=False, icon='LARGE')
            tool_bt(layout=sub, cmd=10, w=2, h=1.4, text=False, icon='LARGE')
            tool_bt(layout=sub, cmd=11, w=2, h=1.4, text=False, icon='LARGE')

            sub.separator(factor = 1)
            tool_bt(layout=sub, cmd=12, w=2, h=1.4, text=True, icon='LARGE')

            sub = col.row(align=True)
            sub.alignment = 'CENTER'
            sub.scale_y = 0.6
            sub.label(text='-----------------------------------------------------')

            sub = col.row(align=True)
            subsub = sub.column(align=True)
            subsubsub = subsub.row(align=True)
            tool_bt(layout=subsubsub, cmd=36, w=2, h=1.4, text=True, icon='LARGE')
            tool_bt(layout=subsubsub, cmd=37, w=2, h=1.4, text=True, icon='LARGE')

            Color(self, context, layout=subsub)   
            sub.separator(factor = 1)

            subsub = sub.column(align=True)
            SmoothStroke(self, context, layout=subsub)
            Stroke(self, context, layout=subsub)

            sub = col.row(align=True)
            sub.alignment = 'CENTER'
            sub.scale_y = 0.6
            sub.label(text='-----------------------------------------------------')

            sub = col.row(align=True)
            col.menu_contents("VIEW3D_MT_TextureMask")
            sub = col.row(align=True)
            sub.menu_contents("VIEW3D_MT_BrushTexture")

            #sub = col.row(align=True)
            #ColorPalette(self, context, layout=sub)

    #PAINT TEXTURE -----------------------------------------------------------------------------------------------

        if context.mode == 'PAINT_TEXTURE':
            brush = context.tool_settings.image_paint.brush

            split = col.split(factor=0.5)
            sub = split.row(align=True)
            sub.prop(brush, "blend", text="")
            sub = split.row(align=True)
            subsub = sub.column(align=True)
            subsub.menu_contents("VIEW3D_MT_Falloff")


            sub = col.row(align=True)
            TextureBrushSettings(self, context, layout=sub)
            col.separator(factor = 1)

            sub = col.row(align=True)
            BrushCopy(self, context, layout=sub)
            tool_bt(layout=sub, cmd=0, w=4, h=1.4, text=False, icon='LARGE')
            col.separator(factor = 1)

            sub = col.row(align=True)
            tool_bt(layout=sub, cmd=1, w=2, h=1.4, text=False, icon='LARGE')
            tool_bt(layout=sub, cmd=2, w=2, h=1.4, text=False, icon='LARGE')
            tool_bt(layout=sub, cmd=3, w=2, h=1.4, text=False, icon='LARGE')
            tool_bt(layout=sub, cmd=4, w=2, h=1.4, text=False, icon='LARGE')
            tool_bt(layout=sub, cmd=5, w=2, h=1.4, text=False, icon='LARGE')
            col.separator(factor = 1)

            sub = col.row(align=True)
            ToolOptions(self, context, layout=sub)
            col.separator(factor = 1)

            sub = col.row()
            Color(self, context, layout=sub) 
            subsub = sub.column(align=True)
            SmoothStroke(self, context, layout=subsub)
            Stroke(self, context, layout=subsub)
            col.separator(factor = 1)

            sub = col.row(align=True)
            col.menu_contents("VIEW3D_MT_TextureMask")
            sub = col.row(align=True)
            sub.menu_contents("VIEW3D_MT_BrushTexture")
            col.separator(factor = 1)

            sub = col.row(align=True)
            ColorPalette(self, context, layout=sub)

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
            VertexBrushSettings(self, context, layout=sub)
            col.separator(factor = 1)
            sub = col.row(align=True)
            BrushCopy(self, context, layout=sub)
            tool_bt(layout=sub, cmd=0, w=4, h=1.4, text=False, icon='LARGE')

            col.separator(factor = 1)

            sub = col.row(align=True)
            tool_bt(layout=sub, cmd=1, w=2, h=1.4, text=False, icon='LARGE')
            tool_bt(layout=sub, cmd=2, w=2, h=1.4, text=False, icon='LARGE')
            tool_bt(layout=sub, cmd=3, w=2, h=1.4, text=False, icon='LARGE')
            col.separator(factor = 1)

            sub = col.row()
            Color(self, context, layout=sub)   

            subsub = sub.column(align=True)
            SmoothStroke(self, context, layout=subsub)
            Stroke(self, context, layout=subsub)
            col.separator(factor = 1)

            sub = col.row(align=True)
            col.menu_contents("VIEW3D_MT_TextureMask")
            sub = col.row(align=True)
            sub.menu_contents("VIEW3D_MT_BrushTexture")
            col.separator(factor = 1)

            sub = col.row(align=True)
            ColorPalette(self, context, layout=sub)

    #PAINT WEIGHT-----------------------------------------------------------------------------------------------

        if context.mode == 'PAINT_WEIGHT':
            brush = context.tool_settings.vertex_paint.brush

            split = col.split(factor=0.5)
            sub = split.row(align=True)
            sub.prop(brush, "blend", text="")
            sub = split.row(align=True)
            subsub = sub.column(align=True)
            subsub.ui_units_x = 2
            subsub.menu_contents("VIEW3D_MT_Falloff")

            sub = col.row(align=True)
            sub.prop(brush, "use_frontface", text="FRONT", toggle=True)
            sub.prop(brush, "use_accumulate", text="ACCU", toggle=True)
            col.separator(factor = 1)

            sub = col.row(align=True)
            BrushCopy(self, context, layout=sub)
            tool_bt(layout=sub, cmd=0, w=4, h=1.4, text=False, icon='LARGE')
            col.separator(factor = 1)

            sub = col.row(align=True)
            tool_bt(layout=sub, cmd=1, w=2, h=1.4, text=False, icon='LARGE')
            tool_bt(layout=sub, cmd=2, w=2, h=1.4, text=False, icon='LARGE')
            tool_bt(layout=sub, cmd=3, w=2, h=1.4, text=False, icon='LARGE')
            tool_bt(layout=sub, cmd=4, w=2, h=1.4, text=False, icon='LARGE')
            tool_bt(layout=sub, cmd=5, w=2, h=1.4, text=False, icon='LARGE')
            tool_bt(layout=sub, cmd=6, w=2, h=1.4, text=False, icon='LARGE')
            col.separator(factor = 1)

            sub = col.row()

            subsub = sub.column(align=True)
            subsub.ui_units_x = 4
            ts = context.tool_settings
            wp = ts.weight_paint
            subsub.prop(ts, "use_auto_normalize", text="NORM", toggle=True)
            subsub.prop(ts, "use_lock_relative", text="RELAT", toggle=True)
            subsub.prop(ts, "use_multipaint", text="MPAINT", toggle=True)
            subsub.prop(wp, "use_group_restrict", text="RESTR", toggle=True)

            subsub = sub.column(align=True)
            subsub.ui_units_x = 4
            SmoothStroke(self, context, layout=subsub)
            Stroke(self, context, layout=subsub)


            col.separator(factor = 1)



    #GP DRAW-----------------------------------------------------------------------------------------------

        if context.mode == 'PAINT_GPENCIL':
            brush = context.tool_settings.gpencil_paint.brush
            gp_settings = brush.gpencil_settings

            sub = col.row(align=True)
            split = sub.split(factor=0.5)         
            BrushCopy(self, context, layout=split)
            col.separator()
            tool_bt(layout=split, cmd=0, w=2.4, h=1.4, text=False, icon='LARGE')
            sub = col.row(align=True)
            tool_bt(layout=sub, cmd=1, w=2.4, h=1.4, text=False, icon='LARGE')
            tool_bt(layout=sub, cmd=2, w=2.4, h=1.4, text=False, icon='LARGE')
            tool_bt(layout=sub, cmd=3, w=2.4, h=1.4, text=False, icon='LARGE')
            tool_bt(layout=sub, cmd=4, w=2.4, h=1.4, text=False, icon='LARGE')
            tool_bt(layout=sub, cmd=5, w=2.4, h=1.4, text=False, icon='LARGE')
            sub = col.row(align=True)
            tool_bt(layout=sub, cmd=6, w=1.2, h=1, text=False, icon='IPO_LINEAR')
            tool_bt(layout=sub, cmd=7, w=1.2, h=1, text=False, icon='IPO_CONSTANT')
            tool_bt(layout=sub, cmd=8, w=1.2, h=1, text=False, icon='IPO_EASE_OUT')
            tool_bt(layout=sub, cmd=9, w=1.2, h=1, text=False, icon='IPO_EASE_IN_OUT')
            tool_bt(layout=sub, cmd=10, w=1.2, h=1, text=False, icon='MESH_PLANE')
            tool_bt(layout=sub, cmd=11, w=1.2, h=1, text=False, icon='MESH_CIRCLE')

            col.separator()

            sub = col.row()
            subsub = sub.column(align=True)
            GPSmoothStroke(self, context, layout=subsub)

            subsub = sub.column(align=True)


            item = subsub.row(align=True)
            item.prop(ts, "use_gpencil_draw_onback", text="", icon='MOD_OPACITY', toggle=True)
            item.separator(factor=0.4)
            item.prop(ts, "use_gpencil_automerge_strokes", text="", toggle=True)


            item = subsub.row(align=True)
            item.prop(ts, "use_gpencil_weight_data_add", text="", icon='WPAINT_HLT', toggle=True)
            item.prop(ts, "use_gpencil_draw_additive", text="", icon='FREEZE', toggle=True)
            item.prop(gpd, "use_multiedit", text="", icon='GP_MULTIFRAME_EDITING', toggle=True)

            col.separator()

            sub = col.row(align=True)
            sub.popover("VIEW3D_PT_tools_grease_pencil_brush_post_processing")
            sub.popover("VIEW3D_PT_tools_grease_pencil_brush_random")
            sub.popover("VIEW3D_PT_tools_grease_pencil_brush_advanced")

    #GP EDIT -----------------------------------------------------------------------------------------------

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
            tool_bt(layout=sub, cmd=0, w=2, h=1.4, text=False, icon='LARGE')
            tool_bt(layout=sub, cmd=1, w=2, h=1.4, text=False, icon='LARGE')
            tool_bt(layout=sub, cmd=2, w=2, h=1.4, text=False, icon='LARGE')
            tool_bt(layout=sub, cmd=3, w=2, h=1.4, text=False, icon='LARGE')
            tool_bt(layout=sub, cmd=4, w=2, h=1.4, text=False, icon='LARGE')
            sub = col.row(align=True)
            tool_bt(layout=sub, cmd=5, w=2, h=1.4, text=False, icon='LARGE')
            tool_bt(layout=sub, cmd=6, w=2, h=1.4, text=False, icon='LARGE')
            tool_bt(layout=sub, cmd=7, w=2, h=1.4, text=False, icon='LARGE')
            tool_bt(layout=sub, cmd=8, w=2, h=1.4, text=False, icon='LARGE')

            col.separator()
            sub = col.split(factor=0.75)
            GPToolSettings(self, context, layout=sub)
            sub.separator()
            ToolOptions(self, context, layout=sub ) 


            col.separator()
            sub = col.row(align=True)
            subsub = sub.column(align=True)
            tool_bt(layout=subsub, cmd=9, w=2, h=1, text=True, icon='OFF')
            tool_bt(layout=subsub, cmd=10, w=2, h=1, text=True, icon='OFF')
            subsub = sub.column(align=True)
            tool_bt(layout=subsub, cmd=11, w=2, h=1, text=True, icon='OFF')
            tool_bt(layout=subsub, cmd=12, w=2, h=1, text=True, icon='OFF')
            subsub = sub.column(align=True)
            tool_bt(layout=subsub, cmd=13, w=2, h=1, text=True, icon='OFF')
            sub.separator(factor=1)
            subsub = sub.column(align=True)
            tool_bt(layout=subsub, cmd=14, w=2, h=1, text=True, icon='OFF')
            tool_bt(layout=subsub, cmd=15, w=2, h=1, text=True, icon='OFF')

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

    #GP SCULPT-----------------------------------------------------------------------------------------------

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
            BrushCopy(self, context, layout=sub)
            subsub = sub.split(factor=0.2)
            subsub.scale_y = 1.4
            subsub.label(text='')
            subsub.menu_contents("VIEW3D_MT_Falloff")
            col.separator()
            sub = col.row(align=True)
            tool_bt(layout=sub, cmd=4, w=2.2, h=1.4, text=True, icon='LARGE')
            tool_bt(layout=sub, cmd=5, w=2.2, h=1.4, text=True, icon='LARGE')
            tool_bt(layout=sub, cmd=6, w=2.2, h=1.4, text=True, icon='LARGE')
            tool_bt(layout=sub, cmd=7, w=2.2, h=1.4, text=True, icon='LARGE')
            tool_bt(layout=sub, cmd=8, w=2.2, h=1.4, text=True, icon='LARGE')
            col.separator()
            sub = col.row(align=True)
            tool_bt(layout=sub, cmd=0, w=2.8, h=1, text=False, icon='OFF')
            tool_bt(layout=sub, cmd=1, w=2.8, h=1, text=False, icon='OFF')
            tool_bt(layout=sub, cmd=2, w=2.8, h=1, text=False, icon='OFF')
            tool_bt(layout=sub, cmd=3, w=2.8, h=1, text=False, icon='OFF')
            sub = col.row(align=True)
            sub.alignment = 'CENTER'
            sub.label(text='-----------------------------------------------------')
            sub = col.row(align=True)
            GPSculptToolSettings(self, context, layout=col)


#-----------------------------------------------------------------------------------------------------------------------
#PANEL-X2:


class PropMenu(bpy.types.Panel):
    bl_label = "X-2"
    bl_idname = "OBJECT_PT_main_menu"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'WINDOW'
    bl_context = "scene"

    def draw(self, context):
        layout = self.layout

##---------------------------------------------------------------------------------------------------------------------

        if context.mode == 'OBJECT':
            col = layout.column()
            col.menu_contents("VIEW3D_MT_Material")
            UVTexture(self, context, layout=col)

##---------------------------------------------------------------------------------------------------------------------

        if context.mode == 'EDIT_MESH':
            col = layout.column()

#           vertex group:
            sub = col.row(align=True)
            sub.operator('object.vertex_group_assign_new', text='Vertex Group   ')
            sub.operator('object.vertex_group_remove',text='',icon='BLANK1')
            sub.operator('object.vertex_group_assign',text='',icon='ADD')
            sub.operator('object.vertex_group_remove_from',text='',icon='REMOVE')
            sub.separator(factor = 1)
            sub.operator('object.vertex_group_select',text='',icon='RADIOBUT_ON')
            sub.operator('object.vertex_group_deselect',text='',icon='RADIOBUT_OFF')

#           vertex-window:
            sub = col.row(align=True)
            ob = context.active_object
            group = ob.vertex_groups.active
            #sub.ui_units_x = 6
            sub.template_list("MESH_UL_vgroups", "", ob, "vertex_groups", ob.vertex_groups, "active_index", rows=1)

            col.separator(factor = 2.5)

#           materials:
            sub = col.row(align=True)
            sub.menu("MATERIAL_MT_context_menu", text="Material")
            sub.operator('object.material_slot_assign',text='',icon='BLANK1')
            sub.operator('object.material_slot_add',text='',icon='ADD')
            sub.operator('object.material_slot_remove',text='',icon='REMOVE')
            sub.separator(factor = 1)
            sub.operator('object.material_slot_select',text='',icon='RADIOBUT_ON')
            sub.operator('object.material_slot_deselect',text='',icon='RADIOBUT_OFF')

#           material-window:
            sub = col.row(align=True)
            ob = context.active_object
            mat = ob.active_material
            slot = ob.material_slots
            space = context.space_data
            #sub.ui_units_x = 7
            sub.template_list("MATERIAL_UL_matslots", "", ob, "material_slots", ob, "active_material_index", rows=1)
            col.separator(factor = 1)
            col.template_ID(ob, "active_material")
            col.operator("xm.override", icon='ADD', text="NEW").cmd='material.new'
##---------------------------------------------------------------------------------------------------------------------

        if context.mode == 'PAINT_TEXTURE':
            col = layout.column()
            TexSlots(self, context, layout=col)
            col.menu_contents("VIEW3D_MT_Material")
            UVTexture(self, context, layout=col)

##---------------------------------------------------------------------------------------------------------------------

        if context.mode == 'SCULPT':
            col = layout.column()
            col.menu_contents("VIEW3D_MT_dynamesh")

            col.separator(factor = 1)
            col.menu_contents("VIEW3D_MT_remesh")

            col.separator(factor = 1)
            subrow = col.row(align=False)
            subcol = subrow.column(align=False)
            subcol.ui_units_x = 3
            item = subcol.row()
            item.scale_y = 0.5
            item.label(text='FILTER')
            item = subcol.row()
            tool_bt(layout=item, cmd=33, w=3, h=1, text=False, icon='OFF')
            item = subcol.row()
            tool_bt(layout=item, cmd=34, w=3, h=1, text=False, icon='OFF')
            item = subcol.row()
            tool_bt(layout=item, cmd=35, w=3, h=1, text=False, icon='OFF')

            col.separator(factor = 1)
            SculptFilterSettings(self, context, layout=subrow)

            col.separator(factor = 1)
            VertexColor(self, context, layout=col)

##---------------------------------------------------------------------------------------------------------------------

        if context.mode == 'PAINT_VERTEX':
            col = layout.column()
            VertexColor(self, context, layout=col)

##---------------------------------------------------------------------------------------------------------------------

        if context.mode == 'PAINT_WEIGHT':
            col = layout.column()
            VertexGroups(self, context, layout=col)

##---------------------------------------------------------------------------------------------------------------------

        if bpy.context.mode == 'PAINT_GPENCIL':
            col = layout.column()
            GPLayers(self, context, layout=col)
            col.menu_contents("VIEW3D_MT_Material")
            col.menu("GPENCIL_MT_material_context_menu")
            col.menu_contents("VIEW3D_MT_GPStroke")
            col.menu_contents("VIEW3D_MT_GPFill")

##---------------------------------------------------------------------------------------------------------------------

        if bpy.context.mode == 'EDIT_GPENCIL':
            col = layout.column()
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

        edit_mode = context.scene.tool_settings.mesh_select_mode
        col = layout.column(align=True)

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
            sub = col.row(align=True)
            op = sub.operator("xm.override2", text="HIERARCHY")
            op.cmd ='object.select_hierarchy'
            op.prop1 ='direction="CHILD"'
            op.prop2 ='extend=True'

            col.separator(factor = 2)

            sub = col.row()
            subsub = sub.column()
            subsub.label(text='')
            subsub = sub.column()
            subsub.ui_units_x = 4
            subsub.operator("screen.redo_last", text="CMD >>")

    #EDIT-----------------------------------------------------------------------------------------------

        if context.mode == 'EDIT_MESH':
            sub = col.row(align=True)
            sub.scale_x = 2
            sub.operator('mesh.select_all',text='',icon='SHADING_SOLID').action='SELECT'
            sub.operator('mesh.select_all',text='', icon='IMAGE_ALPHA').action='INVERT'

            sub.separator(factor = 4)

            sub.operator('mesh.select_less', icon='REMOVE', text='')
            sub.operator('mesh.select_more', icon='ADD',text='')

            col.separator(factor = 2)
            sub = col.row(align=True)
            sub.operator('object.vertex_group_assign_new',text='VERTEX GRP')
            item = sub.row(align=True)
            item.scale_x = 1.2
            item.operator('object.vertex_group_assign',text='',icon='CHECKMARK')



            col.separator(factor = 2)
            sub = col.row(align=True)
            sub.operator('mesh.select_linked',text='LINKED')
            sub.operator('mesh.shortest_path_select',text='PATH')
            sub.operator('mesh.faces_select_linked_flat',text='FLAT')
            sub.separator(factor = 2)
            sub.operator('mesh.select_mirror',text='MIRROR')

            col.separator(factor = 2)


            sub = col.row(align=True)
            sub.operator_menu_enum("mesh.select_similar", "type")
            sub.operator_menu_enum("mesh.select_linked", "delimit")

            col.separator(factor = 2)

            sub = col.row(align=True)
            sub.operator('mesh.select_non_manifold',text='OPEN')
            sub.operator('mesh.select_loose',text='LOOSE')
            sub.operator('mesh.select_interior_faces',text='INTERIOR')
            sub.operator('mesh.select_face_by_sides',text='COUNT')

            col.separator(factor = 2)

            sub = col.row()
            subsub = sub.column()
            subsub.label(text='')
            subsub = sub.column()
            subsub.ui_units_x = 4
            subsub.operator("screen.redo_last", text="CMD >>")

    #GP EDIT-----------------------------------------------------------------------------------------------

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


    #SCULPT-----------------------------------------------------------------------------------------------
        if context.mode == 'SCULPT':

            sub = col.row()
            SculptMask(self, context, layout=sub)
            sub = col.row(align=True)
            op = sub.operator("sculpt.expand", text="NORM>")
            op.target='MASK'
            op.falloff_type='NORMALS'
            op.invert=False
            op = sub.operator("sculpt.expand", text="TOPO>")
            op.target='MASK'
            op.falloff_type='GEODESIC'
            op.invert=True
            sub.operator('sculpt.dirty_mask', text='CURV')
            col.separator(factor=1)

            sub = col.row()
            tool_bt(layout=sub, cmd=13, w=2, h=1.4, text=False, icon='LARGE') 
            subsub = sub.column()
            subsub.ui_units_x = 3.4
            item = subsub.column()
            item.scale_y = 0.5
            item.label(text="MASK")
            grid = subsub.grid_flow(columns=3, align=True)
            tool_bt(layout=grid, cmd=27, w=1.2, h=0.8, text=False, icon='CUSTOM')
            tool_bt(layout=grid, cmd=28, w=1, h=0.8, text=False, icon='CUSTOM')
            tool_bt(layout=grid, cmd=29, w=1.2, h=0.8, text=False, icon='CUSTOM')

            subsub = sub.column()
            subsub.ui_units_x = 2.4
            item = subsub.column()
            item.scale_y = 0.5
            item.label(text="TRIM")
            grid = subsub.grid_flow(columns=2, align=True)
            tool_bt(layout=grid, cmd=16, w=1.2, h=0.8, icon="CUSTOM", text=False)
            tool_bt(layout=grid, cmd=17, w=1.2, h=0.8, icon="CUSTOM", text=False)

            sub = col.row(align=True)
            sub.scale_y = 0.6
            sub.alignment = 'CENTER'
            sub.label(text='-----------------------------------------------------')

            sub = col.row()
            tool_bt(layout=sub, cmd=14, w=2, h=1.4, text=False, icon='LARGE')
            subsub = sub.column()       
            grid = subsub.grid_flow(columns=2, align=True)
            tool_bt(layout=grid, cmd=30, w=1.5, h=0.75, text=False, icon='CUSTOM')
            tool_bt(layout=grid, cmd=31, w=1.5, h=0.75, text=False, icon='CUSTOM')
            tool_bt(layout=subsub, cmd=32, w=1.2, h=0.5, text=False, icon='OFF')
            tool_bt(layout=sub, cmd=15, w=2.4, h=1.4, text=False, icon='LARGE')
            col.separator(factor = 1)

            sub = col.row(align=True)
            op = sub.operator('sculpt.expand',text='ACTIVE>')
            op.target='FACE_SETS'
            op.falloff_type='BOUNDARY_FACE_SET'
            op.invert=False
            op.use_modify_active=True

            op = sub.operator('sculpt.expand',text='TOPO>')
            op.target='FACE_SETS'
            op.falloff_type='GEODESIC'
            op.invert=False
            op.use_modify_active=False

            item = sub.row(align=True)
            item.scale_y = 1
            item.scale_x = 1.4
            item.operator('sculpt.face_set_edit',text='', icon='REMOVE').mode='SHRINK'
            item.operator('sculpt.face_set_edit',text='', icon='ADD').mode='GROW'

            col.separator()
            sub = col.row()
            SculptFaceSet(self, context, layout=sub)
            sub = col.row(align=True)
            sub.alignment = 'CENTER'
            sub.scale_y = 0.6
            sub.label(text='-----------------------------------------------------')
            sub = col.row(align=True)
            sub.operator('mesh.face_set_extract', text='EXT FSET')
            sub.operator('mesh.paint_mask_extract', text='EXT MASK')


#-----------------------------------------------------------------------------------------------------------------------

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
        kmi.properties.keep_open = True
        addon_keymaps.append((km, kmi))

        kmi = km.keymap_items.new('wm.call_panel', 'A', 'PRESS', ctrl=True, shift=False, alt=False)
        kmi.properties.name = SelectMenu.bl_idname
        addon_keymaps.append((km, kmi))

        kmi = km.keymap_items.new('xm.toolhud', 'A', 'PRESS', ctrl=False, shift=False, alt=False)
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

