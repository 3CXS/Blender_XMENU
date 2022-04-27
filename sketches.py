       





        if bpy.context.mode == 'EDIT_MESH': 
            topsubrow.template_edit_mode_selection()
        else:      
            topsubrow.operator("object.shade_flat")
            topsubrow.operator("object.shade_smooth")

        toprow.separator_spacer()
                
        toprow.prop(ts, "use_snap")
        toprow.prop(ts, "use_transform_data_origin")
        toprow.separator_spacer()
        toprow.prop(scene, "my_enum", expand=True,)
        toprow.prop(scene, "frame_start")
        toprow.prop(scene, "frame_end")
        toprow.separator_spacer()
        grid = toprow.grid_flow(columns=6, align=True)
        for i in range(6):
            grid.template_icon(i+24)
        toprow.prop(ts, "use_mesh_automerge", text="Auto Merge")
        toprow.operator("xmenu.lockcam", depress=wm.lockcam_state)
        #text='LOCK', depress=wm.lockcam_state

        #///////////////////////////LEFT////////////////////////////////
        secondrow = layout.row()
        secondsplit = secondrow.split(factor=0.22, align=True)
        leftcol = secondsplit.column()       
        leftbox = leftcol.box()
        leftbox.ui_units_y = 0.6  
        #col.scale_y = 0.8 
        leftcol.operator("xmenu.persp", depress=wm.persp_state)
        leftcol.separator()
        leftcol.separator()
        box = leftcol.box()
        leftsubrow = box.row()
        leftsubrow.scale_y = 2 
        ds = icons.get("icon_draws")
        leftsubrow.operator("xmenu.frames", text="FRAME")
        leftsubrow.operator("xmenu.framea")
        
        #leftsubrow.template_palette(ptr, 'color')
        #leftsubrow.template_header()
        #layout.operator_enum("object.light_add", "type")

        rightcol = midsplit.column()
        rightbox = rightcol.box()
        rightbox.ui_units_y = 0.6
        row = rightcol.row()
        sub = row.column()
        sub.scale_y = 0.7 
        sub.ui_units_x = 4
        sub.template_color_picker(ptr, 'color', value_slider=True)
        subsub = sub.row(align=True)
        subsub.prop(ptr, 'color', text="")
        subsub.prop(ptr, 'secondary_color', text="")
        sub = row.column()
        grid = sub.grid_flow(columns=2, align=True)
        for i in range(8):
            grid.template_icon(i+1)
        
        sub = row.column()
        sub.scale_x = 0.6
        sub.label(text="ICECREAM:")

        sub.operator("xmenu.viewcam", depress=wm.viewcam_state)
        box = sub.box()
        box.operator("object.select_all")
        box.operator("xmenu.xray", icon="XRAY", depress=wm.xray_state)
        box.operator("xmenu.hud", icon="XRAY", depress=wm.hud_state)



    shades = top_row.row()
    shades.ui_units_x = 5
    if bpy.context.mode == 'EDIT_MESH': 
        shades.template_edit_mode_selection()
    else:      
        shades.operator("object.shade_flat")
        shades.operator("object.shade_smooth")