import bpy

#/////////////////////////////////////////////////////////////////////////////////////////////////
class XRay(bpy.types.Operator):
    bl_idname = "xmenu.xray"
    bl_label = "X-RAY"
    bpy.types.WindowManager.xray_state = bpy.props.BoolProperty(default = False)        
    def execute(self, context):
        ct = context.window_manager   
        for window in bpy.context.window_manager.windows:
            screen = window.screen
            for area in screen.areas:
                if area.type == 'VIEW_3D':
                    shading = area.spaces.active.shading
                    if shading.show_xray == False:
                        shading.show_xray = True
                    else:
                        shading.show_xray = False  
                    ct.xray_state = shading.show_xray
                    break
        return {'FINISHED'}

class Persp(bpy.types.Operator):
    bl_idname = "xmenu.persp"
    bl_label = "PERSP"
    bpy.types.WindowManager.persp_state = bpy.props.BoolProperty(default = False)        
    def execute(self, context):
        ct = context.window_manager
        for window in bpy.context.window_manager.windows:
            screen = window.screen
            for area in screen.areas:
                if area.type == 'VIEW_3D':
                    space = area.spaces.active
                    if space.region_3d.view_perspective == 'PERSP':
                        space.region_3d.view_perspective = 'ORTHO'
                        ct.persp_state = 0
                    else:
                        space.region_3d.view_perspective = 'PERSP'
                        ct.persp_state = 1 
                    #ct.persp_state = space.region_3d.view_perspective
                    break
        return {'FINISHED'} 
     
class ViewCam(bpy.types.Operator):
    bl_idname = "xmenu.viewcam"
    bl_label = "ACTIVE CAM"  
    bpy.types.WindowManager.viewcam_state = bpy.props.BoolProperty(default = False)        
    def execute(self, context):
        ct = context.window_manager
        for window in bpy.context.window_manager.windows:
            screen = window.screen
            for area in screen.areas:
                if area.type == 'VIEW_3D':
                    space = area.spaces.active
                    if space.region_3d.view_perspective == 'CAMERA':
                        if ct.persp_state == 0:
                            space.region_3d.view_perspective = 'ORTHO'
                        else:
                            space.region_3d.view_perspective = 'PERSP'
                        ct.viewcam_state = 0
                    else:
                        space.region_3d.view_perspective = 'CAMERA'
                        ct.viewcam_state = 1 
                    break
        return {'FINISHED'}  

class LockCam(bpy.types.Operator):
    bl_idname = "xmenu.lockcam"
    bl_label = "Lock"
    bpy.types.WindowManager.lockcam_state = bpy.props.BoolProperty(default = False)        
    def execute(self, context):
        ct = context.window_manager
        for window in bpy.context.window_manager.windows:
            screen = window.screen
            for area in screen.areas:
                if area.type == 'VIEW_3D':
                    space = area.spaces.active
                    if space.lock_camera == False:
                        space.lock_camera = True
                    else:
                        space.lock_camera = False
                    ct.lockcam_state = space.lock_camera
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

    
#///////////////////////////////////////////////////////////////////////////////////////////////////
classes = (XRay, ViewCam, FrameS, FrameA, Persp, LockCam)

def register():
    for cls in classes:
        bpy.utils.register_class(cls)
    
def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)
