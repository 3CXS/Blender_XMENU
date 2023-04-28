import bpy
import os, platform

from mathutils import Vector
import time
from bpy.types import AddonPreferences


#WINDOW-MANAGEMENT-------------------------------------------------------------------

#globals
#active_process_id = os.getpid()
#import os
#import sys


import Xlib
from Xlib.display import Display
from Xlib import X, Xatom, display, Xutil

from contextlib import contextmanager
from Xlib.xobject.drawable import Window
from typing import Any, Dict, Optional, Tuple, Union

import time

disp = Xlib.display.Display()
root = disp.screen().root
root.change_attributes(event_mask=Xlib.X.SubstructureNotifyMask)

def getProp(win, prop):
    p = win.get_full_property(disp.intern_atom('_NET_WM_' + prop), 0)
    return [None] if (p is None) else p.value







#-----------------------------------------------------------------------------------------------------------------------

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

#funcctions---------------------------------------------------------------------------------------------------------------
def show_win(Window_ID=0, show=True):
    #TITLE = title
    SHOW = show
  
    display = Display()
    root = display.screen().root
    windowIDs = root.get_full_property(display.intern_atom('_NET_CLIENT_LIST'), X.AnyPropertyType).value
    if Window_ID in windowIDs:
        window = display.create_resource_object('window', Window_ID)
        #title = window.get_wm_name()
        #pid = window.get_full_property(display.intern_atom('_NET_WM_PID'), X.AnyPropertyType)

        if show == True:
            window.map()
            display.sync()
            #window.set_wm_state(title, '_NET_WM_STATE_MAXIMIZED')
        else:
            parent = window.query_tree().parent
            #window.unmap_sub_windows()
            window.unmap()
            #window.set_wm_state(title, x, '_NET_WM_STATE_HIDDEN')
            display.sync()
            #display.flush() 


def get_wm_name():
    display = Xlib.display.Display()
    window = display.get_input_focus().focus
    wmname = window.get_wm_name()
    wmclass = window.get_wm_class()
    if wmclass is None: #or wmname is None:
        window = window.query_tree().parent
        wmclass = window.get_wm_class()
        wmname = window.get_wm_name()
    #winclass=wmclass[1]
    #print winclass
    return wmname
 
def modifie(Window_ID, x=0, y=0, width=0, height=0):

    posx=x
    posy=y
    WIDTH = width
    HEIGHT = height
 
    display = Display()
    root = display.screen().root
    windowIDs = root.get_full_property(display.intern_atom('_NET_CLIENT_LIST'), X.AnyPropertyType).value
    if Window_ID in windowIDs:
        window = display.create_resource_object('window', Window_ID)
        #window.change_property(display.get_atom('_NET_WM_WINDOW_OPACITY'), Xatom.CARDINAL,32,[0x20202020])
        window.configure(width=WIDTH, height=HEIGHT, x=posx, y=posy, border_width=0, stack_mode=Xlib.X.Above)
        display.sync()
        display.flush() 




#FLOATERS------------------------------------------------------------------------------------------------------------------

from contextlib import contextmanager
from typing import Any, Dict, Optional, Tuple, Union  # noqa

from Xlib import X
from Xlib.display import Display
from Xlib.error import XError
from Xlib.xobject.drawable import Window
from Xlib.protocol.rq import Event

# Connect to the X server and get the root window
disp = Display()
root = disp.screen().root

# Prepare the property names we use so they can be fed into X11 APIs
NET_ACTIVE_WINDOW = disp.intern_atom('_NET_ACTIVE_WINDOW')
NET_WM_NAME = disp.intern_atom('_NET_WM_NAME')  # UTF-8
WM_NAME = disp.intern_atom('WM_NAME')           # Legacy encoding

last_seen = {'xid': None, 'title': None}  # type: Dict[str, Any]


@contextmanager
def window_obj(win_id: Optional[int]) -> Window:
    """Simplify dealing with BadWindow (make it either valid or None)"""
    window_obj = None
    if win_id:
        try:
            window_obj = disp.create_resource_object('window', win_id)
        except XError:
            pass
    yield window_obj


def get_active_window() -> Tuple[Optional[int], bool]:
    """Return a (window_obj, focus_has_changed) tuple for the active window."""
    response = root.get_full_property(NET_ACTIVE_WINDOW,
                                      X.AnyPropertyType)
    if not response:
        return None, False
    win_id = response.value[0]

    focus_changed = (win_id != last_seen['xid'])
    if focus_changed:
        with window_obj(last_seen['xid']) as old_win:
            if old_win:
                old_win.change_attributes(event_mask=X.NoEventMask)

        last_seen['xid'] = win_id
        with window_obj(win_id) as new_win:
            if new_win:
                new_win.change_attributes(event_mask=X.PropertyChangeMask)

    return win_id, focus_changed


def _get_window_name_inner(win_obj: Window) -> str:
    """Simplify dealing with _NET_WM_NAME (UTF-8) vs. WM_NAME (legacy)"""
    for atom in (NET_WM_NAME, WM_NAME):
        try:
            window_name = win_obj.get_full_property(atom, 0)
        except UnicodeDecodeError:  # Apparently a Debian distro package bug
            title = "<could not decode characters>"
        else:
            if window_name:
                win_name = window_name.value  # type: Union[str, bytes]
                if isinstance(win_name, bytes):
                    # Apparently COMPOUND_TEXT is so arcane that this is how
                    # tools like xprop deal with receiving it these days
                    win_name = win_name.decode('latin1', 'replace')
                return win_name
            else:
                title = "<unnamed window>"

    return "{} (XID: {})".format(title, win_obj.id)


def get_window_name(win_id: Optional[int]) -> Tuple[Optional[str], bool]:
    """Look up the window name for a given X11 window ID"""
    if not win_id:
        last_seen['title'] = None
        return last_seen['title'], True

    title_changed = False
    with window_obj(win_id) as wobj:
        if wobj:
            try:
                win_title = _get_window_name_inner(wobj)
            except XError:
                pass
            else:
                title_changed = (win_title != last_seen['title'])
                last_seen['title'] = win_title

    return last_seen['title'], title_changed


def handle_xevent(event: Event):
    """Handler for X events which ignores anything but focus/title change"""
    if event.type != X.PropertyNotify:
        return

    changed = False
    if event.atom == NET_ACTIVE_WINDOW:
        if get_active_window()[1]:
            get_window_name(last_seen['xid'])  # Rely on the side-effects
            changed = True
    elif event.atom in (NET_WM_NAME, WM_NAME):
        changed = changed or get_window_name(last_seen['xid'])[1]

    if changed:
        handle_change(last_seen)


def handle_change(new_state: dict):
    """Replace this with whatever you want to actually do"""
    print(new_state)

if __name__ == '__main__':
    # Listen for _NET_ACTIVE_WINDOW changes
    root.change_attributes(event_mask=X.PropertyChangeMask)

    # Prime last_seen with whatever window was active when we started this
    get_window_name(get_active_window()[0])
    handle_change(last_seen)

    while True:  # next_event() sleeps until we get an event
        handle_xevent(disp.next_event())


    
def get_window_name(window_id):
    try:
        window_obj = disp.create_resource_object('window', window_id)
        window_name = window_obj.get_full_property(NET_WM_NAME, 0).value
    except Xlib.error.XError:
        window_name = None
    return window_name

def printWindowHierrarchy(window, indent):
    children = window.query_tree().children
    for w in children:
        print(indent, w.get_wm_class())
        printWindowHierrarchy(w, indent+'-')




class Floater_01(bpy.types.Operator):
    bl_idname = "xm.floater_01"
    bl_label = "OUTLINER"

    bpy.types.WindowManager.floater_01_init = bpy.props.BoolProperty(default = False) 
    bpy.types.WindowManager.floater_01_state = bpy.props.BoolProperty(default = False)  
    bpy.types.WindowManager.FloatWin_01 = bpy.props.IntProperty()
    



    def execute(self, context):
    
        display = Display()
        root = display.screen().root
   
        if bpy.types.WindowManager.floater_01_init == False:
            label = bpy.context.preferences.addons[__package__].preferences.floater_01_name
            ui_type = bpy.context.preferences.addons[__package__].preferences.floater_01_type
            loc = bpy.context.preferences.addons[__package__].preferences.floater_01_pos
            size = bpy.context.preferences.addons[__package__].preferences.floater_01_size
            alpha = bpy.context.preferences.addons[__package__].preferences.floater_01_alpha

            bpy.ops.screen.area_dupli('INVOKE_DEFAULT')
            
            FloatWin = bpy.context.window_manager.windows[-1]
            area = FloatWin.screen.areas[-1]
            space_data = bpy.context.space_data
            C_dict = gen_C_dict(bpy.context, FloatWin, area_type='VIEW_3D')
            C_dict.update(space_data=space_data)
            
            Window_ID = get_active_window()[0]
            print(Window_ID)
            Window = disp.create_resource_object('window', Window_ID)
            children = Window.query_tree().children
            for w in children:
                print('x')
            #Window = disp.create_resource_object('window', Window_ID)
            windowIDs = root.get_full_property(display.intern_atom('_NET_ACTIVE_WINDOW'), Xlib.X.AnyPropertyType).value
            for windowID in windowIDs:
                window = display.create_resource_object('window', windowID)
                name = window.get_wm_name() # Title
                prop = window.get_full_property(display.intern_atom('_NET_WM_PID'), Xlib.X.AnyPropertyType)
                pid = prop.value[0] # PID
                            
                children = Window.query_tree().children
                for w in children:
                    print('x')
                print(name)
            

            bpy.types.WindowManager.FloatWin_01 = Window_ID
            #Window.set_wm_name(label)
            #Window.set_wm_icon_name(label)
            #title = Window.get_wm_name()
            #print(title) 
            #modifie(Window_ID, loc[0], loc[1], size[0], size[1])

 

            area.ui_type = ui_type
            
            bpy.types.WindowManager.floater_01_init = True
            bpy.types.WindowManager.floater_01_state = True
            
        else:           
            if bpy.types.WindowManager.floater_01_state == True:
                Window_ID = bpy.types.WindowManager.FloatWin_01
                show_win(Window_ID, show=False)
                bpy.types.WindowManager.floater_01_state = False
            else:
                Window_ID = bpy.types.WindowManager.FloatWin_01
                show_win(Window_ID, show=True)
                bpy.types.WindowManager.floater_01_state = True
        return {'FINISHED'}

class Floater_02(bpy.types.Operator):
    bl_idname = "xm.floater_02"
    bl_label = "OUTLINER"

    def execute(self, context):
 
        return {'FINISHED'}
        
#-----------------------------------------------------------------------------------------------------------------------

classes = (Floater_01, Floater_02,)

def register():

    bpy.types.WindowManager.floater_01_init = False
    bpy.types.WindowManager.floater_01_state = False


    for cls in classes:
        bpy.utils.register_class(cls)

 
def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)
