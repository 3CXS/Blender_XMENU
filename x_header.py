import bpy

from bpy.types import Operator, AddonPreferences, Preferences, Header, Panel, Menu
from bl_ui.space_toolsystem_common import (ToolSelectPanelHelper, ToolDef)
from .hud import redraw_regions
from .functions import tool_grid, tool_bt, funct_bt, paint_settings
from .menuitems import BrushCopy, ModeSelector, Overlay

#////////////////////////////////////////////////////////////////////////////////////////////#

def draw(self, context): 
    layout = self.layout

    ui_scale = context.preferences.view.ui_scale
    ts = context.tool_settings
    scene = context.scene
    view = context.space_data
    wm = context.window_manager
    ups = ts.unified_paint_settings
    ptr = ups if ups.use_unified_color else ts.image_paint.brush
    tool_mode = context.mode
    ob = context.active_object
    overlay = view.overlay

    for region in bpy.context.area.regions:
        if region.type == 'WINDOW':
            view_width = region.width/(19.66*ui_scale)

    row = layout.row()
    row.ui_units_x = view_width
    row.alignment = 'CENTER'

    left = row.row()
    left.ui_units_x = view_width/2-15  
    left.alignment = 'RIGHT'
    ModeSelector(self, context, left)
    left.separator(factor = 2)

    sub = left.row(align=True)
    funct_bt(parent=sub, cmd='framea', w=2, h=1, label='ALL', icon="NONE")
    funct_bt(parent=sub, cmd='frames', w=2, h=1, label='FRME', icon="NONE")
    funct_bt(parent=sub, cmd='localview',tog=True, w=2, h=1, label='ISO', icon="NONE")

    sub.separator(factor = 1)
    for window in bpy.context.window_manager.windows:
        screen = window.screen
        for area in screen.areas:
            if area.type == 'VIEW_3D':
                space = area.spaces.active
                if space.region_3d.view_perspective == 'PERSP':
                    icon_view = "VIEW_PERSPECTIVE"
                else:
                    icon_view = "VIEW_ORTHO"
    funct_bt(parent=sub, cmd='persp', tog=False, w=1.2, h=1, label='', icon=icon_view)


    if bpy.types.WindowManager.maxarea_state == False:
        icon_area = 'TRIA_DOWN'
    else:
        icon_area = 'TRIA_UP'
    funct_bt(parent=sub, cmd='maxarea', tog=False, w=1.2, h=1, label='', icon=icon_area)

    row.separator(factor = 2)

    mid = row.row()
    mid.ui_units_x = 24
    mid.alignment = 'CENTER'
    if context.mode == 'OBJECT':
        select_hud(mid, self, context)
    if context.mode == 'EDIT_MESH':
        sub = mid.row()
        #sub.ui_units_x = 6
        sub.template_edit_mode_selection()  
        select_hud(mid, self, context)
        sub = mid.row()
        subsub = sub.row()
        subsub.ui_units_x = 5
        subsub.separator(factor = 1)
        subsub.menu_contents("VIEW3D_MT_sym")
    if context.mode == 'SCULPT':
        brush = context.tool_settings.sculpt.brush
        ColorHud(self, context, parent=mid)
        paint_hud(mid, brush, self, context)
        sub = mid.row()
        subsub = sub.row()
        subsub.ui_units_x = 5
        subsub.separator(factor = 1)
        subsub.menu_contents("VIEW3D_MT_sym")
    if context.mode == 'PAINT_VERTEX':
        brush = context.tool_settings.vertex_paint.brush
        ColorHud(self, context, parent=mid)
        paint_hud(mid, brush, self, context)
        sub = mid.row()
        subsub = sub.row()
        subsub.ui_units_x = 5
        subsub.separator(factor = 1)
        subsub.menu_contents("VIEW3D_MT_sym")
    if context.mode == 'PAINT_WEIGHT':
        brush = context.tool_settings.weight_paint.brush
        paint_hud(mid, brush, self, context)
        sub = mid.row()
        subsub = sub.row()
        subsub.ui_units_x = 5
        subsub.separator(factor = 1)
        subsub.menu_contents("VIEW3D_MT_sym")
    if context.mode == 'PAINT_TEXTURE':
        brush = context.tool_settings.image_paint.brush
        ColorHud(self, context, parent=mid)
        paint_hud(mid, brush, self, context)
        sub = mid.row()
        subsub = sub.row()
        subsub.ui_units_x = 5
        subsub.separator(factor = 1)
        subsub.menu_contents("VIEW3D_MT_sym")
    if context.mode == 'PAINT_GPENCIL':
        brush = context.tool_settings.gpencil_paint.brush
        gp_settings = brush.gpencil_settings
        #row = mid.row(align=True)
        sub = mid.row(align=True)
        sub.alignment = 'CENTER'
        sub.ui_units_x = 8
        sub.prop(brush, "size", text="Radius")
        sub.prop(gp_settings, "use_pressure", text="", icon='STYLUS_PRESSURE')
        sub.separator(factor = 1)
        sub = mid.row(align=True)
        sub.ui_units_x = 8
        sub.prop(gp_settings, "pen_strength", slider=True)
        sub.prop(gp_settings, "use_strength_pressure", text="", icon='STYLUS_PRESSURE')
    if context.mode == 'EDIT_GPENCIL':
        gp_select_hud(mid, self, context)
    if context.mode == 'SCULPT_GPENCIL':
        brush = context.tool_settings.gpencil_sculpt_paint.brush
        gp_settings = brush.gpencil_settings
        sub = mid.row(align=True)
        sub.alignment = 'CENTER'
        sub.ui_units_x = 8
        sub.prop(brush, "size", text="Radius")
        sub.prop(gp_settings, "use_pressure", text="", icon='STYLUS_PRESSURE')
        sub.separator(factor = 1)
        sub = mid.row(align=True)
        sub.ui_units_x = 8
        sub.prop(brush, "strength", slider=True)
        sub.prop(brush, "use_pressure_strength", text="", icon='STYLUS_PRESSURE')
    if context.mode == 'WEIGHT_GPENCIL':
        brush = context.tool_settings.gpencil_weight_paint.brush
        gp_settings = brush.gpencil_settings
        sub = mid.row(align=True)
        sub.alignment = 'CENTER'
        sub.ui_units_x = 5
        sub.prop(brush, "size", text="Radius")
        sub.separator(factor = 1)
        sub = mid.row(align=True)
        sub.ui_units_x = 5
        sub.prop(brush, "weight", text="Weight")
        sub.separator(factor = 1)
        sub = mid.row(align=True)
        sub.ui_units_x = 5
        sub.prop(brush, "strength", slider=True)
        sub.prop(brush, "use_pressure_strength", text="", icon='STYLUS_PRESSURE')
    if context.mode == 'VERTEX_GPENCIL':
        brush = context.tool_settings.gpencil_vertex_paint.brush
        paint_hud(mid, brush, self, context)

    row.separator(factor = 2)

    right = row.row(align =True)
    right.alignment = 'LEFT'
    right.ui_units_x = view_width/2-15
    sub = right.row(align =True)  
    subsub = sub.column(align =True)
    subsub.ui_units_x = 1.6

    if ob != None and ob.type == 'MESH':
        if context.mode == 'EDIT_MESH':
            subsub.prop(overlay, "show_occlude_wire", text="", icon="MOD_WIREFRAME", toggle=True)
        else:
            subsub.prop(ob, "show_wire", text="", icon="MOD_WIREFRAME", toggle=True)
    else:
        subsub.prop(overlay, "show_occlude_wire", text="", icon="MOD_WIREFRAME", toggle=True)

    #funct_bt(parent=sub, cmd='wire', tog=True, w=2, h=1, label='WIRE', icon="NONE")#global wireframe
    funct_bt(parent=sub, cmd='faceorient', tog=True, w=1.6, h=1, label='', icon="NORMALS_FACE")
    funct_bt(parent=sub, cmd='xray', tog=True, w=1.6, h=1, label='', icon="XRAY")

    sub.separator(factor = 2)
    subsub = sub.row(align=True)
    funct_bt(parent=subsub, cmd='floater_01', tog=True, w=2, h=1, label='', icon="OUTLINER")
    funct_bt(parent=subsub, cmd='floater_02', tog=True, w=2, h=1, label='', icon="PROPERTIES")
    funct_bt(parent=subsub, cmd='floater_03', tog=True, w=2, h=1, label='', icon="MODIFIER")
    funct_bt(parent=subsub, cmd='floater_04', tog=True, w=2, h=1, label='', icon="NODE_MATERIAL")
    funct_bt(parent=subsub, cmd='floater_05', tog=True, w=2, h=1, label='', icon="UV")
    funct_bt(parent=subsub, cmd='floater_06', tog=True, w=2, h=1, label='', icon="IMAGE")
    #subsub.menu("VIEW3D_MT_Floater", text=">>")
    subsub.popover("OBJECT_PT_floater", text=' ', text_ctxt='', icon='MENU_PANEL')

    subsub.separator(factor = 2)

    #subsub.menu("VIEW3D_MT_Material")

    redraw_regions()

#////////////////////////////////////////////////////////////////////////////////////////////#
class FloaterPanel(bpy.types.Panel):
    bl_idname = "OBJECT_PT_floater"
    bl_label = "Floaters"
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = "scene"
    bl_order = 1000
    bl_options = {'DEFAULT_CLOSED',}

    def draw(self, context):
        layout = self.layout

        col = layout.column(align=True)
        row = col.row(align=True)

        funct_bt(parent=row, cmd='floater_07', tog=True, w=2, h=1, label='GEO',)
        funct_bt(parent=row, cmd='floater_09', tog=True, w=2, h=1, label='BAKE',)
        funct_bt(parent=row, cmd='floater_08', tog=True, w=2, h=1, label='CAM',)
        funct_bt(parent=row, cmd='floater_10', tog=True, w=2, h=1, label='COMP',)


def paint_hud(parent, brush, self, context):
    ts = context.tool_settings
    ups = ts.unified_paint_settings
    ptr = ups if ups.use_unified_size else paint_settings(context).brush
    pts = ups if ups.use_unified_strength else paint_settings(context).brush

    sub = parent.row(align=True)
    sub.alignment = 'CENTER'
    sub.ui_units_x = 7
    sub.prop(ptr, "size", slider=True)
    sub.prop(brush, "use_pressure_size", slider=True, text="")
    sub = parent.row(align=True)
    sub.separator(factor = 0.4)
    sub.ui_units_x = 7
    sub.prop(pts, "strength", slider=True)
    sub.prop(brush, "use_pressure_strength", slider=True, text="") 

def ColorHud(self, context, parent):
    ts = context.tool_settings
    ups = ts.unified_paint_settings

    if context.mode == 'PAINT_VERTEX':
        ptr = ts.vertex_paint.brush
    if context.mode == 'SCULPT':
        ptr = ts.sculpt.brush
    else:
        ptr = ups if ups.use_unified_color else paint_settings(context).brush   
    
    row = parent.row(align=True)

    sub = row.row(align=True)
    sub.ui_units_x = 2.6
    sub.prop(ptr, 'color', text="")
    #sub.prop(ptr, 'secondary_color', text="")

    sub = row.row(align=True)
    sub.ui_units_x = 2.4
    sub.operator("paint.brush_colors_flip", icon='FILE_REFRESH', text="")
    sub.operator("xmenu.override", icon='EYEDROPPER', text="").cmd ='ui.eyedropper_color'

def select_hud(parent, self, context):
    sub = parent.row()
    sub.alignment = 'CENTER'
    sub.ui_units_x = 12
    tool = context.workspace.tools.from_space_view3d_mode(context.mode)
    toolname = context.workspace.tools.from_space_view3d_mode(context.mode).idname

    if toolname == 'builtin.select':
        icon_id = ToolSelectPanelHelper._icon_value_from_icon_handle("ops.generic.select")
        sub.template_icon(icon_value=icon_id)
        sub.separator(factor = 2)
        sub.label(text="TWEAK")
    if toolname == 'builtin.select_box':
        icon_id = ToolSelectPanelHelper._icon_value_from_icon_handle("ops.generic.select_box")
        sub.template_icon(icon_value=icon_id)
        props = tool.operator_properties("view3d.select_box")
        sub.prop(props, "mode", text="", expand=True, icon_only=True)
    if toolname == 'builtin.select_circle':
        icon_id = ToolSelectPanelHelper._icon_value_from_icon_handle("ops.generic.select_circle")
        sub.template_icon(icon_value=icon_id)
        props = tool.operator_properties("view3d.select_circle")
        sub.prop(props, "mode", text="", expand=True, icon_only=True)
        sub.prop(props, "radius")
    if toolname == 'builtin.select_lasso':
        icon_id = ToolSelectPanelHelper._icon_value_from_icon_handle("ops.generic.select_lasso")
        sub.template_icon(icon_value=icon_id)
        props = tool.operator_properties("view3d.select_lasso")
        sub.prop(props, "mode", text="", expand=True, icon_only=True)

def gp_select_hud(parent, self, context):
    sub = parent.row()
    sub.alignment = 'CENTER'
    #sub.ui_units_x = 16

    tool = context.workspace.tools.from_space_view3d_mode(context.mode)
    toolname = context.workspace.tools.from_space_view3d_mode(context.mode).idname

    if toolname == 'builtin.select':
        icon_id = ToolSelectPanelHelper._icon_value_from_icon_handle("ops.generic.select")
        sub.template_icon(icon_value=icon_id)
        sub.separator(factor = 2)
        sub.label(text="TWEAK")
    if toolname == 'builtin.select_box':
        icon_id = ToolSelectPanelHelper._icon_value_from_icon_handle("ops.generic.select_box")
        sub.template_icon(icon_value=icon_id)
        props = tool.operator_properties("gpencil.select_box")
        sub.prop(props, "mode", text="", expand=True, icon_only=True)
    if toolname == 'builtin.select_circle':
        icon_id = ToolSelectPanelHelper._icon_value_from_icon_handle("ops.generic.select_circle")
        sub.template_icon(icon_value=icon_id)
        props = tool.operator_properties("gpencil.select_circle")
        sub.prop(props, "mode", text="", expand=True, icon_only=True)
        sub.prop(props, "radius")
    if toolname == 'builtin.select_lasso':
        icon_id = ToolSelectPanelHelper._icon_value_from_icon_handle("ops.generic.select_lasso")
        sub.template_icon(icon_value=icon_id)
        props = tool.operator_properties("gpencil.select_lasso")
        sub.prop(props, "mode", text="", expand=True, icon_only=True)


#////////////////////////////////////////////////////////////////////////////////////////////#
classes = (FloaterPanel,)

def register():
    for cls in classes:
        bpy.utils.register_class(cls)

    bpy.types.VIEW3D_HT_tool_header.prepend(draw)

def unregister():
    bpy.types.VIEW3D_HT_tool_header.remove(draw)

    for cls in classes:
        bpy.utils.unregister_class(cls)
