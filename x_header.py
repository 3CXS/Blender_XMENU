import bpy

from bpy.types import Operator, Header, Panel, Menu, AddonPreferences, Preferences
from bl_ui.space_toolsystem_common import (ToolSelectPanelHelper, ToolDef)

from .hud import redraw_regions
from .functions import tool_bt, funct_bt, paint_settings
from .menuitems import Normals, BrushCopy, ModeSelector, Overlay, History, PaintHud, ColorHud, GPColorHud, SelectHud, GPSelectHud, GPPaintHud

#-----------------------------------------------------------------------------------------------------------------------

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

#LAYOUT-STRUCTURE-----------------------------------------------------------------------------------------

    row = layout.row()
    row.ui_units_x = view_width
    row.alignment = 'CENTER'

    left = row.row(align=True)
    left.ui_units_x = view_width/2-15  
    left.alignment = 'RIGHT'

    mid = row.row(align=True)
    mid.ui_units_x = 27
    mid.alignment = 'CENTER'

    right = row.row(align =True)
    right.alignment = 'LEFT'
    right.ui_units_x = view_width/2-15

    #LEFT -------------------------------------------------------------------------------------------------

    ModeSelector(self, context, left)
    left.separator(factor = 4.7)

    sub = left.row(align=True)
    funct_bt(layout=sub, cmd='viewcam', tog=True, w=1.8, h=1, label='', icon="CAMERA_DATA")
    funct_bt(layout=sub, cmd='lockcam', tog=True, w=1.2, h=1, label='', icon="LOCKED")
    sub.popover("OBJECT_PT_viewcam", text='', icon="SETTINGS")
    sub.separator(factor = 1)
    funct_bt(layout=sub, cmd='framea', w=2, h=1, label='ALL', icon="NONE")
    funct_bt(layout=sub, cmd='frames', w=2, h=1, label='SEL', icon="NONE")
    funct_bt(layout=sub, cmd='localview',tog=True, w=2, h=1, label='ISO', icon="NONE")

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

    funct_bt(layout=sub, cmd='persp', tog=False, w=1.2, h=1, label='', icon=icon_view)

    if bpy.types.WindowManager.max_area_state == False:
        icon_area = 'TRIA_UP'
    else:
        icon_area = 'TRIA_DOWN'
    funct_bt(layout=sub, cmd='max_area', tog=False, w=1.2, h=1, label='', icon=icon_area)

    #funct_bt(layout=sub, cmd='move_area', tog=False, w=1.2, h=1, label='XX')

    left.separator(factor = 1)

    #MID --------------------------------------------------------------------------------------------------

    if context.mode == 'OBJECT':
#       selection:
        SelectHud(mid, self, context)
        mid.separator(factor=2)

#       pivot to COG:
        op = mid.operator('object.origin_set', text='', icon='PIVOT_BOUNDBOX') # COG
        op.type = 'ORIGIN_GEOMETRY'
        op.center ='MEDIAN'

        mid.operator('object.pivotobottom', text='', icon='IMPORT')        #needs 3d viewport pie menu addon#

        op = mid.operator('object.origin_set', text='', icon='PIVOT_CURSOR')
        op.type = 'ORIGIN_CURSOR'
        op.center ='MEDIAN'

        mid.separator(factor=2)

    if context.mode == 'EDIT_MESH':

        sub = mid.row(align=True)
        sub.scale_x = 1.5
        sub.template_edit_mode_selection()

        mid.separator(factor=1)
        SelectHud(mid, self, context)

        mid.separator()
        sub = mid.row(align=True)


#       extra:
        tool_bt(layout=sub, cmd=0, w=1.2, h=1, text='', icon='CUSTOM')
 
        sub.operator('mesh.target_weld_toggle', text='', icon='CON_TRACKTO')

        ts = context.tool_settings
        sub.prop(ts, "use_mesh_automerge", text="", toggle=True)

        sub.separator(factor=1)
        sub.operator('mesh.quick_pivot', text='', icon='PIVOT_BOUNDBOX')

        mid.separator(factor=1)

        sub = mid.row()
        sub.ui_units_x = 5
        sub.menu_contents("VIEW3D_MT_sym")

        mid.separator(factor=1)

        sub = mid.row(align=True)
        sub.ui_units_x = 1.2
        sub.operator('mesh.reveal', icon='HIDE_OFF', text="")
        sub = mid.row(align=True)
        sub.ui_units_x = 1.2
        sub.operator('mesh.hide', icon='HIDE_ON', text="").unselected=False



    if context.mode == 'SCULPT':
        brush = context.tool_settings.sculpt.brush
        ColorHud(self, context, layout=mid)
        PaintHud(mid, brush, self, context)
        mid.separator(factor = 2)

        sub = mid.row()
        sub.ui_units_x = 4
        sub.menu_contents("VIEW3D_MT_sym")

    if context.mode == 'PAINT_VERTEX':
        brush = context.tool_settings.vertex_paint.brush
        ColorHud(self, context, layout=mid)
        PaintHud(mid, brush, self, context)
        mid.separator(factor = 4)
        sub = mid.row()
        sub.ui_units_x = 4
        sub.menu_contents("VIEW3D_MT_sym")

    if context.mode == 'PAINT_WEIGHT':
        ts = context.tool_settings
        ups = ts.unified_paint_settings
        brush = context.tool_settings.weight_paint.brush


        mid.prop(ups, 'weight', slider=True)
        mid.separator(factor = 1)
        PaintHud(mid, brush, self, context)
        mid.separator(factor = 4)
        sub = mid.row(align=True)
        sub.ui_units_x = 4
        sub.menu_contents("VIEW3D_MT_sym")

    if context.mode == 'PAINT_TEXTURE':
        brush = context.tool_settings.image_paint.brush
        ColorHud(self, context, layout=mid)
        PaintHud(mid, brush, self, context)
        mid.separator(factor = 4)
        sub = mid.row()
        sub.ui_units_x = 4
        sub.menu_contents("VIEW3D_MT_sym")

    if context.mode == 'PAINT_GPENCIL':
        brush = context.tool_settings.gpencil_paint.brush

        GPColorHud(self, context, layout=mid)
        mid.separator(factor = 4)
        GPPaintHud(mid, context, brush)


    if context.mode == 'EDIT_GPENCIL':
        sub = mid.row(align=True)
        sub.ui_units_x = 4
        sub.scale_y = 1
        sub.operator("gpencil.stroke_arrange", text="UP").direction='UP'
        sub.operator("gpencil.stroke_arrange", text="DOWN").direction='DOWN'
        GPSelectHud(mid, self, context)

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
        PaintHud(mid, brush, self, context)

    row.separator(factor = 1)

    #RIGHT --------------------------------------------------------------------------------------------------

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

    #funct_bt(layout=sub, cmd='wire', tog=True, w=2, h=1, label='WIRE', icon="NONE")#global wireframe
    funct_bt(layout=sub, cmd='faceorient', tog=True, w=1.6, h=1, label='', icon="NORMALS_FACE")
    funct_bt(layout=sub, cmd='xray', tog=True, w=1.6, h=1, label='', icon="XRAY")

    sub.separator(factor = 2)
    subsub = sub.row(align=True)
    funct_bt(layout=subsub, cmd='floater_01', tog=True, w=2, h=1, label='', icon="OUTLINER")
    funct_bt(layout=subsub, cmd='floater_02', tog=True, w=2, h=1, label='', icon="PROPERTIES")
    funct_bt(layout=subsub, cmd='floater_03', tog=True, w=2, h=1, label='', icon="MODIFIER")
    funct_bt(layout=subsub, cmd='floater_04', tog=True, w=2, h=1, label='', icon="NODE_MATERIAL")
    funct_bt(layout=subsub, cmd='floater_05', tog=True, w=2, h=1, label='', icon="UV")
    funct_bt(layout=subsub, cmd='floater_06', tog=True, w=2, h=1, label='', icon="IMAGE")
    subsub.popover("OBJECT_PT_floater", text=' ', text_ctxt='', icon='MENU_PANEL')

    subsub = sub.row(align=True)
    subsub.ui_units_x = 3
    subsub.label(text='')
    subsub = sub.row(align=True)
    subsub.scale_x = 1.8
    History(self, context, layout=subsub)

    redraw_regions()

#-----------------------------------------------------------------------------------------------------------------------

def register():
    bpy.types.VIEW3D_HT_tool_header.prepend(draw)

def unregister():
    bpy.types.VIEW3D_HT_tool_header.remove(draw)


