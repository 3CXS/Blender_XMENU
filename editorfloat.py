import bpy
import os, platform

from mathutils import Vector
from time import sleep

from .functions import context 
from bpy.types import AddonPreferences

############################################ Ctypes/Win32 globals
active_process_id = os.getpid()

import ctypes 
from ctypes import wintypes
from ctypes import byref
from ctypes import c_int, c_double, c_byte, c_char_p, c_long, Structure
#https://docs.microsoft.com/en-us/windows/win32/api/winuser/

#RGB window class also known as COLORREF DWORD

def RGB(r, g, b):
    r = r & 0xFF
    g = g & 0xFF
    b = b & 0xFF
    return (b << 16) | (g << 8) | r

class POINT(Structure):
    _fields_ = [("x", c_long), ("y", c_long)]


#proper way to define user32 it seems 

user32 = ctypes.WinDLL('user32', use_last_error=True)
screensize = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)

#not sure why this is needed 

if not hasattr(wintypes, 'LPDWORD'): # PY2
    wintypes.LPDWORD = ctypes.POINTER(wintypes.DWORD)
 
#Useful for function

WNDENUMPROC = ctypes.WINFUNCTYPE(
    wintypes.BOOL,
    wintypes.HWND,
    wintypes.LPARAM,)

#all flags we'll use 

NULL            = 0x05
SWP_NOSIZE      = 0x0001
SWP_NOMOVE      = 0x0002
SWP_NOZORDER    = 0x0004
SWP_SHOWWINDOW  = 0x0040
GWL_EXSTYLE     = -20  
WS_EX_LAYERED   = 0x00080000
LWA_ALPHA       = 0x00000002
LWA_COLORKEY    = 0x00000001
SIZESW_MINIMIZE = 6
SW_RESTORE      = 9


############################################ Cursor Position

def get_mouse_position(): #get mouse position
    
    pos = POINT()
    user32.GetCursorPos(byref(pos))

    return pos.x , pos.y

############################################ Show/Hide


def show_win(hWnd, show=True,):
    """minimize or show given window"""
    
    user32.ShowWindow(hWnd, SW_RESTORE if show else SIZESW_MINIMIZE)
    
    return None
 
 
def is_win_minimized(hWnd,):
    """check if window is minimized"""
    
    #TODO
    
    return True


def is_win_visible(hWnd):
    """check if window is visible"""
    
    return user32.IsWindowVisible(hWnd)


############################################ Windows Managers


def get_active_win():
    """get currently active window handle value""" 
    
    return user32.GetActiveWindow()


def get_all_computer_win(filter_process_id=None):
    """return all windows handles (== all process, some have non visible windows)"""

    handles = []
    
    def fct(hWnd, lParam):
        if filter_process_id is None:
            handles.append(hWnd)
        else:
             if get_win_process_id(hWnd,) == filter_process_id:
                 handles.append(hWnd)
        return True
         
    cb_worker = WNDENUMPROC(fct)
    user32.EnumWindows(cb_worker, 0)
    
    return handles


def get_blender_win():
    """return all windows handles used by this instance of blender"""
    
    blender_wins = [ hWnd for hWnd in get_all_computer_win(filter_process_id=active_process_id) if is_win_visible(hWnd) and not get_win_text(hWnd,).startswith("blender.exe")] 
    
    #TODO, might be good to know if win is main window, or children, or console? 
    
    return blender_wins #take this 3dsmax


def get_blender_console():
    """return blender console window handle"""

    return [ hWnd for hWnd in get_all_computer_win(filter_process_id=active_process_id) if get_win_text(hWnd,).startswith("blender.exe")][0]

def get_all_process_info():
    """return dict of key pid and value process name"""

    proc = os.popen('wmic process get description, processid').read()
    proc = proc.split()
    proc = { int(proc[i]) : proc[i-1] for i,e in enumerate(proc) if e.isdigit() }
    
    return proc
 
 
def get_win_process_id(hWnd,):
    """get given window process id"""
    
    pid = wintypes.DWORD()
    tid = user32.GetWindowThreadProcessId(hWnd, byref(pid))
    
    return pid.value


############################################ Window Text


def set_win_text(hWnd, text,): #Well, it's useless, on each save status the title will update with asterix char
    """give the given window a title"""
    
    user32.SetWindowTextA(hWnd, c_char_p(text.encode('utf-8')),) 
    
    return None


def get_win_text(hWnd,):
    """get given window title"""

    length = user32.GetWindowTextLengthW(hWnd) + 1
    buffer = ctypes.create_unicode_buffer(length)
    user32.GetWindowTextW(hWnd, buffer, length)

    return buffer.value

############################################ Close
def shut_window(hWnd):
    bpy.ops.wm.window_close()
    return None

def close_win(hWnd,):
    """close given window"""
    
    #user32.CloseWindow(hWnd,)
    user32.DestroyWindow(hWnd,)
    return None 


############################################ Transforms 


def set_win_transforms(hWnd, location=(0,0), size=(500,500), ):
    """set location and size of given window handle (use vector values)"""

    if (size is None) and (location is None):
        return None
    
    flags  = SWP_SHOWWINDOW #needed to send update signal somehow? witouth it it won't work 
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


def get_win_transforms(hWnd,):
    """get given window handle location and scale (return tuple of two vectors)"""
    
    #TODO
    
    return tuple 


############################################ Transparency 


def set_win_transparency(hWnd, percentage=50, ):
    """set given window handle transparency (note that minimal value is 10 or you're gonna have a bad time)"""
    
    #https://www.experts-exchange.com/articles/1783/Win32-Semi-Transparent-Window.html
    
    if percentage<10:
        percentage=10
    perc_val = int(255/100*percentage)

    r = user32.GetWindowLongA( hWnd, GWL_EXSTYLE ) 
    user32.SetWindowLongA(hWnd, GWL_EXSTYLE, r | WS_EX_LAYERED )
    user32.SetLayeredWindowAttributes( hWnd, 0, perc_val, LWA_ALPHA )
    
    return None 


def get_win_transparency(hWnd,):
    """get transparency value from given window handle"""
    
    #https://docs.microsoft.com/en-us/windows/win32/api/winuser/nf-winuser-getlayeredwindowattributes
    #need to create ctypes obj, pass obj ptr within fct to get modifier ptr value back (it's a cpp thing, they can't return complex values)
    
    a = c_int(0)
    user32.GetLayeredWindowAttributes( hWnd, 0, byref(a), 0) 
    
    return round(a.value/255*100)


####################################################################################

####################################################################################
#invoke_mouse = None 
#invoke_area = None
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
                    #print("found region")
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


class FloatOutliner(bpy.types.Operator):
    bl_idname = "xmenu.float_outliner"
    bl_label = "EDITOR"

    def execute(self, context):
        alpha = bpy.context.preferences.addons[__package__].preferences.float_alpha
        loc = (1700,200)
        size = (300,500)
        label = ""
        ui_type = 'OUTLINER'

        bpy.ops.screen.area_dupli('INVOKE_DEFAULT')
        new_window = bpy.context.window_manager.windows[-1]
        area = new_window.screen.areas[-1]
        space_data = bpy.context.space_data

        C_dict = gen_C_dict(bpy.context, new_window, area_type='VIEW_3D')
        C_dict.update(space_data=space_data)

        hWnd = get_active_win()

        set_win_transforms(hWnd, location=loc, size=size, )
        set_win_text(hWnd, label,)
        if (alpha!=100):
            set_win_transparency(hWnd, percentage=alpha, )
        area.ui_type = ui_type
            
        sv3d = area.spaces.active

        return {'FINISHED'}

class FloatProps(bpy.types.Operator):
    bl_idname = "xmenu.float_props"
    bl_label = "EDITOR"

    def execute(self, context):
        alpha = bpy.context.preferences.addons[__package__].preferences.float_alpha
        loc = (2000,200)
        size = (500,800)
        label = ""
        ui_type = 'PROPERTIES'

        bpy.ops.screen.area_dupli('INVOKE_DEFAULT')
        new_window = bpy.context.window_manager.windows[-1]
        area = new_window.screen.areas[-1]
        space_data = bpy.context.space_data

        C_dict = gen_C_dict(bpy.context, new_window, area_type='VIEW_3D')
        C_dict.update(space_data=space_data)

        hWnd = get_active_win()

        set_win_transforms(hWnd, location=loc, size=size, )
        set_win_text(hWnd, label,)
        if (alpha!=100):
            set_win_transparency(hWnd, percentage=alpha, )

        area.ui_type = ui_type
        sv3d = area.spaces.active

        sv3d.show_region_header = False
        #sv3d.context = 'MODIFIER'
        #sv3d.PROPERTIES_PT_navigation_bar = False 

        return {'FINISHED'}


class FloatShader(bpy.types.Operator):
    bl_idname = "xmenu.float_shader"
    bl_label = "EDITOR"

    def execute(self, context):
        alpha = bpy.context.preferences.addons[__package__].preferences.float_alpha
        loc = (200,500)
        size = (800,500)
        label = ""
        ui_type = 'ShaderNodeTree'

        bpy.ops.screen.area_dupli('INVOKE_DEFAULT')
        new_window = bpy.context.window_manager.windows[-1]
        area = new_window.screen.areas[-1]
        space_data = bpy.context.space_data
        
        C_dict = gen_C_dict(bpy.context, new_window, area_type='VIEW_3D')
        C_dict.update(space_data=space_data)

        hWnd = get_active_win()
        
        set_win_transforms(hWnd, location=loc, size=size, )
        set_win_text(hWnd, label,)

        if (alpha!=100):
            set_win_transparency(hWnd, percentage=alpha, )

        area.ui_type = ui_type

        sv3d = area.spaces.active
        
        sv3d.show_region_ui = False
        sv3d.show_region_toolbar = False 
        sv3d.show_region_header = True

        return {'FINISHED'}

class FloatUV(bpy.types.Operator):
    bl_idname = "xmenu.float_uv"
    bl_label = "EDITOR"

    def execute(self, context):
        alpha = bpy.context.preferences.addons[__package__].preferences.float_alpha
        loc = (200,200)
        size = (1000,800)
        label = ""
        ui_type = 'UV'

        bpy.ops.screen.area_dupli('INVOKE_DEFAULT')
        new_window = bpy.context.window_manager.windows[-1]
        area = new_window.screen.areas[-1]
        space_data = bpy.context.space_data

        C_dict = gen_C_dict(bpy.context, new_window, area_type='VIEW_3D')
        C_dict.update(space_data=space_data)

        hWnd = get_active_win()

        set_win_transforms(hWnd, location=loc, size=size, )
        set_win_text(hWnd, label,)
        if (alpha!=100):
            set_win_transparency(hWnd, percentage=alpha, )
        area.ui_type = ui_type
            
        sv3d = area.spaces.active
        sv3d.show_region_ui = False
        sv3d.show_region_toolbar = True 
        sv3d.show_region_header = True

        return {'FINISHED'}

class FloatImage(bpy.types.Operator):
    bl_idname = "xmenu.float_image"
    bl_label = "EDITOR"

    def execute(self, context):
        alpha = bpy.context.preferences.addons[__package__].preferences.float_alpha
        loc = (200,50)
        size = (600,400)
        label = ""
        ui_type = 'IMAGE_EDITOR'

        bpy.ops.screen.area_dupli('INVOKE_DEFAULT')
        new_window = bpy.context.window_manager.windows[-1]
        area = new_window.screen.areas[-1]
        space_data = bpy.context.space_data

        C_dict = gen_C_dict(bpy.context, new_window, area_type='VIEW_3D')
        C_dict.update(space_data=space_data)

        hWnd = get_active_win()

        set_win_transforms(hWnd, location=loc, size=size, )
        set_win_text(hWnd, label,)
        if (alpha!=100):
            set_win_transparency(hWnd, percentage=alpha, )
        area.ui_type = ui_type
            
        sv3d = area.spaces.active
        sv3d.show_region_ui = False
        sv3d.show_region_toolbar = False 
        sv3d.show_region_header = True

        return {'FINISHED'}





class FloatCam(bpy.types.Operator):
    bl_idname = "xmenu.float_cam"
    bl_label = "EDITOR"

    def execute(self, context):
        alpha = bpy.context.preferences.addons[__package__].preferences.float_alpha
        loc = (400,600)
        size = (600,400)
        label = ""
        ui_type = 'VIEW_3D'

        bpy.ops.screen.area_dupli('INVOKE_DEFAULT')
        new_window = bpy.context.window_manager.windows[-1]
        area = new_window.screen.areas[-1]
        space_data = bpy.context.space_data

        C_dict = gen_C_dict(bpy.context, new_window, area_type='VIEW_3D')
        C_dict.update(space_data=space_data)

        hWnd = get_active_win()

        set_win_transforms(hWnd, location=loc, size=size, )
        set_win_text(hWnd, label,)
        if (alpha!=100):
            set_win_transparency(hWnd, percentage=alpha, )
        area.ui_type = ui_type
            
        sv3d = area.spaces.active

        bpy.ops.view3d.view_camera(C_dict)
        sv3d.lock_camera = True
        sv3d.use_local_camera = True                        
        sv3d.camera = bpy.context.scene.camera if bpy.context.object.type not in ["CAMERA","LIGHT"] else bpy.context.object

        bpy.ops.view3d.view_center_camera(C_dict)

        #v3d.show_region_ui = False
        #sv3d.show_region_toolbar = False 
        sv3d.show_region_header = False

        return {'FINISHED'}


#sv3d.show_region_tool_header = False
#sv3d.overlay.show_overlays = False
#sv3d.show_gizmo = False
#sv3d.shading.show_xray = False
#sv3d.overlay.show_wireframes = True

#////////////////////////////////////////////////////////////////////////////////////////////#

classes = (FloatShader,FloatOutliner,FloatUV,FloatImage,FloatProps,FloatCam)

def register():

    if platform.system() != 'Windows':
        print("This plugin is for window OS only")
        return None

    for cls in classes:
        bpy.utils.register_class(cls)
    
def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)