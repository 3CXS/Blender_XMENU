import bpy
from bpy.types import Menu
from .menuitems import ModeSelector, VertexGroups, ShadingMode, Transforms, UVTexture
from .functions import tool_bt, funct_bt


class ModesMenu(bpy.types.Menu):
    bl_label = ""
    bl_idname = "OBJECT_MT_modes_menu"

    def draw(self, context):
        layout = self.layout

        pie = layout.menu_pie()

        col = pie.column()
        col.label(text='')

        col = pie.column()
        col.label(text='')

        col = pie.column()
        col.scale_y = 1.5
        ModeSelector(self, context, col)

        col = pie.column()
        ShadingMode(self, context, col)

class FileMenu(bpy.types.Menu):
    bl_label = ""
    bl_idname = "OBJECT_MT_file_menu"

    def draw(self, context):
        layout = self.layout

        pie = layout.menu_pie()

        col = pie.column()
        col.operator("wm.save_mainfile", icon='FILE_TICK', text="SAVE")
        col.operator("wm.save_as_mainfile", text="SAVE AS")

        col = pie.column()
        col.label(text='')
        col.operator("wm.link", text="SCREEN")

        col = pie.column()
        col.popover("OBJECT_PT_import_panel")
        sub = col.row(align=True)
        sub.operator("wm.link", icon='LINK_BLEND', text="LINK")
        sub.operator("wm.append", icon='APPEND_BLEND', text="APND")

        col = pie.column()
        sub = col.row(align=True)
        sub.operator("wm.open_mainfile", text="OPEN")
        sub.menu("TOPBAR_MT_file_open_recent", text="RECENT")

class PropMenu(bpy.types.Panel):
    bl_label = "MAIN"
    bl_idname = "OBJECT_PT_main_menu"
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = "material"
    bl_order = 1000
    bl_options = {'DEFAULT_CLOSED',}

    def draw(self, context):
        layout = self.layout
        if context.mode == 'OBJECT':
            col = layout.column()
            col.menu_contents("VIEW3D_MT_Material")
            UVTexture(self, context, parent=col)
        if context.mode == 'EDIT_MESH':
            col = layout.column()
            VertexGroups(self, context, parent=col)
            col.menu_contents("VIEW3D_MT_Material")
            UVTexture(self, context, parent=col)

class ToolMenu(bpy.types.Panel):
    bl_idname = "OBJECT_PT_tool_menu"
    bl_label = "TOOLS"
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = "scene"
    bl_order = 1000
    bl_options = {'DEFAULT_CLOSED',}

    def draw(self, context):
        layout = self.layout
        layout.use_property_split = False
        layout.use_property_decorate = False

        col = layout.column()

        if context.mode == 'EDIT_MESH':

            sub = col.row()
            subsub = sub.column()
            subsub.scale_x=2.5
            subsub.template_edit_mode_selection()
            sub.separator(factor=3)
            funct_bt(parent=sub, cmd='xray', tog=True, w=2.4, h=1, label='', icon="XRAY")

            col.separator(factor=1)
            sub = col.column()
            grid = sub.grid_flow(row_major=True, columns=4, align=True)
            grid.ui_units_x = 6
            tool_bt(parent=grid, cmd=0, w=2, h=1.2, text=False, icon='LARGE')
            tool_bt(parent=grid, cmd=1, w=2, h=1.2, text=False, icon='LARGE')
            tool_bt(parent=grid, cmd=2, w=2, h=1.2, text=False, icon='LARGE')
            tool_bt(parent=grid, cmd=3, w=2, h=1.2, text=False, icon='LARGE')

            sub.separator(factor=2)
            grid = sub.grid_flow(row_major=True, columns=4)
            tool_bt(parent=grid, cmd=20, w=2, h=1.4, text=True, icon='LARGE')
            subsub = grid.column()
            subsub.ui_units_x = 2
            subsub.label(text=' ')
            tool_bt(parent=grid, cmd=24, w=2, h=1.4, text=True, icon='LARGE')
            tool_bt(parent=grid, cmd=22, w=2, h=1.4, text=True, icon='LARGE')

            tool_bt(parent=grid, cmd=19, w=2, h=1.4, text=True, icon='LARGE')
            tool_bt(parent=grid, cmd=18, w=2, h=1.4, text=True, icon='LARGE')
            tool_bt(parent=grid, cmd=15, w=2, h=1.4, text=True, icon='LARGE')
            tool_bt(parent=grid, cmd=16, w=2, h=1.4, text=True, icon='LARGE')
            sub.separator(factor=2)

            grid = sub.grid_flow(row_major=True, columns=4, align=True)
            tool_bt(parent=grid, cmd=29, w=2, h=1, text=False, icon='OFF')
            tool_bt(parent=grid, cmd=30, w=2, h=1, text=False, icon='OFF')
            subsub = grid.column()
            subsub.ui_units_x = 2
            subsub.label(text='X')
            tool_bt(parent=grid, cmd=27, w=2, h=1, text=False, icon='OFF')

            tool_bt(parent=grid, cmd=31, w=2, h=1, text=False, icon='OFF')
            tool_bt(parent=grid, cmd=32, w=2, h=1, text=False, icon='OFF')
            tool_bt(parent=grid, cmd=35, w=2, h=1, text=False, icon='OFF')
            tool_bt(parent=grid, cmd=34, w=2, h=1, text=False, icon='OFF')

            sub.separator(factor=2)
            sub = col.row(align=True)

            subsub = sub.column()
            subsubsub = subsub.row()
            item = subsubsub.column(align=True)
            item.scale_y=0.8
            item.operator('mesh.flip_normals', text='FLIP')

            item = subsubsub.column(align=True)
            item.scale_y=0.8
            item.operator('mesh.remove_doubles', text='CLEAN')
            item.operator('mesh.delete_loose', text='LOOSE')
            item.operator('mesh.fill_holes', text='FILL')

            subsub.separator(factor=0.4)
            item = subsub.row(align=True)
            item.scale_y=0.8
            item.operator('mesh.symmetrize', text='SYM')
            op = item.operator('transform.mirror', text='MIRROR')
            op.orient_type='GLOBAL'
            op.constraint_axis=(True, False, False)

            #subsub.separator(factor=0.2)
            item = subsub.row(align=True)
            item.scale_y=0.8
            item.operator('mesh.split', text='SPLIT')
            item.operator('mesh.duplicate_move', text='DUB')

            #subsub.separator(factor=0.2)
            item = subsub.row(align=True)
            item.scale_y=0.8
            item.operator('mesh.separate', text='SLCT').type='SELECTED'
            item.operator('mesh.separate', text='MAT').type='MATERIAL'
            item.operator('mesh.separate', text='LSE').type='LOOSE'

            subsub.separator(factor=0.2)
            item = subsub.row(align=True)
            item.scale_y=0.8
            item.operator('uv.smart_project', text="AUTO")
            item.operator('uv.unwrap', text="UNWRP")

            sub.separator(factor=2)
            subsub = sub.column(align=True)
            #subsub.ui_units_x = 8
            subsub.operator('mesh.mark_sharp', text='SHARP')
            op = subsub.operator('mesh.mark_sharp', text='CLEAR')
            op.clear = True

            subsub.separator(factor=2)
            subsub = subsub.column(align=True)
            op = subsub.operator('mesh.mark_seam', text='SEAM')
            op = subsub.operator('mesh.mark_seam', text='CLEAR')
            op.clear = True




        if context.mode == 'OBJECT':
            sub = col.row(align=True)
            tool_bt(parent=sub, cmd=0, w=2, h=1.4, text=False, icon='LARGE')
            tool_bt(parent=sub, cmd=1, w=2, h=1.4, text=False, icon='LARGE')
            tool_bt(parent=sub, cmd=2, w=2, h=1.4, text=False, icon='LARGE')
            tool_bt(parent=sub, cmd=3, w=2, h=1.4, text=False, icon='LARGE')

            col.separator(factor=1)
            sub = col.row(align=True)
            subsub = sub.column()
            subsub.ui_units_x = 1.2
            subsub.label(text='')
            subsub = sub.column()
            Transforms(self, context, parent=subsub)
            subsub = sub.column()
            subsub.ui_units_x = 1.2
            subsub.label(text='')

            col.separator(factor=1)
            sub = col.row(align=True)
            #sub.ui_units_x = 4
            sub.operator('mesh.primitive_plane_add', text="", icon='MESH_PLANE')
            sub.operator('mesh.primitive_cube_add', text="", icon='MESH_CUBE')
            sub.operator('mesh.primitive_uv_sphere_add', text="", icon='MESH_UVSPHERE')
            sub.operator('mesh.primitive_cylinder_add', text="", icon='MESH_CYLINDER')
            sub.operator('object.empty_add', text="", icon='EMPTY_DATA')
            sub.operator('object.gpencil_add', text="", icon='GREASEPENCIL')
            sub.operator('curve.primitive_bezier_curve_add', text="", icon='CURVE_DATA')
            sub.separator(factor=1)
            sub.operator('object.delete', text='DELETE').use_global=False

            sub = col.row(align=True)

            subsub = sub.column(align=True)
            #sub.ui_units_x = 4
            subsub.scale_y = 0.8
            subsub.label(text="OBJECT")
            subsub.operator('object.join', text='JOIN')
            subsub.operator('object.duplicate_move', text='DUPLICATE')
            subsub.operator('object.duplicate_move_linked', text='LINKED')
            subsub.operator('object.make_links_data', text='COPY MODS').type='MODIFIERS'

            subsub = sub.column(align=True)
            #sub.ui_units_x = 4
            subsub.scale_y = 0.8
            subsub.label(text="CONVERT")
            #subsub.ui_units_x = 3
            subsub.operator('object.convert', text='MESH').target='MESH'
            subsub.operator('object.convert', text='CURVE').target='CURVE'
            subsub.operator('object.convert', text='GPENCIL').target='GPENCIL'
            subsub.operator('gpencil.trace_image', text='IMG TRACE')

        col.separator(factor=2)
        sub = col.row()
        subsub = sub.column()
        subsub.label(text='')
        subsub = sub.column()
        subsub.ui_units_x = 4
        subsub.operator("screen.redo_last", text="CMD >>")

#WindowManager.invoke_props_dialog(operator, width=300, height=20)
class SelectMenu(bpy.types.Panel):
    bl_label = "SELECTIONS"
    bl_idname = "OBJECT_PT_select_menu"
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = "scene"
    bl_order = 1000
    bl_options = {'DEFAULT_CLOSED',}

    def draw(self, context):
        layout = self.layout

        edit_mode = context.scene.tool_settings.mesh_select_mode
        col = layout.column()

        if context.mode == 'OBJECT':

            sub = col.column(align=True)
            sub.scale_y = 0.8
            sub.label(text="Linked")
            sub.ui_units_x = 4
            subsub = sub.row(align=True)
            subsub.operator('object.select_linked', text='DATA').type='OBDATA'
            subsub.operator('object.select_linked', text='MAT').type='MATERIAL'
            subsub = sub.row(align=True)
            subsub.operator('object.select_linked', text='INST').type='DUPGROUP'
            subsub.operator('object.select_linked', text='LIB').type='LIBRARY_OBDATA'

            col.separator(factor = 1)
            sub = col.row(align=True)
            op = sub.operator("xmenu.override2", text="HIERARCHY")
            op.cmd ='object.select_hierarchy'
            op.prop1 ='direction="CHILD"'
            op.prop2 ='extend=True'

        if context.mode == 'EDIT_MESH':
            sub = col.row(align=True)
            sub.scale_y = 1
            #sub.label(text="SELECT")
            sub.ui_units_x = 4
            sub.operator('mesh.select_all',text='ALL').action='SELECT'
            sub.operator('mesh.select_all',text='CLR').action='DESELECT'
            sub.operator('mesh.select_all',text='INV').action='INVERT'

            col.separator(factor = 2)
            sub = col.column(align=True)
            sub.scale_x = 2
            #sub.label(text="SELECT")
            subsub = sub.row(align=True)
            subsub.alignment = 'CENTER'
            subsub.operator('mesh.select_less', icon='REMOVE', text='')
            subsub.operator('mesh.select_more', icon='ADD',text='')

            col.separator(factor = 2)
            sub = col.row(align=True)
            sub.operator('object.vertex_group_assign_new',text='NEW GRP')
            sub.operator('object.vertex_group_assign',text='ADD')



            col.separator(factor = 1)
            sub = col.row(align=True)
            sub.operator_menu_enum("mesh.select_similar", "type")

            col.separator(factor = 2)
            sub = col.row(align=True)
            sub.operator('mesh.select_linked',text='LINKED')
            sub.operator('mesh.shortest_path_select',text='SHRT')
            sub.operator('mesh.faces_select_linked_flat',text='L-FLAT')

            col.separator(factor = 2)
            sub = col.row(align=True)
            sub.scale_y = 1
            sub.label(text="BY TRAIT")
            sub = col.row(align=True)
            subsub = sub.column(align=True)
            subsub.operator('mesh.select_non_manifold',text='OPEN')
            subsub.operator('mesh.select_loose',text='LOOSE')
            subsub = sub.column(align=True)
            subsub.operator('mesh.select_interior_faces',text='INTERIOR')
            subsub.operator('mesh.select_face_by_sides',text='COUNT')

        sub = col.row()
        subsub = sub.column()
        subsub.label(text='')
        subsub = sub.column()
        subsub.ui_units_x = 4
        subsub.operator("screen.redo_last", text="CMD >>")


addon_keymaps = []
classes = (PropMenu, ModesMenu, FileMenu, ToolMenu, SelectMenu)

def register():
    for cls in classes:
        bpy.utils.register_class(cls)

    wm = bpy.context.window_manager
    kc = wm.keyconfigs.addon
    if kc:
        km = wm.keyconfigs.addon.keymaps.new(name='3D View', space_type='VIEW_3D')

        kmi = km.keymap_items.new('wm.call_menu_pie', 'TAB', 'PRESS', ctrl=False, shift=False, alt=False)
        kmi.properties.name = ModesMenu.bl_idname
        addon_keymaps.append((km, kmi))

        kmi = km.keymap_items.new('wm.call_menu_pie', 'S', 'PRESS', ctrl=True, shift=False, alt=False)
        kmi.properties.name = FileMenu.bl_idname
        addon_keymaps.append((km, kmi))

        kmi = km.keymap_items.new('wm.call_panel', 'D', 'PRESS', ctrl=False, shift=False, alt=False)
        kmi.properties.name = PropMenu.bl_idname
        addon_keymaps.append((km, kmi))

        kmi = km.keymap_items.new('wm.call_panel', 'SPACE', 'PRESS', ctrl=False, shift=False, alt=False)
        kmi.properties.name = ToolMenu.bl_idname
        #kmi.properties.keep_open = True
        addon_keymaps.append((km, kmi))

        kmi = km.keymap_items.new('wm.call_panel', 'A', 'PRESS', ctrl=False, shift=False, alt=False)
        kmi.properties.name = SelectMenu.bl_idname
        addon_keymaps.append((km, kmi))
    
def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)

    for km, kmi in addon_keymaps:
        km.keymap_items.remove(kmi)
    addon_keymaps.clear()

