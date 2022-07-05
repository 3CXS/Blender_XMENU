import os
import bpy
from bpy.types import AddonPreferences
from bpy.props import   (StringProperty, FloatProperty, BoolProperty, EnumProperty)

from .functions import get_brush_mode

user_path = os.path.join(os.path.dirname(__file__))
brush_icons_path = os.path.join(user_path,"icons")

preview_collections = {}

#-----------------------------------------------------------------------------------------------------------------------

def get_tex_path(self, context):
    user_texture_path = bpy.context.preferences.addons[__package__].preferences.tex_path
    return user_texture_path

# PREVIEW -----------------------------------------------------------------------------------------

def get_tex_previews(self, context,tex_type="BRUSH"):  
    misc_icons = preview_collections["xm_misc_icons"]
    icon_id = misc_icons["icon_none"].icon_id
    
    enum_items = []
    enum_items.append(("None","","None",icon_id,0))    
    
    brush = get_brush_mode(self, context)

    texture_path = get_tex_path(self,context)
    category = brush.xm_tex_brush_categories 

    if brush != None:
        # Get the preview collection (defined in register func).
        if tex_type == "BRUSH":
            pcoll = preview_collections["xm_tex_previews"]
            final_texture_path = os.path.join(texture_path, category)
        elif tex_type == "STENCIL":
            pcoll = preview_collections["xm_stencil_previews"]
            final_texture_path = os.path.join(texture_path, context.scene.xm_tex_stencil_categories)   
        if os.path.exists(final_texture_path):
            # Scan the directory for png files
            image_paths = []
            for name in os.listdir(final_texture_path):
                if name.lower().endswith(".png") or name.lower().endswith(".jpg"):
                    image_paths.append(name)
            for i, name in enumerate(image_paths):
                
                # generates a thumbnail preview for a file.
                filepath = os.path.join(final_texture_path, name)
                
                if filepath not in pcoll:
                    thumb = pcoll.load(filepath, filepath, 'IMAGE')
            
            ### sort list of pathes with substring of the filename
            sorted_list = []
            for key in pcoll:
                sorted_list.append(key)
            sorted_list.sort(key= lambda x: os.path.basename(x))   
            
            for i,key in enumerate(sorted_list):
                if os.path.exists(key):
                    preview = pcoll[key]
                    icon_id = preview.icon_id
                    file_name = os.path.basename(key)
                    if tex_type == "BRUSH":        
                        if "xm_brush_img" in bpy.data.images and "xm_brush_tex" in bpy.data.textures:
                            img = bpy.data.images["xm_brush_img"]
                            tex = bpy.data.textures["xm_brush_tex"]
            
                        if category in key:
                            enum_items.append((file_name, file_name, file_name, icon_id, i+1))

                    elif tex_type == "STENCIL":        
                        if "xm_stencil_img" in bpy.data.images and "xm_stencil_tex" in bpy.data.textures:
                            img = bpy.data.images["xm_stencil_img"]
                            tex = bpy.data.textures["xm_stencil_tex"]
                               
                        if context.scene.xm_tex_stencil_categories:
                            enum_items.append((file_name, file_name, file_name, icon_id, i+1))

                else:
                    del(pcoll[key])    
           
    pcoll.my_previews = enum_items
    loaded_previews = []
    pcoll.my_previews_dir = final_texture_path
        
    return pcoll.my_previews

def get_brush_tex_previews(self,context):
    pcoll = preview_collections["xm_tex_previews"]
    if not context.window_manager.xm_brush_textures_loaded:
        context.window_manager.xm_brush_textures_loaded = True
        return get_tex_previews(self,context)
    else:
        return pcoll.my_previews

def get_stencil_tex_previews(self,context):
    pcoll = preview_collections["xm_stencil_previews"]
    if not context.window_manager.xm_stencil_textures_loaded:
        context.window_manager.xm_stencil_textures_loaded = True
        return get_tex_previews(self,context,tex_type="STENCIL")
    else:
        return pcoll.my_previews

def refresh_previews():
    for pcoll in preview_collections.values():
        bpy.utils.previews.remove(pcoll)
    preview_collections.clear()
    register_previews()

def unregister_previews():
    for pcoll in preview_collections.values():
        bpy.utils.previews.remove(pcoll)
    preview_collections.clear()


def register_previews():
    import bpy.utils.previews
    pcoll = bpy.utils.previews.new()
    pcoll.my_previews_dir = ""
    pcoll.my_previews = ()
       
    pcoll2 = bpy.utils.previews.new()
    pcoll2.my_previews_dir = ""
    pcoll2.my_previews = ()
    
    pcoll3 = bpy.utils.previews.new()
    pcoll3.my_previews_dir = ""
    pcoll3.my_previews = ()
    pcoll3.load("icon_none", os.path.join(brush_icons_path,"none.png"), 'IMAGE')
    
    preview_collections["xm_tex_previews"] = pcoll
    preview_collections["xm_stencil_previews"] = pcoll2
    preview_collections["xm_misc_icons"] = pcoll3



# SETUP BRUSH TEX -------------------------------------------------------------------------------------


def clear_brush_textures():
    for brush in bpy.data.brushes:
        if "xm" in brush:
            brush.texture = None
            brush.texture = None

def setup_brush_tex(img_path,tex_type="BRUSH"):
    if tex_type == "BRUSH":
        if "xm_brush_img" not in bpy.data.images:
            brush_img = bpy.data.images.new("xm_brush_img",1024,1024)
            if brush_img.packed_file != None:
                brush_img.unpack()
            brush_img.filepath = img_path
            brush_img.source = "FILE"
        else:
            brush_img = bpy.data.images["xm_brush_img"]
            if brush_img.packed_file != None:
                brush_img.unpack()
            brush_img.filepath = img_path
            brush_img.source = "FILE"
        
        if "xm_brush_tex" not in bpy.data.textures:
            brush_tex = bpy.data.textures.new("xm_brush_tex",type="IMAGE")
        else:
            brush_tex = bpy.data.textures["xm_brush_tex"]
        brush_tex.xm_invert_mask = brush_tex.xm_invert_mask

    elif tex_type == "STENCIL":
        if "xm_stencil_img" not in bpy.data.images:
            brush_img = bpy.data.images.new("xm_stencil_img",1024,1024)
            if brush_img.packed_file != None:
                brush_img.unpack()
            brush_img.filepath = img_path
            brush_img.source = "FILE"
        else:
            brush_img = bpy.data.images["xm_stencil_img"]
            if brush_img.packed_file != None:
                brush_img.unpack()
            brush_img.filepath = img_path
            brush_img.source = "FILE"

        if "xm_stencil_tex" not in bpy.data.textures:
            brush_tex = bpy.data.textures.new("xm_stencil_tex",type="IMAGE")
        else:
            brush_tex = bpy.data.textures["xm_stencil_tex"]
        brush_tex.xm_invert_mask = brush_tex.xm_invert_mask
    
    brush_tex.use_nodes = True
    node_tree = brush_tex.node_tree
    
    if "Image" not in node_tree.nodes:    
        image_node = node_tree.nodes.new('TextureNodeImage')    
    else:
        image_node = node_tree.nodes['Image']
    image_node.location = [0,0]
    image_node.image = brush_img

    if "Output" not in node_tree.nodes:
        output_node = node_tree.nodes.new('TextureNodeOutput')
    else:
        output_node = node_tree.nodes['Output']
    output_node.location = [500,0]

    node_tree.links.new(output_node.inputs['Color'],image_node.outputs['Image']) 
    
    return brush_tex

# COLOR RAMP -----------------------------------------------------------------------------------------

def _invert_ramp(self,context,tex_type="BRUSH"):
    mode = context.active_object.mode
    if ("xm_brush_tex" in bpy.data.textures and tex_type == "BRUSH") or ("xm_stencil_tex" in bpy.data.textures and tex_type == "STENCIL"):
        if self.xm_use_mask == True:
            if tex_type == "BRUSH":
                if mode == 'SCULPT':
                    if self.xm_invert_mask:
                        bpy.data.textures["xm_brush_tex"].color_ramp.elements[0].color = (1,1,1,1)
                        bpy.data.textures["xm_brush_tex"].color_ramp.elements[1].color = (0,0,0,1)
                    else:
                        bpy.data.textures["xm_brush_tex"].color_ramp.elements[0].color = (0,0,0,1)
                        bpy.data.textures["xm_brush_tex"].color_ramp.elements[1].color = (1,1,1,1)
                else:
                    if self.xm_invert_mask:
                        bpy.data.textures["xm_brush_tex"].color_ramp.elements[0].color = (1,1,1,1)
                        bpy.data.textures["xm_brush_tex"].color_ramp.elements[1].color = (1,1,1,0)
                    else:
                        bpy.data.textures["xm_brush_tex"].color_ramp.elements[0].color = (1,1,1,0)
                        bpy.data.textures["xm_brush_tex"].color_ramp.elements[1].color = (1,1,1,1)

            elif tex_type == "STENCIL":
                if self.xm_invert_stencil_mask:
                    bpy.data.textures["xm_brush_tex"].color_ramp.elements[0].color = (1,1,1,1)
                    bpy.data.textures["xm_brush_tex"].color_ramp.elements[1].color = (1,1,1,0)
                else:
                    bpy.data.textures["xm_brush_tex"].color_ramp.elements[0].color = (1,1,1,0)
                    bpy.data.textures["xm_brush_tex"].color_ramp.elements[1].color = (1,1,1,1)   
    
def _tonemap(self,context,tex_type="BRUSH"):
    mode = context.active_object.mode
    if (tex_type == "BRUSH" and "xm_brush_tex" in bpy.data.textures) or (tex_type == "STENCIL" and "xm_stencil_tex" in bpy.data.textures):
        if tex_type == "BRUSH":
            if mode == 'TEXTURE_PAINT':
                bpy.data.textures["xm_brush_tex"].color_ramp.elements[0].position = context.tool_settings.image_paint.brush.xm_ramp_tonemap_l
                bpy.data.textures["xm_brush_tex"].color_ramp.elements[1].position = context.tool_settings.image_paint.brush.xm_ramp_tonemap_r

            if mode == 'SCULPT':
                bpy.data.textures["xm_brush_tex"].color_ramp.elements[0].position = context.tool_settings.sculpt.brush.xm_ramp_tonemap_l
                bpy.data.textures["xm_brush_tex"].color_ramp.elements[1].position = context.tool_settings.sculpt.brush.xm_ramp_tonemap_r

            if mode == 'VERTEX_PAINT':
                bpy.data.textures["xm_brush_tex"].color_ramp.elements[0].position = context.tool_settings.vertex_paint.brush.xm_ramp_tonemap_l
                bpy.data.textures["xm_brush_tex"].color_ramp.elements[1].position = context.tool_settings.vertex_paint.brush.xm_ramp_tonemap_r

        elif tex_type == "STENCIL":
            bpy.data.textures["xm_brush_tex"].color_ramp.elements[0].position = context.tool_settings.image_paint.brush.xm_stencil_ramp_tonemap_l
            bpy.data.textures["xm_brush_tex"].color_ramp.elements[1].position = context.tool_settings.image_paint.brush.xm_stencil_ramp_tonemap_r


def _mute_ramp(self,context):
    brush = get_brush_mode(self, context)
    if "xm_brush_tex" in bpy.data.textures:
        if self.xm_use_mask == True:
            bpy.data.textures["xm_brush_tex"].use_color_ramp = True
        else:
            bpy.data.textures["xm_brush_tex"].use_color_ramp = False

    if brush != None:
        brush.xm_brush_texture = brush.xm_brush_texture


# PROPERTIES -------------------------------------------------------------------------------------

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
    brush = get_brush_mode(self, context)
    
    if brush != None:
        context.scene.xm_active_tex_brush_category = brush.xm_tex_brush_categories
        category = brush.xm_tex_brush_categories
        if self.xm_brush_texture != "None":
            img_path = os.path.join(texture_path,category,self.xm_brush_texture)
            brush_tex = setup_brush_tex(img_path)
            if brush == 'TEXTURE_PAINT':
                context.tool_settings.image_paint.brush.texture = brush_tex
            if brush == 'SCULPT':
                context.tool_settings.sculpt.brush.texture = brush_tex
            if brush == 'VERTEX_PAINT':
                context.tool_settings.vertex_paint.brush.texture = brush_tex  
        else:
            if brush == 'TEXTURE_PAINT':
                context.tool_settings.image_paint.brush.texture = None
            if brush == 'SCULPT':
                context.tool_settings.sculpt.brush.texture = None
            if brush == 'VERTEX_PAINT':
                context.tool_settings.vertex_paint.brush.texture = None

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

 
#-----------------------------------------------------------------------------------------

class XM_OT_RefreshPreviews(bpy.types.Operator):
    bl_idname = "xm.refresh_previews"
    bl_label = "Refresh Previews"
    bl_description = ""
    bl_options = {"REGISTER"}

    @classmethod
    def poll(cls, context):
        return True

    def execute(self, context):
        refresh_previews()
        context.window_manager.xm_brush_textures_loaded = False
        context.window_manager.xm_stencil_textures_loaded = False
        return {"FINISHED"}
 
#-----------------------------------------------------------------------------------------------------------------------

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
    bpy.types.Brush.xm_invert_mask = BoolProperty(default=False,update=invert_ramp)
    bpy.types.Texture.xm_invert_stencil_mask = BoolProperty(default=False,update=invert_stencil_ramp)
    bpy.types.Brush.xm_invert_stencil_mask = BoolProperty(default=False,update=invert_stencil_ramp)

    bpy.types.Brush.xm_ramp_tonemap_l = FloatProperty(default=0.0,min=0.0,max=1.0,update=tonemap)
    bpy.types.Brush.xm_ramp_tonemap_r = FloatProperty(default=1.0,min=0.0,max=1.0,update=tonemap)
    bpy.types.Brush.xm_stencil_ramp_tonemap_l = FloatProperty(default=0.0,min=0.0,max=1.0,update=tonemap_stencil)
    bpy.types.Brush.xm_stencil_ramp_tonemap_r = FloatProperty(default=1.0,min=0.0,max=1.0,update=tonemap_stencil)

    bpy.utils.register_class(XM_OT_RefreshPreviews)
   
def unregister():
    bpy.utils.unregister_class(XM_OT_RefreshPreviews)





