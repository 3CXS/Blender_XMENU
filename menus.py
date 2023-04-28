import bpy
from bpy.types import Menu

#-----------------------------------------------------------------------------------------------------------------------
class Menu1(bpy.types.Panel):
    bl_label = "Menu1"
    bl_idname = "OBJECT_PT_menu1"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'WINDOW'
    bl_context = "scene"

    def draw(self, context):

        layout = self.layout
        col = layout.column()

class Menu2(bpy.types.Panel):
    bl_label = "Menu2"
    bl_idname = "OBJECT_PT_menu2"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'WINDOW'
    bl_context = "scene"

    def draw(self, context):

        layout = self.layout
        col = layout.column()

#-----------------------------------------------------------------------------------------------------------------------

classes = (Menu1, Menu2) 

def register():
    for cls in classes:
        bpy.utils.register_class(cls)

def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)

