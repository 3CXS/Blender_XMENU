import bpy
from .hud import redraw_regions
from .functions import tool_grid, tool_bt, funct_bt
from bpy.types import Operator, AddonPreferences
from bl_ui.properties_data_modifier import DATA_PT_modifiers
from bpy.types import Header, Panel, Menu
from .menuitems import BrushCopy
#////////////////////////////////////////////////////////////////////////////////////////////#



def draw(self, context):
    
    layout = self.layout

    layout.use_property_split = False
    layout.use_property_decorate = False


    dpi = bpy.context.preferences.addons[__package__].preferences.hud_dpi
    dpi_scale = 0.014*dpi

    ts = context.tool_settings
    scene = context.scene
    view = context.space_data
    wm = context.window_manager
    ups = ts.unified_paint_settings
    ptr = ups if ups.use_unified_color else ts.image_paint.brush
    tool_mode = context.mode
    mesh = context.active_object.data

    brush = context.tool_settings.sculpt.brush
    direction = not brush.sculpt_capabilities.has_direction
    for region in bpy.context.area.regions:
        if region.type == 'WINDOW':
            view_width = region.width/(23*dpi_scale)


    if bpy.context.mode == 'SCULPT':  

        top_row = layout.row()
        top_row.ui_units_x = view_width
        top_row.alignment = 'CENTER'
        funct_bt(parent=top_row, cmd='persp', tog=True, w=2, h=1, label='PERSP', icon="NONE")
        top_row.separator(factor = 1) 
        funct_bt(parent=top_row, cmd='frames', w=2, h=1, label='FRAME', icon="NONE")
        funct_bt(parent=top_row, cmd='framea', w=2, h=1, label='ALL', icon="NONE")
        top_row.separator(factor = 12)
        size = top_row.row(align=True)
        size.ui_units_x = 8
        size.prop(ups, "size", slider=True)
        size.prop(brush, "use_pressure_size", slider=True, text="")
        strength = top_row.row(align=True)
        strength.ui_units_x = 8
        strength.prop(brush, "strength", slider=True)
        strength.prop(brush, "use_pressure_strength", slider=True, text="")
        if direction:
            top_row.prop(brush, "direction", expand=True, text="")
        else:
            top_row.label(text="XXXX")
        #top_row.prop(brush, "normal_radius_factor", slider=True)
        top_row.separator(factor = 16)
        top_row.menu_contents("VIEW3D_MT_sym") 
        funct_bt(parent=top_row, cmd='wire', tog=True, w=2, h=1, label='WIRE', icon="NONE")
        funct_bt(parent=top_row, cmd='xray', tog=True, w=2, h=1, label='XRAY', icon="NONE")


#////////////////////////////////////////////////////////////////////////////////////////////#

def register() :
    bpy.types.VIEW3D_HT_tool_header.prepend(draw)

def unregister() :
    bpy.types.VIEW3D_HT_tool_header.remove(draw)

