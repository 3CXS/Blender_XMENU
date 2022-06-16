import bpy, bmesh

class EdgeData(bpy.types.Menu):
    bl_label = "Crease and Bevel"
    bl_idname = "OBJECT_MT_edgedata"

    def draw(self, context):
            layout = self.layout
            props  = context.scene.creaseAndBevelPG # Create reference to property group

            box = layout.box()                    # Draw a box
            col = box.column( align = True )      # Create a column
            col.prop( props, "whoToInfluence"  )  # Add properites to panel
            col.prop( props, "bevelWeight"     )
            col.prop( props, "edgeCrease"      )

class creaseAndBevelPG(bpy.types.PropertyGroup):
    ## Update functions
    def update_bevelWeight( self, context ):
        ''' Update function for bevelWeight property '''

        o  = bpy.context.object
        d  = o.data
        bm = bmesh.from_edit_mesh( d )

        bevelWeightLayer = bm.verts.layers.bevel_weight['BevelWeight']

        if self.whoToInfluence == 'Selected Elements':
            selectedVerts = [ v for v in bm.verts if v.select ]
            for v in selectedVerts: v[ bevelWeightLayer ] = self.bevelWeight
        else:
            for v in bm.verts: v[ bevelWeightLayer ] = self.bevelWeight

        bmesh.update_edit_mesh( d )

    def update_edgeCrease( self, context ):
        ''' Update function for edgeCrease property '''

        o  = bpy.context.object
        d  = o.data
        bm = bmesh.from_edit_mesh( d )

        creaseLayer = bm.edges.layers.crease['SubSurfCrease']

        if self.whoToInfluence == 'Selected Elements':
            selectedEdges = [ e for e in bm.edges if e.select ]
            for e in selectedEdges: e[ creaseLayer ] = self.edgeCrease
        else:
            for e in bm.edges: e[ creaseLayer ] = self.edgeCrease

        bmesh.update_edit_mesh( d )

    ## Properties
    items = [
        ('All', 'All', ''),
        ('Selected Elements', 'Selected Elements', '')
    ]

    whoToInfluence = bpy.props.EnumProperty( # Material distribution method
        description = "Influence all / selection",
        name        = "whoToInfluence",
        items       = items,
        default     = 'Selected Elements'
    )

    bevelWeight = bpy.props.FloatProperty(
        description = "Bevel Weight",
        name        = "bevelWeight",
        min         = 0.0,
        max         = 1.0,
        step        = 0.01,
        default     = 0,
        update      = update_bevelWeight
    )

    edgeCrease = bpy.props.FloatProperty(
        description = "Edge Crease",
        name        = "edgeCrease",
        min         = 0.0,
        max         = 1.0,
        step        = 0.01,
        default     = 0,
        update      = update_edgeCrease
    )

classes = (EdgeData,)


def register():
    for cls in classes:
        bpy.utils.register_class(cls)
    bpy.types.Scene.creaseAndBevelPG = bpy.props.PointerProperty(type = creaseAndBevelPG)

def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)



