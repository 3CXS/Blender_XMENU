import bpy
import os
from mathutils import Vector, Matrix
from bpy.types import Operator, AddonPreferences
from bpy.props import StringProperty,BoolProperty,FloatProperty,IntProperty

from bl_ui.space_toolsystem_common import ToolSelectPanelHelper
from bpy_extras.object_utils import AddObjectHelper, object_data_add

from .toolsets import toolset

from .icons import get_icon_id
#-----------------------------------------------------------------------------------------------------------------------

def redraw_regions():
    for area in bpy.context.window.screen.areas:
        #if area.type == 'VIEW_3D':
        for region in area.regions:
            if region.type == 'WINDOW':
                region.tag_redraw()


def get_brush_mode(self, context):
    if context.active_object != None:
        mode = context.active_object.mode

        if mode == 'TEXTURE_PAINT':
            brush = context.tool_settings.image_paint.brush
        elif mode == 'SCULPT':
            brush = context.tool_settings.sculpt.brush
        elif mode == 'VERTEX_PAINT':
            brush = context.tool_settings.vertex_paint.brush
        elif mode == 'WEIGHT_PAINT':
            brush = context.tool_settings.weight_paint.brush
        elif mode == 'PAINT_GPENCIL':
            brush = context.tool_settings.gpencil_paint.brush
        elif mode == 'SCULPT_GPENCIL':
            brush = context.tool_settings.gpencil_paint.brush
        else:
            brush = None

        return brush


def paint_settings(context):
        tool_settings = context.tool_settings
        mode = context.mode

        if mode == 'SCULPT':
            return tool_settings.sculpt
        elif mode == 'PAINT_VERTEX':
            return tool_settings.vertex_paint
        elif mode == 'PAINT_WEIGHT':
            return tool_settings.weight_paint
        elif mode == 'PAINT_TEXTURE':
            return tool_settings.image_paint
        elif mode == 'PARTICLE':
            return tool_settings.particle_edit
        elif mode == 'PAINT_2D':
            return tool_settings.image_paint
        elif mode == 'UV_SCULPT':
            return tool_settings.uv_sculpt
        elif mode == 'PAINT_GPENCIL':
            return tool_settings.gpencil_paint
        elif mode == 'SCULPT_GPENCIL':
            return tool_settings.gpencil_sculpt_paint
        elif mode == 'WEIGHT_GPENCIL':
            return tool_settings.gpencil_weight_paint
        elif mode == 'VERTEX_GPENCIL':
            return tool_settings.gpencil_vertex_paint
        return None


def update_normaldisp(self, context):
    ob = context.active_object
    polygons = ob.data.polygons
    state = ob.data.polygons[0].use_smooth
    return state


def update_local_view(space_data, states):
    if space_data.local_view:
        for obj, local in states:
            obj.local_view_set(space_data, local)


def parent(obj, parentobj):
    if not parentobj.parent and parentobj.matrix_parent_inverse != Matrix():
        print("Resetting %s's parent inverse matrix, as no parent is defined." % (parentobj.name))
        parentobj.matrix_parent_inverse = Matrix()

    p = parentobj
    while p.parent:
        p = p.parent

    obj.parent = parentobj
    obj.matrix_world = p.matrix_parent_inverse @ obj.matrix_world


#TOOL OPERATOR -----------------------------------------------------------------------------------------


def tool_bt(layout, cmd ,w=1, h=1, text=False, icon="NONE"):    
    tool_icon = bpy.context.preferences.addons[__package__].preferences.tool_icon
    tool_text = bpy.context.preferences.addons[__package__].preferences.tool_text  

    Tools = toolset()
    update_toolset()

    col = layout.column(align=True)
    col.ui_units_x = w
    col.scale_y = h

    if tool_icon == True:
        icon = icon
    else: 
        icon = 'OFF'
    
    if icon == 'LARGE' or icon =='CUSTOM' or icon =='OFF':

        if icon == 'LARGE':
            # using icons from toolpanel
            icon_id = ToolSelectPanelHelper._icon_value_from_icon_handle(Tools[cmd][3])
            toollabel = ' '

        if icon == 'CUSTOM':
            # using custom icons
            c_icon = Tools[cmd][4]

            if c_icon != None:
                icon_id = get_icon_id(c_icon)
            else:
                icon_id = 0
            toollabel = ' '

        if icon == 'OFF':
            icon_id = 0
            toollabel = Tools[cmd][0]

        col.operator('xm.settool', text=toollabel, depress=bpy.types.WindowManager.tool_state[cmd], icon_value=icon_id).tool_index = cmd

    if icon != 'LARGE' and icon !='CUSTOM' and icon !='OFF':
        # using small icons
        icon_id = icon
        toollabel = ' '
        col.operator('xm.settool', text=toollabel, depress=bpy.types.WindowManager.tool_state[cmd], icon=icon_id).tool_index = cmd

    if text == True:
        if tool_text == True:
            subcol = col.column()
            subcol.scale_y = 0.6
            subcol.label(text=Tools[cmd][0])

class SetTool(bpy.types.Operator):
    bl_idname = "xm.settool"
    bl_label = "SETTOOL"
    bl_options = {'REGISTER'}

    tool_index: bpy.props.IntProperty()

    def execute(self, context):

        Tools = toolset()
        Tool = Tools[self.tool_index][1]
        Brush = Tools[self.tool_index][2]

        for screen in bpy.data.screens:
            for area in (a for a in screen.areas if a.type == 'VIEW_3D'):
                region = next((region for region in area.regions if region.type == 'WINDOW'), None)
                if region is not None:
                    area = area

        window = bpy.context.window
        screen =  bpy.context.screen
        region = area.regions[-1]
        scene = bpy.context.scene
        space_data = area.spaces.active
        ob = context.active_object

        if Brush == '':
            with context.temp_override(area=area, region=region, object=ob):
                bpy.ops.wm.tool_set_by_id(name=Tool)

        else:
            with context.temp_override(area=area, region=region, object=ob):
                bpy.ops.wm.tool_set_by_id(name=Tool)

            mode = context.active_object.mode
            if mode == 'TEXTURE_PAINT':
                context.tool_settings.image_paint.brush = bpy.data.brushes[Brush]
            if mode == 'SCULPT':
                context.tool_settings.sculpt.brush = bpy.data.brushes[Brush]
            if mode == 'VERTEX_PAINT':
                context.tool_settings.vertex_paint.brush = bpy.data.brushes[Brush]
            if mode == 'WEIGHT_PAINT':
                context.tool_settings.weight_paint.brush = bpy.data.brushes[Brush]
            if mode == 'PAINT_GPENCIL':
                context.tool_settings.gpencil_paint.brush = bpy.data.brushes[Brush]


        brush = get_brush_mode(self, context)

        if brush != None:
            brush.xm_brush_texture = brush.xm_brush_texture

        return {'FINISHED'}

def update_toolset(): 
    Tools = toolset()
    list = Tools
    NTools = len(list)
    bpy.types.WindowManager.tool_state = [False for i in range(NTools)]

    tool = bpy.context.workspace.tools.from_space_view3d_mode(bpy.context.mode)    
    toolid = str(tool.idname)
    if bpy.context.active_object != None:
        mode = bpy.context.active_object.mode
        if mode == 'TEXTURE_PAINT':
            brushname = bpy.context.tool_settings.image_paint.brush
        if mode == 'SCULPT':
            brushname = bpy.context.tool_settings.sculpt.brush
        if mode == 'VERTEX_PAINT':
            brushname = bpy.context.tool_settings.vertex_paint.brush
        if mode == 'WEIGHT_PAINT':
            brushname = bpy.context.tool_settings.weight_paint.brush
        if mode == 'PAINT_GPENCIL':
            brushname = bpy.context.tool_settings.gpencil_paint.brush

    for i in range(NTools):
        if Tools[i][2] == '' and toolid == Tools[i][1]:
            bpy.types.WindowManager.tool_state[i] = True

        elif Tools[i][2] != '' and brushname == bpy.data.brushes[Tools[i][2]]:
            bpy.types.WindowManager.tool_state[i] = True

        else:
            bpy.types.WindowManager.tool_state[i] = False


def funct_bt(layout, cmd='cmd', tog=False, w=1, h=1, label='', icon="NONE"):    
    tool_icon = bpy.context.preferences.addons[__package__].preferences.tool_icon

    col = layout.column(align=True)
    col.ui_units_x = w
    col.scale_y = h

    if tool_icon == True:
        # using small icons
        icon_id = icon
        label = label 
    else:
        icon_id = 'NONE'
        label = label 
    
    op = 'xm.'
    op += cmd

    dstate = 'bpy.types.WindowManager.'
    dstate += cmd
    dstate += '_state'

    if tog==True:
        if eval(dstate) == True:
            state = True
        else:
            state = False
        col.operator(op, depress=state, text=label, icon=icon_id)
    else:
        col.operator(op, text=label, icon=icon_id)



#OPERATORS -----------------------------------------------------------------------------------------


class NormalShading(bpy.types.Operator):
    bl_idname = "xm.normalshading"
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

class Detailsize(bpy.types.Operator):
    bl_idname = "xm.detailsize"
    bl_label = ""

    size: bpy.props.FloatProperty()

    def execute(self, context):

        context.scene.tool_settings.sculpt.detail_size = self.size

        return {'FINISHED'}

class Voxelsize(bpy.types.Operator):
    bl_idname = "xm.voxelsize"
    bl_label = ""

    size: bpy.props.FloatProperty()

    def execute(self, context):
        mesh = context.active_object.data
        mesh.remesh_voxel_size = self.size
        return {'FINISHED'}

class Hide(bpy.types.Operator):
    bl_idname = "xm.hide"
    bl_label = "TogHide"

    def execute(self, context):
        ob = context.active_object

        if ob.hide_render == True:
            ob.hide_viewport = False
            ob.hide_render = False 
            ob.hide_set(False)  
        else:
            ob.hide_viewport = True
            ob.hide_render = True
            ob.hide_set(True)

        return {'FINISHED'}

class Wire(bpy.types.Operator):
    bl_idname = "xm.wire"
    bl_label = "Wireframe"

    bpy.types.WindowManager.wire_state = bpy.props.BoolProperty(default = False)   

    def execute(self, context):
        for area in bpy.context.workspace.screens[0].areas:
            for space in area.spaces:
                if space.type == 'VIEW_3D':
                    space.overlay.show_wireframes = not space.overlay.show_wireframes
                    bpy.types.WindowManager.wire_state = space.overlay.show_wireframes
        return {'FINISHED'}

class XRay(bpy.types.Operator):
    bl_idname = "xm.xray"
    bl_label = "X-RAY"
    bpy.types.WindowManager.xray_state = bpy.props.BoolProperty(default = False)        
    def execute(self, context):  
        for window in bpy.context.window_manager.windows:
            screen = window.screen
            for area in screen.areas:
                if area.type == 'VIEW_3D':
                    shading = area.spaces.active.shading
                    shading.show_xray = not shading.show_xray
                    bpy.types.WindowManager.xray_state = shading.show_xray
        return {'FINISHED'}

class FaceOrient(bpy.types.Operator):
    bl_idname = "xm.faceorient"
    bl_label = "FaceOrient"

    bpy.types.WindowManager.faceorient_state = bpy.props.BoolProperty(default = False)   

    def execute(self, context):
        for area in bpy.context.workspace.screens[0].areas:
            for space in area.spaces:
                if space.type == 'VIEW_3D':
                    space.overlay.show_face_orientation = not space.overlay.show_face_orientation
                    bpy.types.WindowManager.faceorient_state = space.overlay.show_face_orientation
        return {'FINISHED'}

class Grid(bpy.types.Operator):
    bl_idname = "xm.grid"
    bl_label = "GRID"
   
    bpy.types.WindowManager.grid_state = bpy.props.BoolProperty(default = False)        
    def execute(self, context):
        for window in bpy.context.window_manager.windows:
            screen = window.screen
            for area in screen.areas:
                if area.type == 'VIEW_3D':
                    view = area.spaces.active
                    overlay = view.overlay
                    if overlay.show_floor == False:
                        overlay.show_floor = True
                        overlay.show_ortho_grid = True
                    else:
                        overlay.show_floor = False
                        overlay.show_ortho_grid = False
                    bpy.types.WindowManager.grid_state = overlay.show_floor
                    break
        return {'FINISHED'}

class Axis(bpy.types.Operator):
    bl_idname = "xm.axis"
    bl_label = "AXIS"
   
    bpy.types.WindowManager.axis_state = bpy.props.BoolProperty(default = False)        
    def execute(self, context):
        for window in bpy.context.window_manager.windows:
            screen = window.screen
            for area in screen.areas:
                if area.type == 'VIEW_3D':
                    view = area.spaces.active
                    overlay = view.overlay
                    if overlay.show_axis_x == False:
                        overlay.show_axis_x = True
                        overlay.show_axis_y = True
                        overlay.show_axis_z = False
                    else:
                        overlay.show_axis_x = False
                        overlay.show_axis_y = False
                        overlay.show_axis_z = False
                    bpy.types.WindowManager.axis_state = overlay.show_axis_x
                    break
        return {'FINISHED'}

class Persp(bpy.types.Operator):
    bl_idname = "xm.persp"
    label = "PERSP"
    bl_label = label
    
    bpy.types.WindowManager.persp_state = bpy.props.BoolProperty(default = False)        
    def execute(self, context):
        for window in bpy.context.window_manager.windows:
            screen = window.screen
            for area in screen.areas:
                if area.type == 'VIEW_3D':
                    space = area.spaces.active
                    if space.region_3d.view_perspective == 'PERSP':
                        space.region_3d.view_perspective = 'ORTHO'
                        bpy.types.WindowManager.persp_state = 0
                        label = "ORTO"
                    else:
                        space.region_3d.view_perspective = 'PERSP'
                        bpy.types.WindowManager.persp_state = 1
                        label = "PERSP"
                    #ct.persp_state = space.region_3d.view_perspective
                    break
        return {'FINISHED'} 
     
class ViewCam(bpy.types.Operator):
    bl_idname = "xm.viewcam"
    bl_label = "ACTIVE CAM" 

    bpy.types.WindowManager.viewcam_state = bpy.props.BoolProperty(default = False)        
    def execute(self, context):
        for window in bpy.context.window_manager.windows:
            screen = window.screen
            for area in screen.areas:
                if area.type == 'VIEW_3D':
                    space = area.spaces.active
                    if space.region_3d.view_perspective == 'CAMERA':
                        if bpy.types.WindowManager.persp_state == 0:
                            space.region_3d.view_perspective = 'ORTHO'
                        else:
                            space.region_3d.view_perspective = 'PERSP'
                        bpy.types.WindowManager.viewcam_state = 0
                    else:
                        space.region_3d.view_perspective = 'CAMERA'
                        bpy.types.WindowManager.viewcam_state = 1 
                    break
        return {'FINISHED'}  

class LockCam(bpy.types.Operator):
    bl_idname = "xm.lockcam"
    bl_label = "LOCK"
    bpy.types.WindowManager.lockcam_state = bpy.props.BoolProperty(default = False)        
    def execute(self, context):
        for window in bpy.context.window_manager.windows:
            screen = window.screen
            for area in screen.areas:
                if area.type == 'VIEW_3D':
                    space = area.spaces.active
                    if space.lock_camera == False:
                        space.lock_camera = True
                    else:
                        space.lock_camera = False
                    bpy.types.WindowManager.lockcam_state = space.lock_camera
                    break
        return {'FINISHED'}   
   
class FrameS(bpy.types.Operator):
    bl_idname = "xm.frames"
    bl_label = "FRAME"        
    def execute(self, context):
        for window in bpy.context.window_manager.windows:
            screen = window.screen
            for area in bpy.context.screen.areas:
                if area.type == 'VIEW_3D':
                    ctx = bpy.context.copy()
                    ctx['area'] = area
                    ctx['region'] = area.regions[-1]
                    bpy.ops.view3d.view_selected(ctx)
                    break
        return {'FINISHED'} 
    
class FrameA(bpy.types.Operator):
    bl_idname = "xm.framea"
    bl_label = "ALL"        
    def execute(self, context):
        for window in bpy.context.window_manager.windows:
            screen = window.screen
            for area in bpy.context.screen.areas:
                if area.type == 'VIEW_3D':
                    ctx = bpy.context.copy()
                    ctx['area'] = area
                    ctx['region'] = area.regions[-1]
                    bpy.ops.view3d.view_all(ctx, center=True)
                    break
        return {'FINISHED'} 


class LocalView(bpy.types.Operator):
    bl_idname = "xm.localview"
    bl_label = "LocalView"
    bpy.types.WindowManager.localview_state = bpy.props.BoolProperty(default = False)      
    def execute(self, context):
        for window in bpy.context.window_manager.windows:
            screen = window.screen
            for area in bpy.context.screen.areas:
                if area.type == 'VIEW_3D':
                    ctx = bpy.context.copy()
                    ctx['area'] = area
                    ctx['region'] = area.regions[-1]
                    bpy.ops.view3d.localview(ctx)
                    bpy.types.WindowManager.localview_state = not bpy.types.WindowManager.localview_state
                    break
        return {'FINISHED'}

class MaxArea(bpy.types.Operator):
    bl_idname = "xm.max_area"
    bl_label = "MaximizeArea"
    bpy.types.WindowManager.max_area_state = bpy.props.BoolProperty(default = False)      
    def execute(self, context):
        bpy.ops.screen.screen_full_area()
        bpy.types.WindowManager.max_area_state = not bpy.types.WindowManager.max_area_state
        return {'FINISHED'}


class MoveArea(bpy.types.Operator):
    bl_idname = "xm.move_area"
    bl_label = "MoveArea"
    bpy.types.WindowManager.move_area_state = bpy.props.BoolProperty(default = False)      
    def execute(self, context):

        for screen in bpy.data.screens:
            for area in (a for a in screen.areas if a.type == 'VIEW_3D'):
                region = next((region for region in area.regions if region.type == 'WINDOW'), None)
                if region is not None:
                    area = area

        window = bpy.context.window
        screen =  bpy.context.screen
        region = area.regions[-1]
        scene = bpy.context.scene
        space_data = area.spaces.active


        with context.temp_override(area=area, region=region):

            bpy.ops.screen.area_move(x=0, y=0, delta=-100)


        bpy.types.WindowManager.move_area_state = not bpy.types.WindowManager.move_area_state

        return {'FINISHED'}




class SetActive(bpy.types.Operator):
    bl_idname = "xm.setactive"
    bl_label = "SetActiveCam"
    def execute(self, context):
        for window in bpy.context.window_manager.windows:
            screen = window.screen
            for area in bpy.context.screen.areas:
                if area.type == 'VIEW_3D':
                    ctx = bpy.context.copy()
                    ctx['area'] = area
                    ctx['region'] = area.regions[-1]
                    bpy.ops.view3d.object_as_camera(ctx)
                    bpy.types.WindowManager.viewcam_state = True
                    break
        return {'FINISHED'} 


#OVERRIDES -----------------------------------------------------------------------------------------

class Override(bpy.types.Operator):
    bl_idname = "xm.override"
    bl_label = "Operator Override"
    bl_options = {'REGISTER', 'UNDO'}
    cmd: bpy.props.StringProperty()

    def execute(self, context):
        op = 'bpy.ops.'
        op += self.cmd
        op += '()'

        for screen in bpy.data.screens:
            for area in (a for a in screen.areas if a.type == 'VIEW_3D'):
                region = next((region for region in area.regions if region.type == 'WINDOW'), None)
                if region is not None:
                    area = area

        window = bpy.context.window
        screen =  bpy.context.screen
        region = area.regions[-1]
        scene = bpy.context.scene
        space_data = area.spaces.active
        ob = context.active_object

        with context.temp_override(area=area, region=region, object=ob):
            eval(op)
            return {'FINISHED'}

class Override1(bpy.types.Operator):
    bl_idname = "xm.override1"
    bl_label = "Operator Override"

    cmd: bpy.props.StringProperty()
    prop1: bpy.props.StringProperty()

    def execute(self, context):

        prop1 = self.prop1
        keyword1 = prop1.split('=')
        op = 'bpy.ops.'
        op += self.cmd
        op += '('
        op += keyword1[0]
        op += '='
        op += keyword1[1]
        op += ')'

        for screen in bpy.data.screens:
            for area in (a for a in screen.areas if a.type == 'VIEW_3D'):
                region = next((region for region in area.regions if region.type == 'WINDOW'), None)
                if region is not None:
                    area = area

        window = bpy.context.window
        screen =  bpy.context.screen
        region = area.regions[-1]
        scene = bpy.context.scene
        space_data = area.spaces.active
        ob = context.active_object

        with context.temp_override(area=area, region=region, object=ob):
            eval(op)
            return {'FINISHED'}

class Override2(bpy.types.Operator):
    bl_idname = "xm.override2"
    bl_label = "Operator Override"

    cmd: bpy.props.StringProperty()
    prop1: bpy.props.StringProperty()
    prop2: bpy.props.StringProperty()
    def execute(self, context):

        prop1 = self.prop1
        keyword1 = prop1.split('=')
        prop2 = self.prop2
        keyword2 = prop2.split('=')

        op = 'bpy.ops.'
        op += self.cmd
        op += '('
        op += keyword1[0]
        op += '='
        op += keyword1[1]
        op += ','
        op += keyword1[0]
        op += '='
        op += keyword1[1]
        op += ')'

        for screen in bpy.data.screens:
            for area in (a for a in screen.areas if a.type == 'VIEW_3D'):
                region = next((region for region in area.regions if region.type == 'WINDOW'), None)
                if region is not None:
                    area = area

        window = bpy.context.window
        screen =  bpy.context.screen
        region = area.regions[-1]
        scene = bpy.context.scene
        space_data = area.spaces.active
        ob = context.active_object

        with context.temp_override(area=area, region=region, object=ob):
            eval(op)
            return {'FINISHED'}

#MODES -----------------------------------------------------------------------------------------

class SurfaceDrawMode(bpy.types.Operator):
    bl_idname = "xm.surface_draw_mode"
    bl_label = "Surface Draw Mode"
    bl_description = "Surface Draw"
    bl_options = {'REGISTER', 'UNDO'}

    def invoke(self, context, event):
        # forcing object mode at the beginning, avoids issues when calling this tool from PAINT_WEIGHT mode
        bpy.ops.object.mode_set(mode='OBJECT')

        scene = context.scene
        ts = scene.tool_settings
        mcol = context.collection
        view = context.space_data
        active = context.active_object

        existing_gps = [obj for obj in active.children if obj.type == "GPENCIL"]

        if existing_gps:
            gp = existing_gps[0]

        else:
            name = "%s_SurfaceDrawing" % (active.name)
            gp = bpy.data.objects.new(name, bpy.data.grease_pencils.new(name))

            mcol.objects.link(gp)

            gp.matrix_world = active.matrix_world
            parent(gp, active)

        update_local_view(view, [(gp, True)])

        #gp.data.layers.new(name="SurfaceLayer")

        context.view_layer.objects.active = gp
        active.select_set(False)
        gp.select_set(True)
        
        gp.color = (0, 0, 0, 1)

        bpy.ops.object.mode_set(mode='PAINT_GPENCIL')

        ts.gpencil_stroke_placement_view3d = 'SURFACE'
        gp.data.zdepth_offset = 0.01 

        ''' 
        # optionally select the line tool
        if event.shift:
            bpy.ops.wm.tool_set_by_id(name="builtin.line")
        '''
        return {'FINISHED'}


#-----------------------------------------------------------------------------------------------------------------------

classes = (XRay, ViewCam, Grid, Axis, FrameS, FrameA, LocalView, MaxArea, MoveArea, Persp, LockCam, SetTool, Wire, Hide, 
           SetActive, Detailsize, Voxelsize, SurfaceDrawMode, FaceOrient, Override, Override1, Override2, NormalShading
          )

def register():
    for cls in classes:
        bpy.utils.register_class(cls)
    bpy.types.WindowManager.localview_state = False
    bpy.types.WindowManager.maxarea_state = False
    bpy.types.WindowManager.grid_state = True

def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)