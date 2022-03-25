bl_info = {
    "name": "XMENU",
    "author": "cxs",
    "version": (1, 0),
    "blender": (3, 10, 0),
    "location": "PROPERTIES > Scene > XMENU",
    "description": "Tool and Function Collection Panel",
    "warning": "",
    "doc_url": "",
    "category": "Interface",
}

import bpy

#//UI///////////////////////////////////////////////////////////////////////////////////////////////
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
        
        ts = context.tool_settings
        scene = context.scene
        wm = context.window_manager
        ups = ts.unified_paint_settings
        ptr = ups if ups.use_unified_color else ts.image_paint.brush

        #///////////////////////////TOP/////////////////////////////////
        
        row = layout.row(align=True)
        row.template_edit_mode_selection()
        row.separator_spacer()
        row.ui_units_y = 1
        row.prop(scene, "frame_start")
        row.separator_spacer()
        row.prop(scene, "frame_end")
        grid = row.grid_flow(columns=12, align=True)
        for i in range(12):
            grid.template_icon(i+24)
        row.separator_spacer()
        row.prop(ts, "use_mesh_automerge", text="Auto Merge")
        
        #///////////////////////////LEFT////////////////////////////////
        
        split = layout.split()  
        col = split.column()
        col.label(text="---------------------------------------------------------------------------")  
        #col.scale_y = 0.8
        
        col.operator(Persp.bl_idname)
        col.separator()
        col.separator()
        box = col.box()
        row = box.row()
        row.operator(FrameS.bl_idname)
        row.operator(FrameA.bl_idname)
        row.template_header()
        row.template_palette(ptr, 'color')

                 
        #////////////////////////////MID///////////////////////////////    
        
        col = split.column()
        col.label(text="---------------------------------------------------------------------------")
          
        grid = col.grid_flow(columns=6, align=True)
        for i in range(12):
            grid.template_icon(i+12)

        label = "Operator ON" if wm.my_operator_toggle else "Operator OFF"
        col.prop(wm, 'my_operator_toggle', text=label, toggle=True)
        
        #////////////////////////////RIGHT//////////////////////////////
        
        col = split.column()
        col.label(text="---------------------------------------------------------------------------")
        row = col.row()
        row.scale_x = 1
        row.template_color_picker(ptr, 'color', value_slider=True)
        #col.prop(ptr, 'secondary_color')
        grid = row.grid_flow(columns=2, align=True)
        for i in range(8):
            grid.template_icon(i+1)
        
        col = row.column()
        col.scale_x = 0.6
        col.label(text="ICECREAM:")

        col.operator(ViewCam.bl_idname)
        box = col.box()
        box.operator("object.select_all")
        box.operator(TogXray.bl_idname)

        
        #///////////////////////////////////////////////////////////////

#bpy.data.scenes["Scene"].tool_settings.use_transform_data_origin
#bpy.data.objects["Cube"].use_mesh_mirror_x
#bpy.ops.wm.tool_set_by_id(name="builtin_brush.Grab")
#bpy.ops.sculpt.dynamic_topology_toggle()
#bpy.data.scenes["Scene"].tool_settings.sculpt.detail_size

#//FUNCT/////////////////////////////////////////////////////////////////////////////////////////////     

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
    
class FrameS(bpy.types.Operator):
    bl_idname = "xmenu.frames"
    bl_label = "FRAME"        
    def execute(self, context):
        for window in bpy.context.window_manager.windows:
            screen = window.screen

            for area in bpy.context.screen.areas:
                if area.type == 'VIEW_3D':
                    ctx = bpy.context.copy()
                    ctx['area'] = area
                    ctx['region'] = area.regions[-1]
                    bpy.ops.view3d.view_selected(ctx)
                    break
        return {'FINISHED'} 
    
class FrameA(bpy.types.Operator):
    bl_idname = "xmenu.framea"
    bl_label = "ALL"        
    def execute(self, context):
        for window in bpy.context.window_manager.windows:
            screen = window.screen

            for area in bpy.context.screen.areas:
                if area.type == 'VIEW_3D':
                    ctx = bpy.context.copy()
                    ctx['area'] = area
                    ctx['region'] = area.regions[-1]
                    bpy.ops.view3d.view_all(ctx)
                    break
        return {'FINISHED'} 

class Persp(bpy.types.Operator):
    bl_idname = "xmenu.persp"
    bl_label = "PERSP"        
    def execute(self, context):
        for window in bpy.context.window_manager.windows:
            screen = window.screen

            for area in screen.areas:
                if area.type == 'VIEW_3D':
                    override = {'window': window, 'screen': screen, 'area': area}
                    bpy.ops.view3d.view_persportho(override)
                    break
        return {'FINISHED'}   

    
#///////////////////////////////////////////////////////////////////////////////////////////////////

classes = (XPanel, TogXray, ViewCam, FrameS, FrameA, Persp)

def register():
    for cls in classes:
        bpy.utils.register_class(cls)


def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)
    

if __name__ == "__main__":
    register()
