import bpy
import os
from .icons.icons import load_icons
from.toolsets import Tools_Sculpt
from .functions import tool_grid, tool_bt, funct_bt, paint_settings
from .brushtexture import brush_icons_path, get_brush_mode, setup_brush_tex, _invert_ramp, _mute_ramp
#from bl_ui.properties_data_modifier import DATA_PT_modifiers

from bl_ui.space_toolsystem_common import (ToolSelectPanelHelper,ToolDef)
from bpy.app.translations import contexts as i18n_contexts

from bpy.types import Menu, Panel, UIList
from rna_prop_ui import PropertyPanel
from collections import defaultdict


def ShadingMode(self, context, parent):
        layout = parent

        tool_settings = context.tool_settings
        view = context.space_data
        shading = view.shading

        row = layout.row(align=True)
        row.ui_units_x = 6

        row.prop(shading, "type", text="", expand=True)
        sub = row.row(align=True)
        sub.popover(panel="VIEW3D_PT_shading", text="")



def VertexGroups(self, context, parent):
    ob = context.active_object
    group = ob.vertex_groups.active
    box = parent.box()
    box.ui_units_x = 10
    row = box.row()
    col = row.column()
    rows = 3
    if group:
        rows = 3

    row = box.row()
    row.template_list("MESH_UL_vgroups", "", ob, "vertex_groups", ob.vertex_groups, "active_index", rows=rows)

    col = row.column(align=True)

    col.operator("xmenu.override", icon='ADD', text="").cmd ='object.vertex_group_add'
    col.operator("xmenu.override", icon='REMOVE', text="").cmd='object.vertex_group_remove'
    col.separator()

    #col.menu("MESH_MT_vertex_group_context_menu", icon='DOWNARROW_HLT', text="")
    
    if group:
        col.separator()
        op = col.operator("xmenu.override1", icon='TRIA_UP', text="")
        op.cmd='object.vertex_group_move'
        op.prop1 ='direction="UP"'

        op = col.operator("xmenu.override1", icon='TRIA_DOWN', text="")
        op.cmd='object.vertex_group_move'
        op.prop1 ='direction="DOWN"'

    if (
            ob.vertex_groups and
            (ob.mode == 'EDIT' or
                (ob.mode == 'WEIGHT_PAINT' and ob.type == 'MESH' and ob.data.use_paint_mask_vertex))
    ):
        row = box.row()
        sub = row.row(align=True)
        sub.operator("xmenu.override", text="Assign").cmd ='object.vertex_group_assign'
        sub.operator("xmenu.override", text="Remove").cmd ='object.vertex_group_remove_from'

        sub = row.row(align=True)
        sub.operator("xmenu.override", text="Select").cmd ='object.vertex_group_select'
        sub.operator("xmenu.override", text="Deselect").cmd ='object.vertex_group_deselect'

        box.prop(context.tool_settings, "vertex_group_weight", text="Weight")
        row = box.row()
        sub = row.row(align=True)
        sub.operator("xmenu.override", text="COPY").cmd ='object.vertex_group_copy'
        sub.operator("xmenu.override", text="COPY TO").cmd ='object.vertex_group_copy_to_selected'
        sub = row.row(align=True)
        op = sub.operator("xmenu.override1", text="MIRROR")
        op.cmd = 'object.vertex_group_mirror'
        op.prop1 = 'use_topology=False'

def Materials(self, context, parent):

    #context = bpy.context.copy()
    mat = context.material
    ob = context.active_object
    #ob = context.object
    slot = context.material_slot
    space = context.space_data

    box = parent.box()
    box.ui_units_x = 10

    if ob:
        is_sortable = len(ob.material_slots) > 1
        rows = 3
        if is_sortable:
            rows = 3
        row = box.row()
        row.template_list("MATERIAL_UL_matslots", "", ob, "material_slots", ob, "active_material_index", rows=rows)
        col = row.column(align=True)
        col.operator("xmenu.override", icon='ADD', text="").cmd='object.material_slot_add'
        col.operator("xmenu.override", icon='REMOVE', text="").cmd='object.material_slot_remove'
        col.separator()
        col.menu("MATERIAL_MT_context_menu", icon='DOWNARROW_HLT', text="")
        if is_sortable:
            col.separator()
            op = col.operator("xmenu.override1", icon='TRIA_UP', text="")
            op.cmd='object.material_slot_move'
            op.prop1 ='direction="UP"'
            op = col.operator("xmenu.override1", icon='TRIA_DOWN', text="")
            op.cmd='object.material_slot_move'
            op.prop1 ='direction="DOWN"'

        row = box.row()
        row.template_ID(ob, "active_material", new="material.new")
        if slot:
            icon_link = 'MESH_DATA' if slot.link == 'DATA' else 'OBJECT_DATA'
            row.prop(slot, "link", icon=icon_link, icon_only=True)
        if ob.mode == 'EDIT':
            row = box.row(align=True)
            row.operator("xmenu.override", text="Assign").cmd='object.material_slot_assign'
            row.operator("object.material_slot_select", text="Select")
            row.operator("object.material_slot_deselect", text="Deselect")

    elif mat:
        row.template_ID(space, "pin_id")

def UVTexture(self, context, parent):
    me = context.active_object.data

    box = parent.box()
    box.ui_units_x = 8

    row = box.row()
    col = row.column()
    col.template_list("MESH_UL_uvmaps", "uvmaps", me, "uv_layers", me.uv_layers, "active_index", rows=2)
    col = row.column(align=True)
    col.operator("xmenu.override", icon='ADD', text="").cmd='mesh.uv_texture_add'
    col.operator("xmenu.override", icon='REMOVE', text="").cmd='mesh.uv_texture_remove'

def VertexColor(self, context, parent):
    me = context.active_object.data

    row = parent.row()
    col = row.column()
    col.ui_units_x = 8
    col.template_list("MESH_UL_vcols", "vcols", me, "vertex_colors", me.vertex_colors, "active_index", rows=2)
    col = row.column(align=True)
    col.operator("xmenu.override", icon='ADD', text="").cmd='mesh.vertex_color_add'
    col.operator("xmenu.override", icon='REMOVE', text="").cmd='mesh.vertex_color_remove'

def Normals(self, context, parent):
    layout = parent
    layout.use_property_split = False
    ob = context.active_object
    if ob != None and ob.type == 'MESH':
        mesh = context.active_object.data
        col = layout.column(align=False)
        row = col.row(align=True)
        sub = row.row(align=True)
        sub.prop(mesh, "use_auto_smooth", text="")
        sub = sub.row(align=True)
        sub.active = mesh.use_auto_smooth and not mesh.has_custom_normals
        sub.prop(mesh, "auto_smooth_angle", text="")
        #row.prop_decorator(mesh, "auto_smooth_angle")

def GPLayers(self, context, parent):
    if context.active_object.type == "GPENCIL":
        gpd = context.active_object.data
        gpl = gpd.layers.active

        row = parent.row()
        row.ui_units_x = 11
        layer_rows = 4

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

def ModeSelector(self, context, parent):
    active = context.active_object

    col = parent.column(align=False)
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
            #subsub.ui_units_x = 1
            subsub.label(text=' GP ')
            subsub.label(text="NONE")
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
        sub.label(text="NONE")

def Transforms(self, context, parent):
    layout = parent
    layout.use_property_split = True
    layout.use_property_decorate = False

    ob = context.active_object
    box = parent.box()
    row = box.row()
    if ob != None:
        col = row.column(align=True)
        col.ui_units_x = 8
        subrow = col.row(align=True)
        sub = subrow.column(align=True)
        sub.scale_y = 0.8
        sub.prop(ob, "location", text="")
        sub = subrow.column(align=True)
        sub.scale_y = 0.8
        sub.prop(ob, "rotation_euler", text="", expand=False)
        sub = subrow.column(align=True)
        sub.scale_y = 0.8
        sub.prop(ob, "scale", text="")
        col.separator(factor=1)
        sub = col.row(align=True)
        sub.operator('object.transform_apply', text='APPLY')
        col.separator(factor=1)
        sub = col.row(align=True)
        #sub.scale_y = 0.7 
        #sub.label(text="RESET")
        #sub = col.row(align=True)
        sub.operator('object.location_clear', text='POS').clear_delta=False
        sub.operator('object.rotation_clear', text='ROT').clear_delta=False
        sub.operator('object.scale_clear', text='SCL').clear_delta=False
        sub = col.row(align=True)
        #sub.scale_y = 0.7 
        #sub.label(text="PIVOT")
        #sub = col.row(align=True) 
        op = sub.operator('object.origin_set', text='COG')
        op.type = 'ORIGIN_GEOMETRY'
        op.center ='MEDIAN'
        op = sub.operator('object.origin_set', text='CURSOR')
        op.type = 'ORIGIN_CURSOR'
        op.center ='MEDIAN'
        sub.operator('object.pivotobottom', text='BOTTOM')
    else:
        col = row.column(align=True)
        col.ui_units_x = 8
        sub = col.row(align=True)
        sub.scale_y = 0.8
        sub.label(text="----")

def SetPivot(self, context, parent):
    ob = context.active_object
    box = parent.box()
    col = box.column(align=True)
    col.ui_units_x = 4
    col.label(text="SET PIVOT")   
    op = col.operator('object.origin_set', text='COG')
    op.type = 'ORIGIN_GEOMETRY'
    op.center ='MEDIAN'
    op = col.operator('object.origin_set', text='CURSOR')
    op.type = 'ORIGIN_CURSOR'
    op.center ='MEDIAN'
    col.operator('object.pivotobottom', text='BOTTOM')

def ToolOptions(self, context, parent):
    ts = context.tool_settings   
    layout = parent
    row = parent.row(align=True)   
    row.ui_units_x = 8
    if bpy.context.mode == 'OBJECT': 
        row.prop(ts, "use_transform_data_origin", text="Origin", toggle=True)
        row.prop(ts, "use_transform_pivot_point_align", text="Locations", toggle=True)
        row.prop(ts, "use_transform_skip_children", text="Parents", toggle=True)

    elif bpy.context.mode == 'EDIT_MESH':
        row.prop(ts, "use_mesh_automerge", text="Auto Merge", toggle=True)

    elif bpy.context.mode == 'SCULPT':
        brush = ts.sculpt.brush

        col = row.column(align=True)
        col.ui_units_x = 4
        col.scale_y = 0.7
        col.prop(brush, "use_automasking_topology", text="Topology", toggle=True)
        sub = col.row(align=True)
        sub.prop(brush, "use_frontface", text="Front", toggle=True)
        sub.prop(brush, "use_automasking_boundary_edges", text="Bound", toggle=True)
        col = row.column(align=True)
        col.ui_units_x = 4
        col.scale_y = 0.7       
        col.prop(brush, "use_automasking_face_sets", text="Face Sets", toggle=True)
        sub = col.row(align=True)
        split = sub.split(factor=0.4, align=True)
        split.prop(brush, "use_automasking_boundary_face_sets", text="STP", toggle=True)
        split.prop(brush, "automasking_boundary_edges_propagation_steps", text="",)

    elif bpy.context.mode == 'PAINT_TEXTURE':
        ipaint = ts.image_paint
        
        col = row.column(align=True)
        col.ui_units_x = 3
        col.scale_y = 0.7
        col.prop(ipaint, "use_occlude",  text="Occlude", toggle=True)
        col.prop(ipaint, "use_backface_culling",  text="FrontFace", toggle=True)

        col = row.column(align=True)
        col.ui_units_x = 5
        col.scale_y = 0.7
        col.prop(ipaint, "seam_bleed",  text="Bleed")
        col.prop(ipaint, "dither",  text="Dither")  
        
def ObjectToolSettings(self, context, parent):
    layout = parent
    tool = context.workspace.tools.from_space_view3d_mode(context.mode)
    toolname = context.workspace.tools.from_space_view3d_mode(bpy.context.mode).idname

    col = layout.column()
    col.alignment = 'LEFT'
    col.ui_units_x = 6
    col.scale_y = 0.7

    if toolname == 'builtin.cursor':
        props = tool.operator_properties("view3d.cursor3d")
        sub = col.row(align=True)
        sub.prop(props, "use_depth")
        sub = col.row(align=True)
        sub.prop(props, "orientation")

    else:
        sub = col.row(align=True)
        sub.label(text='------')

def SculptToolSettings(self, context, parent):
    layout = parent
    tool = context.workspace.tools.from_space_view3d_mode(bpy.context.mode).idname
    #if tool.find('brush') != -1:

    col = layout.column()
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
            col.prop(props, "sharpen_smooth_ratio", expand=False, slider=True ,text='SHRP<>SMTH')
            row = col.row(align=True)
            row.prop(props, "sharpen_intensify_detail_strength", expand=False, slider=True ,text='DETAIL')
            row.prop(props, "sharpen_curvature_smooth_iterations", expand=False, text='ITERATION')

    if tool == 'builtin.box_mask':
        tool = context.workspace.tools.from_space_view3d_mode(context.mode)
        props = tool.operator_properties("paint.mask_box_gesture")
        sub = col.row(align=True)
        sub.ui_units_x = 5
        sub.prop(props, "use_front_faces_only", expand=False, text='FrontFaces')

    if tool == 'builtin.lasso_mask':
        tool = context.workspace.tools.from_space_view3d_mode(context.mode)
        props = tool.operator_properties("paint.mask_lasso_gesture")
        sub = col.row(align=True)
        sub.ui_units_x = 5
        sub.prop(props, "use_front_faces_only", expand=False, text='FrontFaces')

    if tool == 'builtin.line_mask':
        tool = context.workspace.tools.from_space_view3d_mode(context.mode)
        props = tool.operator_properties("paint.mask_line_gesture")
        sub = col.column(align=True)
        sub.ui_units_x = 5
        sub.prop(props, "use_front_faces_only", expand=False, text='FrontFaces')
        sub.prop(props, "use_limit_to_segment", expand=False, text='LimitSegment')

    if tool == 'builtin.box_face_set':
        tool = context.workspace.tools.from_space_view3d_mode(context.mode)
        props = tool.operator_properties("sculpt.face_set_box_gesture")
        sub = col.row(align=True)
        sub.ui_units_x = 5
        sub.prop(props, "use_front_faces_only", expand=False, text='FrontFaces')

    if tool == 'builtin.lasso_face_set':
        tool = context.workspace.tools.from_space_view3d_mode(context.mode)
        props = tool.operator_properties("sculpt.face_set_lasso_gesture")
        sub = col.row(align=True)
        sub.ui_units_x = 5
        sub.prop(props, "use_front_faces_only", expand=False, text='FrontFaces')

    if tool == 'builtin.face_set_edit':
        tool = context.workspace.tools.from_space_view3d_mode(context.mode)
        props = tool.operator_properties("sculpt.face_set_edit")
        sub = col.column(align=True)
        sub.ui_units_x = 5
        sub.prop(props, "mode", expand=False, text='')
        sub.prop(props, "modify_hidden")

    if tool == 'builtin.box_trim':
        tool = context.workspace.tools.from_space_view3d_mode(context.mode)
        props = tool.operator_properties("sculpt.trim_box_gesture")
        sub = col.column(align=True)
        sub.ui_units_x = 5
        sub.prop(props, "trim_mode", expand=False, text='')
        sub.prop(props, "use_cursor_depth", text='Cursor Depth', expand=False)

    if tool == 'builtin.lasso_trim':
        tool = context.workspace.tools.from_space_view3d_mode(context.mode)
        props = tool.operator_properties("sculpt.trim_lasso_gesture")
        sub = col.column(align=True)
        sub.ui_units_x = 5
        sub.prop(props, "trim_mode", expand=False, text='')
        sub.prop(props, "use_cursor_depth", text='Cursor Depth', expand=False)
        sub.prop(props, "trim_orientation", text='ORIENT', expand=False)

    if tool == 'builtin.transform':
        scene = context.scene
        orient_slot = scene.transform_orientation_slots[0]
        sub = col.column(align=True)
        sub.ui_units_x = 5
        sub.prop(orient_slot, "type")

    else:
        sub = col.row(align=True)
        sub.label(text='')

def SculptBrushSettings(self, context, parent):
    layout = parent
    brush = context.tool_settings.sculpt.brush
    direction = not brush.sculpt_capabilities.has_direction
    settings = context.tool_settings.sculpt
    capabilities = brush.sculpt_capabilities
    sculpt_tool = brush.sculpt_tool

    col = layout.column()
    col.ui_units_x = 17
    col.scale_y = 0.7
    #ROW1#################################################
    row = col.row()
    sub = row.row(align=True)
    sub.alignment = 'LEFT'
    sub.ui_units_x = 5
    if sculpt_tool == 'GRAB':
        sub.prop(brush, "use_grab_silhouette",  text='SILHOUETTE', toggle=True)
        sub.prop(brush, "use_grab_active_vertex",  text='VERTEX', toggle=True)
    if direction:
        subsub = sub.row()
        subsub.scale_x = 1.5
        subsub.prop(brush, "direction", expand=True, text="")
    else:
        sub.label(text="---")

    sub = row.row()
    sub.alignment = 'CENTER'
    sub.ui_units_x = 5
    if sculpt_tool == 'CLAY_STRIPS':
        sub.prop(brush, "tip_roundness", slider=True, text='ROUND')
    elif sculpt_tool == 'LAYER':
        sub.prop(brush, "height", slider=True, text='HEIGHT')
    elif sculpt_tool == 'CREASE':
        sub.prop(brush, "crease_pinch_factor", slider=True, text='PINCH')
    elif sculpt_tool == 'SCRAPE':
        sub.prop(brush, "area_radius_factor", slider=True, text='AREA')
    elif sculpt_tool == 'FILL':
        sub.prop(brush, "area_radius_factor", slider=True, text='AREA')
    elif sculpt_tool == 'MULTIPLANE_SCRAPE':
        sub.prop(brush, "multiplane_scrape_angle", slider=True, text='ANGLE')
    elif sculpt_tool == 'POSE':
        sub.prop(brush, "pose_ik_segments", slider=True, text='IK')
    elif sculpt_tool == 'GRAB':
        sub.prop(brush, "normal_weight", slider=True, text='PEAK')
    elif sculpt_tool == 'ELASTIC_DEFORM':
        sub.prop(brush, "normal_weight", slider=True, text='PEAK')
    else:
        sub.label(text="")
    
    sub = row.row()
    sub.alignment = 'RIGHT'
    sub.ui_units_x = 5
    if capabilities.has_accumulate:
        sub.prop(brush, "use_accumulate", text="ACCU", toggle=True)
    else:
        sub.label(text='')
    row.separator(factor = 2)
    #ROW2#################################################
    row = col.row()
    sub = row.row()

    sub.ui_units_x = 5
    sub.prop(brush, "normal_radius_factor", slider=True, text='NORMAL')
    sub = row.row()

    sub.ui_units_x = 5
    sub.prop(brush, "hardness", slider=True, text='HARD')
    sub = row.row()

    sub.ui_units_x = 5
    if sculpt_tool == 'MASK':
        sub.prop(brush, "mask_tool", expand=True)
    else:
        sub.prop(brush, "auto_smooth_factor", slider=True, text='SMTH')
    row.separator(factor = 2) 

def TextureBrushSettings(self, context, parent):
    brush = context.tool_settings.image_paint.brush
    settings = context.tool_settings.image_paint
    capabilities = brush.image_paint_capabilities
    use_accumulate = capabilities.has_accumulate
    mode = context.mode

    row = parent.row()

    col = row.column()
    col.ui_units_x = 4
    col.scale_y = 0.7
    col.prop(brush, "use_accumulate", text="ACCU", toggle=True)
    if mode == 'PAINT_2D':
        col.prop(brush, "use_paint_antialiasing")
    else:
        col.prop(brush, "use_alpha", text="ALPHA", toggle=True)

    # Tool specific settings
    col = row.column()
    col.ui_units_x = 6
    col.scale_y = 0.7
    if brush.image_tool == 'SOFTEN':
        col.row().prop(brush, "direction", expand=True)
        col.prop(brush, "threshold")
        #if mode == 'PAINT_2D':
            #col.prop(brush, "blur_kernel_radius")
        #col.prop(brush, "blur_mode")

    elif brush.image_tool == 'MASK':
        col.prop(brush, "weight", text="Mask Value", slider=True)

    elif brush.image_tool == 'CLONE':
        if mode == 'PAINT_2D':
            col.prop(brush, "clone_image", text="Image")
            col.prop(brush, "clone_alpha", text="Alpha")
        else:
            col.label(text='')
    else:
        col.label(text='')

def VertexBrushSettings(self, context, parent):
    brush = context.tool_settings.vertex_paint.brush
    settings = context.tool_settings.vertex_paint

    row = parent.row()
    col = row.column()
    col.ui_units_x = 4
    col.scale_y = 0.7
    col.prop(brush, "use_frontface", text="Front", toggle=True)
    col.prop(brush, "use_alpha", text="ALPHA", toggle=True)

    col = row.column()
    col.ui_units_x = 4
    col.scale_y = 0.7
    if brush.vertex_tool != 'SMEAR':
        col.prop(brush, "use_accumulate", text="ACCU", toggle=True)
    else:
        col.label(text="")

    col = row.column()
    col.ui_units_x = 1.7
    col.label(text="")

def BrushCopy(self, context, parent):
    layout = parent

    get_brush_mode(self, context)
    settings = paint_settings(context)

    col = parent.column(align=True)     
    col.ui_units_x = 4.4
    col.scale_x = 0.2
    col.scale_y = 0.2
    row= col.row()   
    row.template_ID_preview(settings, "brush", rows=1, cols=8, hide_buttons=True )

    '''
    row.template_ID(settings, "brush", new="brush.add")
    row= col.row()
    row.menu("VIEW3D_MT_brush_context_menu", icon='DOWNARROW_HLT', text="")

    if brush is not None:
        row.prop(brush, "use_custom_icon", toggle=True, icon='FILE_IMAGE', text="")

        if brush.use_custom_icon:
            row.prop(brush, "icon_filepath", text="")
    '''
#bpy.ops.brush.reset()


def TexSlots(self, context, parent):
    layout = parent
    layout.use_property_split = True
    layout.use_property_decorate = False

    settings = context.tool_settings.image_paint
    ob = context.active_object

    box = parent.box()
    box.ui_units_x = 8

    box.prop(settings, "mode", text="Mode")
    box.separator()

    if settings.mode == 'MATERIAL':
        if len(ob.material_slots) > 1:
            box.template_list("MATERIAL_UL_matslots", "layers",
                                    ob, "material_slots",
                                    ob, "active_material_index", rows=2)
        mat = ob.active_material
        if mat and mat.texture_paint_images:
            row = box.row()
            row.template_list("TEXTURE_UL_texpaintslots", "",
                                mat, "texture_paint_images",
                                mat, "paint_active_slot", rows=2)

            if mat.texture_paint_slots:
                slot = mat.texture_paint_slots[mat.paint_active_slot]
            else:
                slot = None

            have_image = slot is not None
        else:
            row = box.row()

            box = row.box()
            box.label(text="No Textures")
            have_image = False

        sub = row.column(align=True)
        sub.operator_menu_enum("paint.add_texture_paint_slot", "type", icon='ADD', text="")

    elif settings.mode == 'IMAGE':
        mesh = ob.data
        uv_text = mesh.uv_layers.active.name if mesh.uv_layers.active else ""
        box.template_ID(settings, "canvas", new="image.new", open="image.open")
        if settings.missing_uvs:
            box.operator("paint.add_simple_uvs", icon='ADD', text="Add UVs")
        else:
            box.menu("VIEW3D_MT_tools_projectpaint_uvlayer", text=uv_text, translate=False)
        have_image = settings.canvas is not None

        box.prop(settings, "interpolation", text="")

    if settings.missing_uvs:
        box.separator()
        split = box.split()
        split.label(text="UV Map Needed", icon='INFO')
        split.operator("paint.add_simple_uvs", icon='ADD', text="Add Simple UVs")
    elif have_image:
        box.separator()
        box.operator("image.save_all_modified", text="Save All Images", icon='FILE_TICK')



def Color(self, context, parent):
    layout = parent
    ts = context.tool_settings
    ups = ts.unified_paint_settings
    if context.mode == 'PAINT_VERTEX':
        ptr = ts.vertex_paint.brush
    else:
        ptr = ups if ups.use_unified_color else ts.image_paint.brush    
    
    col = parent.column()
    col.scale_y = 0.7 
    col.ui_units_x = 6
    col.template_color_picker(ptr, 'color', value_slider=True)

def ColorPalette(self, context, parent):
    settings = paint_settings(context)

    col = parent.column()
    col.template_ID(settings, "palette", new="palette.new")
    if settings.palette:
        col.template_palette(settings, "palette", color=True)

def ViewCam(self, context, parent):
    layout = parent

    row = parent.row(align=True)     
    row.ui_units_x = 4.2
    funct_bt(parent=row, cmd='viewcam', tog=True, w=3, h=1.2, label='VIEW CAM', icon="NONE")
    funct_bt(parent=row, cmd='lockcam', tog=True, w=1.2, h=1.2, label='', icon="LOCKED")
    funct_bt(parent=parent, cmd='setactive', tog=False, w=2, h=0.8, label='SET ACTIVE', icon="NONE")  

def Stroke(self, context, parent):
    mode = context.mode
    brush = get_brush_mode(self, context)
    settings = paint_settings(context)

    col = parent.column()
    col.scale_y = 1 
    col.alignment = 'RIGHT'
    #sub = col.row()
    #sub.scale_y = 0.5
    #sub.label(text="STROKE")
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
    col.menu("VIEW3D_MT_StrokeAdv")
    col.separator(factor = 1)
    SmoothStroke(self, context, parent=col)

def SmoothStroke(self, context, parent):
    mode = context.mode
    brush = get_brush_mode(self, context)
    settings = paint_settings(context)

    col = parent.column(align=True)
    col.ui_units_x = 4
    sub = col.column(align=True)
    sub.scale_y = 0.7
    sub.prop(brush, "use_smooth_stroke", text="SMTH STROKE", toggle=True)   
    sub = col.column(align=True)
    sub.scale_y = 0.7
    sub.active = brush.use_smooth_stroke
    sub.prop(brush, "smooth_stroke_factor", text="Factor", slider=True)
    sub.prop(brush, "smooth_stroke_radius", text="Radius", slider=True)



def Falloff(self, context, parent):
    mode = context.mode
    
    settings = paint_settings(context)
    brush = settings.brush  

    col = parent.column(align=True)
    col.ui_units_x = 4
    sub = col.column(align=True)
    sub.scale_y = 0.7

    sub.operator(brush, text='CRV').curve_preset = 'ROOT'


class VIEW3D_MT_Falloff(bpy.types.Menu):
    bl_label = "xmenu.falloff"

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

        '''
        if brush.curve_preset == 'CUSTOM':
            layout.template_curve_mapping(brush, "curve", brush=True)

            col = layout.column(align=True)
            row = col.row(align=True)
            row.operator("brush.curve_preset", icon='SMOOTHCURVE', text="").shape = 'SMOOTH'
            row.operator("brush.curve_preset", icon='SPHERECURVE', text="").shape = 'ROUND'
            row.operator("brush.curve_preset", icon='ROOTCURVE', text="").shape = 'ROOT'
            row.operator("brush.curve_preset", icon='SHARPCURVE', text="").shape = 'SHARP'
            row.operator("brush.curve_preset", icon='LINCURVE', text="").shape = 'LINE'
            row.operator("brush.curve_preset", icon='NOCURVE', text="").shape = 'MAX'
        
        if mode in {'SCULPT', 'PAINT_VERTEX', 'PAINT_WEIGHT'} and brush.sculpt_tool != 'POSE':
            col.separator()
            row = col.row(align=True)
            row.use_property_split = True
            row.use_property_decorate = False
            row.prop(brush, "falloff_shape", expand=True)
        '''

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

def SculptMask(self, context, parent):
    col = parent.column()
    col.scale_y = 0.7 
    row = col.row()

    sub = row.column()
    sub.ui_units_x = 4
    subrow = sub.row(align=True)
    subrow.operator('xmenu.mask', text='FILL').cmd='FILL'
    subrow.operator('xmenu.mask', text='CLR').cmd='CLEAR'
    subrow.operator('xmenu.mask', text='INV').cmd='INVERT'
    subrow = sub.row(align=True)
    subrow.operator('xmenu.mask', text='DIRT').cmd='DIRTMASK'
    subrow.operator('xmenu.mask', text='SLICE').cmd='SLICEOBJ'
    sub = row.column()
    sub.ui_units_x = 4
    subrow = sub.row(align=True)
    subrow.operator('xmenu.mask', text='-').cmd='SHRINK'
    subrow.operator('xmenu.mask', text='+').cmd='GROW'
    subrow = sub.row(align=True)
    subrow.operator('xmenu.mask', text='SHRP').cmd='SHARPEN'
    subrow.operator('xmenu.mask', text='SMTH').cmd='SMOOTH'

def SculptFaceSet(self, context, parent):
    col = parent.column()
    col.scale_y = 0.7 
    col.alignment = 'RIGHT'
    row = col.row()

    sub = row.column()
    sub.ui_units_x = 6
    subrow = sub.row(align=True)
    subrow.operator("sculpt.face_sets_init", text='ISLAND').mode = 'LOOSE_PARTS'
    subrow.operator("sculpt.face_sets_init", text='NORMAL').mode = 'NORMALS'

    subrow = sub.row(align=True)
    subrow.operator("sculpt.face_sets_create", text='VISIBLE').mode = 'VISIBLE'
    subrow.operator("sculpt.face_sets_create", text='MASKED').mode = 'MASKED'

    '''
    subrow = sub.row(align=True)
    subrow.operator("sculpt.face_sets_init", text='UV').mode = 'UV_SEAMS'
    subrow.operator("sculpt.face_sets_init", text='EDGE').mode = 'SHARP_EDGES'
    subrow.operator("sculpt.face_set_edit", text='Grow').mode = 'GROW'
    '''

def SculptTrim(self, context, parent):
    layout = parent
    brush = context.tool_settings.sculpt.brush
    settings = context.tool_settings.sculpt
    capabilities = brush.sculpt_capabilities
    sculpt_tool = brush.sculpt_tool

    col = layout.column()
    col.alignment = 'RIGHT'
    col.ui_units_x = 3
    col.scale_y = 0.7

    if capabilities.has_plane_offset:
        sub = col.row(align=True)
        sub.prop(brush, "plane_offset", slider=True, text='OFFSET')
        sub = col.row(align = True)
        sub.prop(brush, "use_plane_trim", slider=False, toggle=True, text='TRIM')
        sub.prop(brush, "plane_trim", slider=True)
    else:
        sub = col.row(align=True)
        sub.label(text='')

def SculptRake(self, context, parent):
    brush = context.tool_settings.sculpt.brush
    capabilities = brush.sculpt_capabilities

    col = parent.column()
    col.ui_units_x = 4
    col.scale_y = 0.7
    if (capabilities.has_topology_rake and context.sculpt_object.use_dynamic_topology_sculpting):
        col.prop(brush, "topology_rake_factor", slider=True, text='RAKE')
    else:
        col.label(text='')

class VIEW3D_MT_sym(bpy.types.Menu):
    bl_label = "Symmetry"

    def draw(self, context):
        layout = self.layout
        layout.use_property_split = False
        layout.use_property_decorate = False

        sculpt = context.tool_settings.sculpt
        mesh = context.active_object.data

        row = layout.row(align=True)
        row.ui_units_x = 4
        row.scale_y = 1
        split = row.split(factor=0.2, align=True)
        split.label(icon='MOD_MIRROR')
        subrow = split.row(align=True)
        subrow.prop(mesh, "use_mirror_x", text="X", toggle=True)
        subrow.prop(mesh, "use_mirror_y", text="Y", toggle=True)
        subrow.prop(mesh, "use_mirror_z", text="Z", toggle=True)

class VIEW3D_MT_sculpt_sym(bpy.types.Menu):
    bl_label = "Symmetry"

    @classmethod
    def poll(cls, context):
        return (
            (context.sculpt_object and context.tool_settings.sculpt) and
            # When used in the tool header, this is explicitly included next to the XYZ symmetry buttons.
            (context.region.type != 'TOOL_HEADER')
        )

    def draw(self, context):
        layout = self.layout
        layout.use_property_split = False
        layout.use_property_decorate = False

        sculpt = context.tool_settings.sculpt
        mesh = context.active_object.data

        box = layout.box()     
        box.ui_units_x = 6
        sub = box.column(align=True)
        sub.operator("sculpt.symmetrize", text='SYM')
        subsub = sub.row(align=True)
        subsub.scale_y = 0.7
        subsub.prop(sculpt, "symmetrize_direction", text='')

        sub = box.row(align=True)
        sub.scale_y = 0.3 
        sub.label(text="RADIAL")
        sub.label(text="OFFSET")
        sub = box.row(align=True)
        sub.scale_y = 0.7
        subsub = sub.column(align=True)     
        subsub.prop(sculpt, "radial_symmetry", text="")
        subsub = sub.column(align=True)     
        subsub.prop(sculpt, "tile_offset", text="")
        '''
        row = box.row(align=True, heading="Mirror")
        row.scale_y = 0.7
        row.prop(mesh, "use_mirror_x", text="X", toggle=True)
        row.prop(mesh, "use_mirror_y", text="Y", toggle=True)
        row.prop(mesh, "use_mirror_z", text="Z", toggle=True)
        row = box.row(align=True, heading="Lock")
        row.scale_y = 0.7
        row.prop(sculpt, "lock_x", text="X", toggle=True)
        row.prop(sculpt, "lock_y", text="Y", toggle=True)
        row.prop(sculpt, "lock_z", text="Z", toggle=True)
        row = box.row(align=True, heading="Lock")
        row.scale_y = 0.7
        row.prop(sculpt, "use_symmetry_feather", text="Feather")
        row = box.row(align=True, heading="Lock")
        row.scale_y = 0.7
        '''

class VIEW3D_MT_dynamesh(bpy.types.Menu):
    bl_label = "Dyntopo"

    def draw(self, context):
        layout = self.layout
        layout.use_property_split = False
        layout.use_property_decorate = False

        tool_settings = context.tool_settings
        sculpt = tool_settings.sculpt
        box = layout.box()
        box.ui_units_x = 7
        col = box.column()
        col.operator(
            "sculpt.dynamic_topology_toggle",
            depress=True if context.sculpt_object.use_dynamic_topology_sculpting else False,
            text="DYNA",
            emboss=True,
        )
        sub = col.column()
        sub.active = context.sculpt_object.use_dynamic_topology_sculpting

        subrow2 = sub.row(align=True)
        subrow2.scale_y = 0.9
        if sculpt.detail_type_method in {'CONSTANT', 'MANUAL'}:
            row = subrow2.row(align=True)
            row.prop(sculpt, "constant_detail_resolution", text="")
            props = row.operator("sculpt.sample_detail_size", text="", icon='EYEDROPPER')
            props.mode = 'DYNTOPO'
        elif (sculpt.detail_type_method == 'BRUSH'):
            subrow2.prop(sculpt, "detail_percent", text="")
        else:
            subrow2.prop(sculpt, "detail_size", text="")

        subrow1 = sub.row(align=True)
        subrow1.scale_y = 0.8
        subrow1.operator('xmenu.detailsize', text='3').size=3
        subrow1.operator('xmenu.detailsize', text='5').size=5
        subrow1.operator('xmenu.detailsize', text='9').size=9
        subrow1.operator('xmenu.detailsize', text='17').size=17

        subrow3 = sub.row(align=True)
        subrow3.scale_y = 0.8
        subrow3.prop_menu_enum(sculpt, "detail_refine_method", text="METHOD")
        subrow3.prop_menu_enum(sculpt, "detail_type_method", text="TYPE")
        #if sculpt.detail_type_method in {'CONSTANT', 'MANUAL'}:
        col.operator("sculpt.detail_flood_fill", text='FLOOD')
        #col.prop(sculpt, "use_smooth_shading", text='Smooth')

class VIEW3D_MT_remesh(bpy.types.Menu):
    bl_label=""
    @classmethod
    def poll(cls, context):
        return (context.sculpt_object and context.tool_settings.sculpt)

    def draw(self, context):
        layout = self.layout
        layout.use_property_split = False
        layout.use_property_decorate = False

        mesh = context.active_object.data
        
        box = layout.box()
        box.ui_units_x = 7
        col = box.column(align=False)

        row = col.row(align=True)
        row.prop(mesh, "remesh_voxel_size", text="")
        props = row.operator("sculpt.sample_detail_size", text="", icon='EYEDROPPER')
        props.mode = 'VOXEL'
        sub0 = col.row()
        sub0.scale_y = 0.8
        sub0_col1 = sub0.column()
        sub0_col1.ui_units_x = 1.5
        sub0_col1 .label(text="Adapt")
        sub0_col2 = sub0.column()
        sub0_col2.ui_units_x = 6
        sub0_col2.prop(mesh, "remesh_voxel_adaptivity", text="", slider=True)
        sub1 = col.row()
        sub1.scale_y = 0.8

        sub0_col2.prop(mesh, "use_remesh_fix_poles", toggle=True)

        sub2 = col.row(align=False)
        sub2.scale_y = 0.8
        sub2_col1 = sub2.column()
        sub2_col1.ui_units_x = 1.5
        sub2_col1.label(text="Keep")

        sub2_col2 = sub2.column()
        sub2_col2.ui_units_x = 6
        grid = sub2_col2.grid_flow(columns=3, align=True)
        
        grid.prop(mesh, "use_remesh_preserve_volume", text="V", toggle=True)
        grid.prop(mesh, "use_remesh_preserve_paint_mask", text="M", toggle=True)
        grid.prop(mesh, "use_remesh_preserve_sculpt_face_sets", text="FS", toggle=True)

        if context.preferences.experimental.use_sculpt_vertex_colors:
            grid.prop(mesh, "use_remesh_preserve_vertex_colors", text="VertCol", toggle=True)

        col.operator("object.voxel_remesh", text="REMESH")

class VIEW3D_MT_BrushTexture(bpy.types.Menu):
    bl_label = ""
    def draw(self, context):
        layout = self.layout
        wm = context.window_manager
        mode = context.active_object.mode
        brush = get_brush_mode(self, context)

        col = layout.column()
        sub = col.row(align=True)
        sub.prop(brush,"xm_tex_brush_categories",text="")
        sub = col.row(align=True)
        sub.scale_y = 0.5
        sub.template_icon_view(brush,"xm_brush_texture",show_labels=True, scale_popup=4)
        sub = col.row(align=True)
        sub.prop(brush,"xm_use_mask",text="MASK",toggle=True, )
        sub.prop(brush,"xm_invert_mask",text="",toggle=True,icon="IMAGE_ALPHA")

        '''
        sub = col.row(align=True)
        subcol = sub.column(align=True)
        subcol.scale_y = 0.7
        subcol.prop(brush,"xm_ramp_tonemap_l",text="MapL",slider=True)
        subcol.prop(brush,"xm_ramp_tonemap_r",text="MapR",slider=True)
        subcol = sub.column(align=True)
        subcol.scale_y = 1.4
        subcol.prop(brush,"xm_invert_mask",text="",toggle=True,icon="IMAGE_ALPHA")
        sub = col.row(align=True)
        sub.scale_y = 0.7
        sub.prop(brush,"xm_use_mask",text="MASK",toggle=True)
        col.separator(factor=0.2)
        '''
        col = layout.column()
        col.ui_units_x = 12
        sub = col.row(align=True)
        sub.scale_y = 0.7
        brush_texture_settings(col, brush, context.sculpt_object)
        '''
        col = layout.column()
        col.template_icon_view(brush,"xm_stencil_texture",show_labels=True)
        col.prop(brush,"xm_invert_stencil_mask",text="Invert Mask",toggle=True,icon="IMAGE_ALPHA")
        '''
        
def brush_texture_settings(layout, brush, sculpt):
    tex_slot = brush.texture_slot

    # map_mode
    layout.prop(tex_slot, "map_mode", text="")

    if tex_slot.map_mode == 'STENCIL':
        if brush.texture and brush.texture.type == 'IMAGE':
            layout.operator("brush.stencil_fit_image_aspect")
        layout.operator("brush.stencil_reset_transform")

    # angle and texture_angle_source
    if tex_slot.has_texture_angle:
        col = layout.column()
        col.prop(tex_slot, "angle", text="Angle")
        if tex_slot.has_texture_angle_source:
            sub = col.row(align=True)
            sub.prop(tex_slot, "use_rake", text="RAKE", toggle=True)

            if brush.brush_capabilities.has_random_texture_angle and tex_slot.has_random_texture_angle:
                if sculpt:
                    if brush.sculpt_capabilities.has_random_texture_angle:
                        sub.prop(tex_slot, "use_random", text="RAND", toggle=True)
                        if tex_slot.use_random:
                            sub = col.row()
                            sub.scale_y = 0.7
                            sub.prop(tex_slot, "random_angle", text="ANGLE")
                else:
                    sub.prop(tex_slot, "use_random", text="RAND", toggle=True)
                    if tex_slot.use_random:
                        sub = col.row()
                        sub.scale_y = 0.7
                        sub.prop(tex_slot, "random_angle", text="ANGLE")
    if sculpt:
        # texture_sample_bias
        sub = col.row()
        sub.scale_y = 0.7
        sub.prop(brush, "texture_sample_bias", slider=True, text="Sample Bias")

    '''
    # scale and offset
    row = layout.row(align=True)
    sub = row.column(align=True)
    sub.scale_y = 0.7
    sub.label(text='OFFSET')
    sub.prop(tex_slot, "offset", text='')   
    sub = row.column(align=True)
    sub.scale_y = 0.7
    sub.label(text='SCALE')
    sub.prop(tex_slot, 'scale', text='')
    '''

preview_collections = {}

def unregister_previews():
    for pcoll in preview_collections.values():
        bpy.utils.previews.remove(pcoll)
    preview_collections.clear()
        
def register_previews():
    import bpy.utils.previews
    pcoll = bpy.utils.previews.new()
    pcoll.my_previews_dir = ""
    pcoll.my_previews = ()

    #preview_collections["xm_misc_icons"] = pcoll   

classes = (VIEW3D_MT_dynamesh, VIEW3D_MT_remesh, VIEW3D_MT_sculpt_sym, VIEW3D_MT_sym, VIEW3D_MT_BrushTexture, VIEW3D_MT_StrokeAdv, VIEW3D_MT_Falloff)

def register():
    for cls in classes:
        bpy.utils.register_class(cls)
    
def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)