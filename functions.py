import bpy
import os
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
from mathutils import Vector

#////////////////////////////////////////////////////////////////////////////////////////////#

def tool_bt(parent, cmd ,w=1, h=1, text=False, icon="NONE"):
    update_toolset()
    tool_op(parent=parent, cmd=cmd, w=w, h=h, text=text, icon=icon)

def tool_grid(parent, col, align, slotmin, slotmax, h=1, w=1, text=False, icon="NONE"):   
    grid = parent.grid_flow(columns=col, align=align)
    update_toolset()
    for i in range(slotmin,slotmax):
        col = grid.column()
        tool_op(parent=col, cmd=i, w=w, h=h, text=text, icon=icon)

def tool_op(parent, cmd ,w=1, h=1, small=False, text=False, icon="NONE"):    
    tool_icon = bpy.context.preferences.addons['XMENU'].preferences.tool_icon
    tool_text = bpy.context.preferences.addons['XMENU'].preferences.tool_text  
    icons = load_icons()

    col = parent.column(align=True)
    col.ui_units_x = w
    col.scale_y = h

    if tool_icon == True:
        icon = icon
    else: 
        icon = 'OFF'
    
    if icon == 'LARGE' or icon =='CUSTOM' or icon =='OFF':
        if icon == 'LARGE':
            # using icons from toolpanel
            icon_id = ToolSelectPanelHelper._icon_value_from_icon_handle(Tools_Sculpt[cmd][3])
            toollabel = ' '
        if icon == 'CUSTOM':
            # using custom icons            
            ds = icons.get(Tools_Sculpt[cmd][4])
            if ds != None:
                icon_id = ds.icon_id
            else:
                icon_id = 0
            toollabel = ' '
        if icon == 'OFF':
            icon_id = 0
            toollabel = Tools_Sculpt[cmd][0]

        col.operator('xmenu.settool', text=toollabel, depress=bpy.types.WindowManager.tool_state[cmd], icon_value=icon_id).tool_index = cmd

    if icon != 'LARGE' and icon !='CUSTOM' and icon !='OFF':
        # using small icons
        icon_id = icon
        toollabel = ' '
        col.operator('xmenu.settool', text=toollabel, depress=bpy.types.WindowManager.tool_state[cmd], icon=icon_id).tool_index = cmd

    if text == True:
        if tool_text == True:
            subcol = col.column()
            subcol.scale_y = 0.6
            subcol.label(text=Tools_Sculpt[cmd][0])

class SetTool(bpy.types.Operator):
    bl_idname = "xmenu.settool"
    bl_label = "SETTOOL"

    tool_index: bpy.props.IntProperty()

    def execute(self, context):
        area = [area for area in bpy.context.screen.areas if area.type == "VIEW_3D"][0]
        
        override_context = bpy.context.copy()
        override_context['window'] = bpy.context.window
        override_context['screen'] = bpy.context.screen
        override_context['area'] = area
        override_context['region'] = area.regions[-1]
        override_context['scene'] = bpy.context.scene
        override_context['space_data'] = area.spaces.active
        
        Tool = Tools_Sculpt[self.tool_index][1]
        Brush = Tools_Sculpt[self.tool_index][2]

        if Brush == '':
            bpy.ops.wm.tool_set_by_id(override_context, name=Tool)
        else:
            bpy.ops.wm.tool_set_by_id(override_context, name=Tool)
            context.tool_settings.sculpt.brush = bpy.data.brushes[Brush]
        
        return {'FINISHED'}

def update_toolset(): 
    list = Tools_Sculpt
    NTools = len(list)
    bpy.types.WindowManager.tool_state = [False for i in range(NTools)]

    tool = bpy.context.workspace.tools.from_space_view3d_mode(bpy.context.mode)    
    toolid = str(tool.idname)
    brushname = bpy.context.tool_settings.sculpt.brush

    for i in range(NTools):
        if Tools_Sculpt[i][2] == '' and toolid == Tools_Sculpt[i][1]:
            bpy.types.WindowManager.tool_state[i] = True

        elif Tools_Sculpt[i][2] != '' and brushname == bpy.data.brushes[Tools_Sculpt[i][2]]:
            bpy.types.WindowManager.tool_state[i] = True

        else:
            bpy.types.WindowManager.tool_state[i] = False

def funct_bt(parent, cmd='cmd', tog=False, w=1, h=1, label='', icon="NONE"):    
    tool_icon = bpy.context.preferences.addons['XMENU'].preferences.tool_icon

    col = parent.column(align=True)
    col.ui_units_x = w
    col.scale_y = h

    if tool_icon == True:
        # using small icons
        icon_id = icon
        label = label 
    else: 
        label = label 
    
    op = 'xmenu.'
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

class Detailsize(bpy.types.Operator):
    bl_idname = "xmenu.detailsize"
    bl_label = ""

    #bpy.types.WindowManager.detailsize_state = bpy.props.BoolProperty(default = False)

    size: bpy.props.FloatProperty()

    def execute(self, context):
        context.scene.tool_settings.sculpt.detail_size = self.size

        return {'FINISHED'}

class Wire(bpy.types.Operator):
    bl_idname = "xmenu.wire"
    bl_label = "Wireframe"

    bpy.types.WindowManager.wire_state = bpy.props.BoolProperty(default = False)   

    def execute(self, context):
        for area in bpy.context.workspace.screens[0].areas:
            for space in area.spaces:
                if space.type == 'VIEW_3D':
                    space.overlay.show_wireframes = not space.overlay.show_wireframes
                    bpy.types.WindowManager.overlay_state = space.overlay.show_wireframes
        return {'FINISHED'}

class XRay(bpy.types.Operator):
    bl_idname = "xmenu.xray"
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

class Persp(bpy.types.Operator):
    bl_idname = "xmenu.persp"
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
    bl_idname = "xmenu.viewcam"
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
    bl_idname = "xmenu.lockcam"
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
    bl_idname = "xmenu.frames"
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
    bl_idname = "xmenu.framea"
    bl_label = "ALL"        
    def execute(self, context):
        for window in bpy.context.window_manager.windows:
            screen = window.screen
            for area in bpy.context.screen.areas:
                if area.type == 'VIEW_3D':
                    ctx = bpy.context.copy()
                    ctx['area'] = area
                    ctx['region'] = area.regions[-1]
                    bpy.ops.view3d.view_all(ctx)
                    break
        return {'FINISHED'} 

class SetActive(bpy.types.Operator):
    bl_idname = "xmenu.setactive"
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

class Mask(bpy.types.Operator):
    bl_idname = "xmenu.mask"
    bl_label = ""
    cmd: bpy.props.StringProperty()

    def execute(self, context):
        if self.cmd == 'FILL':
            bpy.ops.paint.mask_flood_fill(mode='VALUE', value=1)
        elif self.cmd == 'CLEAR':
            bpy.ops.paint.mask_flood_fill(mode='VALUE', value=0)
        elif self.cmd == "INVERT":
            bpy.ops.paint.mask_flood_fill(mode='INVERT')
        elif self.cmd == "SHRINK":
            bpy.ops.sculpt.mask_filter(filter_type='SHRINK', auto_iteration_count=True)
        elif self.cmd == "GROW":
            bpy.ops.sculpt.mask_filter(filter_type='GROW', auto_iteration_count=True)
        elif self.cmd == "SHARPEN":
            bpy.ops.sculpt.mask_filter(filter_type='SHARPEN', auto_iteration_count=True)
        elif self.cmd == "SMOOTH":
            bpy.ops.sculpt.mask_filter(filter_type='SMOOTH', auto_iteration_count=True)
        return {'FINISHED'}

#////////////////////////////////////////////////////////////////////////////////////////////#

#////////////////////////////////////////////////////////////////////////////////////////////#
def clear_brush_textures():
    for brush in bpy.data.brushes:
        if "xm" in brush:
            brush.texture = None
            brush.texture = None

def setup_brush_tex(img_path,tex_type="BRUSH"):
    if tex_type == "BRUSH":
        if "xm_brush_img" not in bpy.data.images:
            brush_img = bpy.data.images.new("xm_brush_img",1024,1024)
            if brush_img.packed_file != None:
                brush_img.unpack()
            brush_img.filepath = img_path
            brush_img.source = "FILE"
        else:
            brush_img = bpy.data.images["xm_brush_img"]
            if brush_img.packed_file != None:
                brush_img.unpack()
            brush_img.filepath = img_path
            brush_img.source = "FILE"
        
        if "xm_brush_tex" not in bpy.data.textures:
            brush_tex = bpy.data.textures.new("xm_brush_tex",type="IMAGE")
        else:
            brush_tex = bpy.data.textures["xm_brush_tex"]
        brush_tex.xm_invert_mask = brush_tex.xm_invert_mask
    elif tex_type == "STENCIL":
        if "xm_stencil_img" not in bpy.data.images:
            brush_img = bpy.data.images.new("xm_stencil_img",1024,1024)
            if brush_img.packed_file != None:
                brush_img.unpack()
            brush_img.filepath = img_path
            brush_img.source = "FILE"
        else:
            brush_img = bpy.data.images["xm_stencil_img"]
            if brush_img.packed_file != None:
                brush_img.unpack()
            brush_img.filepath = img_path
            brush_img.source = "FILE"

        if "xm_stencil_tex" not in bpy.data.textures:
            brush_tex = bpy.data.textures.new("xm_stencil_tex",type="IMAGE")
        else:
            brush_tex = bpy.data.textures["xm_stencil_tex"]
        brush_tex.xm_invert_mask = brush_tex.xm_invert_mask
    
    brush_tex.use_nodes = True
    node_tree = brush_tex.node_tree
    
    if "Image" not in node_tree.nodes:    
        image_node = node_tree.nodes.new('TextureNodeImage')    
    else:
        image_node = node_tree.nodes['Image']
    image_node.location = [0,0]
    image_node.image = brush_img
    
    if "ColorRamp" not in node_tree.nodes:    
        ramp_node = node_tree.nodes.new('TextureNodeValToRGB')
        
    else:
        ramp_node = node_tree.nodes['ColorRamp']
        
    if "invert_color" not in ramp_node:
        ramp_node["invert_color"] = False    
        
    ramp_node.location = [200,0]
    if tex_type == "BRUSH":
        if brush_tex.xm_invert_mask:
            ramp_node.color_ramp.elements[0].color = [1,1,1,0]
            ramp_node.color_ramp.elements[1].color = [1,1,1,1]
        else:    
            ramp_node.color_ramp.elements[0].color = [1,1,1,1]
            ramp_node.color_ramp.elements[1].color = [1,1,1,0]
    else:
        if brush_tex.xm_invert_stencil_mask:
            ramp_node.color_ramp.elements[0].color = [1,1,1,1]
            ramp_node.color_ramp.elements[1].color = [0,0,0,1]
        else:    
            ramp_node.color_ramp.elements[0].color = [0,0,0,1]
            ramp_node.color_ramp.elements[1].color = [1,1,1,1]
                
    
    if "Output" not in node_tree.nodes:
        output_node = node_tree.nodes.new('TextureNodeOutput')
    else:
        output_node = node_tree.nodes['Output']
    output_node.location = [500,0]
    
    node_tree.links.new(ramp_node.inputs['Fac'],image_node.outputs['Image'])
    node_tree.links.new(output_node.inputs['Color'],ramp_node.outputs['Color'])   
    
    return brush_tex

#////////////////////////////////////////////////////////////////////////////////////////////#
def _invert_ramp(self,context,tex_type="BRUSH"):
    if ("xm_brush_tex" in bpy.data.textures and tex_type == "BRUSH") or ("xm_stencil_tex" in bpy.data.textures and tex_type == "STENCIL"):
        
        if tex_type == "BRUSH":
            node_tree = bpy.data.textures["xm_brush_tex"].node_tree
            tmp_color_01 = Vector((1,1,1,1))
            tmp_color_02 = Vector((1,1,1,0))
        elif tex_type == "STENCIL":
            node_tree = bpy.data.textures["xm_stencil_tex"].node_tree
            tmp_color_01 = Vector((1,1,1,1))
            tmp_color_02 = Vector((0,0,0,1))
        
        if node_tree != None:
            ramp_node = node_tree.nodes["ColorRamp"]
            
            if tex_type == "BRUSH":      
                if self.xm_invert_mask:
                    ramp_node.color_ramp.elements[0].color = tmp_color_01
                    ramp_node.color_ramp.elements[1].color = tmp_color_02
                else:
                    ramp_node.color_ramp.elements[0].color = tmp_color_02
                    ramp_node.color_ramp.elements[1].color = tmp_color_01    
            elif tex_type == "STENCIL":
                if self.xm_invert_stencil_mask:
                    ramp_node.color_ramp.elements[0].color = tmp_color_01
                    ramp_node.color_ramp.elements[1].color = tmp_color_02
                else:
                    ramp_node.color_ramp.elements[0].color = tmp_color_02
                    ramp_node.color_ramp.elements[1].color = tmp_color_01   

def _tonemap(self,context,tex_type="BRUSH"):
    
    if (tex_type == "BRUSH" and "xm_brush_tex" in bpy.data.textures) or (tex_type == "STENCIL" and "xm_stencil_tex" in bpy.data.textures):
        if tex_type == "BRUSH":
            node_tree = bpy.data.textures["xm_brush_tex"].node_tree
            if node_tree != None:
                ramp_node = node_tree.nodes["ColorRamp"]
                ramp_node.color_ramp.elements[0].position = context.tool_settings.image_paint.brush.xm_ramp_tonemap_l
                ramp_node.color_ramp.elements[1].position = context.tool_settings.image_paint.brush.xm_ramp_tonemap_r
        elif tex_type == "STENCIL":
            node_tree = bpy.data.textures["xm_stencil_tex"].node_tree
            if node_tree != None:
                ramp_node = node_tree.nodes["ColorRamp"]
                ramp_node.color_ramp.elements[0].position = context.tool_settings.image_paint.brush.xm_stencil_ramp_tonemap_l
                ramp_node.color_ramp.elements[1].position = context.tool_settings.image_paint.brush.xm_stencil_ramp_tonemap_r

def _mute_ramp(self,context):    
    if "xm_brush_tex" in bpy.data.textures: 
        node_tree = bpy.data.textures["xm_brush_tex"].node_tree
        ramp_node = node_tree.nodes["ColorRamp"]
        if self.xm_use_mask == True:
            ramp_node.mute = False
        else: 
            ramp_node.mute = True
        #ramp_node.mute = not(self.xm_use_mask)
        #bpy.data.textures["xm_brush_tex"].use_color_ramp
    brush = context.tool_settings.image_paint.brush
    if brush != None:    
        brush.xm_brush_texture = brush.xm_brush_texture



#////////////////////////////////////////////////////////////////////////////////////////////#

classes = (XRay, ViewCam, FrameS, FrameA, Persp, LockCam, SetTool, Wire, SetActive, Detailsize, Mask)

def register():
    for cls in classes:
        bpy.utils.register_class(cls)
    
def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)