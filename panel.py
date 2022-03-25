bl_info = {
    "name": "XMENU",
    "author": "",
    "version": (1, 0),
    "blender": (3, 10, 0),
    "location": "PROPERTIES > Scene > XMENU",
    "description": "Tool and Function Collection Panel",
    "warning": "",
    "doc_url": "",
    "category": "",
}

import bpy

#///////////////////////////////////////////////////////////////////////////////////////////////////
class XPanel(bpy.types.Panel):
    bl_label = "XMENU"
    bl_idname = "SCENE_PT_mypanel"
    bl_space_type = "PROPERTIES"
    bl_region_type = "WINDOW"
    bl_context = ""
    bl_order = 2000
    #bl_options = {'HIDE_HEADER','DEFAULT_CLOSED'}
    
    
    bpy.types.WindowManager.my_operator_toggle = bpy.props.BoolProperty()

    def draw(self, context):
        layout = self.layout
        toolsettings = context.tool_settings
    
        scene = context.scene
        wm = context.window_manager


        layout.label(text="BUTTONS:")

        label = "Operator ON" if wm.my_operator_toggle else "Operator OFF"
        layout.prop(wm, 'my_operator_toggle', text=label, toggle=True)


        layout.label(text="THIS:")

        row = layout.row(align=True)
        row.prop(scene, "frame_start")
        row.prop(scene, "frame_end")
        row.prop(toolsettings, "use_mesh_automerge", text="Auto Merge")

        split = layout.split()


        col = split.column()
        col.label(text="ONE:")
        col.scale_y = 2.0
        col.operator("view3d.view_selected")


        col = split.column(align=True)
        col.label(text="TWO:")
        col.scale_y = 2.0
        col.operator("view3d.toggle_xray")
    
        col = split.column(align=True)
        col.label(text="ICECREAM:")
        col.scale_y = 1.0
        col.operator(ViewCam.bl_idname)
        col.operator("object.select_all")
        col.operator(TogXray.bl_idname)

     
class TogXray(bpy.types.Operator):
    bl_idname = "xmenu.xray"
    bl_label = "X-RAY"        
    def execute(self, context):
        for window in bpy.context.window_manager.windows:
            screen = window.screen

            for area in screen.areas:
                if area.type == 'VIEW_3D':
                    override = {'window': window, 'screen': screen, 'area': area}
                    bpy.ops.view3d.toggle_xray(override)
                    break
        return {'FINISHED'}
    
    
class ViewCam(bpy.types.Operator):
    bl_idname = "xmenu.viewcam"
    bl_label = "ACTIVE CAM"        
    def execute(self, context):
        for window in bpy.context.window_manager.windows:
            screen = window.screen

            for area in screen.areas:
                if area.type == 'VIEW_3D':
                    override = {'window': window, 'screen': screen, 'area': area}
                    bpy.ops.view3d.view_camera(override)
                    break
        return {'FINISHED'}    
    
#///////////////////////////////////////////////////////////////////////////////////////////////////

classes = (XPanel, TogXray, ViewCam)

def register():
    for cls in classes:
        bpy.utils.register_class(cls)


def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)
    

if __name__ == "__main__":
    register()
