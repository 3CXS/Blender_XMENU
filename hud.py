import bpy
import gpu
from gpu_extras.batch import batch_for_shader
import bgl
import blf
from bpy.types import Operator, AddonPreferences


xpos = 20
ypos = 200
l = 80
h = 30
vertices = (
    (xpos, ypos), (xpos+l, ypos),
    (xpos+l, ypos), (xpos+l, ypos+h),
    (xpos+l, ypos+h), (xpos, ypos+h),
    (xpos, ypos+h), (xpos, ypos)
    )
shader1 = gpu.shader.from_builtin('2D_UNIFORM_COLOR')
batch1 = batch_for_shader(shader1, 'LINES', {"pos":vertices})


vertices2 = [(0.0, 0.0, 0.0), (1.0, 0.0, 0.0),
    (0.0, 0.0, 0.0), (0.0, 1.0, 0.0),
    (0.0, 0.0, 0.0), (0.0, 0.0, 1.0)]
col2 = [(1.0, 0.0, 0.0, 1.0), (1.0, 0.0, 0.0, 1.0),
    (0.0, 1.0, 0.0, 1.0), (0.0, 1.0, 0.0, 1.0),
    (0.0, 0.0, 1.0, 1.0), (0.0, 0.0, 1.0, 1.0)]
shader2 = gpu.shader.from_builtin('3D_SMOOTH_COLOR')
batch2 = batch_for_shader(shader2, 'LINES', {"pos": vertices2, "color": col2})


font_info = {
    "font_id": 0,
    "handler": None,
}
#////////////////////////////////////////////////////////////////////////////////////////////#
#                                     MESH-FUNCTIONS                                         #
#////////////////////////////////////////////////////////////////////////////////////////////#

def polycount():
    verts, edges, polys = 0, 0, 0
    dg = bpy.context.evaluated_depsgraph_get()  # Getting the dependency graph
    for obj in bpy.context.selected_objects:

        obj = obj.evaluated_get(dg)
        # This gives the evaluated version of the object. Aka with all modifiers  
        mesh = obj.to_mesh()  # Turn it into the mesh data block we want

        count = len(mesh.polygons)
        #total += len(mesh.polygons)
        return count      

def mode():
    obj = bpy.context.active_object
    mode = obj.mode
    if bpy.context.object.mode == "OBJECT":
        cmode = "OBJECT MODE"
    elif bpy.context.object.mode == "EDIT":
        cmode = "EDIT MODE"
    elif bpy.context.object.mode == "SCULPT":
        cmode = "SCULPT MODE"
    elif bpy.context.object.mode == "VERTEX_PAINT":
        cmode= "VERTEXPAINT MODE"
    elif bpy.context.object.mode == "WEIGHT_PAINT":
        cmode = "WEIGHTPAINT MODE"
    elif bpy.context.object.mode == "TEXTURE_PAINT":
        cmode = "TEXTUREPAINT MODE"    
    elif bpy.context.object.mode == "POSE":
        cmode = "POSE MODE"   
    return cmode

def material():
    obj = bpy.context.active_object
    if obj.type in ['MESH', 'CURVE', 'FONT']:
        if obj.material_slots:
            if obj.active_material:
                mat = [(str(len(obj.material_slots))), (str(obj.active_material.name))]
            else:
                mat = [(str(len(obj.material_slots))), ('EmptySlot')]
            return mat

def uvcord():
    obj = bpy.context.active_object
    if obj.type == 'MESH':
        if obj.data.uv_layers:
            uv = [(str(len(obj.data.uv_layers))), 
                (str(obj.data.uv_layers[int(obj.data.uv_layers.active_index)].name))]
        return uv

def vertcolor():
    obj = bpy.context.active_object
    if obj.type == 'MESH':
        if obj.data.vertex_colors:
            vertcol = [(str(len(obj.data.vertex_colors))), 
                    (str(obj.data.vertex_colors[int(obj.data.vertex_colors.active_index)].name))]
        return vertcol

def activetool():
    #obj = bpy.context.active_object
    #toolsettings = bpy.context.tool_settings
    #sculpt = toolsettings.sculpt
    #context_tool = bpy.context.scene.tool_settings.sculpt

    #brush = bpy.context.tool_settings.sculpt.brush
    #capabilities = brush.sculpt_capabilities
    #ups = bpy.context.tool_settings.unified_paint_settings
    tool = bpy.context.workspace.tools.from_space_view3d_mode(bpy.context.mode)
    idname = str(tool.idname.upper())
    toolname = idname.split('.')[-1]
    return toolname


#////////////////////////////////////////////////////////////////////////////////////////////#
#                                           DRAW                                             #
#////////////////////////////////////////////////////////////////////////////////////////////#



def draw_callback_2d(self, context):

    for region in bpy.context.area.regions:
        if region.type == "WINDOW":
            view_width = region.width
            view_height = region.height
        if region.type == 'TOOLS':
            tools_width = region.width
        if region.type == 'TOOL_HEADER':
            header_height = region.height
          
    font_id = font_info["font_id"]
    obj = bpy.context.active_object


    dpi = bpy.context.preferences.addons[__package__].preferences.hud_dpi
    dpi_scale = 0.014*dpi

    blf.position(font_id, tools_width+20*dpi_scale, view_height-90*dpi_scale, 0)
    blf.size(font_id, 28, dpi)
    blf.color(font_id, 1, 1, 1, 1)
    cmode = mode()
    blf.draw(font_id, cmode)

    if obj.type in ['MESH', 'CURVE', 'FONT']:
        if obj.material_slots:
            blf.position(font_id, tools_width+20*dpi_scale, view_height-120*dpi_scale, 0)
            blf.size(font_id, 12, dpi)
            blf.color(font_id, 1, 1, 1, 1)
            blf.draw(font_id, "MAT:")
            if obj.active_material:
                blf.position(font_id, tools_width+20*dpi_scale, view_height-140*dpi_scale, 0)
                blf.size(font_id, 16, dpi)
                blf.color(font_id, 0, 0.6, 1, 1)
                mat = material()
                blf.draw(font_id, str(mat[0]))

                blf.position(font_id, tools_width+40*dpi_scale, view_height-140*dpi_scale, 0)
                blf.size(font_id, 16, dpi)
                blf.color(font_id, 1, 1, 1, 1)  
                mat = material()
                blf.draw(font_id, str(mat[1]))
        if obj.type == 'MESH':
            if obj.data.uv_layers:
                blf.position(font_id, tools_width+20*dpi_scale, view_height-160*dpi_scale, 0)
                blf.size(font_id, 12, dpi)
                blf.color(font_id, 1, 1, 1, 1)
                blf.draw(font_id, "UV:")

                blf.position(font_id, tools_width+20*dpi_scale, view_height-180*dpi_scale, 0)
                blf.size(font_id, 16, dpi)
                blf.color(font_id, 0, 0.6, 1, 1)
                uv = uvcord()
                blf.draw(font_id, str(uv[0]))

                blf.position(font_id, tools_width+40*dpi_scale, view_height-180*dpi_scale, 0)
                blf.size(font_id, 16, dpi)
                blf.color(font_id, 1, 1, 1, 1)  
                uv = uvcord()
                blf.draw(font_id, str(uv[1]))

    if cmode == 'SCULPT MODE':
        pass

    font_id = font_info["font_id"]
    blf.position(font_id, tools_width+20*dpi_scale, header_height+20*dpi_scale, 0)
    blf.size(font_id, 28, dpi)
    blf.color(font_id, 0, 0.7, 1, 1)
    toolname = activetool()
    blf.draw(font_id, toolname)

    blf.position(font_id, view_width-90*dpi_scale, header_height+50*dpi_scale, 0)
    blf.size(font_id, 12, dpi)
    blf.color(font_id, 1, 1, 1, 1)
    blf.draw(font_id, 'POLYCOUNT')

    blf.position(font_id, view_width-90*dpi_scale, header_height+20*dpi_scale, 0)
    blf.size(font_id, 20, dpi)
    blf.color(font_id, 0, 0.7, 1, 1)
    count = polycount()
    blf.draw(font_id, str(count))

    shader1.bind()
    shader1.uniform_float("color", (1, 1, 1, 1.0))
    batch1.draw(shader1)

def draw_callback_3d(self, context):
    bgl.glLineWidth(2.5)
    shader2.bind()
    batch2.draw(shader2)

def remove_draw():
    handler1 = bpy.app.driver_namespace.get('draw1')
    handler2 = bpy.app.driver_namespace.get('draw2')
    if handler1:
        bpy.types.SpaceView3D.draw_handler_remove(handler1, 'WINDOW')
        del bpy.app.driver_namespace['draw1']
        redraw_regions()
    if handler2:
        bpy.types.SpaceView3D.draw_handler_remove(handler2, 'WINDOW')
        del bpy.app.driver_namespace['draw2']
        redraw_regions()

def redraw_regions():
    for area in bpy.context.window.screen.areas:
        if area.type == 'VIEW_3D':
            for region in area.regions:
                if region.type == 'WINDOW':
                    region.tag_redraw()

#////////////////////////////////////////////////////////////////////////////////////////////#
#                                           CLASS                                            #
#////////////////////////////////////////////////////////////////////////////////////////////#

class HUD(bpy.types.Operator):
    bl_idname = "xmenu.hud"
    bl_label = "HUD" 
    bpy.types.WindowManager.hud_state = bpy.props.BoolProperty(default = False)
    def execute(self, context):
        handler1 = bpy.app.driver_namespace.get('draw1')
        handler2 = bpy.app.driver_namespace.get('draw2')
        hud_activate = bpy.context.preferences.addons['XMENU'].preferences.hud_activate
        #if hud_activate == True:
        if context.window_manager.hud_state == False:
            context.window_manager.hud_state = True
            handler1 = bpy.types.SpaceView3D.draw_handler_add(
                draw_callback_2d, (None, None), 'WINDOW', 'POST_PIXEL')
            dns = bpy.app.driver_namespace
            dns['draw1'] = handler1

            handler2 = bpy.types.SpaceView3D.draw_handler_add(
                draw_callback_3d, (None, None), 'WINDOW', 'POST_VIEW')
            dns = bpy.app.driver_namespace
            dns['draw2'] = handler2

            redraw_regions()
        else:
            context.window_manager.hud_state = False
            remove_draw()
            redraw_regions()
        return {'FINISHED'}

#////////////////////////////////////////////////////////////////////////////////////////////#
def register():
    bpy.utils.register_class(HUD)

def unregister():
    bpy.utils.unregister_class(HUD)


