import bpy
from bpy.props import (StringProperty,
                       BoolProperty,
                       FloatVectorProperty,
                       FloatProperty,
                       EnumProperty,
                       IntProperty,
                       PointerProperty)
from bl_ui.space_toolsystem_common import ToolSelectPanelHelper
from bpy.types import Operator, AddonPreferences
from .icons.icons import load_icons
from.toolsets import Tools_Sculpt
from bl_ui.properties_data_modifier import DATA_PT_modifiers
from .functions import tool_grid, tool_bt, funct_bt


def ToolOptions(self, context, parent):
    layout = parent

    row = parent.row(align=False)     

    ts = context.tool_settings
    brush = context.tool_settings.sculpt.brush


    if bpy.context.mode == 'OBJECT': 
        row.prop(ts, "use_transform_data_origin", toggle=True)

    elif bpy.context.mode == 'EDIT_MESH':
        row.prop(ts, "use_mesh_automerge", text="Auto Merge", toggle=True)


    elif bpy.context.mode == 'SCULPT':
        capabilities = brush.sculpt_capabilities
        sculpt_tool = brush.sculpt_tool
        col = row.column(align=True)
        col.ui_units_x = 4
        col.scale_y = 0.7
        col.prop(brush, "use_automasking_topology", text="Topology", toggle=True)
        col.prop(brush, "use_frontface", text="FrontFaces", toggle=True)
        col = row.column(align=True)
        col.ui_units_x = 4
        col.scale_y = 0.7       
        col.prop(brush, "use_automasking_face_sets", text="Face Sets", toggle=True)
        sub = col.row(align=True)
        split = sub.split(factor=0.4, align=True)
        split.prop(brush, "use_automasking_boundary_face_sets", text="STP", toggle=True)
        split.prop(brush, "automasking_boundary_edges_propagation_steps", text="",)
        col = row.column()
        col.ui_units_x = 4
        col.scale_y = 0.7 
        col.prop(brush, "use_automasking_boundary_edges", text="Boundary", toggle=True)






def BrushCopy(self, context, parent):
    layout = parent
    brush = context.tool_settings.sculpt.brush
    settings = context.tool_settings.sculpt

    col = parent.column(align=True)     
    col.ui_units_x = 2
    col.ui_units_y = 1
    row1= col.row()
    #row1.scale_y = 0.16
    
    row1.template_ID_preview(settings, "brush", rows=1, cols=4, hide_buttons=True )
    #row1.template_ID(settings, "brush", new="brush.add")
    '''
    row2= col.row()
    row2.menu("VIEW3D_MT_brush_context_menu", icon='DOWNARROW_HLT', text="")

    if brush is not None:
        row2.prop(brush, "use_custom_icon", toggle=True, icon='FILE_IMAGE', text="")

        if brush.use_custom_icon:
            row2.prop(brush, "icon_filepath", text="")
    '''
#bpy.ops.brush.reset()

def Color(self, context, parent):
    layout = parent
    ts = context.tool_settings
    ups = ts.unified_paint_settings
    ptr = ups if ups.use_unified_color else ts.image_paint.brush    
    
    col = parent.column()
    col.scale_y = 0.7 
    col.ui_units_x = 4
    col.template_color_picker(ptr, 'color', value_slider=True)
    colsub = col.row(align=True)
    colsub.prop(ptr, 'color', text="")
    colsub.prop(ptr, 'secondary_color', text="")



def ViewCam(self, context, parent):
    layout = parent

    row = parent.row(align=True)     
    row.ui_units_x = 4.2
    funct_bt(parent=row, cmd='viewcam', tog=True, w=3, h=1.2, label='VIEW CAM', icon="NONE")
    funct_bt(parent=row, cmd='lockcam', tog=True, w=1.2, h=1.2, label='', icon="LOCKED")
    funct_bt(parent=parent, cmd='setactive', tog=False, w=2, h=0.8, label='SET ACTIVE', icon="NONE")  


def TopoRake(self, context, parent):
    layout = parent
    brush = context.tool_settings.sculpt.brush
    settings = context.tool_settings.sculpt
    capabilities = brush.sculpt_capabilities
    sculpt_tool = brush.sculpt_tool

    col = layout.column()
    col.ui_units_x = 5
    col.scale_y = 0.7
    if bpy.context.mode == 'SCULPT': 
        if (capabilities.has_topology_rake and context.sculpt_object.use_dynamic_topology_sculpting):
            col.prop(brush, "topology_rake_factor", slider=True, text='RAKE')
    else:
        col.label(text='')

def SculptBrushSettings(self, context, parent):
    layout = parent
    brush = context.tool_settings.sculpt.brush
    settings = context.tool_settings.sculpt
    capabilities = brush.sculpt_capabilities
    sculpt_tool = brush.sculpt_tool

    row = layout.row()
    row.alignment = 'CENTER'

    col = row.column()
    col.ui_units_x = 5
    col.scale_y = 0.7
    col.prop(brush, "normal_radius_factor", slider=True, text='NORM')
    col.prop(brush, "hardness", slider=True, text='HARD')

    col = row.column()
    col.ui_units_x = 5
    col.scale_y = 0.7
    if sculpt_tool == 'MASK':
        sub = col.row()
        sub.prop(brush, "mask_tool", expand=True)
    else:
        col.prop(brush, "auto_smooth_factor", slider=True, text='SMTH')
    if sculpt_tool == 'CLAY_STRIPS':
        col.prop(brush, "tip_roundness", slider=True, text='ROUND')
    elif sculpt_tool == 'LAYER':
        col.prop(brush, "height", slider=True, text='HEIGHT')
    elif sculpt_tool == 'CREASE':
        col.prop(brush, "crease_pinch_factor", slider=True, text='PINCH')
    elif sculpt_tool == 'SCRAPE':
        col.prop(brush, "area_radius_factor", slider=True, text='AREA')
    elif sculpt_tool == 'FILL':
        col.prop(brush, "area_radius_factor", slider=True, text='AREA')
    elif sculpt_tool == 'MULTIPLANE_SCRAPE':
        col.prop(brush, "multiplane_scrape_angle", slider=True, text='ANGLE')
    elif sculpt_tool == 'POSE':
        col.prop(brush, "pose_ik_segments", slider=True, text='IK')


    col = row.column()
    col.ui_units_x = 5
    col.scale_y = 0.7
    col.active = capabilities.has_plane_offset
    col.prop(brush, "plane_offset", slider=True, text='OFFSET')
    sub = col.row(align = True)
    sub.prop(brush, "use_plane_trim", slider=False, toggle=True, text='TRIM')
    sub.prop(brush, "plane_trim", slider=True)

    col = row.column()
    col.ui_units_x = 3
    col.scale_y = 0.7
    col.label(text='')
    sub = col.column()
    sub.active = capabilities.has_accumulate
    sub.prop(brush, "use_accumulate", text="ACCU", toggle=True)


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
        box.ui_units_x = 8
        box.operator("sculpt.symmetrize")
        box.prop(sculpt, "symmetrize_direction")
        box.label(text="RadialSym")
        row = box.row(align=True)
        row.scale_y = 0.7
        row.prop(sculpt, "radial_symmetry", text="")

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
        subrow1.operator('xmenu.detailsize', text='2').size=2
        subrow1.operator('xmenu.detailsize', text='4').size=4
        subrow1.operator('xmenu.detailsize', text='8').size=8
        subrow1.operator('xmenu.detailsize', text='16').size=16

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



classes = (VIEW3D_MT_dynamesh, VIEW3D_MT_remesh, VIEW3D_MT_sculpt_sym, VIEW3D_MT_sym)

def register():
    for cls in classes:
        bpy.utils.register_class(cls)
    
def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)