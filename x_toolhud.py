import bpy
import gpu
from gpu_extras.batch import batch_for_shader
from gpu.shader import from_builtin
import bgl
import blf

from bpy.props import StringProperty,BoolProperty,FloatProperty,IntProperty
from bpy.types import Operator, AddonPreferences
from mathutils import Vector

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

def draw_callback(self, context, menu_pos, mouse_pos):

    font_id = 0

    mouse_x = mouse_pos[0]
    mouse_y = mouse_pos[1]

    menu_x = menu_pos[0]
    menu_y = menu_pos[1]

    # menu bg
    Draw_2D_Rectangle(menu_x, menu_y-200, 140, 200, [0.1, 0.1, 0.1, 0.9])
    Draw_2D_Rectangle(menu_x, menu_y-5, 140, 5, [0.2, 0.5, 0.8, 1.0])

    # label
    blf.position(font_id, menu_x, menu_y-16, 0)
    blf.size(font_id, 14, 72)
    blf.color(font_id, 1, 1, 1, 1)
    text = 'xyx'
    blf.draw(font_id, text)

    # tools
    bpy.ops.xm.button(x=0, y=0, w=50, h=20, menu_pos=menu_pos, mouse_pos=mouse_pos, text='XX01', cmd=0)
    bpy.ops.xm.button(x=50, y=0, w=50, h=20, menu_pos=menu_pos, mouse_pos=mouse_pos, text='XX01', cmd=1)

#-- MODAL -----------------------------------------------------------------------------------------

class ToolHUD(bpy.types.Operator):
    bl_idname = "xm.toolhud"
    bl_label = "HUD"

    bpy.types.WindowManager.toolhud_state = bpy.props.BoolProperty(default = False)
    bpy.types.WindowManager.leftclick = bpy.props.BoolProperty(default = False)

    menu_pos: bpy.props.IntVectorProperty(size=2)
    mouse_pos: bpy.props.IntVectorProperty(size=2)

    width: bpy.props.IntProperty()
    hight: bpy.props.IntProperty()

    left: bpy.props.IntProperty()
    right: bpy.props.IntProperty()
    top: bpy.props.IntProperty()
    bottom: bpy.props.IntProperty()

    def modal(self, context, event):

        self.mouse_pos = event.mouse_region_x, event.mouse_region_y

        mouse_x = self.mouse_pos[0]
        mouse_y = self.mouse_pos[1]

        bpy.ops.xm.move_menu(menu_pre=self.menu_pos)

        menu_x = self.menu_pos[0]
        menu_y = self.menu_pos[1]


        self.left = menu_x
        self.right = self.left + 140
        self.top = menu_y
        self.bottom = self.top - 200



        if bpy.types.WindowManager.toolhud_state == True:
            if mouse_x > self.left and mouse_x < self.right and mouse_y < self.top and mouse_y > self.bottom :
                if event.type == 'LEFTMOUSE':
                    if event.value == 'PRESS':
                        self.report({'INFO'}, "LMB")
                        #self.report({'INFO'}, "Mouse %d %d" % (mouse_x, mouse_y))
                        bpy.types.WindowManager.leftclick = True

                    elif event.value == 'RELEASE':
                        bpy.types.WindowManager.leftclick = False

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
                draw_callback, (None, None, self.menu_pos, self.mouse_pos), 'WINDOW', 'POST_PIXEL')

            dns = bpy.app.driver_namespace
            dns['draw'] = handler

        else:
            bpy.types.WindowManager.toolhud_state = False
            remove_draw()

        redraw_regions()

        return {'FINISHED'}


class MoveMenu(bpy.types.Operator):
    bl_idname = "xm.move_menu"
    bl_label = ""

    mouse_pos: bpy.props.IntVectorProperty(size=2)

    menu_pre: bpy.props.IntVectorProperty(size=2)
    menu_pos: bpy.props.IntVectorProperty(size=2)

    def modal(self, context, event):

        if bpy.types.WindowManager.leftclick == True:

            self.mouse_pos = event.mouse_region_x, event.mouse_region_y

            mouse_x = self.mouse_pos[0]
            mouse_y = self.mouse_pos[1]

            if mouse_x > self.menu_pre[0] and mouse_x < self.menu_pre[0]+140 and mouse_y < self.menu_pre[1] and mouse_y > self.menu_pre[1]-15 :
                if bpy.types.WindowManager.leftclick == True:
                    menu_x = self.menu_pre[0] + (self.mouse_pos[0] - self.menu_pre[0])
                    menu_y = self.menu_pre[1] + (self.mouse_pos[1] - self.menu_pre[1])
            else:
                menu_x = self.menu_pre[0]
                menu_y = self.menu_pre[1]

            self.menu_pos = menu_x, menu_y

            return {'RUNNING_MODAL'}

        else:
            self.report({'INFO'}, "MODAL OFF")
            return {'FINISHED'}

    def invoke(self, context, event):

        self.execute(context)
        context.window_manager.modal_handler_add(self)
        self.report({'INFO'}, "MODAL ON")
        return {'RUNNING_MODAL'}


    def execute(self, context):

        redraw_regions()
        return {'FINISHED'}
 

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
    cmd: bpy.props.IntProperty()

    is_hovered:bpy.props.BoolProperty(default=False)
    bt_state:bpy.props.BoolProperty(default=False)

    def execute(self, context):

        Tools = toolset()
        Tool = Tools[self.cmd][1]

        menu_x = self.menu_pos[0]
        menu_y = self.menu_pos[1]

        mouse_x = self.mouse_pos[0]
        mouse_y = self.mouse_pos[1]

        left = menu_x + 10 + self.x 
        right = left + self.w
        top = menu_y - 20 - self.y 
        bottom = top - self.h

        if mouse_x > left and mouse_x < right and mouse_y < top and mouse_y > bottom :
            self.is_hovered = True
        else:
            self.is_hovered = False
  
        if self.is_hovered == True:
            if bpy.types.WindowManager.leftclick == True:
                print ("LMB")
                bpy.ops.wm.tool_set_by_id(name=Tool)
                #update_toolset()
                #bpy.ops.xm.settool(tool_index = self.cmd)
                bpy.types.WindowManager.leftclick = False
 
        self.bt_state = bpy.types.WindowManager.tool_state[self.cmd]

        if self.bt_state == True:
            Draw_2D_Rectangle(left, bottom, self.w, self.h, [0.2, 0.5, 0.8, 1.0])

        else:
            Draw_2D_Rectangle(left, bottom, self.w, self.h, [0.5, 0.5, 0.5, 1.0])

        blf.position(0, left, bottom, 0)
        blf.size(0, 12, 72)
        blf.color(1, 1, 1, 1, 1)
        blf.draw(0, self.text)

        if self.is_hovered == True:
            Draw_2D_Rectangle(left, bottom, self.w, self.h, [1, 1, 1, 0.1])

        redraw_regions()
        return {'FINISHED'}

    def invoke(self, context, event):
        self.item_pos = event.mouse_x, event.mouse_y
        self.execute(context)

# UI ELEMENTS -----------------------------------------------------------------------------------------

def rectangle_points(x, y, w, h):
    return ((x, y), (x+w, y), (x, y+h), (x+w, y+h))

rectangle_indices = ((0, 1, 2), (2, 1, 3))

def Draw_2D_Rectangle(_posX, _posY, _width, _height, _color=[0, 0.5, 0.5, 1.0], _shader=shader_1):
    batch = batch_for_shader(_shader, 'TRIS', {"pos": rectangle_points(
        _posX, _posY, _width, _height)}, indices=rectangle_indices)
    _shader.bind()
    _shader.uniform_float("color", _color)
    bgl.glEnable(bgl.GL_BLEND)
    batch.draw(_shader)
    bgl.glDisable(bgl.GL_BLEND)

def remove_draw():
    handler = bpy.app.driver_namespace.get('draw')
    if handler:
        bpy.types.SpaceView3D.draw_handler_remove(handler, 'WINDOW')
        del bpy.app.driver_namespace['draw']
        redraw_regions()

#-----------------------------------------------------------------------------------------------------------------------

classes = (ToolHUD, Button, MoveMenu)

def register():

    bpy.types.WindowManager.toolhud_state = False

    for cls in classes:
        bpy.utils.register_class(cls)
    
def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)


