import bpy

from .functions import LockCam


class XPanel(bpy.types.Panel):
    bl_idname = "xpanel"
    bl_label = "X-PANEL"
    bl_space_type = "PROPERTIES"
    bl_region_type = "WINDOW"
    bl_context = "scene"
    bl_order = 2000
    #bl_options = {'HIDE_HEADER','DEFAULT_CLOSED'}
    

    def draw(self, context):
        
        layout = self.layout
        ts = context.tool_settings
        scene = context.scene
        view = context.space_data
        wm = context.window_manager
        ups = ts.unified_paint_settings
        ptr = ups if ups.use_unified_color else ts.image_paint.brush
        tool_mode = context.mode

        #///////////////////////////TOP/////////////////////////////////
        
        top = layout.row(align=False)
        split = top.split()
        #row.ui_units_y = 1
        col = split.column()
        row = col.row()
        row.ui_units_x = 5
        if bpy.context.mode == 'EDIT_MESH': 
            row.template_edit_mode_selection()
        else:      
            row.operator("object.shade_flat")
            row.operator("object.shade_smooth")

        top.separator_spacer()
        
        
        top.prop(ts, "use_snap")
        top.prop(ts, "use_transform_data_origin")
        top.separator_spacer()
        top.prop(scene, "frame_start")
        top.prop(scene, "frame_end")
        grid = top.grid_flow(columns=12, align=True)
        for i in range(12):
            grid.template_icon(i+24)
        top.separator_spacer()
        top.prop(ts, "use_mesh_automerge", text="Auto Merge")
        top.operator(LockCam.bl_idname, text='LOCK', depress=wm.lockcam_state)
   
        #///////////////////////////LEFT////////////////////////////////
        row = layout.row()
        split = row.split(factor=0.2, align=True)
        col = split.column()
        col.box()  
        #col.scale_y = 0.8 
        col.operator(Persp.bl_idname, text='', icon='XRAY', depress=wm.persp_state)
        col.separator()
        col.separator()
        box = col.box()
        row = box.row()
        row.operator(FrameS.bl_idname)
        row.operator(FrameA.bl_idname)
        row.template_header()
        row.template_palette(ptr, 'color')
        #layout.operator_enum("object.light_add", "type")
   
        #////////////////////////////MID/////////////////////////////// 

        col = split.column()
        split = col.split(factor=0.64, align=True)
        col = split.column()
        col.box()  
        grid = col.grid_flow(columns=6, align=True)
        for i in range(12):
            grid.template_icon(i+12)
            
  
        #col.prop(scene, "my_enum", expand=True,)

  
        #////////////////////////////RIGHT//////////////////////////////

        col = split.column()
        col.box()
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

        col.operator(ViewCam.bl_idname, text='ActiveCAM', depress=wm.viewcam_state)
        box = col.box()
        box.operator("object.select_all")
        box.operator(Xray.bl_idname, text='', icon='XRAY', depress=wm.xray_state)

        
        #///////////////////////////////////////////////////////////////
        box = layout.box()
        box.ui_units_y = 12
        box = layout.box()

def register() :
    bpy.utils.register_class(XPanel)

def unregister() :
    bpy.utils.unregister_class(XPanel)