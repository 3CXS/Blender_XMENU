import bpy

import os, platform

from bpy.types import Operator, Header, Panel, Menu, AddonPreferences, Preferences, VIEW3D_MT_editor_menus, VIEW3D_HT_header
from bl_ui.space_toolsystem_common import (ToolSelectPanelHelper, ToolDef)
from bl_ui.properties_paint_common import (UnifiedPaintPanel,brush_basic_texpaint_settings,)
from bl_ui.properties_grease_pencil_common import (AnnotationDataPanel,AnnotationOnionSkin,GreasePencilMaterialsPanel,GreasePencilVertexcolorPanel)
from bpy.app.translations import contexts as i18n_contexts
import addon_utils

from .functions import tool_bt, funct_bt, paint_settings, redraw_regions, update_normaldisp
from .menuitems import Normals, BrushCopy, ModeSelector, Overlay, History, PaintHud, ColorHud, GPColorHud, SelectHud, GPSelectHud, GPPaintHud, InsertSpace, Overlay_Wire

#-------------------------------------------------------------------------------------------------------------
def draw_image_header(self, context):
    layout = self.layout
    row = layout.row(align=True)
    funct_bt(layout=row, cmd='setui_image', tog=True, w=2, h=1, label='IMAGE', icon="NONE")
    funct_bt(layout=row, cmd='setui_uv', tog=True, w=2, h=1, label='UV', icon="NONE")
    funct_bt(layout=row, cmd='setui_text', tog=True, w=2, h=1, label='TEXT', icon="NONE")
    row.separator(factor=2)

def draw_node_header(self, context):
    layout = self.layout
    row = layout.row(align=True)
    funct_bt(layout=row, cmd='setui_material', tog=True, w=2, h=1, label='MAT', icon="NONE")
    if addon_utils.check("BakeWrangler")[1]==True:
        funct_bt(layout=row, cmd='setui_bake', tog=True, w=2, h=1, label='BAKE', icon="NONE")
    else:
        row.label(text='>>')
    funct_bt(layout=row, cmd='setui_geo', tog=True, w=2, h=1, label='GEO', icon="NONE")
    funct_bt(layout=row, cmd='setui_tex', tog=True, w=2, h=1, label='TEX', icon="NONE")
    funct_bt(layout=row, cmd='setui_comp', tog=True, w=2, h=1, label='COMP', icon="NONE")
    row.separator(factor=2)


class TogXHeader(bpy.types.Operator):
    bl_idname = "xm.togxheader"
    bl_label = ""
    bpy.types.WindowManager.togxheader_state = bpy.props.BoolProperty(default = True)
    def execute(self, context):
        if bpy.types.WindowManager.togxheader_state == False:
            bpy.types.VIEW3D_HT_tool_header.prepend(draw_3d_toolsettings)
            bpy.types.VIEW3D_HT_header.prepend(VIEW3D_HT_x_header.draw)
            bpy.types.WindowManager.togxheader_state = True
        else:
            bpy.types.VIEW3D_HT_tool_header.remove(draw_3d_toolsettings)
            bpy.types.VIEW3D_HT_header.remove(VIEW3D_HT_x_header.draw)
            bpy.types.WindowManager.togxheader_state = False

        redraw_regions()

        return {'FINISHED'}


#-----------------------------------------------------------------------------------------------------------#
#                                          - TOOLSETTINS -                                                  #
#-----------------------------------------------------------------------------------------------------------#

def draw_3d_toolsettings(self, context):
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

    # LAYOUT-STRUCTURE-----------------------------------------------------------------------------------------
    main_row = layout.row(align=True)
    main_row.ui_units_x = view_width
    main_row.alignment = 'CENTER'
    
    row = main_row.row(align=True)
    row.alignment = 'CENTER'
  
    # LEFTOUTER
    leftouter = row.row(align=True)
    leftouter.ui_units_x = 15
    leftouter.alignment = 'LEFT'
    # LEFT
    left = row.row(align=True)
    left.ui_units_x = 7.5
    left.alignment = 'RIGHT'
    # LEFT_MID
    leftmid = row.row(align=True)
    leftmid.ui_units_x = 8
    leftmid.alignment = 'RIGHT'
    # MID
    mid = row.row(align=True)
    mid.ui_units_x = 18.5
    mid.alignment = 'LEFT'
    # RIGHT_MID
    rightmid = row.row(align =True)
    rightmid.alignment = 'LEFT'
    rightmid.ui_units_x = 8
    # RIGHT
    right = row.row(align =True)
    right.alignment = 'LEFT'
    right.ui_units_x = 7.5
    # RIGHTOUTER
    rightouter = row.row(align =True)
    rightouter.alignment = 'RIGHT'
    rightouter.ui_units_x = 15

    # LEFT OUTER --------------------------------------------------------------------------------------------
    row = leftouter.row(align=True)

    # Modes
    ModeSelector(self, context, row)
    row.separator(factor = 2)
    
    # Cam
    funct_bt(layout=row, cmd='viewcam', tog=True, w=1.8, h=1, label='CAM', icon="NONE")
    funct_bt(layout=row, cmd='lockcam', tog=True, w=1.2, h=1, label='', icon="LOCKED")
    row.popover("OBJECT_PT_viewcam", text='', icon="NONE")
    row.separator(factor = 2)

    # LEFT -------------------------------------------------------------------------------------------------
    row = left.row(align=True)

    # View
    funct_bt(layout=row, cmd='framea', w=1.5, h=1, label='ALL', icon="NONE")
    funct_bt(layout=row, cmd='frames', w=1.5, h=1, label='SEL', icon="NONE")
    funct_bt(layout=row, cmd='localview',tog=True, w=1.5, h=1, label='ISO', icon="NONE")
    row.separator(factor = 2)

    # Tog-Persp
    for window in bpy.context.window_manager.windows:
        screen = window.screen
        for area in screen.areas:
            if area.type == 'VIEW_3D':
                space = area.spaces.active
                if space.region_3d.view_perspective == 'PERSP':
                    icon_view = "VIEW_PERSPECTIVE"
                else:
                    icon_view = "VIEW_ORTHO"
    funct_bt(layout=row, cmd='persp', tog=False, w=1.2, h=1, label='', icon=icon_view)

    # Tog-Area
    if bpy.types.WindowManager.max_area_state == False:
        icon_area = 'TRIA_UP'
    else:
        icon_area = 'TRIA_DOWN'
    funct_bt(layout=row, cmd='max_area', tog=False, w=1.2, h=1, label='', icon=icon_area)

    row.separator(factor = 1)
    #MID --------------------------------------------------------------------------------------------------

    if context.mode == 'OBJECT':  #OBJECT//////////////////////////////////////////////////////////////////

        row = leftmid.row(align=True)
        row.label(text="")

        row = mid.row(align=True)
        # Selection
        tool = context.workspace.tools.from_space_view3d_mode(context.mode)
        toolname = context.workspace.tools.from_space_view3d_mode(bpy.context.mode).idname
        if toolname == 'builtin.cursor':
            props = tool.operator_properties("view3d.cursor3d")
            sub = row.row(align=True)
            sub.ui_units_x = 3
            sub.prop(props, "use_depth", text="PROJECT", toggle=True)
            sub = row.row(align=True)
            sub.ui_units_x = 5
            sub.prop(props, "orientation", text="")
            row.separator(factor=2)
        else:
            SelectHud(row, self, context)
            row.separator(factor=2)

        # Pivot
        sub = row.row(align=True)
        sub.scale_x = 1.4
        op = sub.operator('object.origin_set', text='', icon='PIVOT_BOUNDBOX') # COG
        op.type = 'ORIGIN_GEOMETRY'
        op.center ='MEDIAN'
        sub.operator('xm.floor', text='', icon='IMPORT')
        op = sub.operator('object.origin_set', text='', icon='PIVOT_CURSOR')
        op.type = 'ORIGIN_CURSOR'
        op.center ='MEDIAN'

        row = rightmid.row(align=True)
        row.label(text="")

    if context.mode == 'EDIT_MESH':  #EDIT////////////////////////////////////////////////////////////////

        row = leftmid.row(align=True)
        # Tog Component
        sub = row.row(align=True)
        sub.scale_x = 1.4
        sub.template_edit_mode_selection()
        row.separator(factor=1)
        row = mid.row(align=True)

        # Selection
        SelectHud(row, self, context)
        row.separator(factor=1)

        # Extra
        sub = row.row(align=True)
        sub.scale_x = 1.2
        sub.prop(ts, "use_mesh_automerge", text="", toggle=True)
        #sub.operator('mesh.target_weld_toggle', text='', icon='CON_TRACKTO')
        #sub.operator('mesh.quick_pivot', text='', icon='PIVOT_BOUNDBOX')
        row.separator()

        row = rightmid.row(align=True)
        # Symmetrie
        sub = row.row()
        sub.ui_units_x = 4
        sub.menu_contents("VIEW3D_MT_sym")
        row.separator()

        # Hide-Component
        sub = row.row(align=True)
        sub.ui_units_x = 1.2
        sub.operator('mesh.reveal', icon='HIDE_OFF', text="")
        sub = row.row(align=True)
        sub.ui_units_x = 1.2
        sub.operator('mesh.hide', icon='HIDE_ON', text="").unselected=False


    if context.mode == 'SCULPT': #SCULPT//////////////////////////////////////////////////////////////
        brush = context.tool_settings.sculpt.brush

        row = leftmid.row(align=True)
        # Color
        sub = row.row(align=True)
        sub.ui_units_x = 5
        sub.operator('xm.colorpicker', icon='EYEDROPPER', text="").length=3
        ColorHud(self, context, layout=sub)
        row.separator(factor = 1)

        row = mid.row(align=True)
        # Brush
        PaintHud(row, brush, self, context)
        row.separator(factor = 1)

        row = rightmid.row(align=True)
        # Symmetrie
        sub = row.row()
        sub.ui_units_x = 4
        sub.menu_contents("VIEW3D_MT_sym")
        mid.separator(factor = 1)

    if context.mode == 'PAINT_VERTEX':  #PAINT_VERTEX/////////////////////////////////////////////////
        brush = context.tool_settings.vertex_paint.brush

        row = leftmid.row(align=True)
        # Paint Mask
        sub = row.row(align=True)
        sub.ui_units_x = 2
        sub.template_header_3D_mode()
        row.separator(factor = 1)

        # Color
        sub = row.row(align=True)
        sub.ui_units_x = 5
        sub.operator('xm.colorpicker', icon='EYEDROPPER', text="").length=3
        ColorHud(self, context, layout=sub)
        row.separator(factor = 1)

        row = mid.row(align=True)
        # Brush
        PaintHud(row, brush, self, context)
        row.separator(factor = 1)

        row = rightmid.row(align=True)
        # Symmetrie
        sub = row.row()
        sub.ui_units_x = 4
        sub.menu_contents("VIEW3D_MT_sym")
        row.separator(factor = 1)

   
    if context.mode == 'PAINT_TEXTURE':   #PAINT_TEXTURE///////////////////////////////////////////////
        brush = context.tool_settings.image_paint.brush

        row = leftmid.row(align=True)
        # Paint Mask
        sub = row.column(align=True)
        sub.ui_units_x = 2
        sub.template_header_3D_mode()
        row.separator(factor = 1)

        # Color
        sub = row.row(align=True)
        sub.ui_units_x = 5
        sub.operator('xm.colorpicker', icon='EYEDROPPER', text="").length=3
        ColorHud(self, context, layout=sub)
        row.separator(factor = 1)

        row = mid.row(align=True)
        # Brush
        PaintHud(row, brush, self, context)
        row.separator(factor = 1)

        row = rightmid.row(align=True)
        # Symmetrie
        sub = row.row()
        sub.ui_units_x = 4
        sub.menu_contents("VIEW3D_MT_sym")
        row.separator(factor = 1)

    if context.mode == 'PAINT_WEIGHT':  #PAINT_WEIGHT/////////////////////////////////////////////////
        ts = context.tool_settings
        ups = ts.unified_paint_settings
        brush = context.tool_settings.weight_paint.brush

        row = leftmid.row(align=True)
        # Paint Mask
        sub = row.row(align=True)
        sub.ui_units_x = 2
        sub.template_header_3D_mode()
        row.separator(factor = 1)

        # Weight
        sub = row.row(align=True)
        sub.ui_units_x = 5
        sub.prop(ups, 'weight', slider=True)
        row.separator(factor = 1)

        row = mid.row(align=True)
        # Brush
        PaintHud(row, brush, self, context)
        row.separator(factor = 1)

        row = rightmid.row(align=True)
        # Symmetrie
        sub = row.row(align=True)
        sub.ui_units_x = 4
        sub.menu_contents("VIEW3D_MT_sym")
        row.separator(factor = 1)

    if context.mode == 'PAINT_GPENCIL':  #PAINT_GPENCIL///////////////////////////////////////////////
        brush = context.tool_settings.gpencil_paint.brush

        row = leftmid.row(align=True)
        # Color
        sub = row.row()
        sub.ui_units_x = 6
        GPColorHud(self, context, layout=sub)
        row.separator(factor = 1)



        row = mid.row(align=True)
        # Line Options
        sub = row.row(align=True)
        sub.scale_x = 1.2
        sub.prop(ts, "use_gpencil_draw_onback", text="", icon='MOD_OPACITY')
        sub.prop(ts, "use_gpencil_automerge_strokes", text="")
        row.separator(factor = 1)
        # Brush
        sub = row.row(align=True)
        sub.ui_units_x = 17
        GPPaintHud(sub, context, brush)

        row = rightmid.row(align=True)
        row.label(text='')

    if context.mode == 'EDIT_GPENCIL':  #EDIT_GPENCIL/////////////////////////////////////////////////

        row = leftmid.row(align=True)
        # Stroke
        sub = row.row(align=True)
        sub.ui_units_x = 4
        sub.operator("gpencil.stroke_arrange", text="UP").direction='UP'
        sub.operator("gpencil.stroke_arrange", text="DOWN").direction='DOWN'

        row = mid.row(align=True)
        # Selection
        GPSelectHud(row, self, context)
        row.separator(factor = 1)

        row = rightmid.row(align=True)
        row.label(text='')

    if context.mode == 'SCULPT_GPENCIL':  #SCULPT_GPENCIL/////////////////////////////////////////////
        brush = context.tool_settings.gpencil_sculpt_paint.brush
        gp_settings = brush.gpencil_settings

        row = leftmid.row(align=True)
        row.label(text='')

        row = mid.row(align=True)
        # Brush
        sub = row.row(align=True)
        sub.alignment = 'CENTER'
        sub.ui_units_x = 8
        sub.prop(brush, "size", text="Radius")
        sub.prop(gp_settings, "use_pressure", text="", icon='STYLUS_PRESSURE')
        sub.separator(factor = 1)
        sub = mid.row(align=True)
        sub.ui_units_x = 8
        sub.prop(brush, "strength", slider=True)
        sub.prop(brush, "use_pressure_strength", text="", icon='STYLUS_PRESSURE')

        row = rightmid.row(align=True)
        row.label(text='')

    if context.mode == 'WEIGHT_GPENCIL':  #WEIGHT_GPENCIL////////////////////////////////////////////
        brush = context.tool_settings.gpencil_weight_paint.brush
        gp_settings = brush.gpencil_settings

        row = leftmid.row(align=True)
        # Weight
        sub = row.row(align=True)
        sub.ui_units_x = 5
        sub.prop(brush, "weight", text="Weight")
        row.separator(factor = 1)

        row = mid.row(align=True)
        # Brush
        sub = row.row(align=True)
        sub.alignment = 'CENTER'
        sub.ui_units_x = 5
        sub.prop(brush, "size", text="Radius")
        sub.prop(gp_settings, "use_pressure", text="", icon='STYLUS_PRESSURE')
        sub.separator(factor = 1)

        sub = row.row(align=True)
        sub.ui_units_x = 5
        sub.prop(brush, "strength", slider=True)
        sub.prop(brush, "use_pressure_strength", text="", icon='STYLUS_PRESSURE')

        row = rightmid.row(align=True)
        row.label(text='')

    # RIGHT --------------------------------------------------------------------------------------------------
    row = right.row(align =True)

    # Wireframe
    sub = row.column(align =True)
    sub.ui_units_x = 1.6
    if ob != None and ob.type == 'MESH':
        if context.mode == 'EDIT_MESH':
            sub.prop(overlay, "show_occlude_wire", text="", icon="MOD_WIREFRAME", toggle=True)
        else:
            sub.prop(ob, "show_wire", text="", icon="MOD_WIREFRAME", toggle=True)
    else:
        sub.prop(overlay, "show_occlude_wire", text="", icon="MOD_WIREFRAME", toggle=True)

    # Normal-Display
    funct_bt(layout=row, cmd='faceorient', tog=True, w=1.6, h=1, label='', icon="NORMALS_FACE")

    # X-Ray
    funct_bt(layout=row, cmd='xray', tog=True, w=1.6, h=1, label='', icon="XRAY")

    # RIGHT OUTER --------------------------------------------------------------------------------------------
    row = rightouter.row(align =True)

    # Floaters
    sub = row.row(align=True)
    if platform.system() != 'Windows':
        sub.label(text="")
    else:
        funct_bt(layout=sub, cmd='floater_01', tog=True, w=2, h=1, label='', icon="OUTLINER")
        funct_bt(layout=sub, cmd='floater_02', tog=True, w=2, h=1, label='', icon="PROPERTIES")
        funct_bt(layout=sub, cmd='floater_03', tog=True, w=2, h=1, label='', icon="MODIFIER")
        funct_bt(layout=sub, cmd='floater_04', tog=True, w=2, h=1, label='', icon="NODE_MATERIAL")
        funct_bt(layout=sub, cmd='floater_05', tog=True, w=2, h=1, label='', icon="IMAGE")
    row.separator(factor = 2)

    # History
    sub = row.row(align=True)
    sub.scale_x = 1.8
    History(self, context, layout=sub)

    redraw_regions()

#-----------------------------------------------------------------------------------------------------------#
#                                             - HEADER -                                                    #
#-----------------------------------------------------------------------------------------------------------#

class VIEW3D_HT_x_header(Header):
    bl_space_type = 'VIEW_3D'

    @staticmethod
    def draw_xform_template(layout, context):
        obj = context.active_object
        object_mode = 'OBJECT' if obj is None else obj.mode
        has_pose_mode = (
            (object_mode == 'POSE') or
            (object_mode == 'WEIGHT_PAINT' and context.pose_object is not None))

        tool_settings = context.tool_settings
        scene = context.scene

        # Orientation
        if object_mode in {'OBJECT', 'EDIT', 'EDIT_GPENCIL'} or has_pose_mode:
            orient_slot = scene.transform_orientation_slots[0]
            row = mid.row(align=True)
            sub = row.row()
            sub.ui_units_x = 4
            sub.prop_with_popover(orient_slot,"type",text="",panel="VIEW3D_PT_transform_orientations",)

        # Pivot
        if object_mode in {'OBJECT', 'EDIT', 'EDIT_GPENCIL', 'SCULPT_GPENCIL'} or has_pose_mode:
            row = mid.row(align=True)
            row.prop(tool_settings, "transform_pivot_point", text="", icon_only=True)

        # Snap
        show_snap = False
        if obj is None:
            show_snap = True
        else:
            if (object_mode not in {'SCULPT', 'VERTEX_PAINT', 'WEIGHT_PAINT', 'TEXTURE_PAINT',
                    'PAINT_GPENCIL', 'SCULPT_GPENCIL', 'WEIGHT_GPENCIL', 'VERTEX_GPENCIL'}) or has_pose_mode:
                show_snap = True
            else:
                paint_settings = UnifiedPaintPanel.paint_settings(context)
                if paint_settings:
                    brush = paint_settings.brush
                    if brush and hasattr(brush, "stroke_method") and brush.stroke_method == 'CURVE':
                        show_snap = True

        if show_snap:
            snap_items = bpy.types.ToolSettings.bl_rna.properties["snap_elements"].enum_items
            snap_elements = tool_settings.snap_elements
            if len(snap_elements) == 1:
                text = ""
                for elem in snap_elements:
                    icon = snap_items[elem].icon
                    break
            else:
                text = "Mix"
                icon = 'NONE'
            del snap_items, snap_elements

            sub = mid.row(align=True)
            sub.prop(tool_settings, "use_snap", text="")
            sub = mid.row(align=True)
            sub.popover(panel="VIEW3D_PT_snapping",icon=icon,text=text,)

        # Proportional editing
        if object_mode in {'EDIT', 'PARTICLE_EDIT', 'SCULPT_GPENCIL', 'EDIT_GPENCIL', 'OBJECT'}:
            row = mid.row(align=True)
            kw = {}
            if object_mode == 'OBJECT':
                attr = "use_proportional_edit_objects"
            else:
                attr = "use_proportional_edit"

                if tool_settings.use_proportional_edit:
                    if tool_settings.use_proportional_connected:
                        kw["icon"] = 'PROP_CON'
                    elif tool_settings.use_proportional_projected:
                        kw["icon"] = 'PROP_PROJECTED'
                    else:
                        kw["icon"] = 'PROP_ON'
                else:
                    kw["icon"] = 'PROP_OFF'

            row.prop(tool_settings, attr, icon_only=True, **kw)
            sub = row.row(align=True)
            sub.active = getattr(tool_settings, attr)
            sub.prop_with_popover(tool_settings,"proportional_edit_falloff",text="",icon_only=True,panel="VIEW3D_PT_proportional_edit")

    def draw(self, context):
        layout = self.layout

        tool_settings = context.tool_settings
        view = context.space_data
        shading = view.shading
        obj = context.active_object
        overlay = view.overlay
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

        # LEFT
        left = row.row(align=True)
        left.ui_units_x = 15
        left.alignment = 'LEFT'
        # MID1
        mid1 = row.row(align=True)
        mid1.ui_units_x = 7.5
        mid1.alignment = 'LEFT'
        # MID2
        mid2 = row.row(align=True)
        mid2.ui_units_x = 12
        mid2.alignment = 'LEFT'
        # MID3
        mid3 = row.row(align=True)
        mid3.ui_units_x = 10.5
        mid3.alignment = 'CENTER'
        # MID4
        mid4 = row.row(align =True)
        mid4.alignment = 'RIGHT'
        mid4.ui_units_x = 12
        # MID5
        mid5 = row.row(align =True)
        mid5.alignment = 'LEFT'
        mid5.ui_units_x = 7.5
        # RIGHT
        right = row.row(align =True)
        right.alignment = 'RIGHT'
        right.ui_units_x = 15

        #layout.separator(factor=16)

        # LEFT -------------------------------------------------------------------------------------------------
        object_mode = 'OBJECT' if obj is None else obj.mode
        has_pose_mode = ((object_mode == 'POSE') or
                         (object_mode == 'WEIGHT_PAINT' and context.pose_object is not None))
        act_mode_item = bpy.types.Object.bl_rna.properties["mode"].enum_items[object_mode]
        act_mode_i18n_context = bpy.types.Object.bl_rna.properties["mode"].translation_context
        del act_mode_item

        row = left.row(align =True)

        # Editor Type
        row.template_header()
        row.separator(factor=2)

        # Menus
        VIEW3D_MT_editor_menus.draw_collapsible(context, row)
        row.separator(factor=2)

        # Save
        sub = row.row()
        sub.ui_units_x = 4
        sub.operator("wm.save_mainfile", icon='FILE_TICK', text="SAVE")
        row.separator(factor=2)

        # Script Reload
        sub = row.row()
        sub.scale_x = 1.2
        sub.operator("script.reload", icon='FILE_REFRESH', text="")
        row.separator(factor=2)

        # MID ------------------------------------------------------------------------------------------------

        if object_mode == 'OBJECT':  #OBJECT//////////////////////////////////////////////////////////////////

            row = mid1.row(align =True)
            # Redo Last Cmd
            sub = row.row()
            sub.ui_units_x = 4
            sub.operator("screen.redo_last", text="CMD >")
            row.separator(factor=2)

            row = mid2.row(align=True)
            row.label(text='')

            row = mid3.row(align=True)
            # Transform settings
            VIEW3D_HT_header.draw_xform_template(row, context)
            row.separator(factor=2)

            row = mid4.row(align=True)
            #Normal-Shading
            sub =row.row()
            sub.ui_units_x = 6
            Normals(self, context, layout=sub)
            row.separator(factor=2)

            row = mid5.row(align=True)
            # Wireframe
            sub = row.row()
            sub.ui_units_x = 3
            Overlay_Wire(self, context, layout=sub)
            row.separator(factor=2)

            #Annotate/Measure
            tool_bt(layout=row, cmd=10, w=1.2, h=1, text=False, icon='OUTLINER_DATA_GP_LAYER')
            tool_bt(layout=row, cmd=13, w=1.2, h=1, text=False, icon='OUTLINER_DATA_LIGHTPROBE')
            tool_bt(layout=row, cmd=14, w=1.2, h=1, text=False, icon='DRIVER_ROTATIONAL_DIFFERENCE')
            row.separator(factor=2)

        if object_mode == 'EDIT':  #EDIT///////////////////////////////////////////////////////////////////

            row = mid1.row(align =True)
            # Redo Last Cmd
            sub = row.row()
            sub.ui_units_x = 4
            sub.operator("screen.redo_last", text="CMD >")
            row.separator(factor=2)

            row = mid2.row(align=True)
            row.label(text='')

            row = mid3.row(align=True)
            # Transform settings
            VIEW3D_HT_header.draw_xform_template(row, context)
            row.separator(factor=2)

            row = mid4.row(align=True)
            #Normal-Shading
            sub = row.row()
            sub.ui_units_x = 6
            Normals(self, context, layout=sub)
            row.separator(factor=2)

            row = mid5.row(align=True)
            # Wireframe
            sub = row.row()
            sub.ui_units_x = 3
            Overlay_Wire(self, context, layout=sub)
            row.separator(factor=2)

            #Annotate/Measure
            tool_bt(layout=row, cmd=10, w=1.2, h=1, text=False, icon='OUTLINER_DATA_GP_LAYER')
            tool_bt(layout=row, cmd=11, w=1.2, h=1, text=False, icon='OUTLINER_DATA_LIGHTPROBE')
            tool_bt(layout=row, cmd=12, w=1.2, h=1, text=False, icon='DRIVER_ROTATIONAL_DIFFERENCE')
            row.separator(factor=2)

        if object_mode == 'SCULPT':  #SCULPT//////////////////////////////////////////////////////////////////

            row = mid1.row(align=True)
            #Optimize
            sub = row.row()
            sub.ui_units_x = 3
            sub.operator('object.transfer_mode', text="<>" ,icon='NONE')
            row.separator(factor=1)
            sub = row.row()
            sub.ui_units_x = 1.2
            sub.operator('sculpt.optimize', text="" ,icon='SOLO_ON')
            row.separator(factor=2)

            #Symmetrie
            sub =  row.row()
            sub.ui_units_x = 2
            sub.scale_y = 1
            sub.operator("sculpt.symmetrize", text='SYM')
            sub = row.row()
            sub.ui_units_x = 2
            sub.menu("VIEW3D_MT_sculpt_sym", text='', icon='DOWNARROW_HLT')
            row.separator(factor=2)

            row = mid2.row(align=True)
            # MASK
            row.label(text='MASK')
            row.separator(factor=1)
            op = row.operator("sculpt.expand", text='EXP T')
            op.target='MASK'
            op.falloff_type='GEODESIC'
            op.invert=True

            op = row.operator("sculpt.expand", text='EXP N')
            op.target='MASK'
            op.falloff_type='NORMALS'
            op.invert=True

            row.operator("sculpt.dirty_mask", text='AO')
            row.operator("mesh.paint_mask_extract", text='EXTR')

            op = row.operator("mesh.paint_mask_slice", text='SLICE')
            op.fill_holes=False
            op.new_object=True

            row.separator(factor=3)
            row = mid3.row(align=True)
            # F-SET
            row.label(text='F-SET')
            row.separator(factor=1)

            op = row.operator("sculpt.expand", text='EXP T')
            op.target='FACE_SETS'
            op.falloff_type='GEODESIC'
            op.invert=False
            op.use_modify_active=False

            op = row.operator("sculpt.expand", text='EXP')
            op.target='FACE_SETS'
            op.falloff_type='BOUNDARY_FACE_SET'
            op.invert=False
            op.use_modify_active=True

            row.operator("mesh.face_set_extract", text='EXTR')

            row = mid4.row(align=True)
            # Overlay
            sub = row.row(align=True)
            sub.ui_units_x = 8
            sub.prop(context.space_data.overlay, "sculpt_mode_mask_opacity", text="MASK")
            sub.prop(context.space_data.overlay, "sculpt_mode_face_sets_opacity", text="FSET")
            row.separator(factor=2)

            #Normal-Shading
            sub = row.row()
            sub.ui_units_x = 2
            sub.operator("xm.normalshading", text="SMTH", depress=update_normaldisp(self, context))
            row.separator(factor=2)


            row = mid5.row(align=True)
            # Wireframe
            sub = row.row()
            sub.ui_units_x = 3
            Overlay_Wire(self, context, layout=sub)
            row.separator(factor=2)

        if context.mode == 'PAINT_VERTEX':  #PAINT_VERTEX////////////////////////////////////////////////////////

            row = mid1.row(align=True)
            # Redo Last Cmd
            sub = row.row()
            sub.ui_units_x = 4
            sub.operator("screen.redo_last", text="CMD >")
            row.separator(factor=2)

            row = mid2.row(align=True)
            row.label(text='')

            row = mid3.row(align=True)
            row.label(text='')

            row = mid4.row(align=True)
            #Normal-Shading
            sub = row.row()
            sub.ui_units_x = 2
            sub.operator("xm.normalshading", text="SMTH", depress=update_normaldisp(self, context))
            row.separator(factor=2)

            row = mid5.row(align=True)
            # Wireframe
            sub = row.row()
            sub.ui_units_x = 3
            Overlay_Wire(self, context, layout=sub)
            row.separator(factor=2)



        if context.mode == 'PAINT_TEXTURE':  #PAINT_TEXTURE///////////////////////////////////////////////////////

            row = mid1.row(align=True)
            # Redo Last Cmd
            sub = row.row()
            sub.ui_units_x = 4
            sub.operator("screen.redo_last", text="CMD >")
            row.separator(factor=2)

            row = mid2.row(align=True)
            row.label(text='')

            row = mid3.row(align=True)
            row.label(text='')

            row = mid4.row(align=True)
            #Normal-Shading
            sub = row.row()
            sub.ui_units_x = 2
            sub.operator("xm.normalshading", text="SMTH", depress=update_normaldisp(self, context))
            row.separator(factor=2)

            row = mid5.row(align=True)
            # Wireframe
            sub = row.row()
            sub.ui_units_x = 3
            Overlay_Wire(self, context, layout=sub)
            row.separator(factor=2)

        if context.mode == 'PAINT_WEIGHT':  #PAINT_WEIGHT///////////////////////////////////////////////////////////

            row = mid1.row(align=True)
            # Redo Last Cmd
            sub = row.row()
            sub.ui_units_x = 4
            sub.operator("screen.redo_last", text="CMD >")
            row.separator(factor=2)

            row = mid2.row(align=True)
            row.label(text='')

            row = mid3.row(align=True)
            row.label(text='')

            row = mid4.row(align=True)
            row.label(text='')

            row = mid5.row(align=True)
            # Wireframe
            sub = row.row()
            sub.ui_units_x = 3
            Overlay_Wire(self, context, layout=sub)
            row.separator(factor=2)

        if context.mode == 'PAINT_GPENCIL':  #PAINT_GPENCIL////////////////////////////////////////////////////////

            row = mid1.row(align=True)
            # Redo Last Cmd
            sub = row.row()
            sub.ui_units_x = 4
            sub.operator("screen.redo_last", text="CMD >")

            row = mid2.row(align=True)

            # Draw Options
            gpd = context.gpencil_data

            if gpd.is_stroke_paint_mode:
                sub = row.row(align=True)
                sub.scale_x = 1.2
                sub.prop(tool_settings, "use_gpencil_weight_data_add", text="", icon='WPAINT_HLT')
                sub.prop(tool_settings, "use_gpencil_draw_additive", text="", icon='FREEZE')
            row.separator(factor=2)

            sub = row.row()
            sub.scale_x = 1.2
            sub.prop(gpd, "use_multiedit", text="", icon='GP_MULTIFRAME_EDITING')

            row = mid3.row(align=True)
            sub = row.row()
            sub.ui_units_x = 6
            sub.prop_with_popover(tool_settings,"gpencil_stroke_placement_view3d",text="",panel="VIEW3D_PT_gpencil_origin")
            sub = row.row()
            sub.ui_units_x = 6
            sub.prop_with_popover(tool_settings.gpencil_sculpt,"lock_axis",text="",panel="VIEW3D_PT_gpencil_lock")
            row.separator(factor=2)
            sub = row.row(align=True)
            sub.ui_units_x = 6
            if context.workspace.tools.from_space_view3d_mode(object_mode).idname == "builtin_brush.Draw":
                settings = tool_settings.gpencil_sculpt.guide
                sub = row.row(align=True)
                sub.prop(settings, "use_guide", text="", icon='GRID')
                subsub = sub.row(align=True)
                subsub.active = settings.use_guide
                subsub.popover(panel="VIEW3D_PT_gpencil_guide", text="Guides")

            row = mid4.row(align=True)
            row.label(text='')
            row = mid5.row(align=True)
            row.label(text='')

        if context.mode == 'SCULPT_GPENCIL':  #SCULPT_GPENCIL//////////////////////////////////////////////////////////
            gpd = context.gpencil_data

            row = mid1.row(align=True)
            row.label(text='')

            row = mid2.row(align=True)
            if gpd.is_stroke_sculpt_mode:
                sub = row.row(align=True)
                sub.prop(tool_settings, "use_gpencil_select_mask_point", text="")
                sub.prop(tool_settings, "use_gpencil_select_mask_stroke", text="")
                sub.prop(tool_settings, "use_gpencil_select_mask_segment", text="")

            row = mid3.row(align=True)
            sub = row.row(align=True)
            sub.prop_with_popover(tool_settings.gpencil_sculpt,"lock_axis",text="",panel="VIEW3D_PT_gpencil_lock")

            row = mid4.row(align=True)
            row.label(text='')
            row = mid5.row(align=True)
            row.label(text='')

        if context.mode == 'EDIT_GPENCIL':  #EDIT_GPENCIL///////////////////////////////////////////////////////////////
            gpd = context.gpencil_data

            row = mid1.row(align=True)
            row.label(text='')

            row = mid2.row(align=True)
            if gpd.use_stroke_edit_mode:
                sub = row.row(align=True)
                sub.prop_enum(tool_settings, "gpencil_selectmode_edit", text="", value='POINT')
                sub.prop_enum(tool_settings, "gpencil_selectmode_edit", text="", value='STROKE')
                subrow = sub.row(align=True)
                subrow.enabled = not gpd.use_curve_edit
                subrow.prop_enum(tool_settings, "gpencil_selectmode_edit", text="", value='SEGMENT')

                # Curve edit submode
                row = mid2.row(align=True)
                row.prop(gpd, "use_curve_edit", text="",icon='IPO_BEZIER')
                sub = row.row(align=True)
                sub.active = gpd.use_curve_edit
                sub.popover(panel="VIEW3D_PT_gpencil_curve_edit",text="Curve Editing",)

            row = mid3.row(align=True)
            row.prop(gpd, "use_multiedit", text="", icon='GP_MULTIFRAME_EDITING')

            sub = row.row(align=True)
            sub.enabled = gpd.use_multiedit
            sub.popover(panel="VIEW3D_PT_gpencil_multi_frame",text="Multiframe")

            row = mid4.row(align=True)
            row.label(text='')
            row = mid5.row(align=True)
            row.label(text='')

        if context.mode == 'WEIGHT_GPENCIL':  #WEIGHT_GPENCIL///////////////////////////////////////////////////////////////
            gpd = context.gpencil_data

            row = mid1.row(align=True)
            row.label(text='')

            row = mid2.row(align=True)
            row.label(text='')

            row = mid3.row(align=True)
            row.prop(gpd, "use_multiedit", text="", icon='GP_MULTIFRAME_EDITING')
            sub = row.row(align=True)
            sub.enabled = gpd.use_multiedit
            sub.popover(panel="VIEW3D_PT_gpencil_multi_frame",text="Multiframe")

            row = mid4.row(align=True)
            row.label(text='')

            row = mid5.row(align=True)
            row.label(text='')

        # RIGHT ---------------------------------------------------------------------------------------------------
        row = right.row(align =True)

        # Overlay  
        Overlay(self, context, layout=row)

        # Hud
        funct_bt(layout=row, cmd='hud_tool', tog=True, w=1.2, h=1, label='M', icon="NONE")
        funct_bt(layout=row, cmd='hud_pivot', tog=True, w=1.2, h=1, label='P', icon='NONE')
        funct_bt(layout=row, cmd='hud_info', tog=True, w=1.2, h=1, label='I', icon="NONE")
        row.separator(factor = 2)

        # Viewport Settings
        row.popover(panel="VIEW3D_PT_object_type_visibility",icon_value=view.icon_from_show_object_viewport,text="")
        row.separator(factor = 2)

        # Gizmo
        row.prop(view, "show_gizmo", text="", toggle=True, icon='GIZMO')
        sub = row.row(align=True)
        sub.active = view.show_gizmo
        sub.popover(panel="VIEW3D_PT_gizmo_display",text="")

        # Overlay
        row.prop(overlay, "show_overlays", icon='OVERLAY', text="")
        sub = row.row(align=True)
        sub.active = overlay.show_overlays
        sub.popover(panel="VIEW3D_PT_overlay", text="")
        row.separator(factor = 2)

        # Shading
        sub = row.row()
        sub.active = (object_mode == 'EDIT') or (shading.type in {'WIREFRAME', 'SOLID'})
        if has_pose_mode:
            draw_depressed = overlay.show_xray_bone
        elif shading.type == 'WIREFRAME':
            draw_depressed = shading.show_xray_wireframe
        else:
            draw_depressed = shading.show_xray
        row.prop(shading, "type", text="", expand=True)
        sub = row.row(align=True)
        sub.popover(panel="VIEW3D_PT_shading", text="")

        redraw_regions()

#-----------------------------------------------------------------------------------------------------------------------
classes = (TogXHeader, VIEW3D_HT_x_header)

def register():
    for cls in classes:
        bpy.utils.register_class(cls)
    bpy.types.WindowManager.togxheader_state = True
    bpy.types.VIEW3D_HT_tool_header.prepend(draw_3d_toolsettings)
    bpy.types.VIEW3D_HT_header.prepend(VIEW3D_HT_x_header.draw)
    bpy.types.NODE_HT_header.prepend(draw_node_header)
    bpy.types.IMAGE_HT_header.append(draw_image_header)
    bpy.types.TEXT_HT_header.append(draw_image_header)

def unregister():
    bpy.types.VIEW3D_HT_tool_header.remove(draw_3d_toolsettings)
    bpy.types.VIEW3D_HT_header.remove(VIEW3D_HT_x_header.draw)
    bpy.types.NODE_HT_header.remove(draw_node_header)
    bpy.types.IMAGE_HT_header.remove(draw_image_header)
    bpy.types.TEXT_HT_header.remove(draw_image_header)

    for cls in classes:
        bpy.utils.unregister_class(cls)


