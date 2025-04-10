import bpy
import os

from bpy.types import Menu, Panel, UIList, AddonPreferences
from bpy.props import StringProperty, IntProperty, BoolProperty
from bl_ui.space_toolsystem_common import (ToolSelectPanelHelper,ToolDef)
from bpy.app.translations import contexts as i18n_contexts
from rna_prop_ui import PropertyPanel
from collections import defaultdict
import addon_utils

from .functions import tool_bt, funct_bt, paint_settings, update_normaldisp, get_brush_mode

#LAYOUT----------------------------------------------------------------------------------------------


def InsertSpace(layout, space=0):
    col = layout.column()
    col.ui_units_x = space
    col.separator()

def InsertLine(layout):
    row = layout.row(align=True)
    row.scale_y = 0.6
    row.alignment = 'CENTER'
    row.label(text='-----------------------------------------------------')


#MODES-MENU >> TAB ----------------------------------------------------------------------------------

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
        sub = col.row(align=True)
        sub.operator("wm.link", icon='LINK_BLEND', text="LINK")
        sub.operator("wm.append", icon='APPEND_BLEND', text="APND")
        sub = col.row(align=True)
        col.label(text='')
        sub = col.row()
        sub.label(text='')
        sub.separator(factor=2)
        sub.popover("OBJECT_PT_import_panel", text="IMPORT")
        sub = col.row()
        sub.label(text='')
        sub.separator(factor=2)
        sub.popover("OBJECT_PT_export_panel", text="EXPORT")

        #shading
        col = pie.column()
        col.ui_units_x = 5.8
        #col.scale_x = 1.5
        col.label(text='')
        col.scale_y = 1.2
        ShadingMode(self, context, col)
        col.label(text='')
        sub = col.row()
        sub.operator("screen.screenshot_area", text="SCREEN")
        #sub.label(text='')
        col.label(text='')
        sub = col.row()
        sub.prop(context.scene, "version_number", text="HOU")
        #sub.label(text='')
        sub = col.row(align=True)
        sub.operator("hb.export_to_houdini", text="SEND")
        sub.operator("hb.refresh_from_houdini", text="REFRESH")
        #sub.label(text='')

        #empty
        col = pie.column()
        col.label(text='')

        #modes
        col = pie.column()
        col.scale_y = 1.3
        ModeSelector(self, context, col)


#HUD-----------------------------------------------------------------------------------------------
def ModeSelector(self, context, layout):
    active = context.active_object
    col = layout.column(align=False)
    col.ui_units_x = 10
    col.scale_x = 1.5
    row = col.row(align=True)
    row.alignment = 'RIGHT'
    if active:
        if active.type == 'MESH':
            if context.area.type == "VIEW_3D":
                sub = row.row(align=True)
                sub.active = False if context.mode == ' ' else True
                sub.operator("xm.surface_draw_mode", text="", icon="GREASEPENCIL")
                if context.active_object.particle_systems:
                    sub = row.row(align=True)
                    sub.active = False if context.mode == 'PARTICLE_EDIT' else True
                    sub.operator("object.mode_set", text="", icon="PARTICLEMODE").mode = 'PARTICLE_EDIT'
                sub = row.row(align=True)
                sub.active = False if context.mode == 'PAINT_WEIGHT' else True
                sub.operator("object.mode_set", text="", icon="WPAINT_HLT").mode = 'WEIGHT_PAINT'
                sub = row.row(align=True)
                sub.active = False if context.mode == 'PAINT_TEXTURE' else True
                sub.operator("object.mode_set", text="", icon="TPAINT_HLT").mode = 'TEXTURE_PAINT'
                sub = row.row(align=True)
                sub.active = False if context.mode == 'PAINT_VERTEX' else True
                sub.operator("object.mode_set", text="", icon="VPAINT_HLT").mode = 'VERTEX_PAINT'
                sub = row.row(align=True)
                sub.active = False if context.mode == 'SCULPT' else True
                sub.operator("object.mode_set", text="", icon="SCULPTMODE_HLT").mode = 'SCULPT'
                sub = row.row(align=True)
                sub.active = False if context.mode == 'OBJECT' else True
                sub.operator("object.mode_set", text="", icon="OBJECT_DATA").mode = 'OBJECT'
                sub = row.row(align=True)
                sub.active = False if context.mode == 'EDIT_MESH' else True
                sub.operator("object.mode_set", text="", icon="EDITMODE_HLT").mode = 'EDIT'
        elif active.type == 'ARMATURE':
            sub = row.row(align=True)
            sub.active = False if context.mode == 'EDIT_ARMATURE' else True
            sub.operator("object.mode_set", text="Edit Mode", icon='EDITMODE_HLT').mode = "EDIT"
            sub = row.row(align=True)
            sub.active = False if context.mode == 'POSE' else True
            sub.operator("object.mode_set", text="Pose", icon='POSE_HLT').mode = "POSE"
            sub = row.row(align=True)
            sub.active = False if context.mode == 'OBJECT' else True
            sub.operator("object.mode_set", text="", icon="OBJECT_DATA").mode = 'OBJECT'
        elif active.type in ['CURVE', 'FONT', 'SURFACE', 'META', 'LATTICE']:
            sub = row.row(align=True)
            sub.active = False if context.mode ==  ['EDIT_CURVE', 'EDIT_TEXT', 'EDIT_SURFACE', 'EDIT_METABALL', 'EDIT_LATTICE'] else True
            sub.operator("object.mode_set", text="Edit Mode", icon='EDITMODE_HLT').mode = "EDIT"
            sub = row.row(align=True)
            sub.active = False if context.mode == 'OBJECT' else True
            sub.operator("object.mode_set", text="", icon="OBJECT_DATA").mode = 'OBJECT'
        elif active.type == 'GPENCIL':                
            sub = row.row(align=True)
            subsub = sub.box()
            subsub.label(text=' GP ')
            sub.active = False if context.mode == "WEIGHT_GPENCIL" else True
            sub.operator("object.mode_set", text="", icon="WPAINT_HLT").mode = 'WEIGHT_GPENCIL'
            sub = row.row(align=True)
            sub.active = False if context.mode == "PAINT_GPENCIL" else True
            sub.operator("object.mode_set", text="", icon="GREASEPENCIL").mode = 'PAINT_GPENCIL'
            sub = row.row(align=True)
            sub.active = False if context.mode == "SCULPT_GPENCIL" else True
            sub.operator("object.mode_set", text="", icon="SCULPTMODE_HLT").mode = 'SCULPT_GPENCIL'
            sub = row.row(align=True)
            sub.active = False if context.mode == "OBJECT" else True
            sub.operator("object.mode_set", text="", icon="OBJECT_DATA").mode = 'OBJECT'
            sub = row.row(align=True)
            sub.active = False if context.mode == 'EDIT_GPENCIL' else True
            sub.operator("object.mode_set", text="", icon="EDITMODE_HLT").mode = 'EDIT_GPENCIL'
        elif active.type == 'EMPTY':
            sub = row.row(align=True)
            sub.label(text="NONE")
    else:
        sub = row.row(align=True)
        sub.label(text="<<")

def PaintHud(layout, brush, self, context):
    ts = context.tool_settings
    ups = ts.unified_paint_settings
    ptr = ups if ups.use_unified_size else paint_settings(context).brush
    pts = ups if ups.use_unified_strength else paint_settings(context).brush
    row = layout.row(align=True)
    row.scale_x = 1.2
    row.operator("brush.scale_size", icon='TRIA_LEFT', text="").scalar=0.8
    row = layout.row(align=True)
    row.ui_units_x = 6
    row.prop(ptr, "size", slider=True)
    row.prop(brush, "use_pressure_size", slider=True, text="")
    row = layout.row(align=True)
    row.scale_x = 1.2
    row.operator("brush.scale_size", icon='TRIA_RIGHT', text="").scalar=1.2
    layout.separator(factor = 1)
    row = layout.row(align=True)
    row.ui_units_x = 6
    row.prop(pts, "strength", slider=True)
    row.prop(brush, "use_pressure_strength", slider=True, text="")

def GPPaintHud(layout, context, brush, *, compact=True):
    tool_settings = context.tool_settings
    settings = tool_settings.gpencil_paint
    gp_settings = brush.gpencil_settings
    tool = context.workspace.tools.from_space_view3d_mode(context.mode, create=False)
    if gp_settings is None:
        return
    if brush.gpencil_tool == 'ERASE':
        row = layout.row(align=True)

        row.prop(brush, "size", text="Radius")
        row.prop(gp_settings, "use_pressure", text="", icon='STYLUS_PRESSURE')
        row.prop(gp_settings, "use_occlude_eraser", text="", icon='XRAY')
        row.prop(gp_settings, "use_default_eraser", text="")
        row = layout.row(align=True)

        row.prop(gp_settings, "eraser_mode", expand=True)
        if gp_settings.eraser_mode == 'SOFT':
            row = layout.row(align=True)

            row.prop(gp_settings, "pen_strength", slider=True, text='STR')
            row.prop(gp_settings, "use_strength_pressure", text="", icon='STYLUS_PRESSURE')
            row = layout.row(align=True)

            row.prop(gp_settings, "eraser_strength_factor", text='S')
            row = layout.row(align=True)

            row.prop(gp_settings, "eraser_thickness_factor", text='T')
        else:
            row = layout.row(align=True)

            row.label(text=">")
    elif brush.gpencil_tool == 'FILL':
        use_property_split_prev = layout.use_property_split
        if compact:
            row = layout.row(align=True)
            row.prop(gp_settings, "fill_direction", text="", expand=True)
        else:
            layout.use_property_split = False
            row = layout.row(align=True)
            row.prop(gp_settings, "fill_direction", expand=True)

        row = layout.row(align=True)
        row.ui_units_x = 6
        row.prop(gp_settings, "fill_factor")
        row = layout.row(align=True)
        row.ui_units_x = 6
        row.prop(gp_settings, "dilate")
        row = layout.row(align=True)
        row.ui_units_x = 6
        row.prop(brush, "size", text="Thickness")
        layout.use_property_split = use_property_split_prev
    else:  # brush.gpencil_tool == 'DRAW/TINT':
        row = layout.row(align=True)

        sub = row.row(align=True)
        sub.scale_x = 1.2
        sub.operator("brush.scale_size", icon='TRIA_LEFT', text="").scalar=0.8

        row.prop(brush, "size", text="Radius")
        row.prop(gp_settings, "use_pressure", text="", icon='STYLUS_PRESSURE')

        sub = row.row(align=True)
        sub.scale_x = 1.2
        sub.operator("brush.scale_size", icon='TRIA_RIGHT', text="").scalar=1.2

        row.separator()

        if gp_settings.use_pressure and not compact:
            col = layout.column()
            col.template_curve_mapping(gp_settings, "curve_sensitivity", brush=True,
                                       use_negative_slope=True)
        row = layout.row(align=True)
        row.prop(gp_settings, "pen_strength", slider=True)
        row.prop(gp_settings, "use_strength_pressure", text="", icon='STYLUS_PRESSURE')

        if gp_settings.use_strength_pressure and not compact:
            col = layout.column()
            col.template_curve_mapping(gp_settings, "curve_strength", brush=True,
                                       use_negative_slope=True)
        if brush.gpencil_tool == 'TINT':
            row = layout.row(align=True)
            row.prop(gp_settings, "vertex_mode", text="Mode")
        else:
            row = layout.row(align=True)
            if context.region.type == 'TOOL_HEADER':
                row.prop(gp_settings, "caps_type", text="", expand=True)
            else:
                row.prop(gp_settings, "caps_type", text="Caps Type")
    if tool.idname in {"builtin.arc", "builtin.curve", "builtin.line", "builtin.box", "builtin.circle", "builtin.polyline"}:
        settings = context.tool_settings.gpencil_sculpt
        if compact:
            row = layout.row(align=True)
            row.prop(settings, "use_thickness_curve", text="", icon='SPHERECURVE')
            sub = row.row(align=True)
            sub.active = settings.use_thickness_curve
            sub.popover(panel="TOPBAR_PT_gpencil_primitive", text="Thickness Profile",)
        else:
            row = layout.row(align=True)
            row.prop(settings, "use_thickness_curve", text="Use Thickness Profile")
            sub = row.row(align=True)
            if settings.use_thickness_curve:
                # Curve
                layout.template_curve_mapping(settings, "thickness_primitive_curve", brush=True)

def ColorHud(self, context, layout):
    ts = context.tool_settings
    ups = ts.unified_paint_settings
    if context.mode == 'PAINT_VERTEX':
        ptr = ts.vertex_paint.brush
    if context.mode == 'SCULPT':
        ptr = ts.sculpt.brush
    else:
        ptr = ups if ups.use_unified_color else paint_settings(context).brush

    row = layout.row(align=True)
    sub = row.row(align=True)
    sub.prop(ptr, 'color', text="")
    sub = row.row(align=True)
    sub.operator("paint.brush_colors_flip", icon='FILE_REFRESH', text="")

def GPColorHud(self, context, layout):
    tool_settings = context.scene.tool_settings
    settings = tool_settings.gpencil_paint
    brush = context.tool_settings.gpencil_paint.brush
    gp_settings = brush.gpencil_settings
    ma = gp_settings.material
    row = layout.row(align=True)
    if brush.gpencil_tool in {'DRAW', 'FILL'}:
        sub = row.row(align=True)
        if gp_settings.pin_draw_mode:
            sub.prop_enum(gp_settings, "brush_draw_mode", 'MATERIAL', text="", icon='MATERIAL')
            sub.prop_enum(gp_settings, "brush_draw_mode", 'VERTEXCOLOR', text="", icon='VPAINT_HLT')
        else:
            sub.prop_enum(settings, "color_mode", 'MATERIAL', text="", icon='MATERIAL')
            sub.prop_enum(settings, "color_mode", 'VERTEXCOLOR', text="", icon='VPAINT_HLT')
        sub = row.row(align=True)

        sub.enabled = settings.color_mode == 'VERTEXCOLOR' or gp_settings.brush_draw_mode == 'VERTEXCOLOR'

        sub.prop_with_popover(brush, "color", text="", panel="TOPBAR_PT_gpencil_vertexcolor")
        sub.operator("gpencil.tint_flip", icon='FILE_REFRESH', text="")
        sub.operator('xm.colorpicker', icon='EYEDROPPER', text="").length=3

def SelectHud(layout, self, context):
    tool = context.workspace.tools.from_space_view3d_mode(context.mode)
    toolname = context.workspace.tools.from_space_view3d_mode(context.mode).idname
    row = layout.row(align=True)
    row.alignment = 'LEFT'
    row.ui_units_x = 8
    if toolname == 'builtin.select':
        icon_id = ToolSelectPanelHelper._icon_value_from_icon_handle("ops.generic.select")
        row.separator(factor = 2)
        row.label(text="TWEAK")
    elif toolname == 'builtin.select_box':
        icon_id = ToolSelectPanelHelper._icon_value_from_icon_handle("ops.generic.select_box")
        row.template_icon(icon_value=icon_id)
        row.separator(factor = 2)
        props = tool.operator_properties("view3d.select_box")
        row.prop(props, "mode", text="", expand=True, icon_only=True)
    elif toolname == 'builtin.select_circle':
        icon_id = ToolSelectPanelHelper._icon_value_from_icon_handle("ops.generic.select_circle")
        row.template_icon(icon_value=icon_id)
        row.separator(factor = 2)
        props = tool.operator_properties("view3d.select_circle")
        row.prop(props, "mode", text="", expand=True, icon_only=True)
        row.prop(props, "radius")
    elif toolname == 'builtin.select_lasso':
        icon_id = ToolSelectPanelHelper._icon_value_from_icon_handle("ops.generic.select_lasso")
        row.template_icon(icon_value=icon_id)
        row.separator(factor = 2)
        props = tool.operator_properties("view3d.select_lasso")
        row.prop(props, "mode", text="", expand=True, icon_only=True)
    else:
        sub = row.column(align=True)
        sub.label(text="")

def GPSelectHud(layout, self, context):
    tool = context.workspace.tools.from_space_view3d_mode(context.mode)
    toolname = context.workspace.tools.from_space_view3d_mode(context.mode).idname

    row = layout.row()
    row.alignment = 'CENTER'
    row.ui_units_x = 8

    if toolname == 'builtin.select':
        icon_id = ToolSelectPanelHelper._icon_value_from_icon_handle("ops.generic.select")
        row.template_icon(icon_value=icon_id)
        row.separator(factor = 2)
        row.label(text="TWEAK")
    if toolname == 'builtin.select_box':
        icon_id = ToolSelectPanelHelper._icon_value_from_icon_handle("ops.generic.select_box")
        row.template_icon(icon_value=icon_id)
        props = tool.operator_properties("gpencil.select_box")
        row.prop(props, "mode", text="", expand=True, icon_only=True)
    if toolname == 'builtin.select_circle':
        icon_id = ToolSelectPanelHelper._icon_value_from_icon_handle("ops.generic.select_circle")
        row.template_icon(icon_value=icon_id)
        props = tool.operator_properties("gpencil.select_circle")
        row.prop(props, "mode", text="", expand=True, icon_only=True)
        row.prop(props, "radius")
    if toolname == 'builtin.select_lasso':
        icon_id = ToolSelectPanelHelper._icon_value_from_icon_handle("ops.generic.select_lasso")
        row.template_icon(icon_value=icon_id)
        props = tool.operator_properties("gpencil.select_lasso")
        row.prop(props, "mode", text="", expand=True, icon_only=True)


#VIEWPORT-----------------------------------------------------------------------------------------------

def ShadingMode(self, context, layout):
    tool_settings = context.tool_settings
    view = context.space_data
    shading = view.shading
    overlay = view.overlay

    row = layout.row(align=True)
    row.prop(shading, "type", text="", expand=True)
    sub = row.row(align=True)
    sub.popover(panel="VIEW3D_PT_shading", text="", icon='RADIOBUT_OFF')
    sub.popover(panel="VIEW3D_PT_overlay", text="", icon='OVERLAY')


def Normals(self, context, layout):
    scene = context.scene
    ob = context.active_object
    row = layout.row(align=True)
    if ob != None and ob.type == 'MESH':
        mesh = context.active_object.data
        sub = row.row(align=True)
        sub.operator("xm.normalshading", text="SMTH", depress=update_normaldisp(self, context))
        sub = row.row(align=True)
        sub.active = update_normaldisp(self, context)
        sub.prop(mesh, "use_auto_smooth", text="", icon="TRIA_RIGHT", toggle=True)
        sub = row.row(align=True)
        sub.active = mesh.use_auto_smooth and not mesh.has_custom_normals
        sub.prop(mesh, "auto_smooth_angle", text="")
    else:
        sub = row.row(align=True)
        sub.label(text=">")

def Overlay_Wire(self, context, layout):
    ts = context.scene.tool_settings.sculpt
    scene = context.scene
    ob = context.active_object

    for window in bpy.context.window_manager.windows:
        screen = window.screen
        for area in screen.areas:
            if area.type == 'VIEW_3D':
                view = area.spaces.active
                overlay = view.overlay
                shading = view.shading

    row = layout.row(align=True)

    sub = row.column(align=True)

    if ob != None and ob.type == 'MESH':
        sub.active = ob.show_wire
        sub.prop(overlay, "wireframe_opacity", text="Wire")
    else:
        sub.label(text="")

def Overlay(self, context, layout):
    ts = context.scene.tool_settings.sculpt
    scene = context.scene
    ob = context.active_object
    row = layout.row(align=True)
    sub = row.row(align=True)
    funct_bt(layout=sub, cmd='grid', tog=True, w=1.2, h=1, label='', icon='VIEW_ORTHO')
    #funct_bt(layout=sub, cmd='axis', tog=True, w=1.2, h=1, label='', icon='ORIENTATION_VIEW')

    '''
    sub = row.column(align=True)
    sub.ui_units_x = 4
    if context.mode == 'SCULPT':
        sub = subcol.row(align=True)
        sub.prop(ts, "show_face_sets", text="F-SETS", toggle=True)
        sub.prop(ts, "show_mask", text="MASK", toggle=True)
        sub = subcol.row(align=True)

    else:
        sub.label(text="")
    '''

#SCENE-----------------------------------------------------------------------------------------------

def SaveScene(self, context, layout):
    col = layout.column(align=True)
    col.ui_units_x = 4

    col.operator("wm.save_as_mainfile", text="SAVE AS")

    col.operator("wm.open_mainfile", text="OPEN")
    col.menu("TOPBAR_MT_file_open_recent", text="RECENT")

    sub = col.row(align=True)
    sub.operator("wm.link", text="LINK")
    sub.operator("wm.append", text="APND")


def History(self, context, layout):
    row = layout.row(align=True)

    row.operator("ed.undo", icon='TRIA_LEFT', text="")
    row.operator("ed.redo", icon='TRIA_RIGHT', text="")


class IOMenu(bpy.types.Menu):
    bl_label = "IMPORT"
    bl_idname = "OBJECT_MT_io_menu"
    def draw(self, context):
        layout = self.layout
        layout.use_property_split = False
        layout.use_property_decorate = False
        #file_path = bpy.context.preferences.addons[__package__].preferences.file_path
        scene = context.scene
        col = layout.column(align=True)
        col.ui_units_x = 3
        sub = col.row(align=True)
        sub.prop(scene, "import_items", expand=True)
        sub = col.column(align=True)
        if scene.import_items == '01':
            sub.menu_contents("OBJECT_MT_import_menu")
        else:
            sub.menu_contents("OBJECT_MT_export_menu")

class ImportPanel(bpy.types.Panel):
    bl_label = "IMPORT"
    bl_idname = "OBJECT_PT_import_panel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'WINDOW'
    bl_context = "scene"
    bl_order = 1000
    bl_options = {'DEFAULT_CLOSED',}
    def draw(self, context):
        layout = self.layout
        col = layout.column(align=True)
        col.menu_contents("OBJECT_MT_import_menu")

class ExportPanel(bpy.types.Panel):
    bl_label = "EXPORT"
    bl_idname = "OBJECT_PT_export_panel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'WINDOW'
    bl_context = "scene"
    bl_order = 1000
    bl_options = {'DEFAULT_CLOSED',}
    def draw(self, context):
        layout = self.layout
        col = layout.column(align=True)
        col.menu_contents("OBJECT_MT_export_menu")

class ImportMenu(bpy.types.Menu):
    bl_label = "IMPORT"
    bl_idname = "OBJECT_MT_import_menu"
    def draw(self, context):
        layout = self.layout
        layout.use_property_split = False
        layout.use_property_decorate = False
        file_path = bpy.context.preferences.addons[__package__].preferences.file_path
        scene = context.scene
        col = layout.column(align=True)
        col.ui_units_x = 3
        sub = col.row(align=True)
        sub = col.column(align=True)

        subsub = sub.row(align=True)
        subsub.label(text='>>')
        subsub = sub.row(align=True)
        op = subsub.operator("import_mesh.ply", text="PLY")
        op.filepath = file_path
        op = subsub.operator("import_mesh.stl", text="STL")
        op.filepath = file_path
        op.axis_forward = 'Y'
        op.axis_up = 'Z'
        op = subsub.operator("import_scene.obj", text="OBJ")
        op.filepath = file_path
        op.axis_forward = 'Y'
        op.axis_up = 'Z'
        subsub = sub.row(align=True)
        op = subsub.operator("wm.alembic_import", text="ABC")
        #op.filepath = file_path
        op.relative_path = True
        op = subsub.operator("import_scene.fbx", text="FBX")
        op.filepath = file_path
        op.axis_forward = 'Y'
        op.axis_up = 'Z'

class ExportMenu(bpy.types.Menu):
    bl_label = "EXPORT"
    bl_idname = "OBJECT_MT_export_menu"
    def draw(self, context):
        layout = self.layout
        layout.use_property_split = False
        layout.use_property_decorate = False
        file_path = bpy.context.preferences.addons[__package__].preferences.file_path
        scene = context.scene
        col = layout.column(align=True)
        col.ui_units_x = 3
        sub = col.row(align=True)
        sub = col.column(align=True)

        subsub = sub.row(align=True)
        subsub.label(text='                                                              >>')
        subsub = sub.row(align=True)
        op = subsub.operator("export_mesh.ply", text="PLY")
        op.filepath = file_path
        op = subsub.operator("export_mesh.stl", text="STL")
        op.filepath = file_path
        op.axis_forward = 'Y'
        op.axis_up = 'Z'
        op = subsub.operator("export_scene.obj", text="OBJ")
        op.filepath = file_path
        op.axis_forward = 'Y'
        op.axis_up = 'Z'
        subsub = sub.row(align=True)
        op = subsub.operator("wm.alembic_export", text="ABC")
        op.filepath = file_path
        op = subsub.operator("export_scene.fbx", text="FBX")
        op.filepath = file_path
        op.axis_forward = 'Y'
        op.axis_up = 'Z'

def HideObject(self, context, layout):
    ob = context.active_object

    row = layout.row(align=True)
    row.scale_x = 1.2
    #row.scale_y = 1.3

    if ob != None:
        if ob.hide_viewport == True:
            state = True
            label = 'Hidden  '
            icon = 'HIDE_ON'
        else:
            state = False
            label = 'Visible  '
            icon = 'HIDE_OFF'
        row.operator("xm.hide", text='', icon=icon)


def HideObjectMenuBt(self, context):
    ob = context.active_object

    row = self.layout.row(align=True)
    row.ui_units_x = 2.4

    if ob != None:
        if ob.hide_viewport == True:
            state = True
            label = 'Hidden  '
            icon = 'HIDE_ON'
        else:
            state = False
            label = 'Visible  '
            icon = 'HIDE_OFF'
        row.operator("xm.hide", text='', icon=icon)
    else: 
        row.label(text='')

class ViewCamPanel(bpy.types.Panel):
    bl_idname = "OBJECT_PT_viewcam"
    bl_label = "ViewCam"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'WINDOW'
    bl_context = "scene"
    bl_order = 1000
    bl_options = {'DEFAULT_CLOSED',}

    def draw(self, context):
        layout = self.layout
        view = context.space_data
        active_cam = bpy.context.scene.camera

        col = layout.column(align=True)
        sub = col.row(align=True)
        sub.prop(view, "camera", text="")
        subsub = sub.row(align=True)
        subsub.ui_units_x = 4
        funct_bt(layout=subsub, cmd='setactive', tog=False, w=1.6, h=1, label='SET', icon="NONE")

        if bpy.types.WindowManager.viewcam_state == False:
            col.prop(view, "lens", text="F")

            sub = col.row(align=True)
            subsub = sub.column(align=True)
            subsub.prop(view, "clip_start", text="Clip")
            subsub.prop(view, "clip_end", text="End")
            subsub = sub.column(align=True)
            subsub.scale_y = 2
            subsub.scale_x = 0.6
            if bpy.types.WindowManager.viewclip_state == False:
                label = ' 01 '
            else:
                label = ' 001 '
            op = subsub.operator('xm.viewclip', text=label, icon='NONE')
            op.scale = 10




        else:
            if active_cam.type == 'CAMERA':
                cam = bpy.data.cameras[active_cam.name]
                col.prop(cam, "lens", text="F")

                sub = col.row(align=True)
                sub.prop(cam, "clip_start", text="Clip")

                sub = col.row(align=True)
                sub.prop(cam, "clip_end", text="End")

#OBJECT-----------------------------------------------------------------------------------------------

def Transforms(self, context, layout):

    ob = context.active_object

    col = layout.column(align=True)
    col.ui_units_x = 8

    if ob:
        row = col.row(align=True)
        row.scale_y = 1.1
        sub = row.column(align=True)
        sub.prop(ob, "location", text="")
        sub = row.column(align=True)
        sub.prop(ob, "rotation_euler", text="")
        sub = row.column(align=True)
        sub.prop(ob, "scale", text="")

        row = col.row(align=True)
        row.scale_y = 0.8
        op = row.operator('object.transform_apply', text=' + ')
        op.location = True
        op.rotation = False
        op.scale = False
        row.operator('object.location_clear', text=' - ').clear_delta=False

        op = row.operator('object.transform_apply', text='+')
        op.location = False
        op.rotation = True
        op.scale = False
        row.operator('object.rotation_clear', text='-').clear_delta=False

        op = row.operator('object.transform_apply', text=' + ')
        op.location = False
        op.rotation = False
        op.scale = True
        row.operator('object.scale_clear', text=' - ').clear_delta=False

        row = col.row(align=True)
        row.scale_y = 1.2
        row.operator('object.transform_apply', text='APPLY ALL')

    else:
        row = col.row(align=True)

        row.scale_y = 1
        row.label(text=">")

def Pivot(self, context, layout):

    ob = context.active_object

    col = layout.column(align=True)
    col.ui_units_x = 8

    if ob:
        row = col.row(align=True)
        op = row.operator('object.origin_set', text='COG')
        op.type = 'ORIGIN_GEOMETRY'
        op.center ='MEDIAN'
        row.operator('xm.floor', text='FLOOR')
        op = row.operator('object.origin_set', text='CURSOR')
        op.type = 'ORIGIN_CURSOR'
        op.center ='MEDIAN'

    else:
        row = col.row(align=True)
        row.scale_y = 1
        row.label(text=">")

#PROPERTIES-----------------------------------------------------------------------------------------------

def UVTexture(self, context, layout):
    ob = context.active_object
    row = layout.row()
    if ob != None and ob.type == 'MESH':
        mesh = context.active_object.data
        sub = row.row(align=True)
        sub.scale_y = 1
        sub.operator("xm.override", icon='ADD', text="UV TEX").cmd='mesh.uv_texture_add'
        sub.operator("xm.override", icon='REMOVE', text="").cmd='mesh.uv_texture_remove'
        row = layout.row()
        row.template_list("MESH_UL_uvmaps", "uvmaps", mesh, "uv_layers", mesh.uv_layers, "active_index", rows=2)
    else:
        sub = row.row(align=True)
        sub.label(text=">")

def VertexColor(self, context, layout):
    mesh = context.active_object.data
    col = layout.column()
    col.ui_units_x = 8
    sub = col.row(align=True)
    sub.scale_y = 1.2
    sub.operator("xm.override", icon='ADD', text="VERTEX COLOR").cmd='geometry.color_attribute_add'
    sub.operator("xm.override", icon='REMOVE', text="").cmd='geometry.color_attribute_remove'
    sub = col.column()
    sub.template_list("MESH_UL_color_attributes", "color_attributes", mesh, "color_attributes", mesh.color_attributes, "active_color_index", rows=3)


def TexSlots(self, context, layout):
    layout = layout
    settings = context.tool_settings.image_paint
    ob = context.active_object

    col = layout.column()
    col.ui_units_x = 8
    sub = col.row(align=True)
    sub.prop(settings, "mode", text="")
    sub.separator()
    sub.operator_menu_enum("paint.add_texture_paint_slot", "type", icon='NONE', text="ADD")
    sub.separator()
    sub.operator("image.save_all_modified", text="SAVE", icon='FILE_TICK')

    if settings.mode == 'MATERIAL':
        if len(ob.material_slots) > 1:
            col.template_list("MATERIAL_UL_matslots", "layers",ob, "material_slots",ob, "active_material_index", rows=2)
        mat = ob.active_material
        if mat and mat.texture_paint_images:
            sub = col.row()
            sub.template_list("TEXTURE_UL_texpaintslots", "",mat, "texture_paint_images",mat, "paint_active_slot", rows=2)

            if mat.texture_paint_slots:
                slot = mat.texture_paint_slots[mat.paint_active_slot]
            else:
                slot = None
            have_image = slot is not None
        else:
            sub = col.row()
            box = sub.box()
            box.label(text="No Textures")
            have_image = False

    elif settings.mode == 'IMAGE':
        mesh = ob.data
        uv_text = mesh.uv_layers.active.name if mesh.uv_layers.active else ""
        col.template_ID(settings, "canvas", new="image.new", open="image.open")

        col.menu("VIEW3D_MT_tools_projectpaint_uvlayer", text=uv_text, translate=False)
        have_image = settings.canvas is not None

        col.prop(settings, "interpolation", text="")

    if settings.missing_uvs:
        col.separator()
        col.operator("paint.add_simple_uvs", icon='ADD', text="Add UVs")

def GPLayers(self, context, layout):
    if context.active_object.type == "GPENCIL":
        gpd = context.active_object.data
        gpl = gpd.layers.active

        row = layout.row()
        row.ui_units_x = 11
        layer_rows = 3

        col = row.column()
        col.template_list("GPENCIL_UL_layer", "", gpd, "layers", gpd.layers, "active_index",
                        rows=layer_rows, sort_reverse=True, sort_lock=True)
        if gpl:
            sub = col.column(align=True)
            sub.prop(gpl, "blend_mode", text="Blend")
            sub.prop(gpl, "opacity", text="Opacity", slider=True)
            sub.prop(gpl, "use_lights")

        col = row.column()
        sub = col.column(align=True)
        sub.operator("gpencil.layer_add", icon='ADD', text="")
        sub.operator("gpencil.layer_remove", icon='REMOVE', text="")

def GPLayersWide(self, context, layout):
    if context.active_object.type == "GPENCIL":
        gpd = context.active_object.data
        gpl = gpd.layers.active

        row = layout.row()
        sub = row.column(align=True)
        sub.ui_units_x = 5
        subsub = sub.row(align=True)
        subsub.scale_y = 1
        subsub.operator("gpencil.layer_add", icon='ADD', text="LAYER")
        subsub.operator("gpencil.layer_remove", icon='REMOVE', text="")
        sub.template_list("GPENCIL_UL_layer", "", gpd, "layers", gpd.layers, "active_index",
                            rows=3, sort_reverse=True, sort_lock=True)
        sub = row.column(align=True)
        sub.ui_units_x = 4
        subsub = sub.row(align=True)
        subsub.scale_y = 1
        subsub.label(text='>>')
        if gpl:
            sub.prop(gpl, "blend_mode", text="Blend")
            sub.prop(gpl, "opacity", text="Opacity", slider=True)
            sub.prop(gpl, "use_lights")
        else:
            sub.label(text='')

def VertexGroups(self, context, layout):
    ob = context.active_object
    if ob:
        group = ob.vertex_groups.active
        col = layout.column()

        row = col.row(align=True)
        row.scale_y = 1
        row.operator('xm.override', text='Vertex Group',icon='ADD').cmd='object.vertex_group_add'
        row.operator('xm.override',text='',icon='REMOVE').cmd='object.vertex_group_remove'

        if (ob.vertex_groups and (ob.mode == 'EDIT' or (ob.mode == 'WEIGHT_PAINT' and ob.type == 'MESH' and ob.data.use_paint_mask_vertex))):
            row.separator(factor = 1)
            row.operator('xm.override',text='',icon='CHECKMARK').cmd='object.vertex_group_assign'
            row.operator("xm.override", text="", icon="REMOVE").cmd ='object.vertex_group_remove_from'
            row.operator('xm.override',text='',icon='RADIOBUT_ON').cmd='object.vertex_group_select'
            row.operator("xm.override", text="", icon="RADIOBUT_OFF").cmd ='object.vertex_group_deselect'
            row.prop(context.tool_settings, "vertex_group_weight", text="WEIGHT")
        if (ob.vertex_groups and (ob.mode == 'EDIT_GPENCIL' )):
            row.separator(factor = 1)
            row.operator('xm.override',text='',icon='CHECKMARK').cmd='gpencil.vertex_group_assign'
            row.operator("xm.override", text="", icon="REMOVE").cmd ='gpencil.vertex_group_remove_from'
            row.operator('xm.override',text='',icon='RADIOBUT_ON').cmd='gpencil.vertex_group_select'
            row.operator("xm.override", text="", icon="RADIOBUT_OFF").cmd ='gpencil.vertex_group_deselect'

        row = col.row(align=True)
        row.template_list("MESH_UL_vgroups", "", ob, "vertex_groups", ob.vertex_groups, "active_index", rows=3)
        sub = row.column(align=True)

        if group:
            op = sub.operator("xm.override1", icon='TRIA_UP', text="")
            op.cmd='object.vertex_group_move'
            op.prop1 ='direction="UP"'
            op = sub.operator("xm.override1", icon='TRIA_DOWN', text="")
            op.cmd='object.vertex_group_move'
            op.prop1 ='direction="DOWN"'
            sub.separator(factor = 3)
            sub.menu("MESH_MT_vertex_group_context_menu", icon='DOWNARROW_HLT', text="")

            #sub.operator("xm.override", text="COPY").cmd ='object.vertex_group_copy'
            #sub.operator("xm.override", text="COPY TO").cmd ='object.vertex_group_copy_to_selected'
            #sub = row.row(align=True)
            #op = sub.operator("xm.override1", text="MIRROR")
            #op.cmd = 'object.vertex_group_mirror'
            #op.prop1 = 'use_topology=False'
    else:
        col = layout.column(align=True)
        col.label(text='>')

class VIEW3D_MT_Material2(bpy.types.Menu):
    bl_label = ""
    bl_context = "material"
    bl_options = {'HIDE_HEADER'}
    COMPAT_ENGINES = {'BLENDER_EEVEE', 'BLENDER_WORKBENCH'}

    def draw(self, context):
        layout = self.layout
        ob = context.active_object
        if ob:
            mat = ob.active_material
            slot = ob.material_slots
            space = context.space_data

            col = layout.column(align=True)
            row = col.row(align=True)
            row.scale_y = 1
            row.template_ID(ob, "active_material")


            col.separator(factor=0.3)

            row = col.row(align=True)
            sub = row.column(align=True)
            sub.ui_units_x = 7
            sub.template_list("MATERIAL_UL_matslots", "", ob, "material_slots", ob, "active_material_index", rows=3)
            sub = row.column(align=True)
            sub.ui_units_x = 1

            op = sub.operator("xm.override1", icon='TRIA_UP', text="")
            op.cmd='object.material_slot_move'
            op.prop1 ='direction="UP"'
            op = sub.operator("xm.override1", icon='TRIA_DOWN', text="")
            op.cmd='object.material_slot_move'
            op.prop1 ='direction="DOWN"'
            sub.separator(factor = 3)
            sub.menu("MATERIAL_MT_context_menu", text="",icon='DOWNARROW_HLT')
            slot = context.material_slot
            if slot:
                icon_link = 'MESH_DATA' if slot.link == 'DATA' else 'OBJECT_DATA'
                row.prop(slot, "link", icon=icon_link, icon_only=True)

            row = col.row(align=True)
            sub = row.column(align=True)
            sub.ui_units_x = 1.5
            sub.operator("xm.newmat", text="NEW")
            row.operator('xm.override',text='',icon='ADD').cmd='object.material_slot_add'
            row.operator('xm.override',text='',icon='REMOVE').cmd='object.material_slot_remove'

            if context.mode == 'EDIT_MESH':
                #row.separator(factor = 1)
                row.operator('xm.override',text='',icon='CHECKMARK').cmd='object.material_slot_assign'
                row.operator("object.material_slot_select", text="", icon='RADIOBUT_ON')
                row.operator("object.material_slot_deselect", text="", icon='RADIOBUT_OFF')
            if context.mode == 'EDIT_GPENCIL':
                #row.separator(factor = 1)
                row.operator('xm.override',text='',icon='CHECKMARK').cmd='object.material_slot_assign'
                row.operator("object.material_slot_select", text="", icon='RADIOBUT_ON')
                row.operator("object.material_slot_deselect", text="", icon='RADIOBUT_OFF')



        else:
            col = layout.column(align=True)
            col.label(text='>')

class VIEW3D_MT_Material(bpy.types.Menu):
    bl_label = ""
    bl_context = "material"
    bl_options = {'HIDE_HEADER'}
    COMPAT_ENGINES = {'BLENDER_EEVEE', 'BLENDER_WORKBENCH'}

    def draw(self, context):
        layout = self.layout
        ob = context.active_object
        if ob:
            mat = ob.active_material
            slot = ob.material_slots
            space = context.space_data

            col = layout.column(align=True)
            row = col.row(align=True)
            row.scale_y = 1
            row.template_ID(ob, "active_material")
            sub = row.column(align=True)
            sub.ui_units_x = 2
            sub.operator("xm.newmat", text="NEW")
            row.operator('xm.override',text='',icon='ADD').cmd='object.material_slot_add'
            row.operator('xm.override',text='',icon='REMOVE').cmd='object.material_slot_remove'

            if context.mode == 'EDIT_MESH':
                #row.separator(factor = 1)
                row.operator('xm.override',text='',icon='CHECKMARK').cmd='object.material_slot_assign'
                row.operator("object.material_slot_select", text="", icon='RADIOBUT_ON')
                row.operator("object.material_slot_deselect", text="", icon='RADIOBUT_OFF')
            if context.mode == 'EDIT_GPENCIL':
                #row.separator(factor = 1)
                row.operator('xm.override',text='',icon='CHECKMARK').cmd='object.material_slot_assign'
                row.operator("object.material_slot_select", text="", icon='RADIOBUT_ON')
                row.operator("object.material_slot_deselect", text="", icon='RADIOBUT_OFF')

            col.separator(factor=0.3)

            row = col.row(align=True)
            sub = row.column(align=True)
            sub.ui_units_x = 7
            sub.template_list("MATERIAL_UL_matslots", "", ob, "material_slots", ob, "active_material_index", rows=3)
            sub = row.column(align=True)
            sub.ui_units_x = 1

            op = sub.operator("xm.override1", icon='TRIA_UP', text="")
            op.cmd='object.material_slot_move'
            op.prop1 ='direction="UP"'
            op = sub.operator("xm.override1", icon='TRIA_DOWN', text="")
            op.cmd='object.material_slot_move'
            op.prop1 ='direction="DOWN"'
            sub.separator(factor = 3)
            sub.menu("MATERIAL_MT_context_menu", text="",icon='DOWNARROW_HLT')
            slot = context.material_slot
            if slot:
                icon_link = 'MESH_DATA' if slot.link == 'DATA' else 'OBJECT_DATA'
                row.prop(slot, "link", icon=icon_link, icon_only=True)
        else:
            col = layout.column(align=True)
            col.label(text='>')

class VIEW3D_MT_GPMaterial(bpy.types.Menu):
    bl_label = "Materials"

    def draw(self, context):
        layout = self.layout
        ob = context.active_object
        tool_settings = context.scene.tool_settings
        gpencil_paint = tool_settings.gpencil_paint
        brush = gpencil_paint.brush if gpencil_paint else None
        if ob:
            mat = ob.active_material
            slot = ob.material_slots
            space = context.space_data

            col = layout.column(align=True)
            row = col.row(align=True)
            row.scale_y = 1
            row.template_ID(ob, "active_material")
            sub = row.column(align=True)
            sub.ui_units_x = 2
            sub.operator("xm.newmat", text="NEW")
            row.operator('xm.override',text='',icon='ADD').cmd='object.material_slot_add'
            row.operator('xm.override',text='',icon='REMOVE').cmd='object.material_slot_remove'

            if context.mode == 'EDIT_MESH':
                row.separator(factor = 1)
                row.operator('xm.override',text='',icon='CHECKMARK').cmd='object.material_slot_assign'
                row.operator("object.material_slot_select", text="", icon='RADIOBUT_ON')
                row.operator("object.material_slot_deselect", text="", icon='RADIOBUT_OFF')
            if context.mode == 'EDIT_GPENCIL':
                row.separator(factor = 1)
                row.operator('xm.override',text='',icon='CHECKMARK').cmd='object.material_slot_assign'
                row.operator("object.material_slot_select", text="", icon='RADIOBUT_ON')
                row.operator("object.material_slot_deselect", text="", icon='RADIOBUT_OFF')

            col.separator(factor=0.5)

            row = col.row(align=True)
            sub = row.column(align=True)
            sub.ui_units_x = 7
            sub.template_list("GPENCIL_UL_matslots", "", ob, "material_slots", ob, "active_material_index", rows=3)
            sub = row.column(align=True)
            sub.ui_units_x = 1

            op = sub.operator("xm.override1", icon='TRIA_UP', text="")
            op.cmd='object.material_slot_move'
            op.prop1 ='direction="UP"'
            op = sub.operator("xm.override1", icon='TRIA_DOWN', text="")
            op.cmd='object.material_slot_move'
            op.prop1 ='direction="DOWN"'
            sub.separator(factor = 3)
            sub.menu("GPENCIL_MT_material_context_menu", text="",icon='DOWNARROW_HLT')

            slot = context.material_slot
            if slot:
                icon_link = 'MESH_DATA' if slot.link == 'DATA' else 'OBJECT_DATA'
                row.prop(slot, "link", icon=icon_link, icon_only=True)

            if ob.data.use_stroke_edit_mode:
                row = layout.row(align=True)
                row.operator("gpencil.stroke_change_color", text="Assign")
                row.operator("gpencil.material_select", text="Select").deselect = False
                row.operator("gpencil.material_select", text="Deselect").deselect = True
            
        else:
            col = layout.column(align=True)
            col.label(text='>')

def ModifierWindow(self, context, layout):
    ob = context.active_object
    col = layout.column()
    row = col.row(align=True)
    if ob != None:
        if addon_utils.check("modifier_list")[1]==True:
            ml_props = bpy.context.window_manager.modifier_list
            #Old Version
            #row.template_list("OBJECT_UL_ml_modifier_list", "", ob, "modifiers", ml_props, "active_object_modifier_active_index", rows=3)
            #New Version
            row.template_list("OBJECT_UL_ml_modifier_list", "", ob, "modifiers", ob, "ml_modifier_active_index", rows=2)
        else:
            row.label(text='>>')

        row = col.row(align=True)
        row.scale_y = 1
        row.operator('xm.override', text='APPLY').cmd='view3d.ml_apply_all_modifiers'
        row.operator('xm.override', text='REMOVE').cmd='view3d.ml_remove_all_modifiers'

    else:
        row.label(text='>')
#TOOLSETTINGS-----------------------------------------------------------------------------------------------

def ToolOptions(self, context, layout):
    ts = context.tool_settings   
    row = layout.row()

    if bpy.context.mode == 'OBJECT': 
        subrow = row.row(align=True)
        subrow.prop(ts, "use_transform_data_origin", text="ORIG", toggle=True)
        subrow.prop(ts, "use_transform_pivot_point_align", text="LOC", toggle=True)
        subrow.prop(ts, "use_transform_skip_children", text="PARENT", toggle=True)

    elif bpy.context.mode == 'EDIT_MESH':
        subrow = row.row(align=True)
        subrow.prop(ts, "use_mesh_automerge", text="Auto Merge", toggle=True)

    elif bpy.context.mode == 'EDIT_GPENCIL':
        subrow = row.row(align=True) 
        subrow.prop(ts, "use_mesh_automerge", text="Auto Merge", toggle=True)

    elif bpy.context.mode == 'SCULPT':
        brush = ts.sculpt.brush
        subrow = row.row(align=True)
        subrow.scale_y = 1
        sub = subrow.column(align=True)
        sub.ui_units_x = 2
        sub.prop(brush, "use_automasking_topology", text="TOPO", toggle=True)
        sub = subrow.column(align=True)
        sub.ui_units_x = 2
        sub.prop(brush, "use_frontface", text="FRONT", toggle=True)
        sub = subrow.column(align=True)
        sub.ui_units_x = 2
        sub.prop(brush, "use_automasking_boundary_edges", text="BND", toggle=True)

        subrow = row.row(align=True)
        sub = subrow.column(align=True)
        sub.ui_units_x = 4
        sub.scale_y = 0.7
        subsub = sub.row(align=True)
        split = subsub.split(factor=0.6, align=True)
        split.prop(brush, "use_automasking_face_sets", text="F-SET", toggle=True)
        split.prop(brush, "use_automasking_boundary_face_sets", text="BND", toggle=True)
        sub.prop(brush, "automasking_boundary_edges_propagation_steps", text="",)

    elif bpy.context.mode == 'PAINT_TEXTURE':
        ipaint = ts.image_paint
        
        sub = row.row(align=True)
        sub.ui_units_x = 6
        sub.scale_y = 1
        sub.prop(ipaint, "use_occlude",  text="OCCL", toggle=True)
        sub.prop(ipaint, "use_backface_culling",  text="FRONT", toggle=True)

        sub = row.column(align=True)
        sub.ui_units_x = 5
        sub.scale_y = 0.7
        sub.prop(ipaint, "seam_bleed",  text="Bleed")
        sub.prop(ipaint, "dither",  text="Dither")  
        
def ObjectToolSettings(self, context, layout):
    layout = layout
    tool = context.workspace.tools.from_space_view3d_mode(context.mode)
    toolname = context.workspace.tools.from_space_view3d_mode(bpy.context.mode).idname

    col = layout.column(align=True)
    col.alignment = 'LEFT'
    col.ui_units_x = 4
    col.scale_y = 0.7

    if toolname == 'builtin.cursor':
        props = tool.operator_properties("view3d.cursor3d")
        sub = col.row(align=True)
        sub.prop(props, "use_depth", text="PROJECT", toggle=True)
        sub = col.row(align=True)
        sub.prop(props, "orientation", text="")

    elif toolname == 'builtin.extrude':
        props = tool.gizmo_group_properties("VIEW3D_GGT_xform_extrude")
        layout.prop(props, "axis_type", expand=True)

    else:
        sub = col.row(align=True)
        sub.label(text='>>')


def SculptToolSettings(self, context, layout):
    layout = layout

    tool = context.workspace.tools.from_space_view3d_mode(bpy.context.mode).idname
    brush = context.tool_settings.sculpt.brush
    settings = context.tool_settings.sculpt
    capabilities = brush.sculpt_capabilities
    sculpt_tool = brush.sculpt_tool

    col = layout.column(align=True)
    col.alignment = 'LEFT'
    col.ui_units_x = 8
    col.scale_y = 0.7

    if tool == 'builtin.box_mask':
        tool = context.workspace.tools.from_space_view3d_mode(context.mode)
        props = tool.operator_properties("paint.mask_box_gesture")
        sub = col.row(align=True)
        sub.prop(props, "use_front_faces_only", expand=False, text='FrontFaces')

    elif tool == 'builtin.lasso_mask':
        tool = context.workspace.tools.from_space_view3d_mode(context.mode)
        props = tool.operator_properties("paint.mask_lasso_gesture")
        sub = col.row(align=True)
        sub.prop(props, "use_front_faces_only", expand=False, text='FrontFaces')

    elif tool == 'builtin.line_mask':
        tool = context.workspace.tools.from_space_view3d_mode(context.mode)
        props = tool.operator_properties("paint.mask_line_gesture")
        sub = col.column(align=True)
        sub.prop(props, "use_front_faces_only", expand=False, text='FrontFaces')
        sub.prop(props, "use_limit_to_segment", expand=False, text='LimitSegment')

    elif tool == 'builtin.box_face_set':
        tool = context.workspace.tools.from_space_view3d_mode(context.mode)
        props = tool.operator_properties("sculpt.face_set_box_gesture")
        sub = col.row(align=True)
        sub.prop(props, "use_front_faces_only", expand=False, text='FrontFaces')

    elif tool == 'builtin.lasso_face_set':
        tool = context.workspace.tools.from_space_view3d_mode(context.mode)
        props = tool.operator_properties("sculpt.face_set_lasso_gesture")
        sub = col.row(align=True)
        sub.prop(props, "use_front_faces_only", expand=False, text='FrontFaces')

    elif tool == 'builtin.face_set_edit':
        tool = context.workspace.tools.from_space_view3d_mode(context.mode)
        props = tool.operator_properties("sculpt.face_set_edit")
        sub = col.column(align=True)
        sub.prop(props, "mode", expand=False, text='')
        sub.prop(props, "modify_hidden")

    elif tool == 'builtin.box_trim':
        tool = context.workspace.tools.from_space_view3d_mode(context.mode)
        props = tool.operator_properties("sculpt.trim_box_gesture")
        sub = col.column(align=True)
        sub.prop(props, "trim_mode", expand=False, text='')
        sub.prop(props, "use_cursor_depth", text='Cursor Depth', expand=False)

    elif tool == 'builtin.lasso_trim':
        tool = context.workspace.tools.from_space_view3d_mode(context.mode)
        props = tool.operator_properties("sculpt.trim_lasso_gesture")
        sub = col.column(align=True)
        sub.prop(props, "trim_mode", expand=False, text='')
        subsub = sub.row(align=True)
        subsub.prop(props, "use_cursor_depth", text='Cursor Depth', expand=False, toggle=True)
        subsub.prop(props, "trim_orientation", text='', expand=False)

    elif tool == 'builtin.transform':
        scene = context.scene
        orient_slot = scene.transform_orientation_slots[0]
        sub = col.column(align=True)
        sub.prop(orient_slot, "type")

    elif tool == 'builtin_brush.Paint':
        brush = context.tool_settings.sculpt.brush

        sub = col.row(align=True)
        subsub = sub.column(align=True)
        subsub.prop(brush, "blend", text="")
        item = subsub.row(align=True)
        item.prop(brush, "density", slider=True, text="DENS")
        item.prop(brush, "invert_density_pressure", text="")
        item.prop(brush, "use_density_pressure", text="")

        subsub = sub.column(align=True)
        subsub.prop(brush, "tip_roundness", slider=True, text='ROUND')
        subsub.prop(brush, "tip_scale_x", slider=True, text='SCALE')

    else:
        if capabilities.has_plane_offset:
            sub = col.row(align=True)
            sub.prop(brush, "plane_offset", slider=True, text='OFFSET')
            sub = col.row(align = True)
            sub.prop(brush, "use_plane_trim", slider=False, toggle=True, text='TRIM')
            sub.prop(brush, "plane_trim", slider=True)


def GPToolSettings(self, context, layout):
    layout = layout
    tool = context.workspace.tools.from_space_view3d_mode(context.mode)
    toolname = context.workspace.tools.from_space_view3d_mode(bpy.context.mode).idname

    col = layout.column(align=True)
    col.ui_units_x = 6

    if toolname == 'builtin.cursor':
        props = tool.operator_properties("view3d.cursor3d")
        sub = col.row(align=True)
        sub.scale_y = 0.7
        sub.prop(props, "use_depth")
        sub = col.row(align=True)
        sub.scale_y = 0.7
        sub.prop(props, "orientation")

    elif toolname == 'builtin.extrude':
        props = tool.gizmo_group_properties("VIEW3D_GGT_xform_extrude")
        sub = col.row(align=True)
        sub.prop(props, "axis_type", expand=True)
        sub = col.row(align=True)
        sub.scale_y = 0.4
        sub.label(text='')

    elif toolname == 'builtin.transform_fill':
        props = tool.operator_properties("gpencil.transform_fill")
        sub = col.row(align=True)
        sub.prop(props, "mode", expand=True)
        sub = col.row(align=True)
        sub.scale_y = 0.4
        sub.label(text='')


    elif toolname == 'builtin.interpolate':
        props = tool.operator_properties("gpencil.interpolate")
        sub = col.row(align=True)
        sub.scale_y = 0.7
        sub.prop(props, "layers", text='')
        #sub.prop(props, "interpolate_selected_only",toggle=True)
        sub.prop(props, "flip", text='')
        sub = col.row(align=True)
        sub.scale_y = 0.7
        sub.prop(props, "smooth_factor")
        sub.prop(props, "smooth_steps")

    else:
        sub = col.column(align=True)
        sub.scale_y = 0.7
        sub.label(text='>')
        sub.label(text='')

def GPSculptToolSettings(self, context, layout):
    layout = layout

    tool = context.workspace.tools.from_space_view3d_mode(bpy.context.mode).idname
    brush = context.tool_settings.gpencil_paint.brush
    gp_settings = brush.gpencil_settings
    sculpt_tool = brush.gpencil_sculpt_tool

    sub = layout.row(align=True)

    if tool == 'builtin_brush.Smooth':
        sub.popover("VIEW3D_PT_tools_grease_pencil_sculpt_options")
    elif tool == 'builtin_brush.Randomize':
        sub.popover("VIEW3D_PT_tools_grease_pencil_sculpt_options")
    elif tool == 'builtin_brush.Thickness':
        sub.prop(gp_settings, "direction", expand=True)
    elif tool == 'builtin_brush.Strength':
        sub.prop(gp_settings, "direction", expand=True)
    elif tool == 'builtin_brush.Twist':
        sub.prop_enum(gp_settings, "direction", value='ADD', text="CCW")
        sub.prop_enum(gp_settings, "direction", value='SUBTRACT', text="CW")
    elif tool == 'builtin_brush.Pinch':
        sub.prop_enum(gp_settings, "direction", value='ADD', text="Pinch")
        sub.prop_enum(gp_settings, "direction", value='SUBTRACT', text="Inflate")
    else:
        sub.label(text='')



#BRUSHSETTINGS-----------------------------------------------------------------------------------------------

def SculptBrushSettings(self, context, layout):
    layout = layout
    brush = context.tool_settings.sculpt.brush
    direction = not brush.sculpt_capabilities.has_direction
    settings = context.tool_settings.sculpt
    capabilities = brush.sculpt_capabilities
    sculpt_tool = brush.sculpt_tool

    row = layout.row(align=True)
    row.scale_y = 0.7

    # col 1
    sub = row.column(align=True)

    #       row 1

    if sculpt_tool == 'GRAB':
        subsub = sub.row(align=True)
        subsub.scale_x = 0.5
        subsub.prop(brush, "use_grab_silhouette",  text='SILHOUETTE', toggle=True)
        subsub.prop(brush, "use_grab_active_vertex",  text='VERTEX', toggle=True)
    elif direction:
        subsub = sub.row(align=True)
        subsub.scale_x = 1.6
        subsub.prop(brush, "direction", expand=True, text="")

    elif sculpt_tool == 'PAINT':
        subsub = sub.row(align=True)
        subsub.prop(brush, "flow", slider=True, text="FLOW")
        subsub.prop(brush, "invert_flow_pressure", text="")
        subsub.prop(brush, "use_flow_pressure", text="")
    elif sculpt_tool == 'SMEAR':
        subsub = sub.row(align=True)
        subsub.scale_x = 0.33
        subsub.prop(brush, "smear_deform_type", expand=True)
    else:
        subsub = sub.row(align=True)
        subsub.label(text="")


    #       row 2
    subsub = sub.row(align=True)
    subsub.prop(brush, "normal_radius_factor", slider=True, text='NORMAL')


    # col 2
    sub = row.column(align=True)

    #       row 1
    subsub = sub.row(align=True)
    if sculpt_tool == 'CLAY_STRIPS':
        subsub.prop(brush, "tip_roundness", slider=True, text='ROUND')
    elif sculpt_tool == 'LAYER':
        subsub.prop(brush, "height", slider=True, text='HEIGHT')
    elif sculpt_tool == 'CREASE':
        subsub.prop(brush, "crease_pinch_factor", slider=True, text='PINCH')
    elif sculpt_tool == 'SCRAPE':
        subsub.prop(brush, "area_radius_factor", slider=True, text='AREA')
    elif sculpt_tool == 'FILL':
        subsub.prop(brush, "area_radius_factor", slider=True, text='AREA')
    elif sculpt_tool == 'MULTIPLANE_SCRAPE':
        subsub.prop(brush, "multiplane_scrape_angle", slider=True, text='ANGLE')
    elif sculpt_tool == 'POSE':
        subsub.prop(brush, "pose_ik_segments", slider=True, text='IK')
    elif sculpt_tool == 'GRAB':
        subsub.prop(brush, "normal_weight", slider=True, text='PEAK')
    elif sculpt_tool == 'ELASTIC_DEFORM':
        subsub.prop(brush, "normal_weight", slider=True, text='PEAK')
    elif sculpt_tool == 'PAINT':
        subsub.prop(brush, "wet_mix", slider=True, text="WETMIX")
        subsub.prop(brush, "invert_wet_mix_pressure", text="")
        subsub.prop(brush, "use_wet_mix_pressure", text="")
    else:
        subsub.label(text="")


    #       row 2
    subsub = sub.row(align=True)
    subsub.prop(brush, "hardness", slider=True, text='HARD')

    #row.separator(factor=2)

    # col 3
    sub = row.column(align=True)
    #       row 1
    subsub = sub.row(align=True)

    if (capabilities.has_topology_rake and context.sculpt_object.use_dynamic_topology_sculpting):
        subsub.scale_x = 0.5
        subsub.prop(brush, "topology_rake_factor", slider=True, text='RAKE')
        if capabilities.has_accumulate:
            subsub.prop(brush, "use_accumulate", text="ACCU", toggle=True)
        else:
            subsub.label(text='')
    elif capabilities.has_accumulate:
        subsub.scale_x = 0.5
        subsub.label(text='')
        subsub.prop(brush, "use_accumulate", text="ACCU", toggle=True)

    elif sculpt_tool == 'PAINT':
        subsub.prop(brush, "wet_persistence", slider=True, text="PERS")
        subsub.prop(brush, "invert_wet_persistence_pressure", text="")
        subsub.prop(brush, "use_wet_persistence_pressure", text="")
    else:
        subsub.label(text='')

    #       row 2
    subsub = sub.row(align=True)
    if sculpt_tool == 'MASK':
        subsub.scale_x = 0.5
        subsub.prop(brush, "mask_tool", expand=True)
    elif sculpt_tool == 'PAINT':
        subsub.prop(brush, "wet_paint_radius_factor", slider=True, text='WET RAD')
    else:
        subsub.prop(brush, "auto_smooth_factor", slider=True, text='SMTH')


def TextureBrushSettings(self, context, layout):
    brush = context.tool_settings.image_paint.brush
    settings = context.tool_settings.image_paint
    capabilities = brush.image_paint_capabilities
    use_accumulate = capabilities.has_accumulate
    mode = context.mode

    row = layout.row(align=True)
    sub = row.row(align=True)
    sub.scale_y = 1
    sub.prop(brush, "use_accumulate", text="ACCU", toggle=True)
    if mode == 'PAINT_2D':
        sub.prop(brush, "use_paint_antialiasing")
    else:
        sub.prop(brush, "use_alpha", text="ALPHA", toggle=True)

    # Tool specific settings
    sub = row.row(align=True)
    sub.ui_units_x = 2
    sub.scale_y = 1
    if brush.image_tool == 'SOFTEN':
        sub.prop(brush, "direction", expand=True, text="")
        sub.prop(brush, "threshold", text="")
        #if mode == 'PAINT_2D':
            #col.prop(brush, "blur_kernel_radius")
        #col.prop(brush, "blur_mode")

    elif brush.image_tool == 'MASK':
        sub.prop(brush, "weight", text="Mask Value", slider=True)

    elif brush.image_tool == 'CLONE':
        if mode == 'PAINT_2D':
            sub.prop(brush, "clone_image", text="Image")
            sub.prop(brush, "clone_alpha", text="Alpha")
        else:
            sub.label(text='')
    else:
        sub.label(text='')

def VertexBrushSettings(self, context, layout):
    brush = context.tool_settings.vertex_paint.brush
    settings = context.tool_settings.vertex_paint

    row = layout.row(align=True)
    row.scale_y = 1
    if brush.vertex_tool != 'SMEAR':
        row.prop(brush, "use_accumulate", text="ACCU", toggle=True)
    else:
        row.label(text="")
    row.prop(brush, "use_alpha", text="ALPHA", toggle=True)
    row.separator(factor=1)
    row.prop(brush, "use_frontface", text="FRONT", toggle=True)


#BRUSH-----------------------------------------------------------------------------------------------

def BrushCopy(self, context, layout):
    layout = layout
    get_brush_mode(self, context)
    settings = paint_settings(context)

    row = layout.row(align=True)
    sub = row.column()
    sub.ui_units_x = 2
    sub.scale_y = 1.4
    sub.operator("xm.override", icon='ADD', text="").cmd='brush.add' 
    sub = row.column()
    sub.ui_units_x = 3
    sub.scale_x = 0.2
    sub.scale_y = 0.2
    sub.template_ID_preview(settings, "brush", rows=1, cols=8, hide_buttons=True)

    #bpy.ops.brush.reset()
    '''
    row.template_ID(settings, "brush", new="brush.add")
    row= col.row()
    row.menu("VIEW3D_MT_brush_context_menu", icon='DOWNARROW_HLT', text="")

    if brush is not None:
        row.prop(brush, "use_custom_icon", toggle=True, icon='FILE_IMAGE', text="")

        if brush.use_custom_icon:
            row.prop(brush, "icon_filepath", text="")
    '''


def Color(self, context, layout):
    layout = layout
    ts = context.tool_settings
    ups = ts.unified_paint_settings
    if context.mode == 'PAINT_VERTEX':
        ptr = ts.vertex_paint.brush
    if context.mode == 'SCULPT':
        ptr = ts.sculpt.brush
    else:
        ptr = ups if ups.use_unified_color else paint_settings(context).brush

    col = layout.column()
    col.scale_y = 0.7 
    col.ui_units_x = 6
    col.template_color_picker(ptr, 'color', value_slider=True)

def ColorPalette(self, context, layout):
    settings = paint_settings(context)

    col = layout.column()
    col.scale_y = 0.8
    col.template_ID(settings, "palette", new="palette.new")
    if settings.palette:
        col.template_palette(settings, "palette", color=True)

def Stroke(self, context, layout):
    mode = context.mode
    brush = get_brush_mode(self, context)
    settings = paint_settings(context)

    col = layout.column(align=True)
    col.scale_y = 1 
    col.alignment = 'RIGHT'
    col.ui_units_x = 4
    col.prop(brush, "stroke_method", text="")
    if brush.use_anchor:
        col.prop(brush, "use_edge_to_edge", text="Edge to Edge")
    elif brush.use_airbrush:
        col.prop(brush, "rate", text="Rate", slider=True)
    elif brush.use_line or brush.use_curve:
        row = col.row(align=True)
        row.prop(brush, "spacing", text="Spacing")
    elif brush.use_space:
        row = col.row(align=True)
        row.prop(brush, "spacing", text="Spacing")
        row.prop(brush, "use_pressure_spacing", toggle=True, text="")
    else:
        col.label(text="")
    sub = col.column(align=True)
    sub.scale_y = 1
    sub.menu("VIEW3D_MT_StrokeAdv")

def SmoothStroke(self, context, layout):
    mode = context.mode
    brush = get_brush_mode(self, context)
    settings = paint_settings(context)

    row = layout.row(align=True)
    sub = row.column(align=True)
    sub.ui_units_x = 1.6
    sub.scale_y = 1.4
    sub.prop(brush, "use_smooth_stroke", text="", icon='SNAP_NORMAL' ,toggle=True)
    sub = row.column(align=True)
    sub.ui_units_x = 2.8
    sub.scale_y = 0.7
    sub.active = brush.use_smooth_stroke
    sub.prop(brush, "smooth_stroke_radius", text="Radius", slider=True)
    sub.prop(brush, "smooth_stroke_factor", text="Factor", slider=True)

def GPSmoothStroke(self, context, layout):
    mode = context.mode
    brush = get_brush_mode(self, context)
    gp_settings = brush.gpencil_settings

    row = layout.row(align=True)
    sub = row.column(align=True)
    sub.ui_units_x = 1.6
    sub.scale_y = 1.4
    sub.prop(gp_settings, "use_settings_stabilizer", text="", icon='SNAP_NORMAL', toggle=True)
    sub = row.column(align=True)
    sub.ui_units_x = 2.8
    sub.scale_y = 0.7
    sub.active = gp_settings.use_settings_stabilizer
    sub.prop(brush, "smooth_stroke_radius", text="Radius", slider=True)
    sub.prop(brush, "smooth_stroke_factor", text="Factor", slider=True)



class VIEW3D_MT_StrokeAdv(bpy.types.Menu):
    bl_label = "Settings"

    def draw(self, context):
        layout = self.layout
        mode = context.mode
        brush = get_brush_mode(self, context)
        settings = paint_settings(context)

        col = layout.column()
        col.scale_y = 1
        col.ui_units_x = 5
        col.alignment = 'RIGHT'
        col.prop(settings, "input_samples")
        '''
        if mode == 'SCULPT':
            col.row().prop(brush, "use_scene_spacing", text="Spacing Distance", expand=True)

        if mode in {'PAINT_TEXTURE', 'PAINT_2D', 'SCULPT'}:
            if brush.image_paint_capabilities.has_space_attenuation or brush.sculpt_capabilities.has_space_attenuation:
                col.prop(brush, "use_space_attenuation")
        '''
        if brush.use_curve:
            col.separator()
            col.template_ID(brush, "paint_curve", new="paintcurve.new")
            col.operator("paintcurve.draw")
            col.separator()
        if brush.use_space or brush.use_line or brush.use_curve:
            col.separator()
            row = col.row(align=True)
            col.prop(brush, "dash_ratio", text="Dash Ratio")
            col.prop(brush, "dash_samples", text="Dash Length")

        if (mode == 'SCULPT' and brush.sculpt_capabilities.has_jitter) or mode != 'SCULPT':
            col.separator()
            row = col.row(align=True)
            if brush.jitter_unit == 'BRUSH':
                row.prop(brush, "jitter", slider=True)
            else:
                row.prop(brush, "jitter_absolute")
            row.prop(brush, "use_pressure_jitter", toggle=True, text="")
            #col.row().prop(brush, "jitter_unit", expand=True)

class VIEW3D_MT_Falloff(bpy.types.Menu):
    bl_label = "Falloff"

    def draw(self, context):
        layout = self.layout
        settings = paint_settings(context)
        mode = context.mode
        brush = settings.brush
        if brush is None:
            return

        col = layout.column(align=True)
        col.ui_units_x = 2
        row = col.row(align=True)
        row.prop(brush, "curve_preset", text="")

#SCULPT----------------------------------------------------------------------------------------------

def SculptMask(self, context, layout):

    row = layout.row(align=True)

    sub = row.row(align=True)
    sub.scale_y = 1.4
    sub.scale_x = 1.3
    op = sub.operator('paint.mask_flood_fill', text='', icon='RADIOBUT_OFF')
    op.mode='VALUE'
    op.value=0
    sub.operator('paint.mask_flood_fill', text='', icon='IMAGE_ALPHA').mode='INVERT'

    sub = row.row(align=True)
    sub.scale_y = 1.4
    sub.scale_x = 1.2
    op = sub.operator('sculpt.mask_filter', text='', icon='REMOVE')
    op.filter_type='SHRINK'
    op.auto_iteration_count=True

    op = sub.operator('sculpt.mask_filter', text='', icon='ADD')
    op.filter_type='GROW'
    op.auto_iteration_count=True

    sub = row.column(align=True)
    sub.scale_y = 0.7
    sub.scale_x = 1.2
    op = sub.operator('sculpt.mask_filter', text='', icon='TRIA_UP')
    op.filter_type='SHARPEN'
    op.auto_iteration_count=True

    op = sub.operator('sculpt.mask_filter', text='', icon='TRIA_DOWN')
    op.filter_type='SMOOTH'
    op.auto_iteration_count=True

    '''
    sub = row.column(align=True)
    sub.scale_y = 0.7
    sub.scale_x = 1.1
    op = sub.operator('sculpt.mask_filter', text='', icon='LAYER_ACTIVE')
    op.filter_type='CONTRAST_INCREASE'
    op.auto_iteration_count=False
    op = sub.operator('sculpt.mask_filter', text='', icon='LAYER_USED')
    op.filter_type='CONTRAST_DECREASE'
    op.auto_iteration_count=False
    '''

class FSetPanel(bpy.types.Panel):
    bl_label = "INIT"
    bl_idname = "OBJECT_PT_Fset_panel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'WINDOW'
    bl_context = "scene"
    bl_order = 1000
    bl_options = {'DEFAULT_CLOSED',}

    def draw(self, context):
        layout = self.layout
        sculpt = context.tool_settings.sculpt
        mesh = context.active_object.data
        col = layout.column()
        sub = col.row(align=True)
        sub.operator("sculpt.face_sets_init", text='ISLAND').mode = 'LOOSE_PARTS'
        sub.operator("sculpt.face_sets_init", text='NORMAL').mode = 'NORMALS'

        sub = col.row(align=True)
        sub.operator("sculpt.face_sets_create", text='SEL').mode = 'SELECTION'
        sub.operator("sculpt.face_sets_init", text='UV').mode = 'UV_SEAMS'

def SculptFaceSet(self, context, layout):
    col = layout.column()
    col.scale_y = 0.7 
    row = col.row()
    sub = row.column(align=True)
    sub.ui_units_x = 6
    subrow = sub.row(align=True)
    subrow.operator("sculpt.face_sets_init", text='ISLAND').mode = 'LOOSE_PARTS'
    subrow.operator("sculpt.face_sets_init", text='NORMAL').mode = 'NORMALS'
    subrow.operator("sculpt.face_sets_create", text='VISIBLE').mode = 'VISIBLE'
    subrow = sub.row(align=True)
    subrow.operator("sculpt.face_sets_create", text='MASKED').mode = 'MASKED'
    subrow.operator("sculpt.face_sets_create", text='EDIT').mode = 'SELECTION'
    subrow.operator("sculpt.face_sets_init", text='UV').mode = 'UV_SEAMS'

def SculptFilterSettings(self, context, layout):
    layout = layout
    tool = context.workspace.tools.from_space_view3d_mode(bpy.context.mode).idname
    col = layout.column(align=True)
    col.alignment = 'LEFT'
    col.ui_units_x = 6.4
    col.scale_y = 0.7

    if tool == 'builtin.mesh_filter':
        tool = context.workspace.tools.from_space_view3d_mode(context.mode)
        props = tool.operator_properties("sculpt.mesh_filter")
        sub = col.row(align=True)
        sub.ui_units_x = 5
        sub.prop(props, "type", text='', expand=False)
        sub.prop(props, "strength")
        row = col.row(align=True)
        row.prop(props, "deform_axis")
        row.prop(props, "orientation", expand=False, text='')
        if props.type == 'SURFACE_SMOOTH':
            row = col.row(align=True)
            row.prop(props, "surface_smooth_shape_preservation", expand=False, slider=True, text='SHAPE')
            row.prop(props, "surface_smooth_current_vertex", expand=False, slider=True ,text='VERT')
        elif props.type == 'SHARPEN':
            row = col.row(align=True)
            row.prop(props, "sharpen_smooth_ratio", expand=False, slider=True ,text='SHRP<>SMTH')
            row.prop(props, "sharpen_intensify_detail_strength", expand=False, slider=True ,text='DETAIL')
            row.prop(props, "sharpen_curvature_smooth_iterations", expand=False, text='ITERATION')

    elif tool == 'builtin.color_filter':
        tool = context.workspace.tools.from_space_view3d_mode(context.mode)
        props = tool.operator_properties("sculpt.color_filter")
        sub = col.column(align=True)
        sub.ui_units_x = 5
        sub.prop(props, "type", text='', expand=False)
        if props.type == 'FILL':
            sub.prop(props, "fill_color", expand=False)
        sub.prop(props, "strength")

    elif tool == 'builtin.cloth_filter':
        tool = context.workspace.tools.from_space_view3d_mode(context.mode)
        props = tool.operator_properties("sculpt.cloth_filter")
        sub = col.column(align=True)
        sub.ui_units_x = 5
        subsub = sub.row(align=True)
        subsub.prop(props, "type", text='', expand=False)
        subsub.popover("OBJECT_PT_clothfilter_panel", text="SET")
        sub.prop(props, "strength")
        subsub = sub.row(align=True)
        subsub.prop(props, "force_axis")
    else:
        sub = col.row(align=True)
        sub.ui_units_x = 5
        sub.label(text='>')


class ClothFilterPanel(bpy.types.Panel):
    bl_label = "EXPORT"
    bl_idname = "OBJECT_PT_clothfilter_panel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'WINDOW'
    bl_context = "scene"
    bl_order = 1000
    bl_options = {'DEFAULT_CLOSED',}
    def draw(self, context):
        tool = context.workspace.tools.from_space_view3d_mode(context.mode)
        props = tool.operator_properties("sculpt.cloth_filter")
        layout = self.layout
        col = layout.column(align=True)
        col.prop(props, "orientation", expand=False)
        col.prop(props, "cloth_mass")
        col.prop(props, "cloth_damping")
        sub = col.row(align=True)
        sub.prop(props, "use_face_sets", toggle=True)
        sub.prop(props, "use_collisions", toggle=True)


class VIEW3D_MT_sym(bpy.types.Menu):
    bl_label = "Symmetry"

    def draw(self, context):
        layout = self.layout
        sculpt = context.tool_settings.sculpt
        mesh = context.active_object.data
        row = layout.row(align=True)
        row.prop(mesh, "use_mirror_x", text="X", toggle=True)
        row.prop(mesh, "use_mirror_y", text="Y", toggle=True)
        row.prop(mesh, "use_mirror_z", text="Z", toggle=True)

class VIEW3D_MT_sculpt_sym(bpy.types.Menu):
    bl_label = ""

    @classmethod
    def poll(cls, context):
        return ((context.sculpt_object and context.tool_settings.sculpt) and (context.region.type != 'TOOL_HEADER'))

    def draw(self, context):
        layout = self.layout
        sculpt = context.tool_settings.sculpt
        mesh = context.active_object.data

        col = layout.column()
        col.ui_units_x = 6
        sub = col.column(align=True)
        sub.scale_y = 1 
        sub.prop(sculpt, "symmetrize_direction", text='')

        sub = col.column(align=True)
        sub.scale_y = 0.7 
        sub.prop(sculpt, "radial_symmetry", text="")
        sub.label(text="RADIAL")

class VIEW3D_MT_dynamesh(bpy.types.Menu):
    bl_label = "Dyntopo"

    def draw(self, context):
        layout = self.layout
        tool_settings = context.tool_settings
        sculpt = tool_settings.sculpt

        col = layout.column(align=True)
        col.ui_units_x = 5.5
        sub = col.row(align=True)
        split = sub.split(factor=0.8, align=True)
        split.operator("sculpt.dynamic_topology_toggle",
                    depress=True if context.sculpt_object.use_dynamic_topology_sculpting else False,
                    text="DYNA",emboss=True,)
        split.popover("OBJECT_PT_dyna_panel", text="SET")


        sub = col.column(align=True)
        sub.active = context.sculpt_object.use_dynamic_topology_sculpting

        subsub = sub.row(align=True)
        item = subsub.row(align=True)

        if sculpt.detail_type_method in {'CONSTANT', 'MANUAL'}:
            item.prop(sculpt, "constant_detail_resolution", text="")
            op = item.operator("sculpt.sample_detail_size", text="", icon='EYEDROPPER')
            op.mode = 'DYNTOPO'
        elif (sculpt.detail_type_method == 'BRUSH'):
            item.prop(sculpt, "detail_percent", text="")
        else:
            item.prop(sculpt, "detail_size", text="")

        subsub = sub.row(align=True)
        subsub.prop_enum(sculpt, "detail_refine_method", 'SUBDIVIDE_COLLAPSE' ,text="FULL")
        subsub.prop_enum(sculpt, "detail_refine_method", 'COLLAPSE' ,text="COL")
        subsub.prop_enum(sculpt, "detail_refine_method", 'SUBDIVIDE' ,text="SUB")

class DynaPanel(bpy.types.Panel):
    bl_label = "EXPORT"
    bl_idname = "OBJECT_PT_dyna_panel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'WINDOW'
    bl_context = "scene"
    bl_order = 1000
    bl_options = {'DEFAULT_CLOSED',}
    def draw(self, context):
        tool_settings = context.tool_settings
        sculpt = tool_settings.sculpt
        layout = self.layout
        col = layout.column(align=True)
        col.prop_enum(sculpt, "detail_type_method", 'RELATIVE' ,text="REL")
        col.prop_enum(sculpt, "detail_type_method", 'CONSTANT' ,text="CON")
        col.prop_enum(sculpt, "detail_type_method", 'BRUSH' ,text="BRUSH")
        col.prop_enum(sculpt, "detail_type_method", 'MANUAL' ,text="MAN")

        if sculpt.detail_type_method in {'CONSTANT', 'MANUAL'}:
            col.operator("sculpt.detail_flood_fill", text='FLOOD')


class VIEW3D_MT_remesh(bpy.types.Menu):
    bl_label=""

    @classmethod
    def poll(cls, context):
        return (context.sculpt_object and context.tool_settings.sculpt)

    def draw(self, context):
        layout = self.layout
        mesh = context.active_object.data
        
        col = layout.column(align=True)
        col.ui_units_x = 6
        sub = col.row(align=True)
        split = sub.split(factor=0.82, align=True)
        split.operator("object.voxel_remesh", text="REMESH")
        split.popover("OBJECT_PT_remesh_panel", text="SET")

        sub = col.row(align=True)
        sub.prop(mesh, "remesh_voxel_size", text="")
        op = sub.operator("sculpt.sample_detail_size", text="", icon='EYEDROPPER')
        op.mode = 'VOXEL'

        sub = col.row(align=True)
        sub.operator('xm.voxelsize', text='S').size=0.01
        sub.operator('xm.voxelsize', text='M').size=0.02
        sub.operator('xm.voxelsize', text='L').size=0.05

class RemeshPanel(bpy.types.Panel):
    bl_label = "EXPORT"
    bl_idname = "OBJECT_PT_remesh_panel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'WINDOW'
    bl_context = "scene"
    bl_order = 1000
    bl_options = {'DEFAULT_CLOSED',}
    def draw(self, context):
        mesh = context.active_object.data
        layout = self.layout
        col = layout.column(align=True)
        sub = col.row()
        sub.scale_y = 0.8
        subsub = sub.column()
        subsub.ui_units_x = 1.5
        subsub .label(text="Adapt")
        subsub = sub.column()
        subsub.ui_units_x = 6
        subsub.prop(mesh, "remesh_voxel_adaptivity", text="", slider=True)

        #sub = col.row()
        #sub.scale_y = 0.8
        #sub0_col2.prop(mesh, "use_remesh_fix_poles", toggle=True)

        sub = col.row(align=False)
        sub.scale_y = 0.8
        subsub = sub.column()
        subsub.ui_units_x = 1.5
        subsub.label(text="Keep")

        subsub = sub.column()
        subsub.ui_units_x = 6
        grid = subsub.grid_flow(columns=3, align=True)
        
        grid.prop(mesh, "use_remesh_preserve_volume", text="V", toggle=True)
        grid.prop(mesh, "use_remesh_preserve_paint_mask", text="M", toggle=True)
        grid.prop(mesh, "use_remesh_preserve_sculpt_face_sets", text="FS", toggle=True)

        '''
        if context.preferences.experimental.use_sculpt_vertex_colors:
            grid.prop(mesh, "use_remesh_preserve_vertex_colors", text="VertCol", toggle=True)
        '''
#GP ----------------------------------------------------------------------------------------------

class VIEW3D_MT_GPStroke(bpy.types.Menu):
    bl_label = ""

    def draw(self, context):
        layout = self.layout
        ob = context.active_object
        ma = ob.active_material

        if ma is not None and ma.grease_pencil is not None:
            gpcolor = ma.grease_pencil

            box = layout.box()
            col = box.column()
            col.prop(gpcolor, "show_stroke", text="STROKE")
            col = box.column()

            if gpcolor.show_stroke:
                sub = col.row()
                sub.prop(gpcolor, "mode", text="")
                sub.prop(gpcolor, "stroke_style", text="")
                col.prop(gpcolor, "color", text="")
                sub = col.row()
                sub.prop(gpcolor, "use_stroke_holdout")
                if gpcolor.stroke_style == 'TEXTURE':
                    row = sub.row()
                    row.enabled = not gpcolor.lock
                    col = row.column(align=True)
                    col.template_ID(gpcolor, "stroke_image", open="image.open")
                if gpcolor.stroke_style == 'TEXTURE':
                    row =sub.row()
                    row.prop(gpcolor, "mix_stroke_factor", text="Blend", slider=True)
                    if gpcolor.mode == 'LINE':
                        sub.prop(gpcolor, "pixel_size", text="UV Factor")
                if gpcolor.mode in {'DOTS', 'BOX'}:
                    sub.prop(gpcolor, "alignment_mode")
                    sub.prop(gpcolor, "alignment_rotation")
                if gpcolor.mode == 'LINE':
                    sub.prop(gpcolor, "use_overlap_strokes")
        else:
            sub = layout.row(align=True)
            sub.label(text='>')

class VIEW3D_MT_GPFill(bpy.types.Menu):
    bl_label = ""

    def draw(self, context):
        layout = self.layout
        ob = context.active_object
        ma = ob.active_material
        if ma:
            gpcolor = ma.grease_pencil
            box = layout.box()
            col = box.column()
            col.prop(gpcolor, "show_fill", text="FILL")
            col = box.column()
            if gpcolor.show_fill:
                col.prop(gpcolor, "fill_style", text="")
                if gpcolor.fill_style == 'SOLID':
                    col.prop(gpcolor, "fill_color", text="")
                    col.prop(gpcolor, "use_fill_holdout")
                elif gpcolor.fill_style == 'GRADIENT':
                    col.prop(gpcolor, "gradient_type")
                    col.prop(gpcolor, "fill_color", text="Base Color")
                    col.prop(gpcolor, "mix_color", text="Secondary Color")
                    col.prop(gpcolor, "use_fill_holdout")
                    col.prop(gpcolor, "mix_factor", text="Blend", slider=True)
                    col.prop(gpcolor, "flip", text="Flip Colors")
                    col.prop(gpcolor, "texture_offset", text="Location")
                    row = col.row()
                    row.enabled = gpcolor.gradient_type == 'LINEAR'
                    row.prop(gpcolor, "texture_angle", text="Rotation")
                    col.prop(gpcolor, "texture_scale", text="Scale")
                elif gpcolor.fill_style == 'TEXTURE':
                    col.prop(gpcolor, "fill_color", text="Base Color")
                    col.prop(gpcolor, "use_fill_holdout")
                    col.template_ID(gpcolor, "fill_image", open="image.open")
                    col.prop(gpcolor, "mix_factor", text="Blend", slider=True)
                    col.prop(gpcolor, "texture_offset", text="Location")
                    col.prop(gpcolor, "texture_angle", text="Rotation")
                    col.prop(gpcolor, "texture_scale", text="Scale")
                    col.prop(gpcolor, "texture_clamp", text="Clip Image")

#BRUSH-TEXTURE----------------------------------------------------------------------------------------------

class VIEW3D_MT_BrushTexture(bpy.types.Menu):
    bl_label = ""

    def draw(self, context):
        layout = self.layout
        wm = context.window_manager
        mode = context.active_object.mode
        brush = get_brush_mode(self, context)
        tex_slot = brush.texture_slot

        row = layout.row(align=True)
        split = row.split(factor=0.6, align=True)
        col = split.column(align=True)
        # categorie
        col.prop(brush,"xm_tex_brush_categories",text="")
        # texture
        sub = col.row(align=True)
        subsplit = sub.split(factor=0.6, align=True)
        subsub = subsplit.row(align=True)
        subsub.scale_y = 0.5
        subsub.template_icon_view(brush,"xm_brush_texture",show_labels=False, scale_popup=1.5)
        # scale 
        subsub = subsplit.column(align=True)
        subsub.prop(tex_slot, 'scale', text='', slider=True)

        #split.separator(factor=1)

        col = split.column(align=True)
        sub = col.row(align=True)
        sub.scale_y = 0.7
        BrushTexSettings(col, brush, context.sculpt_object)

class VIEW3D_MT_TextureMask(bpy.types.Menu):
    bl_label = ""

    def draw(self, context):
        layout = self.layout
        brush = get_brush_mode(self, context)
        tex_slot = brush.texture_slot

        row = layout.row(align=True)

        sub = row.row(align=True)
        sub.ui_units_x = 4
        sub.scale_y = 1.4
        sub.prop(brush,"xm_use_mask",text="RAMP",toggle=True)

        subsub = sub.row(align=True)
        subsub.scale_x = 1.2
        subsub.active = brush.xm_use_mask
        subsub.prop(brush,"xm_invert_mask",text="",toggle=True, icon="IMAGE_ALPHA")

        sub = row.column(align=True)
        sub.ui_units_x = 4
        sub.scale_y = 0.7
        sub.active = brush.xm_use_mask
        sub.prop(brush,"xm_ramp_tonemap_l",text="L",slider=True)
        sub.prop(brush,"xm_ramp_tonemap_r",text="R",slider=True)

def BrushTexSettings(layout, brush, sculpt):
    tex_slot = brush.texture_slot

    col = layout.column(align=True)
    col.prop(tex_slot, "map_mode", text="")

    if tex_slot.map_mode == 'STENCIL':
        sub = col.row(align=True)
        sub.scale_y = 0.7
        if brush.texture and brush.texture.type == 'IMAGE':
            sub.operator("brush.stencil_fit_image_aspect")
        sub.operator("brush.stencil_reset_transform")

    if tex_slot.has_texture_angle:
        sub = col.column(align=True)
        sub.scale_y = 1
        sub.prop(tex_slot, "angle", text="Angle")
        if tex_slot.has_texture_angle_source:
            sub = col.row(align=True)
            #sub.scale_y = 0.7
            sub.prop(tex_slot, "use_rake", text="RAKE", toggle=True)

            if brush.brush_capabilities.has_random_texture_angle and tex_slot.has_random_texture_angle:
                if sculpt:
                    if brush.sculpt_capabilities.has_random_texture_angle:
                        sub.prop(tex_slot, "use_random", text="RAND", toggle=True)
                        if tex_slot.use_random:
                            sub = col.row()
                            sub.scale_y = 1
                            sub.prop(tex_slot, "random_angle", text="ANGLE")
                else:
                    sub.prop(tex_slot, "use_random", text="RAND", toggle=True)
                    if tex_slot.use_random:
                        sub = col.row()
                        #sub.scale_y = 0.7
                        sub.prop(tex_slot, "random_angle", text="ANGLE")
    if sculpt:
        sub = col.row(align=True)
        #sub.scale_y = 0.7
        sub.prop(brush, "texture_sample_bias", slider=True, text="Sample Bias")

#-----------------------------------------------------------------------------------------------------------------------

classes = (ModesMenu, VIEW3D_MT_Material, VIEW3D_MT_Material2, VIEW3D_MT_GPMaterial, ViewCamPanel, VIEW3D_MT_GPStroke, VIEW3D_MT_GPFill,  
            ImportMenu, ExportMenu, IOMenu, ImportPanel, ExportPanel, VIEW3D_MT_dynamesh, VIEW3D_MT_remesh, VIEW3D_MT_sculpt_sym, VIEW3D_MT_sym, 
            VIEW3D_MT_BrushTexture, VIEW3D_MT_TextureMask, VIEW3D_MT_StrokeAdv, VIEW3D_MT_Falloff, DynaPanel, RemeshPanel, ClothFilterPanel,
            FSetPanel
          )

def register():
    bpy.types.Scene.import_items = bpy.props.EnumProperty(default="01",items=[("01","IMPORT",""),("02","EXPORT","")])
    bpy.types.WindowManager.normalshading_state = bpy.props.BoolProperty(default = False)

    for cls in classes:
        bpy.utils.register_class(cls)

    bpy.types.OUTLINER_HT_header.prepend(HideObjectMenuBt) 

def unregister():
    bpy.types.OUTLINER_HT_header.remove(HideObjectMenuBt)

    for cls in classes:
        bpy.utils.unregister_class(cls)
