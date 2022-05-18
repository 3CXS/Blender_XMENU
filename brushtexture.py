import os
import bpy
from bpy.types import AddonPreferences

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

user_path = os.path.join(os.path.dirname(__file__))
brush_icons_path = os.path.join(user_path,"icons")

preview_collections = {}

#/////////////////////////////////////////////////////////////////////#
def get_tex_path(self, context):
    user_texture_path = bpy.context.preferences.addons[__package__].preferences.tex_path
    return user_texture_path

def get_brush_mode(self, context):
    mode = context.active_object.mode
    if mode == 'TEXTURE_PAINT':
        brush = context.tool_settings.image_paint.brush
    if mode == 'SCULPT':
        brush = context.tool_settings.sculpt.brush
    if mode == 'VERTEX_PAINT':
        brush = context.tool_settings.vertex_paint.brush
    if mode == 'WEIGHT_PAINT':
        brush = context.tool_settings.weight_paint.brush
    if mode == 'GEPNCIL_PAINT':
        brush = context.tool_settings.gpencil_paint.brush
    return brush

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

#/////////////////////////////////////////////////////////////////////#
class XM_OT_RefreshPreviews(bpy.types.Operator):
    bl_idname = "xm.refresh_previews"
    bl_label = "Refresh Previews"
    bl_description = ""
    bl_options = {"REGISTER"}

    @classmethod
    def poll(cls, context):
        return True

    def execute(self, context):
        #refresh_previews()
        context.window_manager.xm_brush_textures_loaded = False
        context.window_manager.xm_stencil_textures_loaded = False
        return {"FINISHED"}
 
#/////////////////////////////////////////////////////////////////////#

def register():
    bpy.utils.register_class(XM_OT_RefreshPreviews)
    
def unregister():
    bpy.utils.unregister_class(XM_OT_RefreshPreviews)





