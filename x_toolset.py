import bpy

import gpu
from gpu_extras.batch import batch_for_shader
from gpu_extras.presets import draw_circle_2d
from gpu.shader import from_builtin
import blf
import bmesh
import ctypes

from bpy.props import StringProperty,BoolProperty,FloatProperty,IntProperty
from bpy.types import Operator, AddonPreferences
from mathutils import Vector, Matrix 

from .functions import redraw_regions, update_toolset
from .floaters import get_mouse_position, screensize
from .toolsets import toolset

# CTYPES----------------------------------------------------------------------------------------------
# --> ctypes.windll.user32.keybd_event(KEY_0)

LONG = ctypes.c_long
DWORD = ctypes.c_ulong
ULONG_PTR = ctypes.POINTER(DWORD)
WORD = ctypes.c_ushort

#keys
VK_ESCAPE = 0x1B
VK_SHIFT = 0x10
VK_CONTROL = 0x11
VK_ALT = 0x12

KEY_0 = 0x30
KEY_1 = 0x31
KEY_2 = 0x32
KEY_3 = 0x33
KEY_4 = 0x34
KEY_5 = 0x35
KEY_6 = 0x36
KEY_7 = 0x37
KEY_8 = 0x38
KEY_9 = 0x39
KEY_A = 0x41
KEY_B = 0x42
KEY_C = 0x43
KEY_D = 0x44
KEY_E = 0x45
KEY_F = 0x46
KEY_G = 0x47
KEY_H = 0x48
KEY_I = 0x49
KEY_J = 0x4A
KEY_K = 0x4B
KEY_L = 0x4C
KEY_M = 0x4D
KEY_N = 0x4E
KEY_O = 0x4F
KEY_P = 0x50
KEY_Q = 0x51
KEY_R = 0x52
KEY_S = 0x53
KEY_T = 0x54
KEY_U = 0x55
KEY_V = 0x56
KEY_W = 0x57
KEY_X = 0x58
KEY_Y = 0x59
KEY_Z = 0x5A

KEYEVENTF_EXTENDEDKEY = 0x0001
KEYEVENTF_KEYUP = 0x0002
KEYEVENTF_SCANCODE = 0x0008
KEYEVENTF_UNICODE = 0x0004

WHEEL_DELTA = 120
XBUTTON1 = 0x0001
XBUTTON2 = 0x0002
MOUSEEVENTF_ABSOLUTE = 0x8000
MOUSEEVENTF_HWHEEL = 0x01000
MOUSEEVENTF_MOVE = 0x0001
MOUSEEVENTF_MOVE_NOCOALESCE = 0x2000
MOUSEEVENTF_LEFTDOWN = 0x0002
MOUSEEVENTF_LEFTUP = 0x0004
MOUSEEVENTF_RIGHTDOWN = 0x0008
MOUSEEVENTF_RIGHTUP = 0x0010
MOUSEEVENTF_MIDDLEDOWN = 0x0020
MOUSEEVENTF_MIDDLEUP = 0x0040
MOUSEEVENTF_VIRTUALDESK = 0x4000
MOUSEEVENTF_WHEEL = 0x0800
MOUSEEVENTF_XDOWN = 0x0080
MOUSEEVENTF_XUP = 0x0100

INPUT_MOUSE = 0
INPUT_KEYBOARD = 1
INPUT_HARDWARE = 2

class MOUSEINPUT(ctypes.Structure):
    _fields_ = (('dx', LONG),
                ('dy', LONG),
                ('mouseData', DWORD),
                ('dwFlags', DWORD),
                ('time', DWORD),
                ('dwExtraInfo', ULONG_PTR))
                
class KEYBDINPUT(ctypes.Structure):
    _fields_ = (('wVk', WORD),
                ('wScan', WORD),
                ('dwFlags', DWORD),
                ('time', DWORD),
                ('dwExtraInfo', ULONG_PTR))
                
class HARDWAREINPUT(ctypes.Structure):
    _fields_ = (('uMsg', DWORD),
                ('wParamL', WORD),
                ('wParamH', WORD))
                
class _INPUTunion(ctypes.Union):
    _fields_ = (('mi', MOUSEINPUT),
                ('ki', KEYBDINPUT),
                ('hi', HARDWAREINPUT))

class INPUT(ctypes.Structure):
    _fields_ = (('type', DWORD),
                ('union', _INPUTunion))

def SendInput(*inputs):
    nInputs = len(inputs)
    LPINPUT = INPUT * nInputs
    pInputs = LPINPUT(*inputs)
    cbSize = ctypes.c_int(ctypes.sizeof(INPUT))
    return ctypes.windll.user32.SendInput(nInputs, pInputs, cbSize)

def Input(structure):
    if isinstance(structure, MOUSEINPUT):
        return INPUT(INPUT_MOUSE, _INPUTunion(mi=structure))
    if isinstance(structure, KEYBDINPUT):
        return INPUT(INPUT_KEYBOARD, _INPUTunion(ki=structure))
    if isinstance(structure, HARDWAREINPUT):
        return INPUT(INPUT_HARDWARE, _INPUTunion(hi=structure))
    raise TypeError('Cannot create INPUT structure!')

def MouseInput(flags, x, y, data):
    return MOUSEINPUT(x, y, data, flags, 0, None)

def KeybdInput(code, flags):
    return KEYBDINPUT(code, code, flags, 0, None)

def HardwareInput(message, parameter):
    return HARDWAREINPUT(message & 0xFFFFFFFF,
                         parameter & 0xFFFF,
                         parameter >> 16 & 0xFFFF)

def Mouse(flags, x=0, y=0, data=0):
    return Input(MouseInput(flags, x, y, data))

def Keyboard(code, flags=0):
    return Input(KeybdInput(code, flags))

def Hardware(message, parameter=0):
    return Input(HardwareInput(message, parameter))

#----------------------------------------------------------------------------------------------------

# SHADERS
shader_image = from_builtin('2D_IMAGE')
shader_1 = from_builtin('2D_UNIFORM_COLOR')
shader_2 = from_builtin('2D_FLAT_COLOR')
shader_3 = from_builtin('2D_SMOOTH_COLOR')


# DRAW ----------------------------------------------------------------------------------------------

def draw_callback(self, context, menu_pos, mouse_pos, offset):

    #context = bpy.context

    font_id = 0

    if bpy.types.WindowManager.menu_move == True:
        menu_x = mouse_pos[0] + offset[0]
        menu_y = mouse_pos[1] + offset[1]  
        menu_pos = menu_x, menu_y

    else:
        menu_pos = menu_pos[0], menu_pos[1]

    # menu move
    Draw_Text(2, 2, '>>', 12, font_id=0, color=[1, 1, 1, 1], menu_pos=menu_pos)

    # menu bg
    #Rectangle(0, 0, 220, 230, [0.2, 0.2, 0.2, 0.8], menu_pos=menu_pos)


    # MENU ---------------------------------------------------------------------------------
    if context.mode == 'OBJECT':
        Draw_Text(5, 20 , 'OBJECT', 12, font_id=0, color=[1, 1, 1, 1], menu_pos=menu_pos)

    elif context.mode == 'SCULPT':
        # mask
        bpy.ops.xm.button(x=5, y=20, w=30, h=30, text='', icon='icon_05', tool=14, corner='left', menu_pos=menu_pos, mouse_pos=mouse_pos)

        bpy.ops.xm.button(x=36, y=20, w=23, h=30, text='', icon='icon_05', tool=28, corner='none', menu_pos=menu_pos, mouse_pos=mouse_pos)
        bpy.ops.xm.button(x=60, y=20, w=23, h=30, text='', icon='icon_05', tool=29, corner='none', menu_pos=menu_pos, mouse_pos=mouse_pos)
        bpy.ops.xm.button(x=84, y=20, w=23, h=30, text='', icon='icon_05', tool=30, corner='right', menu_pos=menu_pos, mouse_pos=mouse_pos)

        # faceset
        bpy.ops.xm.button(x=112, y=20, w=30, h=30, text='', icon='icon_05', tool=15, corner='left', menu_pos=menu_pos, mouse_pos=mouse_pos)

        bpy.ops.xm.button(x=143, y=20, w=22, h=16, text='', icon='icon_05', tool=31, corner='none', menu_pos=menu_pos, mouse_pos=mouse_pos)
        bpy.ops.xm.button(x=166, y=20, w=22, h=16, text='', icon='icon_05', tool=32, corner='topright', menu_pos=menu_pos, mouse_pos=mouse_pos)

        bpy.ops.xm.button(x=143, y=37, w=45, h=13, text='EDIT', tool=33, corner='bottomright', menu_pos=menu_pos, mouse_pos=mouse_pos)

        bpy.ops.xm.button(x=190, y=20, w=24, h=30, text='', icon='icon_05', tool=16, corner='all', menu_pos=menu_pos, mouse_pos=mouse_pos)

        # transform
        bpy.ops.xm.button(x=5, y=56, w=50, h=14, text='PVT M', icon='', op='sculpt.set_pivot_position', cmd="mode='UNMASKED'", corner='topleft', menu_pos=menu_pos, mouse_pos=mouse_pos)
        bpy.ops.xm.button(x=5, y=72, w=50, h=14 , text='RESET', icon='', op='sculpt.set_pivot_position', cmd="mode='ORIGIN'", corner='bottomleft', menu_pos=menu_pos, mouse_pos=mouse_pos)
        bpy.ops.xm.button(x=56, y=56, w=50, h=30, text='', icon='icon_01', tool=19, corner='right', menu_pos=menu_pos, mouse_pos=mouse_pos)

        # grab
        bpy.ops.xm.button(x=112, y=56, w=40, h=30, text='', icon='icon_03', tool=1, corner='left', menu_pos=menu_pos, mouse_pos=mouse_pos)
        bpy.ops.xm.button(x=153, y=56, w=30, h=30, text='', icon='icon_03', tool=20, corner='none', menu_pos=menu_pos, mouse_pos=mouse_pos)
        bpy.ops.xm.button(x=184, y=56, w=30, h=30, text='', icon='icon_03', tool=22, corner='right', menu_pos=menu_pos, mouse_pos=mouse_pos)

        # clay
        bpy.ops.xm.button(x=5, y=92, w=50, h=30, text='', icon='icon_02', tool=2, corner='topleft', menu_pos=menu_pos, mouse_pos=mouse_pos)
        bpy.ops.xm.button(x=56, y=92, w=50, h=30, text='', icon='icon_02', tool=3, corner='none', menu_pos=menu_pos, mouse_pos=mouse_pos)
        bpy.ops.xm.button(x=107, y=92, w=50, h=30, text='', icon='icon_02', tool=4, corner='topright', menu_pos=menu_pos, mouse_pos=mouse_pos)

        # crease
        bpy.ops.xm.button(x=164, y=92, w=50, h=30, text='', icon='icon_02', tool=8, corner='top', menu_pos=menu_pos, mouse_pos=mouse_pos)

        # clay
        bpy.ops.xm.button(x=5, y=123, w=50, h=30, text='', icon='icon_02', tool=5, corner='bottomleft', menu_pos=menu_pos, mouse_pos=mouse_pos)
        bpy.ops.xm.button(x=56, y=123, w=50, h=30, text='', icon='icon_02', tool=6, corner='none', menu_pos=menu_pos, mouse_pos=mouse_pos)
        bpy.ops.xm.button(x=107, y=123, w=50, h=30, text='', icon='icon_02', tool=7, corner='bottomright', menu_pos=menu_pos, mouse_pos=mouse_pos)

        # pinch
        bpy.ops.xm.button(x=164, y=123, w=50, h=30, text='', icon='icon_03', tool=9, corner='bottom', menu_pos=menu_pos, mouse_pos=mouse_pos)

        # polish
        bpy.ops.xm.button(x=5, y=159, w=50, h=30, text='', icon='icon_04', tool=10, corner='left', menu_pos=menu_pos, mouse_pos=mouse_pos)
        bpy.ops.xm.button(x=56, y=159, w=50, h=30, text='', icon='icon_04', tool=11, corner='none', menu_pos=menu_pos, mouse_pos=mouse_pos)
        bpy.ops.xm.button(x=107, y=159, w=50, h=30, text='', icon='icon_04', tool=12, corner='right', menu_pos=menu_pos, mouse_pos=mouse_pos)

        # smooth
        bpy.ops.xm.button(x=164, y=159, w=50, h=30, text='', icon='icon_04', tool=13, corner='all', menu_pos=menu_pos, mouse_pos=mouse_pos)

        # functions
        bpy.ops.xm.button(x=5, y=200, w=50, h=20, text='DYNA', cmd='dyna', key=KEY_1, mod=VK_ALT, tog=True, corner='all', menu_pos=menu_pos, mouse_pos=mouse_pos)
        bpy.ops.xm.button(x=56, y=200, w=50, h=20, text='REMESH', key=KEY_R, mod=VK_CONTROL, corner='all', menu_pos=menu_pos, mouse_pos=mouse_pos)

        bpy.ops.xm.button(x=107, y=200, w=20, h=20, text='S', key=KEY_2, mod=VK_ALT, corner='all', menu_pos=menu_pos, mouse_pos=mouse_pos)
        bpy.ops.xm.button(x=127, y=200, w=20, h=20, text='M', key=KEY_3, mod=VK_ALT, corner='all', menu_pos=menu_pos, mouse_pos=mouse_pos)
        bpy.ops.xm.button(x=147, y=200, w=20, h=20, text='L', key=KEY_4, mod=VK_ALT, corner='all', menu_pos=menu_pos, mouse_pos=mouse_pos)

        mesh = context.active_object.data

        #bpy.ops.xm.slider(x=167, y=200, w=20, h=20, text='L', prop='mesh.remesh_voxel_size', corner='all', menu_pos=menu_pos, mouse_pos=mouse_pos)


        voxelsize = str(round(mesh.remesh_voxel_size, 3))
        Draw_Text(167, 200, voxelsize, 12, font_id=0, color=[1, 1, 1, 1], menu_pos=menu_pos)


    redraw_regions()

'''
bpy.ops.sculpt.mask_filter(filter_type='GROW')
bpy.ops.mesh.primitive_cube_add()
bpy.ops.object.duplicate_move()

'''
# UI FUNCTIONS ---------------------------------------------------------------------------------------
class Slider(bpy.types.Operator):
    bl_idname = "xm.slider"
    bl_label = "Slider"

    x: bpy.props.IntProperty()
    y: bpy.props.IntProperty()
    w: bpy.props.IntProperty()
    h: bpy.props.IntProperty()

    menu_pos: bpy.props.IntVectorProperty(size=2)
    mouse_pos: bpy.props.IntVectorProperty(size=2)
    item_pos: bpy.props.IntVectorProperty(size=2)

    text: bpy.props.StringProperty()
    icon: bpy.props.StringProperty()

    prop: bpy.props.StringProperty()

    value: bpy.props.FloatProperty()


    is_hovered:bpy.props.BoolProperty(default=False)
    is_pressed:bpy.props.BoolProperty(default=False)
    bt_state:bpy.props.BoolProperty(default=False)

    corner: bpy.props.StringProperty()

    def execute(self, context):

        mesh = context.active_object.data

        menu_x = self.menu_pos[0]
        menu_y = self.menu_pos[1]

        mouse_x = self.mouse_pos[0]
        mouse_y = self.mouse_pos[1]


        left = self.menu_pos[0] + self.x 
        right = self.menu_pos[0] + self.x  + self.w
        top =  self.menu_pos[1] - self.y 
        bottom = self.menu_pos[1] - self.y - self.h

        pos = left, bottom
        center = left + self.w/2, top - self.h/2,

        if mouse_x > left and mouse_x < right and mouse_y < top and mouse_y > bottom :
            self.is_hovered = True
            if bpy.types.WindowManager.leftclick == True:
                self.is_pressed = True
            else:
                self.is_pressed = False
        else:
            self.is_hovered = False

        in_value = eval(self.prop)
  
        out_value = in_value + self.item_pos[0]-self.mouse_pos[0]

        voxelsize = str(round(out_value, 3))
        Draw_Text(left, bottom, voxelsize, 12, font_id=0, color=[1, 1, 1, 1], menu_pos=self.menu_pos)

        in_value = out_value




        if self.bt_state == True:
            Rectangle(self.x, self.y, self.w, self.h, [0.2, 0.5, 0.8, 1.0], corner=self.corner, menu_pos=self.menu_pos)
        else:
            Rectangle(self.x, self.y, self.w, self.h, [0.35, 0.35, 0.35, 1.0], corner=self.corner, menu_pos=self.menu_pos)

        if self.text != '':
            Draw_Text(self.x, self.y, self.text, 12, font_id=0, color=[0.9, 0.9, 0.9, 1], menu_pos=self.menu_pos)

        if self.icon != '':
            draw_icon(icon=self.icon, item_pos=center)

        if self.is_hovered == True:
            Rectangle(self.x, self.y, self.w, self.h, [1, 1, 1, 0.1], corner=self.corner, menu_pos=self.menu_pos)

        redraw_regions()

        return {'FINISHED'}


    def invoke(self, context, event):
        self.item_pos = event.mouse_x, event.mouse_y
        self.execute(context)




class Button(bpy.types.Operator):
    bl_idname = "xm.button"
    bl_label = "Button"

    x: bpy.props.IntProperty()
    y: bpy.props.IntProperty()
    w: bpy.props.IntProperty()
    h: bpy.props.IntProperty()

    menu_pos: bpy.props.IntVectorProperty(size=2)
    mouse_pos: bpy.props.IntVectorProperty(size=2)
    item_pos: bpy.props.IntVectorProperty(size=2)

    text: bpy.props.StringProperty()
    icon: bpy.props.StringProperty()

    tool: bpy.props.IntProperty()
    op: bpy.props.StringProperty()
    cmd: bpy.props.StringProperty()
    key: bpy.props.IntProperty()
    mod: bpy.props.IntProperty()
    tog: bpy.props.BoolProperty(default=False)

    is_hovered:bpy.props.BoolProperty(default=False)
    is_pressed:bpy.props.BoolProperty(default=False)
    bt_state:bpy.props.BoolProperty(default=False)

    corner: bpy.props.StringProperty()

    def execute(self, context):

        menu_x = self.menu_pos[0]
        menu_y = self.menu_pos[1]

        mouse_x = self.mouse_pos[0]
        mouse_y = self.mouse_pos[1]


        left = self.menu_pos[0] + self.x 
        right = self.menu_pos[0] + self.x  + self.w
        top =  self.menu_pos[1] - self.y 
        bottom = self.menu_pos[1] - self.y - self.h

        pos = left, bottom
        center = left + self.w/2, top - self.h/2,

        if mouse_x > left and mouse_x < right and mouse_y < top and mouse_y > bottom :
            self.is_hovered = True
            if bpy.types.WindowManager.leftclick == True:
                self.is_pressed = True
            else:
                self.is_pressed = False
        else:
            self.is_hovered = False
  
        if self.tool:
            Tools = toolset()
            Tool = Tools[self.tool][1]

            if self.is_hovered == True:
                if bpy.types.WindowManager.leftclick == True:

                    bpy.ops.wm.tool_set_by_id(name=Tool)
                    #bpy.data.brushes["Pencil Soft"].name = "Pencil Soft"

                    #bpy.ops.xm.settool(tool_index = self.tool)
                    #update_toolset()
                    
                    bpy.types.WindowManager.leftclick = False


            self.bt_state = bpy.types.WindowManager.tool_state[self.tool]

        if self.op:
            if self.is_hovered == True:
                if bpy.types.WindowManager.leftclick == True:

                    operator = 'bpy.ops.'
                    operator += self.op
                    operator += '('
                    if self.cmd != '':
                        operator += self.cmd
                    operator += ')'

                    eval(operator)

                    bpy.types.WindowManager.leftclick = False

        if self.key:
            if self.tog == False:
                if self.is_pressed == True:
                    if self.mod != '':
                        SendInput(Keyboard(self.mod), Keyboard(self.key))
                        SendInput(Keyboard(self.mod, KEYEVENTF_KEYUP),
                                Keyboard(self.key, KEYEVENTF_KEYUP))
                    else:
                        SendInput(Keyboard(self.key))
                        SendInput(Keyboard(self.key, KEYEVENTF_KEYUP))

                self.bt_state = self.is_pressed

            else:
                if self.is_pressed == True:

                    if self.mod != '':
                        SendInput(Keyboard(self.mod), Keyboard(self.key))
                        SendInput(Keyboard(self.mod, KEYEVENTF_KEYUP),
                                Keyboard(self.key, KEYEVENTF_KEYUP))
                    else:
                        SendInput(Keyboard(self.key))
                        SendInput(Keyboard(self.key, KEYEVENTF_KEYUP))

                    bpy.types.WindowManager.leftclick = False


                dstate = 'bpy.types.WindowManager.'
                dstate += self.cmd
                dstate += '_state'


                if eval(dstate) == True:
                    self.bt_state = True
                else:
                    self.bt_state = False

        if self.bt_state == True:
            Rectangle(self.x, self.y, self.w, self.h, [0.2, 0.5, 0.8, 1.0], corner=self.corner, menu_pos=self.menu_pos)
        else:
            Rectangle(self.x, self.y, self.w, self.h, [0.35, 0.35, 0.35, 1.0], corner=self.corner, menu_pos=self.menu_pos)

        if self.text != '':
            Draw_Text(self.x, self.y, self.text, 12, font_id=0, color=[0.9, 0.9, 0.9, 1], menu_pos=self.menu_pos)

        if self.icon != '':
            draw_icon(icon=self.icon, item_pos=center)

        if self.is_hovered == True:
            Rectangle(self.x, self.y, self.w, self.h, [1, 1, 1, 0.1], corner=self.corner, menu_pos=self.menu_pos)

        redraw_regions()

        return {'FINISHED'}

'''
    def invoke(self, context, event):
        self.item_pos = event.mouse_x, event.mouse_y
        self.execute(context)
'''
# UI ELEMENTS -----------------------------------------------------------------------------------------

def Draw_Text(x, y, text, size, font_id=0, color=[1, 1, 1, 1], menu_pos=[0, 0]):

    left = menu_pos[0]  + x + 4
    top = menu_pos[1] - y + 1

    blf.color(font_id, color[0], color[1], color[2], color[3])
    blf.position(font_id, left, top-size, 0)
    blf.size(font_id, size, 72)
    blf.draw(font_id, text)

def Rectangle(x, y, width, height, color=[0, 0.5, 0.5, 1.0], corner='all', shader=shader_1, menu_pos=[0, 0]):

    left = menu_pos[0] + x 
    top = menu_pos[1] - y

    batch = batch_for_shader(shader, 'TRIS', {"pos": rectangle_rc_points(
        left, top-height, width, height, rc=4, corner=corner)}, indices=rectangle_rc_indices)

    gpu.state.blend_set('ALPHA')

    shader.bind()
    shader.uniform_float("color", color)

    batch.draw(shader)


def Rectangle_Border(_posX, _posY, _width, _height, _color=[0, 0.5, 0.5, 1.0], _shader=shader_1):
    batch = batch_for_shader(_shader, 'LINES', {"pos": rectangle_rc_border_points(
        _posX, _posY, _width, _height,rc=4)})

    gpu.state.blend_set('ALPHA')

    _shader.bind()
    _shader.uniform_float("color", _color)

    batch.draw(_shader)


def draw_square(pos, color=[1, 1, 1, 1], w=2, shader=shader_1):

    pos_x = pos[0]
    pos_y = pos[1]

    batch = batch_for_shader(shader, 'LINES', {"pos": rectangle_border_points(
        pos_x - w/2, pos_y - w/2, w, w)})
    shader.bind()
    shader.uniform_float("color", color)

    batch.draw(shader)


def draw_square_rc(pos, color=[1, 1, 1, 1], w=2, shader=shader_1):

    pos_x = pos[0]
    pos_y = pos[1]

    batch = batch_for_shader(shader, 'LINES', {"pos": rectangle_rc_border_points(
        pos_x - w/2, pos_y - w/2, w, w, 3)})

    shader.bind()
    shader.uniform_float("color", color)

    batch.draw(shader)


def rectangle_points(x, y, w, h):
    return ((x, y), (x+w, y), (x, y+h), (x+w, y+h))

rectangle_indices = ((0, 1, 2), (2, 1, 3))

def rectangle_border_points(x, y, w, h):
    return ((x, y), (x+w, y), 
            (x+w, y), (x+w, y+h), 
            (x+w, y+h), (x, y+h), 
            (x, y+h), (x, y))

def rectangle_rc_border_points(x, y, w, h, rc=2):

    arc1 = rc/2 + rc/6
    arc2 = rc/2 - rc/6

    return ((x+rc, y), (x+w-rc, y),

            (x+w-rc, y), (x+w-rc+arc1, y+arc2),
            (x+w-rc+arc1, y+arc2), (x+w, y+rc),

            (x+w, y+rc),(x+w, y+h-rc),

            (x+w, y+h-rc), (x+w-arc2, y+h-rc+arc1),
            (x+w-arc2, y+h-rc+arc1), (x+w-rc, y+h), 

            (x+w-rc, y+h), (x+rc, y+h),

            (x+rc, y+h),(x+rc-arc1, y+h-arc2),

            (x+rc-arc1, y+h-arc2), (x, y+h-rc),

            (x, y+h-rc),(x, y+rc),

            (x, y+rc), (x+arc2, y+rc-arc1),

            (x+arc2, y+rc-arc1), (x+rc, y),

            )


def rectangle_rc_points(x, y, w, h, rc=2, corner = 'all'):

    arc1 = rc/2 + rc/6
    arc2 = rc/2 - rc/6

    if corner == 'all':
        return ((x+rc, y), (x+w-rc, y),
                (x+w-rc+arc1, y+arc2), (x+w, y+rc),
                (x+w, y+h-rc), (x+w-arc2, y+h-rc+arc1),
                (x+w-rc, y+h), (x+rc, y+h),
                (x+rc-arc1, y+h-arc2), (x, y+h-rc),
                (x, y+rc), (x+arc2, y+rc-arc1),
                )
    elif corner == 'top':
        return ((x, y), (x+w, y),
                (x+w-rc+arc1, y+arc2), (x+w, y+rc),
                (x+w, y+h-rc), (x+w-arc2, y+h-rc+arc1),
                (x+w-rc, y+h), (x+rc, y+h),
                (x+rc-arc1, y+h-arc2), (x, y+h-rc),
                (x, y+rc), (x+arc2, y+rc-arc1),
                )
    if corner == 'bottom':
        return ((x+rc, y), (x+w-rc, y),
                (x+w-rc+arc1, y+arc2), (x+w, y+rc),
                (x+w, y+h), (x+w-arc2, y+h-rc+arc1),
                (x+w-rc, y+h), (x+rc, y+h),
                (x+rc-arc1, y+h-arc2), (x, y+h),
                (x, y+rc), (x+arc2, y+rc-arc1),
                )
    if corner == 'left':
        return ((x+rc, y), (x+w-rc, y),
                (x+w-rc+arc1, y+arc2), (x+w, y),
                (x+w, y+h-rc), (x+w-arc2, y+h-rc+arc1),
                (x+w, y+h), (x+rc, y+h),
                (x+rc-arc1, y+h-arc2), (x, y+h-rc),
                (x, y+rc), (x+arc2, y+rc-arc1),
                )
    if corner == 'topleft':
        return ((x+rc, y), (x+w-rc, y),
                (x+w-rc+arc1, y+arc2), (x+w, y),
                (x+w, y+h-rc), (x+w-arc2, y+h-rc+arc1),
                (x+w, y+h), (x+rc, y+h),
                (x+rc-arc1, y+h-arc2), (x, y+h-rc),
                (x, y), (x+arc2, y+rc-arc1),
                )
    if corner == 'bottomleft':
        return ((x+rc, y), (x+w, y),
                (x+w-rc+arc1, y+arc2), (x+w, y+rc),
                (x+w, y+h), (x+w-arc2, y+h-rc+arc1),
                (x+w-rc, y+h), (x+rc, y+h),
                (x+rc-arc1, y+h-arc2), (x, y+h),
                (x, y+rc), (x+arc2, y+rc-arc1),
                )


    if corner == 'right':
        return ((x+rc, y), (x+w-rc, y),
                (x+w-rc+arc1, y+arc2), (x+w, y+rc),
                (x+w, y+h-rc), (x+w-arc2, y+h-rc+arc1),
                (x+w-rc, y+h), (x+rc, y+h),
                (x+rc-arc1, y+h-arc2), (x, y+h),
                (x, y), (x+arc2, y+rc-arc1),
                )

    if corner == 'topright':
        return ((x+rc, y), (x+w, y),
                (x+w-rc+arc1, y+arc2), (x+w, y+rc),
                (x+w, y+h-rc), (x+w-arc2, y+h-rc+arc1),
                (x+w-rc, y+h), (x+rc, y+h),
                (x+rc-arc1, y+h-arc2), (x, y+h),
                (x, y), (x+arc2, y+rc-arc1),
                )
    if corner == 'bottomright':
        return ((x+rc, y), (x+w-rc, y),
                (x+w-rc+arc1, y+arc2), (x+w, y+rc),
                (x+w, y+h), (x+w-arc2, y+h-rc+arc1),
                (x+w-rc, y+h), (x+rc, y+h),
                (x+rc-arc1, y+h-arc2), (x, y+h),
                (x, y), (x+arc2, y+rc-arc1),
                )

    if corner == 'none':
        return ((x, y), (x+w, y),
                (x+w-rc+arc1, y+arc2), (x+w, y+rc),
                (x+w, y+h), (x+w-arc2, y+h-rc+arc1),
                (x+w, y+h), (x, y+h),
                (x+rc-arc1, y+h-arc2), (x, y+h),
                (x, y), (x+arc2, y+rc-arc1),
                )

rectangle_rc_indices = ((1, 2, 3), (4, 5, 6), (7, 8, 9), (10, 11, 0), (0, 1, 6), (0, 6, 7), (1, 3, 4), (1, 4, 6), (0, 7, 9), (0, 9, 10))


# ICON -----------------------------------------------------------------------------------------


def draw_icon(icon='',item_pos=(0,0)):
    op = icon
    op += '(item_pos=item_pos)'
    eval(op)


def icon_01(color=(1, 1, 1, 1), shader=shader_1, item_pos=[0, 0]):

    x = item_pos[0]
    y = item_pos[1]

    pos = x,y

    gpu.state.line_width_set(2)

    draw_circle_2d(pos, color, 8, segments=5)

    draw_square_rc(pos, (1, 1, 1, 0.2), 28)


def icon_02(color=(0.4, 0.7, 1, 1), shader=shader_1, item_pos=[0, 0]):

    x = item_pos[0]
    y = item_pos[1]

    pos = x,y
    gpu.state.line_width_set(2)

    draw_circle_2d(pos, color, 8, segments=4)

    coords=[(x, y), (x+8, y+8)]

    shader.bind()
    shader.uniform_float("color", color)
    batch = batch_for_shader(shader, 'LINES', {"pos": coords})
    batch.draw(shader)

def icon_03(color=(1, 0.9, 0.4, 1), shader=shader_1, item_pos=[0, 0]):

    x = item_pos[0]
    y = item_pos[1]

    pos = x,y

    draw_circle_2d(pos, color, 8, segments=5)
    coords=[(x, y), (x+10, y+5)]

    shader.bind()
    shader.uniform_float("color", color)
    batch = batch_for_shader(shader, 'LINES', {"pos": coords})
    batch.draw(shader)

def icon_04(color=(1, 0.5, 0.4, 1), shader=shader_1, item_pos=[0, 0]):

    x = item_pos[0]
    y = item_pos[1]

    pos = x,y

    draw_circle_2d(pos, color, 8, segments=7)
    coords=[(x, y), (x+10, y+5)]

    shader.bind()
    shader.uniform_float("color", color)
    batch = batch_for_shader(shader, 'LINES', {"pos": coords})
    batch.draw(shader)

def icon_05(color=(0.4, 0.4, 0.4, 1), shader=shader_1, item_pos=[0, 0]):

    x = item_pos[0]
    y = item_pos[1]

    pos = x,y

    draw_circle_2d(pos, color, 8, segments=7)
    coords=[(x, y), (x+10, y+5)]

    shader.bind()
    shader.uniform_float("color", color)
    batch = batch_for_shader(shader, 'LINES', {"pos": coords})
    batch.draw(shader)



#-- MODAL -----------------------------------------------------------------------------------------


class ToolSet(bpy.types.Operator):
    bl_idname = "xm.toolset"
    bl_label = "HUD"

    bpy.types.WindowManager.toolhud_state = bpy.props.BoolProperty(default = False)
    bpy.types.WindowManager.leftclick = bpy.props.BoolProperty(default = False)
    bpy.types.WindowManager.menu_move = bpy.props.BoolProperty(default = False)

    mouse_pos: bpy.props.IntVectorProperty(size=2)
    menu_pos: bpy.props.IntVectorProperty(size=2)
    offset: bpy.props.IntVectorProperty(size=2)

    left: bpy.props.IntProperty()
    right: bpy.props.IntProperty()
    top: bpy.props.IntProperty()
    bottom: bpy.props.IntProperty()

    def modal(self, context, event):

        self.mouse_pos = event.mouse_region_x, event.mouse_region_y

        mouse_x = self.mouse_pos[0]
        mouse_y = self.mouse_pos[1]

        menu_x = self.menu_pos[0]
        menu_y = self.menu_pos[1]

        self.left = menu_x
        self.right = self.left + 210
        self.top = menu_y
        self.bottom = self.top - 230

        if bpy.types.WindowManager.toolhud_state == True:
            if event.type == 'LEFTMOUSE':
                if event.value == 'PRESS':
                    if mouse_x > self.left and mouse_x < self.right and mouse_y < self.top and mouse_y > self.top-12 :
                        bpy.types.WindowManager.menu_move = True
                        self.offset = menu_x - mouse_x,  menu_y - mouse_y
                        return {'RUNNING_MODAL'}

                    elif mouse_x > self.left and mouse_x < self.right and mouse_y < self.top-12 and mouse_y > self.bottom :
                        bpy.types.WindowManager.leftclick = True
                        return {'RUNNING_MODAL'}

                    else:
                        return {'PASS_THROUGH'}

                elif event.value == 'RELEASE':
                    if bpy.types.WindowManager.menu_move == True:
                        bpy.types.WindowManager.menu_move = False
                        self.menu_pos = mouse_x + self.offset[0], mouse_y + self.offset[1]
                    bpy.types.WindowManager.leftclick = False
                    return {'PASS_THROUGH'}


                else:
                    return {'PASS_THROUGH'}
            else:
                return {'PASS_THROUGH'}

        else:
            self.report({'INFO'}, "MODAL OFF")
            return {'FINISHED'}

    def invoke(self, context, event):

        self.menu_pos = event.mouse_x, event.mouse_y - 100

        self.execute(context)
        context.window_manager.modal_handler_add(self)
        self.report({'INFO'}, "MODAL ON")
        return {'RUNNING_MODAL'}

    def execute(self, context):

        handler = bpy.app.driver_namespace.get('draw')


        if bpy.types.WindowManager.toolhud_state == False:
            bpy.types.WindowManager.toolhud_state = True

            handler = bpy.types.SpaceView3D.draw_handler_add(
                draw_callback, (self, context, self.menu_pos, self.mouse_pos, self.offset), 'WINDOW', 'POST_PIXEL')

            dns = bpy.app.driver_namespace
            dns['draw'] = handler

        else:
            bpy.types.WindowManager.toolhud_state = False
            remove_draw()

        redraw_regions()

        return {'FINISHED'}

def remove_draw():
    handler = bpy.app.driver_namespace.get('draw')
    if handler:
        bpy.types.SpaceView3D.draw_handler_remove(handler, 'WINDOW')
        del bpy.app.driver_namespace['draw']
        redraw_regions()

#-----------------------------------------------------------------------------------------------------------------------

classes = (ToolSet, Button, Slider)

def register():

    bpy.types.WindowManager.toolhud_state = False
    bpy.types.WindowManager.menu_move = False

    for cls in classes:
        bpy.utils.register_class(cls)
    
def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)
