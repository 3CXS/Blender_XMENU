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

def draw_callback(self, context, x=0, y=0):

    font_id = 0

    # menu bg
    Draw_2D_Rectangle(x, y-200, 140, 200, [0.1, 0.1, 0.1, 0.9])
    Draw_2D_Rectangle(x, y-5, 140, 4, [0.2, 0.5, 0.8, 1.0])

    # label
    blf.position(font_id, x, y-16, 0)
    blf.size(font_id, 14, 72)
    blf.color(font_id, 1, 1, 1, 1)
    text = 'xyx'
    blf.draw(font_id, text)

    # tools
    bpy.ops.xm.button(x=x, y=y-30, w=50, h=20, text='XX01', cmd=0)
    bpy.ops.xm.button(x=x+60, y=y-30, w=50, h=20, text='XX02', cmd=1)
    bpy.ops.xm.button(x=x, y=y-60, w=50, h=20, text='XX03', cmd=2)
    bpy.ops.xm.button(x=x+60, y=y-60, w=50, h=20, text='XX04', cmd=3)


#-- MODAL -----------------------------------------------------------------------------------------

class ToolHUD(bpy.types.Operator):
    bl_idname = "xm.toolhud"
    bl_label = "HUD"

    bpy.types.WindowManager.toolhud_state = bpy.props.BoolProperty(default = False)
    bpy.types.WindowManager.leftclick = bpy.props.BoolProperty(default = False)  

    mouse_pos: bpy.props.IntVectorProperty(size=2)
    width: bpy.props.IntProperty()
    hight: bpy.props.IntProperty()
    def modal(self, context, event):

        mouse_x = self.mouse_pos[0]
        mouse_y = self.mouse_pos[1]



        if bpy.types.WindowManager.toolhud_state == True:
            if mouse_x > left and mouse_x < right and mouse_y < top and mouse_y > bottom :
                if event.type == 'LEFTMOUSE':
                    if event.value == 'PRESS':
                        self.report({'INFO'}, "LMB")
                        bpy.types.WindowManager.leftclick = True
                    elif event.value == 'RELEASE':
                        bpy.types.WindowManager.leftclick = False
            else:
                return {'CANCELLED'}
        else:
            self.report({'INFO'}, "MODAL OFF")
            return {'CANCELLED'}

        return {'RUNNING_MODAL'}

    def invoke(self, context, event):

        self.mouse_pos = event.mouse_x, event.mouse_y

        mouse_x = self.mouse_pos[0]
        mouse_y = self.mouse_pos[1]

        left = mouse_x 
        right = left + 140
        top = mouse_y
        bottom = mouse_y - 200

        self.report({'INFO'}, "MODAL ON")
        self.execute(context)
        context.window_manager.modal_handler_add(self)

        return {'RUNNING_MODAL'}

    def execute(self, context):

        mouse_x = self.mouse_pos[0]
        mouse_y = self.mouse_pos[1]

        self.report({'INFO'}, "Mouse coords are %d %d" % (mouse_x, mouse_y))

        handler = bpy.app.driver_namespace.get('draw')

        if bpy.types.WindowManager.toolhud_state == False:
            bpy.types.WindowManager.toolhud_state = True

            handler = bpy.types.SpaceView3D.draw_handler_add(
                draw_callback, (None, None, mouse_x, mouse_y), 'WINDOW', 'POST_PIXEL')

            dns = bpy.app.driver_namespace
            dns['draw'] = handler

        else:
            bpy.types.WindowManager.toolhud_state = False
            remove_draw()

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
    text: bpy.props.StringProperty()
    cmd: bpy.props.IntProperty()

    mouse_pos: bpy.props.IntVectorProperty(size=2)

    is_hovered:bpy.props.BoolProperty(default=False)
    bt_state:bpy.props.BoolProperty(default=False)

    def invoke(self, context, event):

        self.mouse_pos = event.mouse_x, event.mouse_y

        self.execute(context)

    def execute(self, context):
        #context = bpy.context
        #Tools = toolset()

        mouse_x = self.mouse_pos[0]
        mouse_y = self.mouse_pos[1]

        left = self.x
        right = left + self.w
        top = self.y
        bottom = self.y - self.h

        
        if mouse_x > left and mouse_x < right and mouse_y < top and mouse_y > bottom :
            self.is_hovered = True
        else:
            self.is_hovered = False
  
        if self.is_hovered == True and bpy.types.WindowManager.leftclick == True:
            self.bt_state != self.bt_state
            self.report({'INFO'}, 'XYYX')
            #self.report({'INFO'}, self.bt_state)
            #update_toolset()
            #bpy.ops.xm.settool(tool_index = self.cmd)

        if self.bt_state == True:
            Draw_2D_Rectangle(self.x, self.y, self.w, self.h, [0.2, 0.5, 0.8, 1.0])

        else:
            Draw_2D_Rectangle(self.x, self.y, self.w, self.h, [0.5, 0.5, 0.5, 1.0])

        blf.position(0, self.x, self.y, 0)
        blf.size(0, 12, 72)
        blf.color(1, 1, 1, 1, 1)
        blf.draw(0, self.text)

        if self.is_hovered == True:
            Draw_2D_Rectangle(self.x, self.y, self.w, self.h, [1, 1, 1, 0.1])

        return {'FINISHED'}

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

classes = (ToolHUD, Button)

def register():


    bpy.types.WindowManager.toolhud_state = False

    for cls in classes:
        bpy.utils.register_class(cls)
    
def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)


