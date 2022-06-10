import bpy
from .hud import redraw_regions
from .functions import tool_grid, tool_bt, funct_bt
from bpy.types import Operator, AddonPreferences, Preferences
from bl_ui.properties_data_modifier import DATA_PT_modifiers
from bpy.types import Header, Panel, Menu
from .menuitems import BrushCopy, ModeSelector

from bl_ui.space_toolsystem_common import (
    ToolSelectPanelHelper,
    ToolDef,
)

#////////////////////////////////////////////////////////////////////////////////////////////#

def draw(self, context): 
    layout = self.layout

    dpi = bpy.context.preferences.addons[__package__].preferences.hud_dpi
    dpi_scale = 0.014*dpi
    ui_scale = context.preferences.view.ui_scale
    ts = context.tool_settings
    scene = context.scene
    view = context.space_data
    wm = context.window_manager
    ups = ts.unified_paint_settings
    ptr = ups if ups.use_unified_color else ts.image_paint.brush
    tool_mode = context.mode

    for region in bpy.context.area.regions:
        if region.type == 'WINDOW':
            view_width = region.width/(19.66*ui_scale)

    row = layout.row()
    row.ui_units_x = view_width
    row.alignment = 'CENTER'

    left = row.row()
    left.ui_units_x = view_width/2-15  
    left.alignment = 'RIGHT'
    funct_bt(parent=left, cmd='floater_08', tog=False, w=3, h=1, label='CAM', icon="NONE")
    left.separator(factor = 4)
    ModeSelector(self, context, left)
    left.separator(factor = 2)
    sub = left.row()
    funct_bt(parent=sub, cmd='frames', w=2, h=1, label='FRAME', icon="NONE")
    funct_bt(parent=sub, cmd='framea', w=2, h=1, label='ALL', icon="NONE")

    row.separator(factor = 2)

    mid = row.row()
    mid.ui_units_x = 24
    mid.alignment = 'CENTER'
    if context.mode == 'OBJECT':
        select_hud(mid, self, context)
    if context.mode == 'EDIT_MESH':  
        select_hud(mid, self, context)
        sub = mid.row()
        subsub = sub.row()
        subsub.ui_units_x = 5
        subsub.menu_contents("VIEW3D_MT_sym")
    if context.mode == 'SCULPT':
        brush = context.tool_settings.sculpt.brush
        paint_hud(mid, brush, self, context)
        sub = mid.row()
        subsub = sub.row()
        subsub.ui_units_x = 5
        subsub.menu_contents("VIEW3D_MT_sym")
    if context.mode == 'PAINT_VERTEX':
        brush = context.tool_settings.vertex_paint.brush
        ColorHud(self, context, parent=mid)
        paint_hud(mid, brush, self, context)
        sub = mid.row()
        subsub = sub.row()
        subsub.ui_units_x = 5
        subsub.menu_contents("VIEW3D_MT_sym")
    if context.mode == 'PAINT_WEIGHT':
        brush = context.tool_settings.weight_paint.brush
        paint_hud(mid, brush, self, context)
        sub = mid.row()
        subsub = sub.row()
        subsub.ui_units_x = 5
        subsub.menu_contents("VIEW3D_MT_sym")
    if context.mode == 'PAINT_TEXTURE':
        brush = context.tool_settings.image_paint.brush
        ColorHud(self, context, parent=mid)
        paint_hud(mid, brush, self, context)
        sub = mid.row()
        subsub = sub.row()
        subsub.ui_units_x = 5
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

    right = row.row()
    right.alignment = 'LEFT'
    right.ui_units_x = view_width/2-15
    sub = right.row()
    funct_bt(parent=sub, cmd='wire', tog=True, w=2, h=1, label='WIRE', icon="NONE")
    funct_bt(parent=sub, cmd='xray', tog=True, w=2, h=1, label='XRAY', icon="NONE")
    sub.separator(factor = 1) 
    funct_bt(parent=sub, cmd='persp', tog=True, w=2, h=1, label='PERSP', icon="NONE")
    sub.separator(factor = 2)
    subsub = sub.row(align=True)
    funct_bt(parent=subsub, cmd='floater_01', tog=True, w=2, h=1, label='', icon="OUTLINER")
    funct_bt(parent=subsub, cmd='floater_02', tog=True, w=2, h=1, label='', icon="PROPERTIES")
    funct_bt(parent=subsub, cmd='floater_03', tog=True, w=2, h=1, label='', icon="MODIFIER")
    funct_bt(parent=subsub, cmd='floater_04', tog=True, w=2, h=1, label='', icon="NODE_MATERIAL")
    funct_bt(parent=subsub, cmd='floater_05', tog=True, w=2, h=1, label='', icon="UV")
    funct_bt(parent=subsub, cmd='floater_06', tog=True, w=2, h=1, label='', icon="IMAGE")
    funct_bt(parent=subsub, cmd='floater_07', tog=True, w=2, h=1, label='', icon="NODETREE")


    #sub.separator(factor = 55)

def paint_hud(parent, brush,  self, context):
    ts = context.tool_settings
    ups = ts.unified_paint_settings

    #ptr = ups if ups.use_unified_color else ts.image_paint.brush

    sub = parent.row(align=True)
    sub.alignment = 'CENTER'
    sub.ui_units_x = 7
    sub.prop(ups, "size", slider=True)
    sub.prop(brush, "use_pressure_size", slider=True, text="")
    sub = parent.row(align=True)
    sub.separator(factor = 0.4)
    sub.ui_units_x = 7
    sub.prop(brush, "strength", slider=True)
    sub.prop(brush, "use_pressure_strength", slider=True, text="") 

def ColorHud(self, context, parent):
    ts = context.tool_settings
    ups = ts.unified_paint_settings
    if context.mode == 'PAINT_VERTEX':
        ptr = ts.vertex_paint.brush
    else:
        ptr = ups if ups.use_unified_color else ts.image_paint.brush    
    
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
    #sub.ui_units_x = 20

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

def register() :
    bpy.types.VIEW3D_HT_tool_header.prepend(draw)

def unregister() :
    bpy.types.VIEW3D_HT_tool_header.remove(draw)

