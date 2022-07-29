import bpy
import os, platform

from mathutils import Vector
import time
from bpy.types import AddonPreferences


#Ctypes-------------------------------------------------------------------
#https://docs.microsoft.com/en-us/windows/win32/api/winuser/

#globals
active_process_id = os.getpid()

import ctypes 
from ctypes import wintypes
from ctypes import byref
from ctypes import c_int, c_double, c_byte, c_char_p, c_long, Structure

def RGB(r, g, b):
    r = r & 0xFF
    g = g & 0xFF
    b = b & 0xFF
    return (b << 16) | (g << 8) | r

class POINT(Structure):
    _fields_ = [("x", c_long), ("y", c_long)]


user32 = ctypes.WinDLL('user32', use_last_error=True)
screensize = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)


if not hasattr(wintypes, 'LPDWORD'): # PY2
    wintypes.LPDWORD = ctypes.POINTER(wintypes.DWORD)
 
WNDENUMPROC = ctypes.WINFUNCTYPE(
    wintypes.BOOL,
    wintypes.HWND,
    wintypes.LPARAM,)

#flags
NULL            = 0x05
SWP_NOSIZE      = 0x0001
SWP_NOMOVE      = 0x0002
SWP_NOZORDER    = 0x0004
SWP_SHOWWINDOW  = 0x0040
GWL_EXSTYLE     = -20  
WS_EX_LAYERED   = 0x00080000
LWA_ALPHA       = 0x00000002
LWA_COLORKEY    = 0x00000001
SW_MINIMIZE     = 6
SW_RESTORE      = 9
SW_HIDE         = 0

#funcctions---------------------------------------------------------------------------------------------------------------

def get_mouse_position():
    pos = POINT()
    user32.GetCursorPos(byref(pos))

    return pos.x , pos.y


def detect_click(button, watchtime = 5):
    '''Waits watchtime seconds. Returns True on click, False otherwise'''
    if button in (1, '1', 'l', 'L', 'left', 'Left', 'LEFT'):
        bnum = 0x01
    elif button in (2, '2', 'r', 'R', 'right', 'Right', 'RIGHT'):
        bnum = 0x02


    while 1:
        if ctypes.windll.user32.GetKeyState(bnum) not in [0, 1]:
            # ^ this returns either 0 or 1 when button is not being held down
            return True

    return False


def show_win(hWnd, show=True,):
    user32.ShowWindow(hWnd, SW_RESTORE if show else SW_HIDE)
    
    return None

def get_active_win():

    return user32.GetActiveWindow()

def set_win_text(hWnd, text,): #Well, it's useless, on each save status the title will update with asterix char
    """give the given window a title"""
    
    user32.SetWindowTextA(hWnd, c_char_p(text.encode('utf-8')),)
    #user32.SetWindowLongA(hWnd, GWL_EXSTYLE, 0 )
    
    return None

def set_win_transforms(hWnd, location=(0,0), size=(500,500), ):

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
    user32.SetWindowPos(hWnd,0,X,Y,cx,cy,flags )
    
    return None

def set_win_transparency(hWnd, percentage=50, ):

    if percentage<10:
        percentage=10
    perc_val = int(255/100*percentage)

    r = user32.GetWindowLongA( hWnd, GWL_EXSTYLE ) 
    user32.SetWindowLongA(hWnd, GWL_EXSTYLE, r | WS_EX_LAYERED )
    user32.SetLayeredWindowAttributes( hWnd, 0, perc_val, LWA_ALPHA )
    
    return None 


def get_win_transparency(hWnd,):
  
    a = c_int(0)
    user32.GetLayeredWindowAttributes( hWnd, 0, byref(a), 0) 
    
    return round(a.value/255*100)

#-----------------------------------------------------------------------------------------------------------------------

invoke_mouse = None 
invoke_area = None
invoke_window = None 


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

#FLOATERS------------------------------------------------------------------------------------------------------------------

class Floater_01(bpy.types.Operator):
    bl_idname = "xm.floater_01"
    bl_label = "OUTLINER"

    bpy.types.WindowManager.floater_01_init = bpy.props.BoolProperty(default = False) 
    bpy.types.WindowManager.floater_01_state = bpy.props.BoolProperty(default = False)  
    bpy.types.WindowManager.hWnd_01 = bpy.props.StringProperty()

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

            hWnd = get_active_win()
            bpy.types.WindowManager.hWnd_01 = hWnd

            #hWnd.titleBar = False

            set_win_transforms(hWnd, location=loc, size=size, )

            set_win_text(hWnd, label,)
            if (alpha!=100):
                set_win_transparency(hWnd, percentage=alpha, )
            area.ui_type = ui_type
                
            #sv3d = area.spaces.active

            bpy.types.WindowManager.floater_01_init = True
            bpy.types.WindowManager.floater_01_state = True

        else:           
            if bpy.types.WindowManager.floater_01_state == True:
                hWnd = bpy.types.WindowManager.hWnd_01
                show_win(hWnd, show=False)
                bpy.types.WindowManager.floater_01_state = False
            else:
                hWnd = bpy.types.WindowManager.hWnd_01
                show_win(hWnd, show=True)
                bpy.types.WindowManager.floater_01_state = True

        return {'FINISHED'}

class Floater_02(bpy.types.Operator):
    bl_idname = "xm.floater_02"
    bl_label = "PROPERTIES"

    bpy.types.WindowManager.floater_02_init = bpy.props.BoolProperty(default = False) 
    bpy.types.WindowManager.floater_02_state = bpy.props.BoolProperty(default = False)  
    bpy.types.WindowManager.hWnd_02 = bpy.props.StringProperty()

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

            hWnd = get_active_win()
            bpy.types.WindowManager.hWnd_02 = hWnd

            set_win_transforms(hWnd, location=loc, size=size, )
            set_win_text(hWnd, label,)
            if (alpha!=100):
                set_win_transparency(hWnd, percentage=alpha, )

            
            area.ui_type = ui_type
            
            
            sv3d = area.spaces.active

            sv3d.show_region_header = False

            #bpy.context.space_data.context = 'MODIFIER' 

            bpy.types.WindowManager.floater_02_init = True
            bpy.types.WindowManager.floater_02_state = True

        else:           
            if bpy.types.WindowManager.floater_02_state == True:
                hWnd = bpy.types.WindowManager.hWnd_02
                show_win(hWnd, show=False)
                bpy.types.WindowManager.floater_02_state = False
            else:
                hWnd = bpy.types.WindowManager.hWnd_02
                show_win(hWnd, show=True)
                bpy.types.WindowManager.floater_02_state = True

        return {'FINISHED'}

class Floater_03(bpy.types.Operator):
    bl_idname = "xm.floater_03"
    bl_label = "PROP_MODIFIER"

    bpy.types.WindowManager.floater_03_init = bpy.props.BoolProperty(default = False) 
    bpy.types.WindowManager.floater_03_state = bpy.props.BoolProperty(default = False)  
    bpy.types.WindowManager.hWnd_03 = bpy.props.StringProperty()

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

            hWnd = get_active_win()
            bpy.types.WindowManager.hWnd_03 = hWnd

            set_win_transforms(hWnd, location=loc, size=size, )
            set_win_text(hWnd, label,)
            if (alpha!=100):
                set_win_transparency(hWnd, percentage=alpha, )

            
            area.ui_type = ui_type
            
            
            sv3d = area.spaces.active

            sv3d.show_region_header = False

            with context.temp_override(window=new_window, area=area, region = area.regions[0]):
                bpy.ops.screen.region_toggle(region_type='NAVIGATION_BAR')
                bpy.context.space_data.context = 'MODIFIER' 

            bpy.types.WindowManager.floater_03_init = True
            bpy.types.WindowManager.floater_03_state = True

        else:           
            if bpy.types.WindowManager.floater_03_state == True:
                hWnd = bpy.types.WindowManager.hWnd_03
                show_win(hWnd, show=False)
                bpy.types.WindowManager.floater_03_state = False
            else:
                hWnd = bpy.types.WindowManager.hWnd_03
                show_win(hWnd, show=True)
                bpy.types.WindowManager.floater_03_state = True

        return {'FINISHED'}


class Floater_04(bpy.types.Operator):
    bl_idname = "xm.floater_04"
    bl_label = "SHADER"

    bpy.types.WindowManager.floater_04_init = bpy.props.BoolProperty(default = False) 
    bpy.types.WindowManager.floater_04_state = bpy.props.BoolProperty(default = False)  
    bpy.types.WindowManager.hWnd_04 = bpy.props.StringProperty()

    def execute(self, context):
        if bpy.types.WindowManager.floater_04_init == False:
            label = bpy.context.preferences.addons[__package__].preferences.floater_04_name
            ui_type = bpy.context.preferences.addons[__package__].preferences.floater_04_type
            loc = bpy.context.preferences.addons[__package__].preferences.floater_04_pos
            size = bpy.context.preferences.addons[__package__].preferences.floater_04_size
            alpha = bpy.context.preferences.addons[__package__].preferences.floater_04_alpha

            bpy.ops.screen.area_dupli('INVOKE_DEFAULT')
            new_window = bpy.context.window_manager.windows[-1]
            area = new_window.screen.areas[-1]
            space_data = bpy.context.space_data
            
            C_dict = gen_C_dict(bpy.context, new_window, area_type='VIEW_3D')
            C_dict.update(space_data=space_data)

            hWnd = get_active_win()
            bpy.types.WindowManager.hWnd_04 = hWnd
            
            set_win_transforms(hWnd, location=loc, size=size, )
            set_win_text(hWnd, label,)

            if (alpha!=100):
                set_win_transparency(hWnd, percentage=alpha, )

            area.ui_type = ui_type

            sv3d = area.spaces.active
            
            sv3d.show_region_ui = False
            sv3d.show_region_toolbar = False 
            sv3d.show_region_header = True

            bpy.types.WindowManager.floater_04_init = True
            bpy.types.WindowManager.floater_04_state = True

        else:           
            if bpy.types.WindowManager.floater_04_state == True:
                hWnd = bpy.types.WindowManager.hWnd_04
                show_win(hWnd, show=False)
                bpy.types.WindowManager.floater_04_state = False
            else:
                hWnd = bpy.types.WindowManager.hWnd_04
                show_win(hWnd, show=True)
                bpy.types.WindowManager.floater_04_state = True

        return {'FINISHED'}

class Floater_05(bpy.types.Operator):
    bl_idname = "xm.floater_05"
    bl_label = "UV"

    bpy.types.WindowManager.floater_05_init = bpy.props.BoolProperty(default = False) 
    bpy.types.WindowManager.floater_05_state = bpy.props.BoolProperty(default = False)  
    bpy.types.WindowManager.hWnd_05 = bpy.props.StringProperty()

    def execute(self, context):
        if bpy.types.WindowManager.floater_05_init == False:
            label = bpy.context.preferences.addons[__package__].preferences.floater_05_name
            ui_type = bpy.context.preferences.addons[__package__].preferences.floater_05_type
            loc = bpy.context.preferences.addons[__package__].preferences.floater_05_pos
            size = bpy.context.preferences.addons[__package__].preferences.floater_05_size
            alpha = bpy.context.preferences.addons[__package__].preferences.floater_05_alpha

            bpy.ops.screen.area_dupli('INVOKE_DEFAULT')
            new_window = bpy.context.window_manager.windows[-1]
            area = new_window.screen.areas[-1]
            space_data = bpy.context.space_data

            C_dict = gen_C_dict(bpy.context, new_window, area_type='VIEW_3D')
            C_dict.update(space_data=space_data)

            hWnd = get_active_win()
            bpy.types.WindowManager.hWnd_05 = hWnd

            set_win_transforms(hWnd, location=loc, size=size, )
            set_win_text(hWnd, label,)
            if (alpha!=100):
                set_win_transparency(hWnd, percentage=alpha, )
            area.ui_type = ui_type
                
            sv3d = area.spaces.active
            sv3d.show_region_ui = False
            sv3d.show_region_toolbar = True 
            sv3d.show_region_header = True

            bpy.types.WindowManager.floater_05_init = True
            bpy.types.WindowManager.floater_05_state = True

        else:           
            if bpy.types.WindowManager.floater_05_state == True:
                hWnd = bpy.types.WindowManager.hWnd_05
                show_win(hWnd, show=False)
                bpy.types.WindowManager.floater_05_state = False
            else:
                hWnd = bpy.types.WindowManager.hWnd_05
                show_win(hWnd, show=True)
                bpy.types.WindowManager.floater_05_state = True

        return {'FINISHED'}

class Floater_06(bpy.types.Operator):
    bl_idname = "xm.floater_06"
    bl_label = "IMAGE"

    bpy.types.WindowManager.floater_06_init = bpy.props.BoolProperty(default = False) 
    bpy.types.WindowManager.floater_06_state = bpy.props.BoolProperty(default = False)  
    bpy.types.WindowManager.hWnd_06 = bpy.props.StringProperty()

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

            hWnd = get_active_win()
            bpy.types.WindowManager.hWnd_06 = hWnd

            set_win_transforms(hWnd, location=loc, size=size, )
            set_win_text(hWnd, label,)
            if (alpha!=100):
                set_win_transparency(hWnd, percentage=alpha, )
            area.ui_type = ui_type
                
            sv3d = area.spaces.active
            sv3d.show_region_ui = False
            sv3d.show_region_toolbar = False 
            sv3d.show_region_header = True

            bpy.types.WindowManager.floater_06_init = True
            bpy.types.WindowManager.floater_06_state = True

        else:           
            if bpy.types.WindowManager.floater_06_state == True:
                hWnd = bpy.types.WindowManager.hWnd_06
                show_win(hWnd, show=False)
                bpy.types.WindowManager.floater_06_state = False
            else:
                hWnd = bpy.types.WindowManager.hWnd_06
                show_win(hWnd, show=True)
                bpy.types.WindowManager.floater_06_state = True

        return {'FINISHED'}

class Floater_07(bpy.types.Operator):
    bl_idname = "xm.floater_07"
    bl_label = "GEO_NODES"

    bpy.types.WindowManager.floater_07_init = bpy.props.BoolProperty(default = False) 
    bpy.types.WindowManager.floater_07_state = bpy.props.BoolProperty(default = False)  
    bpy.types.WindowManager.hWnd_07 = bpy.props.StringProperty()

    def execute(self, context):
        if bpy.types.WindowManager.floater_07_init == False:
            label = bpy.context.preferences.addons[__package__].preferences.floater_07_name
            ui_type = bpy.context.preferences.addons[__package__].preferences.floater_07_type
            loc = bpy.context.preferences.addons[__package__].preferences.floater_07_pos
            size = bpy.context.preferences.addons[__package__].preferences.floater_07_size
            alpha = bpy.context.preferences.addons[__package__].preferences.floater_07_alpha

            bpy.ops.screen.area_dupli('INVOKE_DEFAULT')
            new_window = bpy.context.window_manager.windows[-1]
            area = new_window.screen.areas[-1]
            space_data = bpy.context.space_data
            
            C_dict = gen_C_dict(bpy.context, new_window, area_type='VIEW_3D')
            C_dict.update(space_data=space_data)

            hWnd = get_active_win()
            bpy.types.WindowManager.hWnd_07 = hWnd
            
            set_win_transforms(hWnd, location=loc, size=size, )
            set_win_text(hWnd, label,)

            if (alpha!=100):
                set_win_transparency(hWnd, percentage=alpha, )

            area.ui_type = ui_type

            sv3d = area.spaces.active
            
            sv3d.show_region_ui = False
            sv3d.show_region_toolbar = False 
            sv3d.show_region_header = True

            bpy.types.WindowManager.floater_07_init = True
            bpy.types.WindowManager.floater_07_state = True

        else:           
            if bpy.types.WindowManager.floater_07_state == True:
                hWnd = bpy.types.WindowManager.hWnd_07
                show_win(hWnd, show=False)
                bpy.types.WindowManager.floater_07_state = False
            else:
                hWnd = bpy.types.WindowManager.hWnd_07
                show_win(hWnd, show=True)
                bpy.types.WindowManager.floater_07_state = True

        return {'FINISHED'}


class Floater_08(bpy.types.Operator):
    bl_idname = "xm.floater_08"
    bl_label = "CAM"

    bpy.types.WindowManager.floater_08_init = bpy.props.BoolProperty(default = False) 
    bpy.types.WindowManager.floater_08_state = bpy.props.BoolProperty(default = False)  
    bpy.types.WindowManager.hWnd_08 = bpy.props.StringProperty()

    def execute(self, context):
        if bpy.types.WindowManager.floater_08_init == False:
            label = bpy.context.preferences.addons[__package__].preferences.floater_08_name
            ui_type = bpy.context.preferences.addons[__package__].preferences.floater_08_type
            loc = bpy.context.preferences.addons[__package__].preferences.floater_08_pos
            size = bpy.context.preferences.addons[__package__].preferences.floater_08_size
            alpha = bpy.context.preferences.addons[__package__].preferences.floater_08_alpha

            bpy.ops.screen.area_dupli('INVOKE_DEFAULT')
            new_window = bpy.context.window_manager.windows[-1]
            area = new_window.screen.areas[-1]
            space_data = bpy.context.space_data

            C_dict = gen_C_dict(bpy.context, new_window, area_type='VIEW_3D')
            C_dict.update(space_data=space_data)

            hWnd = get_active_win()
            bpy.types.WindowManager.hWnd_08 = hWnd

            set_win_transforms(hWnd, location=loc, size=size, )
            set_win_text(hWnd, label,)
            if (alpha!=100):
                set_win_transparency(hWnd, percentage=alpha, )
            
            area.ui_type = 'DOPESHEET'
            sv3d = area.spaces.active
            sv3d.show_region_header = True


            with context.temp_override(window=new_window, area=area, region = area.regions[0]):
                bpy.ops.screen.region_flip()

            with context.temp_override(window=new_window, area=area):
                bpy.ops.screen.area_split(direction='HORIZONTAL', factor=0.3)

            area.ui_type = 'VIEW_3D'
            sv3d = area.spaces.active
            bpy.ops.view3d.view_camera(C_dict)
            sv3d.lock_camera = True
            sv3d.use_local_camera = True                        
            sv3d.camera = bpy.context.scene.camera if bpy.context.object.type not in ["CAMERA","LIGHT"] else bpy.context.object
            context.scene.camera.data.sensor_fit = 'HORIZONTAL'
            bpy.ops.view3d.view_center_camera(C_dict)
            sv3d.show_region_header = False
            bpy.ops.screen.area_move(x=300, y=200, delta=200)

            bpy.types.WindowManager.floater_08_init = True
            bpy.types.WindowManager.floater_08_state = True

        else:           
            if bpy.types.WindowManager.floater_08_state == True:
                hWnd = bpy.types.WindowManager.hWnd_08
                show_win(hWnd, show=False)
                bpy.types.WindowManager.floater_08_state = False
            else:
                hWnd = bpy.types.WindowManager.hWnd_08
                show_win(hWnd, show=True)
                bpy.types.WindowManager.floater_08_state = True

        return {'FINISHED'}

class Floater_09(bpy.types.Operator):
    bl_idname = "xm.floater_09"
    bl_label = "BAKE_NODES"

    bpy.types.WindowManager.floater_09_init = bpy.props.BoolProperty(default = False) 
    bpy.types.WindowManager.floater_09_state = bpy.props.BoolProperty(default = False)  
    bpy.types.WindowManager.hWnd_09 = bpy.props.StringProperty()

    def execute(self, context):
        if bpy.types.WindowManager.floater_09_init == False:
            label = bpy.context.preferences.addons[__package__].preferences.floater_09_name
            ui_type = bpy.context.preferences.addons[__package__].preferences.floater_09_type
            loc = bpy.context.preferences.addons[__package__].preferences.floater_09_pos
            size = bpy.context.preferences.addons[__package__].preferences.floater_09_size
            alpha = bpy.context.preferences.addons[__package__].preferences.floater_09_alpha

            bpy.ops.screen.area_dupli('INVOKE_DEFAULT')
            new_window = bpy.context.window_manager.windows[-1]
            area = new_window.screen.areas[-1]
            space_data = bpy.context.space_data
            
            C_dict = gen_C_dict(bpy.context, new_window, area_type='VIEW_3D')
            C_dict.update(space_data=space_data)

            hWnd = get_active_win()
            bpy.types.WindowManager.hWnd_09 = hWnd
            
            set_win_transforms(hWnd, location=loc, size=size, )
            set_win_text(hWnd, label,)

            if (alpha!=100):
                set_win_transparency(hWnd, percentage=alpha, )

            area.ui_type = ui_type

            sv3d = area.spaces.active
            
            sv3d.show_region_ui = False
            sv3d.show_region_toolbar = False 
            sv3d.show_region_header = True

            bpy.types.WindowManager.floater_09_init = True
            bpy.types.WindowManager.floater_09_state = True

        else:           
            if bpy.types.WindowManager.floater_09_state == True:
                hWnd = bpy.types.WindowManager.hWnd_09
                show_win(hWnd, show=False)
                bpy.types.WindowManager.floater_09_state = False
            else:
                hWnd = bpy.types.WindowManager.hWnd_09
                show_win(hWnd, show=True)
                bpy.types.WindowManager.floater_09_state = True

        return {'FINISHED'}


class Floater_10(bpy.types.Operator):
    bl_idname = "xm.floater_10"
    bl_label = "COMP_NODES"

    bpy.types.WindowManager.floater_10_init = bpy.props.BoolProperty(default = False) 
    bpy.types.WindowManager.floater_10_state = bpy.props.BoolProperty(default = False)  
    bpy.types.WindowManager.hWnd_10 = bpy.props.StringProperty()

    def execute(self, context):
        if bpy.types.WindowManager.floater_10_init == False:
            label = bpy.context.preferences.addons[__package__].preferences.floater_10_name
            ui_type = bpy.context.preferences.addons[__package__].preferences.floater_10_type
            loc = bpy.context.preferences.addons[__package__].preferences.floater_10_pos
            size = bpy.context.preferences.addons[__package__].preferences.floater_10_size
            alpha = bpy.context.preferences.addons[__package__].preferences.floater_10_alpha

            bpy.ops.screen.area_dupli('INVOKE_DEFAULT')
            new_window = bpy.context.window_manager.windows[-1]
            area = new_window.screen.areas[-1]
            space_data = bpy.context.space_data
            
            C_dict = gen_C_dict(bpy.context, new_window, area_type='VIEW_3D')
            C_dict.update(space_data=space_data)

            hWnd = get_active_win()
            bpy.types.WindowManager.hWnd_10 = hWnd
            
            set_win_transforms(hWnd, location=loc, size=size, )
            set_win_text(hWnd, label,)

            if (alpha!=100):
                set_win_transparency(hWnd, percentage=alpha, )

            area.ui_type = ui_type

            sv3d = area.spaces.active
            
            sv3d.show_region_ui = False
            sv3d.show_region_toolbar = False 
            sv3d.show_region_header = True

            bpy.types.WindowManager.floater_10_init = True
            bpy.types.WindowManager.floater_10_state = True

        else:           
            if bpy.types.WindowManager.floater_10_state == True:
                hWnd = bpy.types.WindowManager.hWnd_10
                show_win(hWnd, show=False)
                bpy.types.WindowManager.floater_10_state = False
            else:
                hWnd = bpy.types.WindowManager.hWnd_10
                show_win(hWnd, show=True)
                bpy.types.WindowManager.floater_10_state = True

        return {'FINISHED'}



#-----------------------------------------------------------------------------------------------------------------------

classes = (Floater_01, Floater_02, Floater_03, Floater_04, Floater_05, Floater_06, Floater_07, Floater_08, Floater_09, Floater_10)

def register():
    if platform.system() != 'Windows':
        print("FLOATERS only work in Windows so far..")
        return None

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
    bpy.types.WindowManager.floater_07_init = False
    bpy.types.WindowManager.floater_07_state = False
    bpy.types.WindowManager.floater_08_init = False
    bpy.types.WindowManager.floater_08_state = False
    bpy.types.WindowManager.floater_09_init = False
    bpy.types.WindowManager.floater_09_state = False
    bpy.types.WindowManager.floater_10_init = False
    bpy.types.WindowManager.floater_10_state = False

    for cls in classes:
        bpy.utils.register_class(cls)

 
def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)
