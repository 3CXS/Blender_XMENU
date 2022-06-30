import bpy
import os
from .icons.icons import load_icons
from.toolsets import Tools_Sculpt
from .functions import tool_grid, tool_bt, funct_bt, paint_settings
from .brushtexture import brush_icons_path, get_brush_mode, setup_brush_tex, _invert_ramp, _mute_ramp
from bpy.props import StringProperty, IntProperty, BoolProperty
from bl_ui.space_toolsystem_common import (ToolSelectPanelHelper,ToolDef)
from bpy.app.translations import contexts as i18n_contexts

from bpy.types import Menu, Panel, UIList, AddonPreferences
from rna_prop_ui import PropertyPanel
from collections import defaultdict


def HeaderInset(self, context):

    inset = bpy.context.preferences.addons[__package__].preferences.header_inset

    ob = context.active_object
    row = self.layout.row(align=True)
    row.ui_units_x = inset
    row.label(text=' ')

def SaveScene(self, context, parent):
    layout = parent
    box = layout.box()

    col = box.column(align=True)
    col.ui_units_x = 4
    col.operator("wm.save_as_mainfile", text="SAVE AS")
    col.separator()
    col.operator("wm.open_mainfile", text="OPEN")
    col.menu("TOPBAR_MT_file_open_recent", text="RECENT")
    col.separator()
    sub = col.row(align=True)
    sub.operator("wm.link", icon='LINK_BLEND', text="LINK")
    sub.operator("wm.append", icon='APPEND_BLEND', text="APND")

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
        layout.use_property_split = False
        layout.use_property_decorate = False

        file_path = bpy.context.preferences.addons[__package__].preferences.file_path              
        scene = context.scene

        col = layout.column(align=True)
        col.ui_units_x = 4.5
        col.menu_contents("OBJECT_MT_import_menu")

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
        col.ui_units_x = 4.5
        sub = col.row(align=True)
        sub.prop(scene, "import_items", expand=True)
        sub = col.column(align=True)
        if scene.import_items == '01':
            subsub = sub.row(align=True)
            subsub.label(text='-->')
            subsub.scale_y = 0.7
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
        else:
            subsub = sub.row(align=True)
            subsub.label(text='                                                                -->')
            subsub.scale_y = 0.7
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



def ViewCamSettings(self, context, layout):

    view = context.space_data

    layout.use_property_split = False
    layout.use_property_decorate = False  # No animation.

    row = layout.row(align=True)

    subcol = row.column()
    #   subcol.active = bool(view.region_3d.view_perspective != 'CAMERA' or view.region_quadviews)
    subcol.prop(view, "lens", text="F")

    subsub = row.column(align=True)
    subsub.scale_y = 0.7    
    subsub.prop(view, "clip_start", text="Clip")
    subsub.prop(view, "clip_end", text="End")


def HideObject(self, context, parent):
        ob = context.active_object

        row = parent.row(align=True)
        row.ui_units_x = 3

        if ob != None:
            if ob.hide_viewport == True:
                state = True
                label = 'UNHIDE'
            else:
                state = False
                label = 'HIDE'
            row.operator("xmenu.hide", text=label)


def HideObjectMenuBt(self, context):
        ob = context.active_object

        row = self.layout.row(align=True)
        row.ui_units_x = 2.4

        if ob != None:
            if ob.hide_viewport == True:
                state = True
                label = 'UNHIDE'
            else:
                state = False
                label = 'HIDE'
            row.operator("xmenu.hide", text=label)
        else: 
            row.label(text='')

def History(self, context, parent):
        layout = parent
        row = layout.row(align=True)

        row.ui_units_x = 4
        sub = row.row(align=True)
        sub.alignment = 'LEFT'
        sub.scale_x = 2
        sub.operator("ed.undo", icon='TRIA_LEFT', text="")
        sub = row.row(align=True)
        sub.alignment = 'RIGHT'
        sub.scale_x = 2
        sub.operator("ed.redo", icon='TRIA_RIGHT', text="")

def ShadingMode(self, context, parent):
        layout = parent

        tool_settings = context.tool_settings
        view = context.space_data
        shading = view.shading
        overlay = view.overlay

        row = layout.row(align=True)
        row.prop(shading, "type", text="", expand=True)
        sub = row.row(align=True)
        sub.popover(panel="VIEW3D_PT_shading", text="")

        #row.prop(overlay, "show_overlays", text="", icon='OVERLAY', expand=True)
        #row.popover(panel="VIEW3D_PT_overlay", text="")
        #row.separator(factor=1)


def VertexGroups(self, context, parent):
    ob = context.active_object
    group = ob.vertex_groups.active
    box = parent.box()

    row = box.row()
    col = row.column(align=True)
    col.ui_units_x = 6
    col.template_list("MESH_UL_vgroups", "", ob, "vertex_groups", ob.vertex_groups, "active_index", rows=5)

    col = row.column(align=True)
    col.ui_units_x = 1
    col.operator("xmenu.override", icon='ADD', text="").cmd ='object.vertex_group_add'
    col.operator("xmenu.override", icon='REMOVE', text="").cmd='object.vertex_group_remove'
    col.separator()
    col.menu("MESH_MT_vertex_group_context_menu", icon='DOWNARROW_HLT', text="")   
    if group:
        col.separator()
        op = col.operator("xmenu.override1", icon='TRIA_UP', text="")
        op.cmd='object.vertex_group_move'
        op.prop1 ='direction="UP"'

        op = col.operator("xmenu.override1", icon='TRIA_DOWN', text="")
        op.cmd='object.vertex_group_move'
        op.prop1 ='direction="DOWN"'

    if (ob.vertex_groups and (ob.mode == 'EDIT' or (ob.mode == 'WEIGHT_PAINT' and ob.type == 'MESH' and ob.data.use_paint_mask_vertex))):
        col = row.column(align=True)
        col.ui_units_x = 5
        sub = col.row(align=True)
        sub.operator("xmenu.override", text="ASSIGN").cmd ='object.vertex_group_assign'
        sub.operator("xmenu.override", text="REMOVE").cmd ='object.vertex_group_remove_from'

        sub = col.row(align=True)
        sub.operator("xmenu.override", text="SELECT").cmd ='object.vertex_group_select'
        sub.operator("xmenu.override", text="DESELCT").cmd ='object.vertex_group_deselect'

        col.prop(context.tool_settings, "vertex_group_weight", text="WEIGHT")

    else:
        col = row.column(align=True)
        col.ui_units_x = 2
        col.label(text='>')

        #row = box.row()
        #sub = row.row(align=True)
        #sub.operator("xmenu.override", text="COPY").cmd ='object.vertex_group_copy'
        #sub.operator("xmenu.override", text="COPY TO").cmd ='object.vertex_group_copy_to_selected'
        #sub = row.row(align=True)
        #op = sub.operator("xmenu.override1", text="MIRROR")
        #op.cmd = 'object.vertex_group_mirror'
        #op.prop1 = 'use_topology=False'


class VIEW3D_MT_Material(bpy.types.Menu):
    bl_label = "Materials"

    def draw(self, context):
        layout = self.layout

        layout.use_property_split = False
        layout.use_property_decorate = False

        ob = context.active_object
        mat = ob.active_material

        slot = ob.material_slots

        space = context.space_data

        box = layout.box()

        if ob:
            is_sortable = len(ob.material_slots) > 1

            row = box.row()
            col = row.column(align=True)
            col.ui_units_x = 7
            col.template_list("MATERIAL_UL_matslots", "", ob, "material_slots", ob, "active_material_index", rows=4)
            col.template_ID(ob, "active_material")
            col.operator("xmenu.override", icon='ADD', text="NEW").cmd='material.new'
            col = row.column(align=True)
            col.ui_units_x = 1
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

            '''
            if slot:
                icon_link = 'MESH_DATA' if slot.link == 'DATA' else 'OBJECT_DATA'
                row.prop(slot, "link", icon=icon_link, icon_only=True)
            '''

            if context.mode == 'EDIT_MESH':
                col = row.column(align=True)
                col.ui_units_x = 3
                col.operator("xmenu.override", text="Assign").cmd='object.material_slot_assign'
                col.operator("object.material_slot_select", text="Select")
                col.operator("object.material_slot_deselect", text="Deselect")

        elif mat:
            row.template_ID(space, "pin_id")

def newmaterial(self, context):
        area = [area for area in bpy.context.screen.areas if area.type == "VIEW_3D"][0]
        
        window = bpy.context.window
        screen =  bpy.context.screen
        region = area.regions[-1]
        scene = bpy.context.scene
        space_data = area.spaces.active
        ob = bpy.context.active_object
        with context.temp_override(area=area, region=region, space_data=space_data):
            bpy.ops.material.new()


def UVTexture(self, context, parent):
    ob = context.active_object
    box = parent.box()
    box.ui_units_x = 8

    if ob != None and ob.type == 'MESH':
        mesh = context.active_object.data
        row = box.row()
        col = row.column()
        col.template_list("MESH_UL_uvmaps", "uvmaps", mesh, "uv_layers", mesh.uv_layers, "active_index", rows=2)
        col = row.column(align=True)
        col.operator("xmenu.override", icon='ADD', text="").cmd='mesh.uv_texture_add'
        col.operator("xmenu.override", icon='REMOVE', text="").cmd='mesh.uv_texture_remove'
    else:
        sub = box.row(align=True)
        sub.label(text=">")

def VertexColor(self, context, parent):
    mesh = context.active_object.data

    box = parent.box()
    row = box.row()
    row.ui_units_x = 8
    col = row.column()
    col.template_list("MESH_UL_color_attributes", "color_attributes", mesh, "color_attributes", mesh.color_attributes, "active_color_index", rows=2)
    col = row.column(align=True)
    col.operator("xmenu.override", icon='ADD', text="").cmd='geometry.color_attribute_add'
    col.operator("xmenu.override", icon='REMOVE', text="").cmd='geometry.color_attribute_remove'

def Normals(self, context, parent):
    layout = parent
    layout.use_property_split = False
    scene = context.scene
    ob = context.active_object

    col = layout.column(align=False)
    row = col.row(align=True)

    if ob != None and ob.type == 'MESH':
        mesh = context.active_object.data
        sub = row.row(align=True)
        sub.ui_units_x = 2
        sub.operator("xmenu.normalshading", text="SMTH", depress=updatenormaldisp(self, context))
        #sub.separator()
        sub = row.row(align=True)
        sub.ui_units_x = 2
        sub.active = updatenormaldisp(self, context)
        sub.prop(mesh, "use_auto_smooth", text="ANGL", toggle=True)
        sub = row.row(align=True)
        sub.ui_units_x = 4
        sub.active = mesh.use_auto_smooth and not mesh.has_custom_normals
        sub.prop(mesh, "auto_smooth_angle", text="")
    else:
        sub = row.row(align=True)
        sub.label(text=">")

def updatenormaldisp(self, context):
    ob = context.active_object
    polygons = ob.data.polygons
    state = ob.data.polygons[0].use_smooth
    return state

class NormalShading(bpy.types.Operator):
    bl_idname = "xmenu.normalshading"
    bl_label = "NORMALS"
      
    def execute(self, context):
        ob = context.active_object
        polygons = ob.data.polygons
        for window in bpy.context.window_manager.windows:
            screen = window.screen
            for area in screen.areas:
                if area.type == 'VIEW_3D':
                    for polygons in ob.data.polygons:
                        polygons.use_smooth  = not polygons.use_smooth
        return {'FINISHED'}



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
        sub.label(text="<<")

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
        sub.operator('object.pivotobottom', text='BOTTOM')        #needs 3d viewport pie menu addon#
        op = sub.operator('object.origin_set', text='CURSOR')
        op.type = 'ORIGIN_CURSOR'
        op.center ='MEDIAN'

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
    row = layout.row()
    #row.ui_units_x = 12
    if bpy.context.mode == 'OBJECT': 
        subrow = row.row(align=True)
        subrow.ui_units_x = 8
        subrow.prop(ts, "use_transform_data_origin", text="ORIG", toggle=True)
        subrow.prop(ts, "use_transform_pivot_point_align", text="LOC", toggle=True)
        subrow.prop(ts, "use_transform_skip_children", text="PARENT", toggle=True)

    elif bpy.context.mode == 'EDIT_MESH':
        subrow = row.row(align=True)
        subrow.ui_units_x = 4.2
        subrow.prop(ts, "use_mesh_automerge", text="Auto Merge", toggle=True)

    elif bpy.context.mode == 'EDIT_GPENCIL':
        subrow = row.row(align=True)
        subrow.ui_units_x = 4.2
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

    if toolname == 'builtin.extrude':
        props = tool.gizmo_group_properties("VIEW3D_GGT_xform_extrude")
        layout.prop(props, "axis_type", expand=True)

    else:
        sub = col.row(align=True)
        sub.label(text='------')


def GPToolSettings(self, context, parent):
    layout = parent
    tool = context.workspace.tools.from_space_view3d_mode(context.mode)
    toolname = context.workspace.tools.from_space_view3d_mode(bpy.context.mode).idname

    col = layout.column()
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

    elif toolname == 'builtin.transform_fill':
        props = tool.operator_properties("gpencil.transform_fill")
        sub = col.row(align=True)
        sub.prop(props, "mode", expand=True)

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
        sub = col.row(align=True)
        sub.label(text='------')

def SculptFilterSettings(self, context, parent):
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
        sub.prop(props, "type", text='', expand=False)
        sub.prop(props, "strength")
        subsub = sub.row(align=True)
        subsub.prop(props, "force_axis")
        sub.prop(props, "orientation", expand=False)
        sub.prop(props, "cloth_mass")
        sub.prop(props, "cloth_damping")
        sub.prop(props, "use_face_sets")
        sub.prop(props, "use_collisions")

    else:
        sub = col.row(align=True)
        sub.ui_units_x = 5
        sub.label(text='>')

def SculptToolSettings(self, context, parent):
    layout = parent

    tool = context.workspace.tools.from_space_view3d_mode(bpy.context.mode).idname
    brush = context.tool_settings.sculpt.brush
    settings = context.tool_settings.sculpt
    capabilities = brush.sculpt_capabilities
    sculpt_tool = brush.sculpt_tool

    col = layout.column()
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



def SculptBrushSettings(self, context, parent):
    layout = parent
    brush = context.tool_settings.sculpt.brush
    direction = not brush.sculpt_capabilities.has_direction
    settings = context.tool_settings.sculpt
    capabilities = brush.sculpt_capabilities
    sculpt_tool = brush.sculpt_tool

    col = layout.column(align=True)
    #col.ui_units_x = 15
    col.scale_y = 0.7
    #ROW1#################################################
    row = col.row()
    sub = row.row(align=True)

    sub.ui_units_x = 6
    if sculpt_tool == 'GRAB':
        sub.prop(brush, "use_grab_silhouette",  text='SILHOUETTE', toggle=True)
        sub.prop(brush, "use_grab_active_vertex",  text='VERTEX', toggle=True)

    elif direction:
        subsub = sub.row(align=True)
        subsub.scale_x = 1.5
        subsub.prop(brush, "direction", expand=True, text="")
        subsub.label(text="")
    elif sculpt_tool == 'PAINT':
        sub.prop(brush, "flow", slider=True, text="FLOW")
        sub.prop(brush, "invert_flow_pressure", text="")
        sub.prop(brush, "use_flow_pressure", text="")

    elif sculpt_tool == 'SMEAR':
        sub.prop(brush, "smear_deform_type", expand=True)

    else:
        sub.label(text="")
    #sub.separator(factor=1)

    sub = row.row(align=True)
    sub.ui_units_x = 6
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
    elif sculpt_tool == 'PAINT':
        sub.prop(brush, "wet_mix", slider=True, text="WETMIX")
        sub.prop(brush, "invert_wet_mix_pressure", text="")
        sub.prop(brush, "use_wet_mix_pressure", text="")
    else:
        sub.label(text="")
    sub.separator(factor=1)

    sub = row.row(align=True)
    sub.ui_units_x = 6
    if (capabilities.has_topology_rake and context.sculpt_object.use_dynamic_topology_sculpting):
        sub.prop(brush, "topology_rake_factor", slider=True, text='RAKE')

        if capabilities.has_accumulate:
            sub.prop(brush, "use_accumulate", text="ACCU", toggle=True)
        else:
            sub.label(text='')
    elif capabilities.has_accumulate:
        sub.label(text='')
        sub.prop(brush, "use_accumulate", text="ACCU", toggle=True)

    elif sculpt_tool == 'PAINT':
        sub.prop(brush, "wet_persistence", slider=True, text="PERS")
        sub.prop(brush, "invert_wet_persistence_pressure", text="")
        sub.prop(brush, "use_wet_persistence_pressure", text="")
    else:
        sub.label(text='')

    #ROW2#################################################
    row = col.row()
    sub = row.row(align=True)
    sub.ui_units_x = 6
    sub.prop(brush, "normal_radius_factor", slider=True, text='NORMAL')
    sub.separator(factor=1)

    sub = row.row(align=True)
    sub.ui_units_x = 6
    sub.prop(brush, "hardness", slider=True, text='HARD')
    sub.separator(factor=1)

    sub = row.row(align=True)
    sub.ui_units_x = 6
    if sculpt_tool == 'MASK':
        sub.prop(brush, "mask_tool", expand=True)
    elif sculpt_tool == 'PAINT':
        sub.prop(brush, "wet_paint_radius_factor", slider=True, text='WET RAD')
    else:
        sub.prop(brush, "auto_smooth_factor", slider=True, text='SMTH')


def Overlay(self, context, layout):
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

    col = layout.column(align=True)
    col.scale_y = 0.7
    col.ui_units_x = 4
    subcol = col.column(align=True)
    if context.mode == 'SCULPT':
        sub = subcol.row(align=True)
        sub.prop(ts, "show_face_sets", text="F-SETS", toggle=True)
        sub.prop(ts, "show_mask", text="MASK", toggle=True)
        sub = subcol.row(align=True)
        if ob != None and ob.type == 'MESH':
            sub.active = ob.show_wire
            sub.prop(overlay, "wireframe_opacity", text="Wire")
        else:
            sub.label(text="")

    else:
        sub = subcol.row(align=True)
        funct_bt(parent=sub, cmd='grid', tog=True, w=2, h=1, label='GRID', icon="NONE")
        funct_bt(parent=sub, cmd='axis', tog=True, w=2, h=1, label='AXIS', icon="NONE")
        sub = subcol.row(align=True)
        if ob != None and ob.type == 'MESH':
            sub.active = ob.show_wire
            sub.prop(overlay, "wireframe_opacity", text="Wire")
        else:
            sub.label(text="")

def TextureBrushSettings(self, context, parent):
    brush = context.tool_settings.image_paint.brush
    settings = context.tool_settings.image_paint
    capabilities = brush.image_paint_capabilities
    use_accumulate = capabilities.has_accumulate
    mode = context.mode

    row = parent.row()

    sub = row.row(align=True)
    sub.ui_units_x = 4
    sub.scale_y = 1
    sub.prop(brush, "use_accumulate", text="ACCU", toggle=True)
    if mode == 'PAINT_2D':
        sub.prop(brush, "use_paint_antialiasing")
    else:
        sub.prop(brush, "use_alpha", text="ALPHA", toggle=True)

    # Tool specific settings
    sub = row.row()
    sub.ui_units_x = 5
    sub.scale_y = 1
    if brush.image_tool == 'SOFTEN':
        sub.row().prop(brush, "direction", expand=True)
        sub.prop(brush, "threshold")
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

def VertexBrushSettings(self, context, parent):
    brush = context.tool_settings.vertex_paint.brush
    settings = context.tool_settings.vertex_paint

    row = parent.row(align=True)

    row.scale_y = 1
    row.prop(brush, "use_frontface", text="FRONT", toggle=True)
    row.prop(brush, "use_alpha", text="ALPHA", toggle=True)

    row = row.column(align=True)

    if brush.vertex_tool != 'SMEAR':
        row.prop(brush, "use_accumulate", text="ACCU", toggle=True)
    else:
        row.label(text="")


def BrushCopy(self, context, parent):
    layout = parent

    get_brush_mode(self, context)
    settings = paint_settings(context)

    col = parent.column(align=True)     
    col.ui_units_x = 4
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
    box = parent.box()
    col = box.column()
    #col.scale_y = 0.8    
    col.template_ID(settings, "palette", new="palette.new")
    if settings.palette:
        col.template_palette(settings, "palette", color=True)

def ViewCam(self, context, parent):
    layout = parent

    row = parent.row(align=True)     
    funct_bt(parent=row, cmd='viewcam', tog=True, w=2.4, h=1, label='CAM', icon="NONE")
    funct_bt(parent=row, cmd='lockcam', tog=True, w=1.2, h=1, label='', icon="LOCKED")
    funct_bt(parent=row, cmd='setactive', tog=False, w=1.6, h=1, label='SET', icon="NONE")  

def Stroke(self, context, parent):
    mode = context.mode
    brush = get_brush_mode(self, context)
    settings = paint_settings(context)

    col = parent.column()
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
    col.menu("VIEW3D_MT_StrokeAdv")
    #col.separator(factor = 1)
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
    row = col.row(align=True)

    sub = row.column(align=True)
    sub.scale_y = 1.4
    sub.ui_units_x = 3.2
    subrow = sub.row(align=True)
    #subrow.operator('xmenu.mask', text='FILL').cmd='FILL'
    subrow.operator('xmenu.mask', text='CLR').cmd='CLEAR'
    subrow.operator('xmenu.mask', text='INV').cmd='INVERT'
    #subrow = sub.row(align=True)
    #subrow.operator('xmenu.mask', text='DIRT').cmd='DIRTMASK'
    #subrow.operator('xmenu.mask', text='SLICE').cmd='SLICEOBJ'

    sub = row.column(align=True)
    sub.ui_units_x = 3.2
    sub.scale_y = 0.7
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

class VIEW3D_MT_sym(bpy.types.Menu):
    bl_label = "Symmetry"

    def draw(self, context):
        layout = self.layout
        layout.use_property_split = False
        layout.use_property_decorate = False

        sculpt = context.tool_settings.sculpt
        mesh = context.active_object.data

        row = layout.row(align=True)
        #row.ui_units_x = 2
        #row.scale_y = 1
        #split = row.split(factor=0.2, align=True)
        #split.label(icon='MOD_MIRROR')
        row.prop(mesh, "use_mirror_x", text="X", toggle=True)
        row.prop(mesh, "use_mirror_y", text="Y", toggle=True)
        row.prop(mesh, "use_mirror_z", text="Z", toggle=True)

class VIEW3D_MT_sculpt_sym(bpy.types.Menu):
    bl_label = "MENU"

    @classmethod
    def poll(cls, context):
        return (
            (context.sculpt_object and context.tool_settings.sculpt) and
            # When used in the tool header, this is explicitly included next to the XYZ symmetry buttons.
            (context.region.type != 'TOOL_HEADER')
        )

    def draw(self, context):
        layout = self.layout
        layout.use_property_split = True
        layout.use_property_decorate = False
        layout.separator_spacer()

        sculpt = context.tool_settings.sculpt
        mesh = context.active_object.data

        col = layout.column()     
        col.ui_units_x = 4

        sub = col.row()
        sub.prop(sculpt, "symmetrize_direction", text='')

        sub = col.row(align=True)
        sub.scale_y = 0.3 
        sub.label(text="RADIAL")
        sub.label(text="OFFSET")

        sub = col.row(align=True)
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
        box.ui_units_x = 6
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
        box.ui_units_x = 6
        col = box.column(align=False)

        row = col.row(align=True)
        row.prop(mesh, "remesh_voxel_size", text="")
        props = row.operator("sculpt.sample_detail_size", text="", icon='EYEDROPPER')
        props.mode = 'VOXEL'

        sub = col.row(align=True)
        sub.scale_y = 0.8
        sub.operator('xmenu.voxelsize', text='S').size=0.01
        sub.operator('xmenu.voxelsize', text='M').size=0.02
        sub.operator('xmenu.voxelsize', text='L').size=0.05

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

        #sub0_col2.prop(mesh, "use_remesh_fix_poles", toggle=True)

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

        '''
        if context.preferences.experimental.use_sculpt_vertex_colors:
            grid.prop(mesh, "use_remesh_preserve_vertex_colors", text="VertCol", toggle=True)
        '''
        col.operator("object.voxel_remesh", text="REMESH")


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


class VIEW3D_MT_GPFill(bpy.types.Menu):
    bl_label = ""

    def draw(self, context):
        layout = self.layout

        ob = context.active_object
        ma = ob.active_material
        gpcolor = ma.grease_pencil

        box = layout.box()
        col = box.column()
        col.prop(gpcolor, "show_fill", text="FILL")

        # color settings
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


class VIEW3D_MT_BrushTexture(bpy.types.Menu):
    bl_label = ""
    def draw(self, context):
        layout = self.layout
        wm = context.window_manager
        mode = context.active_object.mode
        brush = get_brush_mode(self, context)

        row = layout.row(align=True) 
        col = row.column()
        col.ui_units_x = 4
        sub = col.row(align=True)
        sub.prop(brush,"xm_tex_brush_categories",text="")
        sub = col.row(align=True)
        sub.scale_y = 0.4
        sub.template_icon_view(brush,"xm_brush_texture",show_labels=True, scale_popup=4)
        row.separator()
        col = layout.column()
        col.ui_units_x = 4
        sub = col.row(align=True)
        sub.scale_y = 0.7
        brush_texture_settings(col, brush, context.sculpt_object)

class VIEW3D_MT_TextureMask(bpy.types.Menu):
    bl_label = ""
    def draw(self, context):
        layout = self.layout
        brush = get_brush_mode(self, context)

        row = layout.row(align=True)

        sub = row.row(align=True)
        sub.ui_units_x = 4
        sub.scale_y = 1.4
        sub.prop(brush,"xm_use_mask",text="RAMP",toggle=True,)

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

def brush_texture_settings(layout, brush, sculpt):
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
        sub.scale_y = 0.7
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
                            sub.scale_y = 0.7
                            sub.prop(tex_slot, "random_angle", text="ANGLE")
                else:
                    sub.prop(tex_slot, "use_random", text="RAND", toggle=True)
                    if tex_slot.use_random:
                        sub = col.row()
                        sub.scale_y = 0.7
                        sub.prop(tex_slot, "random_angle", text="ANGLE")
    if sculpt:
        sub = col.row(align=True)
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

classes = (VIEW3D_MT_Material, VIEW3D_MT_GPStroke, VIEW3D_MT_GPFill, NormalShading,  ImportMenu, ImportPanel, VIEW3D_MT_dynamesh, VIEW3D_MT_remesh, VIEW3D_MT_sculpt_sym, VIEW3D_MT_sym, VIEW3D_MT_BrushTexture, VIEW3D_MT_TextureMask, VIEW3D_MT_StrokeAdv, VIEW3D_MT_Falloff)

def register():
    bpy.types.Scene.import_items = bpy.props.EnumProperty(default="01",items=[("01","IMPORT",""),("02","EXPORT","")])
    bpy.types.WindowManager.normalshading_state = bpy.props.BoolProperty(default = False)

    for cls in classes:
        bpy.utils.register_class(cls)

    bpy.types.VIEW3D_HT_header.prepend(HeaderInset)
    bpy.types.VIEW3D_HT_header.append(HeaderInset)
    bpy.types.OUTLINER_HT_header.prepend(HideObjectMenuBt) 

def unregister():

    bpy.types.OUTLINER_HT_header.remove(HideObjectMenuBt)
    bpy.types.OUTLINER_HT_header.remove(HeaderInset)

    for cls in classes:
        bpy.utils.unregister_class(cls)