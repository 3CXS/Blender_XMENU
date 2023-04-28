import bpy
import os, platform

from mathutils import Vector
import time
from bpy.types import AddonPreferences


#-----------------------------------------------------------------------------------------------------------#
#                                          - CTYPES -                                                       #
#-----------------------------------------------------------------------------------------------------------#

#https://docs.microsoft.com/en-us/windows/win32/api/winuser/

import ctypes 
from ctypes import wintypes
from ctypes import byref
from ctypes import c_char_p

user32 = ctypes.WinDLL('user32', use_last_error=True)

#FLAGS
SWP_NOSIZE      = 0x0001
SWP_NOMOVE      = 0x0002
SWP_NOZORDER    = 0x0004
SWP_SHOWWINDOW  = 0x0040
GWL_EXSTYLE     = -20  
WS_EX_LAYERED   = 0x00080000
LWA_ALPHA       = 0x00000002
SW_RESTORE      = 9
SW_HIDE         = 0

def show_win(FloaterWindow, show=True,):
    user32.ShowWindow(FloaterWindow, SW_RESTORE if show else SW_HIDE)   
    return None

def get_active_win():
    return user32.GetActiveWindow()

def set_win_text(FloaterWindow, text,): 
    user32.SetWindowTextA(FloaterWindow, c_char_p(text.encode('utf-8')))
    return None

def set_win_transforms(FloaterWindow, location=(0,0), size=(500,500)):
    if (size is None) and (location is None):
        return None
    flags  = SWP_SHOWWINDOW
    flags |= SWP_NOZORDER

    if (location is None): 
          X=Y=0
          flags |= SWP_NOMOVE 
    else: X,Y=location[0],location[1]

    if (size is None):
          cx=cy=0
          flags |= SWP_NOSIZE 
    else: cx,cy=size[0],size[1]

    X,Y,cx,cy = int(X),int(Y),int(cx),int(cy)
    user32.SetWindowPos(FloaterWindow,0,X,Y,cx,cy,flags)
    
    return None

def set_win_transparency(FloaterWindow, percentage=50):
    if percentage<10:
        percentage=10
    perc_val = int(255/100*percentage)
    r = user32.GetWindowLongA( FloaterWindow, GWL_EXSTYLE)
    user32.SetWindowLongA(FloaterWindow, GWL_EXSTYLE, r | WS_EX_LAYERED)
    user32.SetLayeredWindowAttributes(FloaterWindow, 0, perc_val, LWA_ALPHA)
    
    return None

# FUNCTIONS -------------------------------------------------------------------------------------------------#

def gen_C_dict(context, window, area_type='VIEW_3D'):
    C_dict = {}
    area=None
    region=None
    region_data=None
    space=None
    for area in window.screen.areas:
        if area.type == area_type:
            for region in area.regions:
                if region.type == 'WINDOW':
                    break
            for space in area.spaces:
                if space.type == area_type:
                    region_data = None
                    if area_type == 'VIEW_3D':
                        region_data = space.region_3d
                    break
            break
    C_dict.update(window=window,area=area,region=region,region_data=region_data,screen=window.screen,space_data=space)
    return C_dict

#-----------------------------------------------------------------------------------------------------------#
#                                          - SWITCHES -                                                     #
#-----------------------------------------------------------------------------------------------------------#

# NODE-EDITOR-SWITCH ---------------------------------------------------------------------------------------#
class SetUI_Material(bpy.types.Operator):
    bl_idname = "xm.setui_material"
    bl_label=""
    bpy.types.WindowManager.setui_material_state = bpy.props.BoolProperty(default = False)
    def execute(self, context):
        area = bpy.context.area
        if area.ui_type !='ShaderNodeTree':
            area.ui_type ='ShaderNodeTree'
            bpy.types.WindowManager.setui_material_state = True
            bpy.types.WindowManager.setui_bake_state = False
            bpy.types.WindowManager.setui_geo_state = False
            bpy.types.WindowManager.setui_tex_state = False
            bpy.types.WindowManager.setui_comp_state = False
        return {'FINISHED'}

class SetUI_Bake(bpy.types.Operator):
    bl_idname = "xm.setui_bake"
    bl_label=""
    bpy.types.WindowManager.setui_bake_state = bpy.props.BoolProperty(default = False)
    def execute(self, context):
        area = bpy.context.area
        if area.ui_type !='BakeWrangler_Tree':
            area.ui_type ='BakeWrangler_Tree'
            bpy.types.WindowManager.setui_material_state = False
            bpy.types.WindowManager.setui_bake_state = True
            bpy.types.WindowManager.setui_geo_state = False
            bpy.types.WindowManager.setui_tex_state = False
            bpy.types.WindowManager.setui_comp_state = False
        return {'FINISHED'}

class SetUI_Geo(bpy.types.Operator):
    bl_idname = "xm.setui_geo"
    bl_label=""
    bpy.types.WindowManager.setui_geo_state = bpy.props.BoolProperty(default = False)
    def execute(self, context):
        area = bpy.context.area
        if area.ui_type !='GeometryNodeTree':
            area.ui_type ='GeometryNodeTree'
            bpy.types.WindowManager.setui_material_state = False
            bpy.types.WindowManager.setui_bake_state = False
            bpy.types.WindowManager.setui_geo_state = True
            bpy.types.WindowManager.setui_tex_state = False
            bpy.types.WindowManager.setui_comp_state = False
        return {'FINISHED'}

class SetUI_Tex(bpy.types.Operator):
    bl_idname = "xm.setui_tex"
    bl_label=""
    bpy.types.WindowManager.setui_tex_state = bpy.props.BoolProperty(default = False)
    def execute(self, context):
        area = bpy.context.area
        if area.ui_type !='TextureNodeTree':
            area.ui_type ='TextureNodeTree'
            bpy.types.WindowManager.setui_material_state = False
            bpy.types.WindowManager.setui_bake_state = False
            bpy.types.WindowManager.setui_geo_state = False
            bpy.types.WindowManager.setui_tex_state = True
            bpy.types.WindowManager.setui_comp_state = False
        return {'FINISHED'}

class SetUI_Comp(bpy.types.Operator):
    bl_idname = "xm.setui_comp"
    bl_label=""
    bpy.types.WindowManager.setui_comp_state = bpy.props.BoolProperty(default = False)
    def execute(self, context):
        area = bpy.context.area
        if area.ui_type !='CompositorNodeTree':
            area.ui_type ='CompositorNodeTree'
            bpy.types.WindowManager.setui_material_state = False
            bpy.types.WindowManager.setui_bake_state = False
            bpy.types.WindowManager.setui_geo_state = False
            bpy.types.WindowManager.setui_tex_state = False
            bpy.types.WindowManager.setui_comp_state = True
        return {'FINISHED'}

# IMAGE EDITOR SWITCH --------------------------------------------------------------------------------------#
class SetUI_Image(bpy.types.Operator):
    bl_idname = "xm.setui_image"
    bl_label=""
    bpy.types.WindowManager.setui_image_state = bpy.props.BoolProperty(default = False)
    def execute(self, context):
        area = bpy.context.area
        if area.ui_type !='IMAGE_EDITOR':
            area.ui_type ='IMAGE_EDITOR'
            bpy.types.WindowManager.setui_image_state = True
            bpy.types.WindowManager.setui_uv_state = False
            bpy.types.WindowManager.setui_text_state = False
        return {'FINISHED'}

class SetUI_UV(bpy.types.Operator):
    bl_idname = "xm.setui_uv"
    bl_label=""
    bpy.types.WindowManager.setui_uv_state = bpy.props.BoolProperty(default = False)
    def execute(self, context):
        area = bpy.context.area
        if area.ui_type !='UV':
            area.ui_type ='UV'
            bpy.types.WindowManager.setui_uv_state = True
            bpy.types.WindowManager.setui_image_state = False
            bpy.types.WindowManager.setui_text_state = False
        return {'FINISHED'}

class SetUI_Text(bpy.types.Operator):
    bl_idname = "xm.setui_text"
    bl_label=""
    bpy.types.WindowManager.setui_text_state = bpy.props.BoolProperty(default = False)
    def execute(self, context):
        area = bpy.context.area
        if area.ui_type !='TEXT_EDITOR':
            area.ui_type ='TEXT_EDITOR'
            bpy.types.WindowManager.setui_text_state = True
            bpy.types.WindowManager.setui_image_state = False
            bpy.types.WindowManager.setui_uv_state = False
        return {'FINISHED'}

#-----------------------------------------------------------------------------------------------------------#
#                                          - FLOATERS -                                                     #
#-----------------------------------------------------------------------------------------------------------#

class Floater_00(bpy.types.Operator):
    bl_idname = "xm.floater_00"
    bl_label = "Tool Menu"

    bpy.types.WindowManager.floater_00_init = bpy.props.BoolProperty(default = False) 
    bpy.types.WindowManager.floater_00_state = bpy.props.BoolProperty(default = False)  
    bpy.types.WindowManager.FloaterWindow_00 = bpy.props.StringProperty()
    x: bpy.props.IntProperty()
    y: bpy.props.IntProperty()

    def invoke(self, context, event):
        for window in bpy.context.window_manager.windows:
            for area in window.screen.areas:
                for region in area.regions:
                    if region.type == 'WINDOW':
                        view_width = region.width
                        view_height = region.height

        self.x = event.mouse_region_x
        self.y = view_height - event.mouse_region_y + 450
        return self.execute(context)
    
    def execute(self, context):
        if bpy.types.WindowManager.floater_00_init == False:

            label = bpy.context.preferences.addons[__package__].preferences.floater_00_name
            ui_type = bpy.context.preferences.addons[__package__].preferences.floater_00_type
            size = bpy.context.preferences.addons[__package__].preferences.floater_00_size
            alpha = bpy.context.preferences.addons[__package__].preferences.floater_00_alpha

            bpy.ops.screen.area_dupli('INVOKE_DEFAULT')
            new_window = bpy.context.window_manager.windows[-1]
            area = new_window.screen.areas[-1]

            space_data = bpy.context.space_data
            C_dict = gen_C_dict(bpy.context, new_window, area_type='VIEW_3D')
            C_dict.update(space_data=space_data)

            FloaterWindow = get_active_win()
            bpy.types.WindowManager.FloaterWindow_00 = FloaterWindow

            set_win_transforms(FloaterWindow, location=(self.x, self.y), size=size, )
            set_win_text(FloaterWindow, label,)
            if (alpha!=100):
                set_win_transparency(FloaterWindow, percentage=alpha, )

            area.ui_type = ui_type
            UISpace = area.spaces.active
            UISpace.show_region_header = False

            with context.temp_override(window=new_window, area=area, region = area.regions[0]):
                bpy.ops.screen.region_toggle(region_type='NAVIGATION_BAR')
                bpy.context.space_data.context = 'SCENE'

            bpy.types.WindowManager.floater_00_init = True
            bpy.types.WindowManager.floater_00_state = True

        else:
            if bpy.types.WindowManager.floater_00_state == True:
                FloaterWindow = bpy.types.WindowManager.FloaterWindow_00
                show_win(FloaterWindow, show=False)
                bpy.types.WindowManager.floater_00_state = False
            else:
                FloaterWindow = bpy.types.WindowManager.FloaterWindow_00
                size = bpy.context.preferences.addons[__package__].preferences.floater_00_size
                set_win_transforms(FloaterWindow, location=(self.x, self.y), size=size, )
                show_win(FloaterWindow, show=True)
                bpy.types.WindowManager.floater_00_state = True

        return {'FINISHED'}

class Floater_01(bpy.types.Operator):
    bl_idname = "xm.floater_01"
    bl_label = "OUTLINER"

    bpy.types.WindowManager.floater_01_init = bpy.props.BoolProperty(default = False) 
    bpy.types.WindowManager.floater_01_state = bpy.props.BoolProperty(default = False)  
    bpy.types.WindowManager.FloaterWindow_01 = bpy.props.StringProperty()

    def execute(self, context):
        if bpy.types.WindowManager.floater_01_init == False:

            label = bpy.context.preferences.addons[__package__].preferences.floater_01_name
            ui_type = bpy.context.preferences.addons[__package__].preferences.floater_01_type
            loc = bpy.context.preferences.addons[__package__].preferences.floater_01_pos
            size = bpy.context.preferences.addons[__package__].preferences.floater_01_size
            alpha = bpy.context.preferences.addons[__package__].preferences.floater_01_alpha

            bpy.ops.screen.area_dupli('INVOKE_DEFAULT')
            new_window = bpy.context.window_manager.windows[-1]
            area = new_window.screen.areas[-1]

            space_data = bpy.context.space_data
            C_dict = gen_C_dict(bpy.context, new_window, area_type='VIEW_3D')
            C_dict.update(space_data=space_data)

            FloaterWindow = get_active_win()
            bpy.types.WindowManager.FloaterWindow_01 = FloaterWindow
            set_win_transforms(FloaterWindow, location=loc, size=size, )
            set_win_text(FloaterWindow, label,)
            if (alpha!=100):
                set_win_transparency(FloaterWindow, percentage=alpha, )

            area.ui_type = ui_type
            bpy.types.WindowManager.floater_01_init = True
            bpy.types.WindowManager.floater_01_state = True

        else:
            if bpy.types.WindowManager.floater_01_state == True:
                FloaterWindow = bpy.types.WindowManager.FloaterWindow_01
                show_win(FloaterWindow, show=False)
                bpy.types.WindowManager.floater_01_state = False
            else:
                FloaterWindow = bpy.types.WindowManager.FloaterWindow_01
                show_win(FloaterWindow, show=True)
                bpy.types.WindowManager.floater_01_state = True

        return {'FINISHED'}

class Floater_02(bpy.types.Operator):
    bl_idname = "xm.floater_02"
    bl_label = "PROPERTIES"

    bpy.types.WindowManager.floater_02_init = bpy.props.BoolProperty(default = False) 
    bpy.types.WindowManager.floater_02_state = bpy.props.BoolProperty(default = False)  
    bpy.types.WindowManager.FloaterWindow_02 = bpy.props.StringProperty()

    def execute(self, context):
        if bpy.types.WindowManager.floater_02_init == False:

            label = bpy.context.preferences.addons[__package__].preferences.floater_02_name
            ui_type = bpy.context.preferences.addons[__package__].preferences.floater_02_type
            loc = bpy.context.preferences.addons[__package__].preferences.floater_02_pos
            size = bpy.context.preferences.addons[__package__].preferences.floater_02_size
            alpha = bpy.context.preferences.addons[__package__].preferences.floater_02_alpha

            bpy.ops.screen.area_dupli('INVOKE_DEFAULT')
            new_window = bpy.context.window_manager.windows[-1]
            area = new_window.screen.areas[-1]

            space_data = bpy.context.space_data
            C_dict = gen_C_dict(bpy.context, new_window, area_type='VIEW_3D')
            C_dict.update(space_data=space_data)

            FloaterWindow = get_active_win()
            bpy.types.WindowManager.FloaterWindow_02 = FloaterWindow

            set_win_transforms(FloaterWindow, location=loc, size=size, )
            set_win_text(FloaterWindow, label,)
            if (alpha!=100):
                set_win_transparency(FloaterWindow, percentage=alpha, )

            area.ui_type = ui_type
            UISpace = area.spaces.active
            UISpace.show_region_header = False

            bpy.types.WindowManager.floater_02_init = True
            bpy.types.WindowManager.floater_02_state = True

        else:
            if bpy.types.WindowManager.floater_02_state == True:
                FloaterWindow = bpy.types.WindowManager.FloaterWindow_02
                show_win(FloaterWindow, show=False)
                bpy.types.WindowManager.floater_02_state = False
            else:
                FloaterWindow = bpy.types.WindowManager.FloaterWindow_02
                show_win(FloaterWindow, show=True)
                bpy.types.WindowManager.floater_02_state = True

        return {'FINISHED'}

class Floater_03(bpy.types.Operator):
    bl_idname = "xm.floater_03"
    bl_label = "MODIFIER"

    bpy.types.WindowManager.floater_03_init = bpy.props.BoolProperty(default = False) 
    bpy.types.WindowManager.floater_03_state = bpy.props.BoolProperty(default = False)  
    bpy.types.WindowManager.FloaterWindow_03 = bpy.props.StringProperty()

    def execute(self, context):
        if bpy.types.WindowManager.floater_03_init == False:

            label = bpy.context.preferences.addons[__package__].preferences.floater_03_name
            ui_type = bpy.context.preferences.addons[__package__].preferences.floater_03_type
            loc = bpy.context.preferences.addons[__package__].preferences.floater_03_pos
            size = bpy.context.preferences.addons[__package__].preferences.floater_03_size
            alpha = bpy.context.preferences.addons[__package__].preferences.floater_03_alpha

            bpy.ops.screen.area_dupli('INVOKE_DEFAULT')
            new_window = bpy.context.window_manager.windows[-1]
            area = new_window.screen.areas[-1]

            space_data = bpy.context.space_data
            C_dict = gen_C_dict(bpy.context, new_window, area_type='VIEW_3D')
            C_dict.update(space_data=space_data)

            FloaterWindow = get_active_win()
            bpy.types.WindowManager.FloaterWindow_03 = FloaterWindow

            set_win_transforms(FloaterWindow, location=loc, size=size, )
            set_win_text(FloaterWindow, label,)
            if (alpha!=100):
                set_win_transparency(FloaterWindow, percentage=alpha, )

            area.ui_type = ui_type
            UISpace = area.spaces.active
            UISpace.show_region_header = False

            with context.temp_override(window=new_window, area=area, region = area.regions[0]):
                bpy.ops.screen.region_toggle(region_type='NAVIGATION_BAR')
                bpy.context.space_data.context = 'MODIFIER' 

            bpy.types.WindowManager.floater_03_init = True
            bpy.types.WindowManager.floater_03_state = True

        else:
            if bpy.types.WindowManager.floater_03_state == True:
                FloaterWindow = bpy.types.WindowManager.FloaterWindow_03
                show_win(FloaterWindow, show=False)
                bpy.types.WindowManager.floater_03_state = False
            else:
                FloaterWindow = bpy.types.WindowManager.FloaterWindow_03
                show_win(FloaterWindow, show=True)
                bpy.types.WindowManager.floater_03_state = True

        return {'FINISHED'}

class Floater_04(bpy.types.Operator):
    bl_idname = "xm.floater_04"
    bl_label = "NODE TREE"

    bpy.types.WindowManager.floater_04_init = bpy.props.BoolProperty(default = False) 
    bpy.types.WindowManager.floater_04_state = bpy.props.BoolProperty(default = False)  
    bpy.types.WindowManager.FloaterWindow_04 = bpy.props.StringProperty()

    def execute(self, context):
        if bpy.types.WindowManager.floater_04_init == False:

            label = bpy.context.preferences.addons[__package__].preferences.floater_04_name
            ui_type = bpy.context.preferences.addons[__package__].preferences.floater_04_type
            loc = bpy.context.preferences.addons[__package__].preferences.floater_04_pos
            size = bpy.context.preferences.addons[__package__].preferences.floater_04_size
            alpha = bpy.context.preferences.addons[__package__].preferences.floater_04_alpha

            bpy.types.WindowManager.setui_material_state = True

            bpy.ops.screen.area_dupli('INVOKE_DEFAULT')
            new_window = bpy.context.window_manager.windows[-1]
            area = new_window.screen.areas[-1]

            space_data = bpy.context.space_data
            C_dict = gen_C_dict(bpy.context, new_window, area_type='VIEW_3D')
            C_dict.update(space_data=space_data)

            FloaterWindow = get_active_win()
            bpy.types.WindowManager.FloaterWindow_04 = FloaterWindow
            
            set_win_transforms(FloaterWindow, location=loc, size=size)
            set_win_text(FloaterWindow, label)

            if (alpha!=100):
                set_win_transparency(FloaterWindow, percentage=alpha)

            area.ui_type = ui_type
            UISpace = area.spaces.active
            UISpace.show_region_ui = False
            UISpace.show_region_toolbar = False 
            UISpace.show_region_header = True

            bpy.types.WindowManager.floater_04_init = True
            bpy.types.WindowManager.floater_04_state = True

        else:
            if bpy.types.WindowManager.floater_04_state == True:
                FloaterWindow = bpy.types.WindowManager.FloaterWindow_04
                show_win(FloaterWindow, show=False)
                bpy.types.WindowManager.floater_04_state = False
            else:
                FloaterWindow = bpy.types.WindowManager.FloaterWindow_04
                show_win(FloaterWindow, show=True)
                bpy.types.WindowManager.floater_04_state = True

        return {'FINISHED'}

class Floater_05(bpy.types.Operator):
    bl_idname = "xm.floater_05"
    bl_label = "IMAGE"

    bpy.types.WindowManager.floater_05_init = bpy.props.BoolProperty(default = False) 
    bpy.types.WindowManager.floater_05_state = bpy.props.BoolProperty(default = False)  
    bpy.types.WindowManager.FloaterWindow_05 = bpy.props.StringProperty()

    def execute(self, context):
        if bpy.types.WindowManager.floater_05_init == False:

            label = bpy.context.preferences.addons[__package__].preferences.floater_05_name
            ui_type = bpy.context.preferences.addons[__package__].preferences.floater_05_type
            loc = bpy.context.preferences.addons[__package__].preferences.floater_05_pos
            size = bpy.context.preferences.addons[__package__].preferences.floater_05_size
            alpha = bpy.context.preferences.addons[__package__].preferences.floater_05_alpha

            bpy.types.WindowManager.setui_image_state = True

            bpy.ops.screen.area_dupli('INVOKE_DEFAULT')
            new_window = bpy.context.window_manager.windows[-1]
            area = new_window.screen.areas[-1]

            space_data = bpy.context.space_data
            C_dict = gen_C_dict(bpy.context, new_window, area_type='VIEW_3D')
            C_dict.update(space_data=space_data)

            FloaterWindow = get_active_win()
            bpy.types.WindowManager.FloaterWindow_05 = FloaterWindow

            set_win_transforms(FloaterWindow, location=loc, size=size, )
            set_win_text(FloaterWindow, label,)
            if (alpha!=100):
                set_win_transparency(FloaterWindow, percentage=alpha, )
            area.ui_type = ui_type
                
            UISpace = area.spaces.active
            UISpace.show_region_ui = False
            UISpace.show_region_toolbar = False 
            UISpace.show_region_header = True

            bpy.types.WindowManager.floater_05_init = True
            bpy.types.WindowManager.floater_05_state = True

        else:
            if bpy.types.WindowManager.floater_05_state == True:
                FloaterWindow = bpy.types.WindowManager.FloaterWindow_05
                show_win(FloaterWindow, show=False)
                bpy.types.WindowManager.floater_05_state = False
            else:
                FloaterWindow = bpy.types.WindowManager.FloaterWindow_05
                show_win(FloaterWindow, show=True)
                bpy.types.WindowManager.floater_05_state = True

        return {'FINISHED'}

class Floater_06(bpy.types.Operator):
    bl_idname = "xm.floater_06"
    bl_label = "CAM"

    bpy.types.WindowManager.floater_06_init = bpy.props.BoolProperty(default = False) 
    bpy.types.WindowManager.floater_06_state = bpy.props.BoolProperty(default = False)  
    bpy.types.WindowManager.FloaterWindow_06 = bpy.props.StringProperty()

    def execute(self, context):
        if bpy.types.WindowManager.floater_06_init == False:

            label = bpy.context.preferences.addons[__package__].preferences.floater_06_name
            ui_type = bpy.context.preferences.addons[__package__].preferences.floater_06_type
            loc = bpy.context.preferences.addons[__package__].preferences.floater_06_pos
            size = bpy.context.preferences.addons[__package__].preferences.floater_06_size
            alpha = bpy.context.preferences.addons[__package__].preferences.floater_06_alpha

            bpy.ops.screen.area_dupli('INVOKE_DEFAULT')
            new_window = bpy.context.window_manager.windows[-1]
            area = new_window.screen.areas[-1]
            space_data = bpy.context.space_data

            C_dict = gen_C_dict(bpy.context, new_window, area_type='VIEW_3D')
            C_dict.update(space_data=space_data)

            FloaterWindow = get_active_win()
            bpy.types.WindowManager.FloaterWindow_06 = FloaterWindow

            set_win_transforms(FloaterWindow, location=loc, size=size, )
            set_win_text(FloaterWindow, label,)
            if (alpha!=100):
                set_win_transparency(FloaterWindow, percentage=alpha, )
            
            area.ui_type = 'DOPESHEET'
            UISpace = area.spaces.active
            UISpace.show_region_header = True

            with context.temp_override(window=new_window, area=area, region = area.regions[0]):
                bpy.ops.screen.region_flip()

            with context.temp_override(window=new_window, area=area):
                bpy.ops.screen.area_split(direction='HORIZONTAL', factor=0.3)

            area.ui_type = 'VIEW_3D'
            UISpace = area.spaces.active
            bpy.ops.view3d.view_camera(C_dict)
            UISpace.lock_camera = True
            UISpace.use_local_camera = True                        
            UISpace.camera = bpy.context.scene.camera if bpy.context.object.type not in ["CAMERA","LIGHT"] else bpy.context.object
            context.scene.camera.data.sensor_fit = 'HORIZONTAL'
            bpy.ops.view3d.view_center_camera(C_dict)
            UISpace.show_region_header = False
            bpy.ops.screen.area_move(x=300, y=200, delta=200)

            bpy.types.WindowManager.floater_06_init = True
            bpy.types.WindowManager.floater_06_state = True

        else:
            if bpy.types.WindowManager.floater_06_state == True:
                FloaterWindow = bpy.types.WindowManager.FloaterWindow_06
                show_win(FloaterWindow, show=False)
                bpy.types.WindowManager.floater_06_state = False
            else:
                FloaterWindow = bpy.types.WindowManager.FloaterWindow_06
                show_win(FloaterWindow, show=True)
                bpy.types.WindowManager.floater_06_state = True

        return {'FINISHED'}

#-----------------------------------------------------------------------------------------------------------------------#

classes = (Floater_00, Floater_01, Floater_02, Floater_03, Floater_04, Floater_05, Floater_06, 
            SetUI_UV, SetUI_Image, SetUI_Text, SetUI_Material, SetUI_Bake, SetUI_Geo, SetUI_Tex, SetUI_Comp)

def register():
    if platform.system() != 'Windows':
        print("FLOATERS only work in Windows so far..")
        return None

    else:
        bpy.types.WindowManager.floater_00_init = False
        bpy.types.WindowManager.floater_00_state = False
        bpy.types.WindowManager.floater_01_init = False
        bpy.types.WindowManager.floater_01_state = False
        bpy.types.WindowManager.floater_02_init = False
        bpy.types.WindowManager.floater_02_state = False
        bpy.types.WindowManager.floater_03_init = False
        bpy.types.WindowManager.floater_03_state = False
        bpy.types.WindowManager.floater_04_init = False
        bpy.types.WindowManager.floater_04_state = False
        bpy.types.WindowManager.floater_05_init = False
        bpy.types.WindowManager.floater_05_state = False
        bpy.types.WindowManager.floater_06_init = False
        bpy.types.WindowManager.floater_06_state = False

        for cls in classes:
            bpy.utils.register_class(cls)

def unregister():
    if platform.system() != 'Windows':
        return None
    
    else:
        for cls in classes:
            bpy.utils.unregister_class(cls)

#-----------------------------------------------------------------------------------------------------------------------#
