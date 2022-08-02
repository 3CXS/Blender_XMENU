import bpy

import gpu
from gpu_extras.batch import batch_for_shader
from gpu_extras.presets import draw_circle_2d
from gpu.shader import from_builtin
import blf
import bmesh

from bpy.props import StringProperty,BoolProperty,FloatProperty,IntProperty
from bpy.types import Operator, AddonPreferences
from mathutils import Vector, Matrix 

from .functions import redraw_regions, update_toolset
from .floaters import get_mouse_position, screensize
from .toolsets import toolset



#----------------------------------------------------------------------------------------------------

# SHADERS
shader_image = from_builtin('2D_IMAGE')
shader_1 = from_builtin('2D_UNIFORM_COLOR')
shader_2 = from_builtin('2D_FLAT_COLOR')
shader_3 = from_builtin('2D_SMOOTH_COLOR')


# DRAW ----------------------------------------------------------------------------------------------

def draw_callback(self, context, menu_pos, mouse_pos, offset):

    context = bpy.context

    font_id = 0

    mouse_x = mouse_pos[0]
    mouse_y = mouse_pos[1]

    menu_x = menu_pos[0]
    menu_y = menu_pos[1]

    if bpy.types.WindowManager.menu_move == True:

        menu_pos = mouse_x , mouse_y
        menu_x = menu_pos[0]
        menu_y = menu_pos[1]


    # menu move
    Draw_Text(2, 2, '>>', 12, font_id=0, color=[1, 1, 1, 1], menu_pos=menu_pos)

    # menu bg
    #Rectangle(0, 0, 220, 210, [0.2, 0.2, 0.2, 0.8], menu_pos=menu_pos)


    # MENU ---------------------------------------------------------------------------------

    if context.mode == 'SCULPT':
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

# UI FUNCTIONS ---------------------------------------------------------------------------------------

class Button(bpy.types.Operator):
    bl_idname = "xm.button"
    bl_label = "Button"
    #bl_options = {'REGISTER'}

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

    is_hovered:bpy.props.BoolProperty(default=False)
    bt_state:bpy.props.BoolProperty(default=False)

    corner: bpy.props.StringProperty()

    def execute(self, context):

        context = bpy.context

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
        else:
            self.is_hovered = False
  
        if self.tool:
            Tools = toolset()
            Tool = Tools[self.tool][1]

            if self.is_hovered == True:
                if bpy.types.WindowManager.leftclick == True:

                    bpy.ops.wm.tool_set_by_id(name=Tool)
                    #update_toolset()
                    #bpy.ops.xm.settool(tool_index = self.cmd)
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
        self.bottom = self.top - 210

        if bpy.types.WindowManager.toolhud_state == True:
            if mouse_x > self.left and mouse_x < self.right and mouse_y < self.top and mouse_y > self.bottom :
                if event.type == 'LEFTMOUSE':
                    if event.value == 'PRESS':
                        bpy.types.WindowManager.leftclick = True
                        if mouse_x > self.left+2 and mouse_x < self.left+20 and mouse_y < self.top and mouse_y > self.top-12 :
                            bpy.types.WindowManager.menu_move = True
                            self.offset = mouse_x - menu_x, mouse_y - menu_y

                    elif event.value == 'RELEASE':
                        bpy.types.WindowManager.leftclick = False
                        if bpy.types.WindowManager.menu_move == True:
                            bpy.types.WindowManager.menu_move = False

                return {'RUNNING_MODAL'}

            elif bpy.types.WindowManager.menu_move == True:
                if event.type == 'LEFTMOUSE':
                    if event.value == 'RELEASE':
                        self.menu_pos = self.mouse_pos
                        bpy.types.WindowManager.menu_move = False

                return {'RUNNING_MODAL'} 

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
                draw_callback, (None, None, self.menu_pos, self.mouse_pos, self.offset), 'WINDOW', 'POST_PIXEL')

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

classes = (ToolSet, Button)

def register():

    bpy.types.WindowManager.toolhud_state = False
    bpy.types.WindowManager.menu_move = False

    for cls in classes:
        bpy.utils.register_class(cls)
    
def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)
