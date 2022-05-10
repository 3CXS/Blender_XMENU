import os
import bpy
from bpy.props import   (
                        CollectionProperty, 
                        StringProperty, 
                        PointerProperty, 
                        IntProperty, 
                        FloatProperty, 
                        BoolProperty, 
                        EnumProperty, 
                        FloatVectorProperty, 
                        IntVectorProperty
                        )

from .functions import _tonemap, _invert_ramp, _mute_ramp, setup_brush_tex 
from .brushtexture import get_tex_path, get_tex_previews, get_brush_tex_previews, get_stencil_tex_previews, get_brush_mode


def invert_ramp(self,context):
    context.window_manager.xm_brush_textures_loaded = False
    context.window_manager.xm_stencil_textures_loaded = False
    
    _invert_ramp(self,context,tex_type="BRUSH")
    
def invert_stencil_ramp(self,context):
    context.window_manager.xm_brush_textures_loaded = False
    context.window_manager.xm_stencil_textures_loaded = False
    
    _invert_ramp(self,context,tex_type="STENCIL")

def tonemap(self,context):
    context.window_manager.xm_brush_textures_loaded = False
    context.window_manager.xm_stencil_textures_loaded = False
    
    _tonemap(self,context)

def tonemap_stencil(self,context):
    context.window_manager.xm_brush_textures_loaded = False
    context.window_manager.xm_stencil_textures_loaded = False
    
    _tonemap(self,context,tex_type="STENCIL")

def mute_ramp(self,context): 
    context.window_manager.xm_brush_textures_loaded = False
    context.window_manager.xm_stencil_textures_loaded = False
    
    _mute_ramp(self,context)  

IMAGES = []
def get_brush_textures(self,context):
    global IMAGES
    IMAGES = []
    IMAGES.append(("None","None","None","NONE",0))
    for i,image in enumerate(bpy.data.images):
        if "xm" in image:
            icon_id = bpy.types.UILayout.icon(image)    
            IMAGES.append((image.name,image.name,image.name,icon_id,i+1))
    return IMAGES

CATEGORIES = []
def get_category_dirs(self,context):
    texture_path = get_tex_path(self,context)
    global CATEGORIES
    CATEGORIES = [] 
    i = 0 
    for name in os.listdir(texture_path):
        if os.path.isdir(os.path.join(texture_path,name)):
            # CATEGORIES.append((name,name,name,"None",id_from_string(name)))
            CATEGORIES.append((name,name,name,"None",i))
            i += 1
    if i == 0:
        CATEGORIES.append(("Default Category","Default Category","Default Category"))        
    return CATEGORIES

def set_texture(self,context):
    context.window_manager.xm_brush_textures_loaded = False
    context.window_manager.xm_stencil_textures_loaded = False

    texture_path = get_tex_path(self,context)

    brush = get_brush_mode(self, context)

    if brush != None:  
        context.scene.xm_active_tex_brush = str(self.xm_brush_texture)
        category = brush.xm_tex_brush_categories
        if self.xm_brush_texture != "None":
            img_path = os.path.join(texture_path,category,self.xm_brush_texture)
            brush_tex = setup_brush_tex(img_path)
            img = brush_tex.node_tree.nodes["Image"].image
            img_aspect_ratio = img.size[0]/img.size[1]
            brush.texture = brush_tex
            brush.texture_slot.scale[0] = 1
            brush.texture_slot.scale[1] = img_aspect_ratio
            brush.texture_slot.scale[2] = 1
        else:
            brush.texture = None
            brush.texture_slot.scale[0] = 1
            brush.texture_slot.scale[1] = 1
            brush.texture_slot.scale[2] = 1

    _invert_ramp(brush,context) 
    context.window_manager.xm_brush_textures_loaded = False
    context.window_manager.xm_stencil_textures_loaded = False

def set_stencil_texture(self,context):
    context.window_manager.xm_brush_textures_loaded = False
    context.window_manager.xm_stencil_textures_loaded = False
    texture_path = get_tex_path(self,context)  
    brush = context.tool_settings.image_paint.brush
    if brush != None:
        category = context.scene.xm_tex_stencil_categories
        if self.xm_stencil_texture != "None":
            img_path = os.path.join(texture_path,category,self.xm_stencil_texture)
            brush_tex = setup_brush_tex(img_path,tex_type="STENCIL")
            context.tool_settings.image_paint.brush.mask_texture = brush_tex
        else:
            context.tool_settings.image_paint.brush.mask_texture = None

    if brush.mask_texture != None:
        img = brush.mask_texture.node_tree.nodes["Image"].image
        ratio = img.size[1]/img.size[0]
        brush.mask_stencil_dimension = [256,256*ratio]

    _invert_ramp(context.tool_settings.image_paint.brush,context,tex_type="STENCIL")

def refresh_brush_category(self,context):
    context.window_manager.xm_brush_textures_loaded = False
    context.window_manager.xm_stencil_textures_loaded = False
    texture_path = get_tex_path(self,context)
    brush = context.tool_settings.image_paint.brush
    
    if brush != None:
        context.scene.xm_active_tex_brush_category = brush.xm_tex_brush_categories
        category = brush.xm_tex_brush_categories
        if self.xm_brush_texture != "None":
            img_path = os.path.join(texture_path,category,self.xm_brush_texture)
            brush_tex = setup_brush_tex(img_path)
            context.tool_settings.image_paint.brush.texture = brush_tex  
        else:
            context.tool_settings.image_paint.brush.texture = None  
    bpy.ops.xm.refresh_previews()

def refresh_stencil_category(self,context):
    context.window_manager.xm_stencil_textures_loaded = False
    context.window_manager.xm_brush_textures_loaded = False
    texture_path = get_tex_path(self,context)
    context.scene.xm_active_stencil_category = context.scene.xm_tex_stencil_categories
    brush = context.tool_settings.image_paint.brush
    
    if brush != None:
        category = context.scene.xm_tex_stencil_categories
        if brush.xm_stencil_texture != "None":
            img_path = os.path.join(texture_path,category,brush.xm_stencil_texture)
            brush_tex = setup_brush_tex(img_path,tex_type="STENCIL")
            context.tool_settings.image_paint.brush.mask_texture = brush_tex  
        else:
            context.tool_settings.image_paint.brush.mask_texture = None            
    bpy.ops.xm.refresh_previews()

def register():
    bpy.types.WindowManager.xm_brush_textures_loaded = BoolProperty(default=False)
    bpy.types.WindowManager.xm_stencil_textures_loaded = BoolProperty(default=False)

    bpy.types.Brush.xm_brush_texture = EnumProperty(items=get_brush_tex_previews,update=set_texture)
    bpy.types.Brush.xm_stencil_texture = EnumProperty(items=get_stencil_tex_previews,update=set_stencil_texture)
    bpy.types.Brush.xm_tex_brush_categories = EnumProperty(items=get_category_dirs,name="Texture Categories",update=refresh_brush_category)
    bpy.types.Scene.xm_tex_stencil_categories = EnumProperty(items=get_category_dirs,name="Stencil Categories",update=refresh_stencil_category)
    bpy.types.Scene.xm_active_tex_brush_category = StringProperty(default="None")
    bpy.types.Scene.xm_active_stencil_category = StringProperty(default="None")
    bpy.types.Scene.xm_active_tex_brush = StringProperty(default="None")

    bpy.types.Texture.xm_use_mask = BoolProperty(default=False,update=mute_ramp)
    bpy.types.Brush.xm_use_mask = BoolProperty(default=False,update=mute_ramp)

    bpy.types.Texture.xm_invert_mask = BoolProperty(default=False,update=invert_ramp)
    bpy.types.Brush.xm_invert_mask = BoolProperty(default=True,update=invert_ramp)
    bpy.types.Texture.xm_invert_stencil_mask = BoolProperty(default=False,update=invert_stencil_ramp)
    bpy.types.Brush.xm_invert_stencil_mask = BoolProperty(default=False,update=invert_stencil_ramp)

    bpy.types.Brush.xm_ramp_tonemap_l = FloatProperty(default=0.0,min=0.0,max=1.0,update=tonemap)
    bpy.types.Brush.xm_ramp_tonemap_r = FloatProperty(default=1.0,min=0.0,max=1.0,update=tonemap)
    bpy.types.Brush.xm_stencil_ramp_tonemap_l = FloatProperty(default=0.0,min=0.0,max=1.0,update=tonemap_stencil)
    bpy.types.Brush.xm_stencil_ramp_tonemap_r = FloatProperty(default=1.0,min=0.0,max=1.0,update=tonemap_stencil)