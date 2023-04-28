import bpy
import os
from mathutils import Vector, Matrix
from bpy.types import Operator, AddonPreferences
from bpy.props import StringProperty, BoolProperty, FloatProperty, IntProperty, EnumProperty

from bl_ui.space_toolsystem_common import ToolSelectPanelHelper
from bpy_extras.object_utils import AddObjectHelper, object_data_add

from .toolsets import toolset

from .icons import get_icon_id
import gpu
import numpy as np

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
    tool_text = bpy.context.preferences.addons[__package__].preferences.tool_text
    Tools = toolset()
    update_toolset()
    col = layout.column(align=True)
    col.ui_units_x = w
    col.scale_y = h

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


'''
override_context = bpy.context.copy() 
area = [area for area in bpy.context.screen.areas if area.type == "NODE_EDITOR"][-1]
override_context['window'] = bpy.context.window
override_context['screen'] = bpy.context.screen
override_context['area'] = area
override_context['region'] = area.regions[-1]
override_context['scene'] = bpy.context.scene


areas = [area for area in bpy.context.screen.areas if area.type == "NODE_EDITOR"]


for area in areas:
    bpy.ops.screen.area_close(override_context)

'''

class SetTool(bpy.types.Operator):
    bl_idname = "xm.settool"
    bl_label = "SETTOOL"
    bl_options = {'REGISTER'}
    tool_index: bpy.props.IntProperty()
    def execute(self, context):
        Tools = toolset()
        Tool = Tools[self.tool_index][1]
        Brush = Tools[self.tool_index][2]
        update_toolset()
        scene = bpy.context.scene
        ob = context.active_object
        mode = context.active_object.mode

        window = bpy.context.window_manager.windows[0]
        area = [area for area in window.screen.areas if area.type == "VIEW_3D"][0]

        if Brush == '':
            with context.temp_override(window=window, area=area, object=ob):
                bpy.ops.wm.tool_set_by_id(name=Tool)
        else:
            with context.temp_override(window=window, area=area, object=ob):
                bpy.ops.wm.tool_set_by_id(name=Tool)
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
        if mode != 'PAINT_GPENCIL':
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
    col = layout.column(align=True)
    col.ui_units_x = w
    col.scale_y = h

    icon_id = icon
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
class ColorPicker(bpy.types.Operator):
    bl_idname = "xm.colorpicker"
    bl_label = "Sample Color"
    bl_description = 'Color Picker'

    length: bpy.props.IntProperty()
    bpy.types.WindowManager.picker_median = bpy.props.FloatVectorProperty(default=(0.5, 0.5, 0.5),precision=4)

    def modal(self, context, event):
        context.area.tag_redraw()
        wm = context.window_manager
        mode = bpy.context.active_object.mode

        if event.type in {'MOUSEMOVE', 'LEFTMOUSE'}:
            distance = self.length // 2

            start_x = max(event.mouse_x - distance, 0)
            start_y = max(event.mouse_y - distance, 0)

            fb = gpu.state.active_framebuffer_get()
            screen_buffer = fb.read_color(start_x, start_y, self.length, self.length, 3, 0, 'FLOAT')

            channels = np.array(screen_buffer.to_list())\
                .reshape((self.length * self.length, 3))

            dot = np.sum(channels, axis=1)
            max_ind = np.argmax(dot, axis=0)
            min_ind = np.argmin(dot, axis=0)

            wm.picker_median = tuple(np.median(channels, axis=0))

            if mode == 'TEXTURE_PAINT':
                brush = bpy.context.tool_settings.image_paint.brush
            if mode == 'SCULPT':
                brush = bpy.context.tool_settings.sculpt.brush
            if mode == 'VERTEX_PAINT':
                brush = bpy.context.tool_settings.vertex_paint.brush
            if mode == 'WEIGHT_PAINT':
                brush = bpy.context.tool_settings.weight_paint.brush
            if mode == 'PAINT_GPENCIL':
                brush = bpy.context.tool_settings.gpencil_paint.brush

            brush.color = wm.picker_median

        if event.type == 'LEFTMOUSE':
            context.window.cursor_modal_restore()
            return {'FINISHED'}

        elif event.type in {'RIGHTMOUSE', 'ESC'}:

            wm.picker_median = self.prev_median

            context.window.cursor_modal_restore()
            return {'CANCELLED'}

        return {'RUNNING_MODAL'}

    def invoke(self, context, event):
        wm = context.window_manager

        self.prev_median = (wm.picker_median[0], wm.picker_median[1], wm.picker_median[2])

        context.window_manager.modal_handler_add(self)
        context.window.cursor_modal_set('EYEDROPPER')
        return {'RUNNING_MODAL'}

class Floor(bpy.types.Operator):
    bl_idname = "xm.floor"
    bl_label = "Floor"

    def execute(self, context):
        for ob in context.selected_objects:
            origin_to_bottom(ob)
        return {'FINISHED'}

def origin_to_bottom(ob, matrix=Matrix()):
    me = ob.data
    mw = ob.matrix_world
    local_verts = [matrix @ Vector(v[:]) for v in ob.bound_box]
    o = sum(local_verts, Vector()) / 8
    o.z = min(v.z for v in local_verts)
    o = matrix.inverted() @ o
    me.transform(Matrix.Translation(-o))
    mw.translation = mw @ o

class ViewClip(bpy.types.Operator):
    bl_idname = "xm.viewclip"
    bl_label = "NORMALS"
    scale: bpy.props.FloatProperty()
    bpy.types.WindowManager.viewclip_state = bpy.props.BoolProperty(default = False)
    def execute(self, context):
        view = context.space_data
        active_cam = bpy.context.scene.camera
        if bpy.types.WindowManager.viewclip_state == False:
            context.space_data.clip_start = context.space_data.clip_start * self.scale
            context.space_data.clip_end = context.space_data.clip_end * self.scale
            bpy.types.WindowManager.viewclip_state = True
        else:
            context.space_data.clip_start = context.space_data.clip_start / self.scale
            context.space_data.clip_end = context.space_data.clip_end / self.scale
            bpy.types.WindowManager.viewclip_state = False
        return {'FINISHED'}



class ClearScreens(bpy.types.Operator):
    bl_idname = "xm.clearscreens"
    bl_label = ""
    def execute(self, context):
        for scr in bpy.data.screens:
            if "temp." in scr.name:
                scr.user_clear()
        #bpy.ops.outliner.orphans_purge(do_local_ids=True, do_linked_ids=True, do_recursive=False)
        return {'FINISHED'}


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
                        polygons.use_smooth = not polygons.use_smooth
        return {'FINISHED'}

class Detailsize(bpy.types.Operator):
    bl_idname = "xm.detailsize"
    bl_label = ""
    size: bpy.props.FloatProperty()
    def execute(self, context):
        context.scene.tool_settings.sculpt.detail_size = self.size
        return {'FINISHED'}

class Dyna(bpy.types.Operator):
    bl_idname = "xm.dyna"
    bl_label = "DYNA"
    bpy.types.WindowManager.dyna_state = bpy.props.BoolProperty(default = False)        
    def execute(self, context):
        for window in bpy.context.window_manager.windows:
            screen = window.screen
            for area in screen.areas:
                if area.type == 'VIEW_3D':
                    obj = context.object
                    bpy.ops.sculpt.dynamic_topology_toggle()
                    bpy.types.WindowManager.dyna_state = obj.use_dynamic_topology_sculpting
                    break
        return {'FINISHED'} 

class Voxelsize(bpy.types.Operator):
    bl_idname = "xm.voxelsize"
    bl_label = ""
    size: bpy.props.FloatProperty()
    bpy.types.WindowManager.voxelsize_state = bpy.props.BoolProperty(default = False)
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
   

class NewMat(bpy.types.Operator):
    bl_idname = "xm.newmat"
    bl_label = "NEW MAT"        
    def execute(self, context):
        ob = context.active_object
        for window in bpy.context.window_manager.windows:
            window = bpy.context.window 
            for screen in bpy.data.screens:
                screen = bpy.context.screen
                for area in (a for a in screen.areas if a.type == 'PROPERTIES'):
                    region = next((region for region in area.regions if region.type == 'WINDOW'), None)
                    if region is not None:
                        area = area
        with context.temp_override(area=area, region=region):
            mat = bpy.data.materials.new(name="Mat.001")
            ob.data.materials.append(mat)
            if context.mode == 'PAINT_GPENCIL':
                bpy.data.materials.create_gpencil_data(mat)
        return {'FINISHED'} 


class FrameS(bpy.types.Operator):
    bl_idname = "xm.frames"
    bl_label = "FRAME"        
    def execute(self, context):
        for screen in bpy.data.screens:
            for area in (a for a in screen.areas if a.type == 'VIEW_3D'):
                region = next((region for region in area.regions if region.type == 'WINDOW'), None)
                if region is not None:
                    area = area
        with context.temp_override(area=area, region=region):
            bpy.ops.view3d.view_selected()
        return {'FINISHED'} 
  
class FrameA(bpy.types.Operator):
    bl_idname = "xm.framea"
    bl_label = "ALL"        
    def execute(self, context):
        for screen in bpy.data.screens:
            for area in (a for a in screen.areas if a.type == 'VIEW_3D'):
                region = next((region for region in area.regions if region.type == 'WINDOW'), None)
                if region is not None:
                    area = area
        with context.temp_override(area=area, region=region):
            bpy.ops.view3d.view_all(center=True)
        return {'FINISHED'} 

class LocalView(bpy.types.Operator):
    bl_idname = "xm.localview"
    bl_label = "LocalView"
    bpy.types.WindowManager.localview_state = bpy.props.BoolProperty(default = False)
    def execute(self, context):
        ob = context.active_object
        for screen in bpy.data.screens:
            for area in (a for a in screen.areas if a.type == 'VIEW_3D'):
                region = next((region for region in area.regions if region.type == 'WINDOW'), None)
                if region is not None:
                    area = area
        with context.temp_override(area=area, region=region, object=ob):
            bpy.ops.view3d.localview(frame_selected=False)
        bpy.types.WindowManager.localview_state = not bpy.types.WindowManager.localview_state
        return {'FINISHED'}

class MaxArea(bpy.types.Operator):
    bl_idname = "xm.max_area"
    bl_label = "MaximizeArea"
    bpy.types.WindowManager.max_area_state = bpy.props.BoolProperty(default = False)      
    def execute(self, context):
        bpy.ops.screen.screen_full_area()
        bpy.types.WindowManager.max_area_state = not bpy.types.WindowManager.max_area_state
        return {'FINISHED'}


class SetActive(bpy.types.Operator):
    bl_idname = "xm.setactive"
    bl_label = "SetActiveCam"
    def execute(self, context):
        for screen in bpy.data.screens:
            for area in (a for a in screen.areas if a.type == 'VIEW_3D'):
                region = next((region for region in area.regions if region.type == 'WINDOW'), None)
                if region is not None:
                    area = area

        with context.temp_override(area=area, region=region):
            bpy.ops.view3d.object_as_camera()

        bpy.types.WindowManager.viewcam_state = True

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

        for window in bpy.context.window_manager.windows:
            window = bpy.context.window 
            for screen in bpy.data.screens:
                screen = bpy.context.screen
                for area in (a for a in screen.areas if a.type == 'PROPERTIES'):
                    region = next((region for region in area.regions if region.type == 'WINDOW'), None)
                    if region is not None:
                        area = area

        scene = bpy.context.scene
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

        for window in bpy.context.window_manager.windows:
            window = bpy.context.window 
            for screen in bpy.data.screens:
                screen = bpy.context.screen
                for area in (a for a in screen.areas if a.type == 'PROPERTIES'):
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
        op += keyword2[0]
        op += '='
        op += keyword2[1]
        op += ')'

        for window in bpy.context.window_manager.windows:
            window = bpy.context.window 
            for screen in bpy.data.screens:
                screen = bpy.context.screen
                for area in (a for a in screen.areas if a.type == 'PROPERTIES'):
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

classes = (ColorPicker, Floor, ClearScreens, ViewClip, XRay, ViewCam, Grid, Axis, FrameS, FrameA, NewMat, LocalView, MaxArea, Persp, LockCam, SetTool, Wire, Hide, 
           SetActive, Detailsize, Voxelsize, Dyna, SurfaceDrawMode, FaceOrient, Override, Override1, Override2, NormalShading
          )

def register():

    for cls in classes:
        bpy.utils.register_class(cls)
    bpy.types.WindowManager.localview_state = False
    bpy.types.WindowManager.maxarea_state = False
    bpy.types.WindowManager.grid_state = True
    bpy.types.WindowManager.screen_state = False
    bpy.types.WindowManager.viewclip_state = False

def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)