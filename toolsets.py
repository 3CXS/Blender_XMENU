import bpy

#------------------------------------------------------------------------------------------------------------------------------------

def Toolset():
    if bpy.context.mode == 'OBJECT':
        Toolset = Tools_Object
    if bpy.context.mode == 'EDIT_MESH':
        Toolset = Tools_Edit
    if bpy.context.mode == 'SCULPT':
        Toolset = Tools_Sculpt
    if bpy.context.mode == 'PAINT_TEXTURE':
        Toolset = Tools_Texture
    if bpy.context.mode == 'PAINT_VERTEX':
        Toolset = Tools_Vertex
    if bpy.context.mode == 'PAINT_WEIGHT':
        Toolset = Tools_Weight
    if bpy.context.mode == 'PAINT_GPENCIL':
        Toolset = Tools_GP_Draw
    if bpy.context.mode == 'EDIT_GPENCIL':
        Toolset = Tools_GP_Edit
    if bpy.context.mode == 'SCULPT_GPENCIL':
        Toolset = Tools_GP_Sculpt
    if bpy.context.mode == 'WEIGHT_GPENCIL':
        Toolset = Tools_GP_Weight
    return Toolset

#------------------------------------------------------------------------------------------------------------------------------------

Tools_Object= [ 
                ('TWEAK',               'builtin.select',                   '',             'ops.generic.select',               ''), 
                ('BOX',                 'builtin.select_box',               '',             'ops.generic.select_box',           ''),
                ('CIRCLE',              'builtin.select_circle',            '',             'ops.generic.select_circle',        ''),
                ('LASSO',               'builtin.select_lasso',             '',             'ops.generic.select_lasso',         ''),
                ('CURSOR',              'builtin.cursor',                   '',             'ops.generic.cursor',               ''),
                ('MOVE',                'builtin.move',                     '',             'ops.transform.translate',          ''),
                ('ROTATE',              'builtin.rotate',                   '',             'ops.transform.rotate',             ''),
                ('SCALE',               'builtin.scale',                    '',             'ops.transform.resize',             ''),
                ('TRANSFORM',           'builtin.transform',                '',             'ops.transform.transform',          ''),
                ('ANNOTATE',            'builtin.annotate',                 '',             'ops.gpencil.draw',                 ''),
                ('LINE',                'builtin.annotate_line',            '',             'ops.gpencil.draw.line',            ''),
                ('POLY',                'builtin.annotate_polygon',         '',             'ops.gpencil.draw.poly',            ''),
                ('ERASE',               'builtin.annotate_eraser',          '',             'ops.gpencil.draw.eraser',          ''),
                ('MEASURE',             'builtin.measure',                  '',             'ops.view3d.ruler',                 ''),
                ('CUBE_ADD',            'builtin.primitive_cube_add',       '',             'ops.mesh.primitive_cube_add_gizmo','')
                ] 

Tools_Edit = [ 
                ('TWEAK',               'builtin.select',                   '',             'ops.generic.select',               ''), 
                ('BOX',                 'builtin.select_box',               '',             'ops.generic.select_box',           ''),
                ('CIRCLE',              'builtin.select_circle',            '',             'ops.generic.select_circle',        ''),
                ('LASSO',               'builtin.select_lasso',             '',             'ops.generic.select_lasso',         ''),
                ('CURSOR',              'builtin.cursor',                   '',             'ops.generic.cursor',               ''),
                ('MOVE',                'builtin.move',                     '',             'ops.transform.translate',          ''),
                ('ROTATE',              'builtin.rotate',                   '',             'ops.transform.rotate',             ''),
                ('SCALE',               'builtin.scale',                    '',             'ops.transform.resize',             ''),
                ('TRANSFORM',           'builtin.transform',                '',             'ops.transform.transform',          ''),
                ('ANNOTATE',            'builtin.annotate',                 '',             'ops.gpencil.draw',                 ''),
                ('ERASE',               'builtin.annotate_eraser',          '',             'ops.gpencil.draw.eraser',          ''),
                ('MEASURE',             'builtin.measure',                  '',             'ops.view3d.ruler',                 ''),
                ('CUBE_ADD',            'builtin.primitive_cube_add',       '',             'ops.mesh.primitive_cube_add_gizmo',''),

                ('EXT_REG',             'builtin.extrude_region',           '',             'ops.mesh.extrude_region_move',     ''),
                ('EXT MFD',             'builtin.extrude_manifold',         '',             'ops.mesh.extrude_manifold',        ''),
                ('EXT NORM',            'builtin.extrude_along_normals',    '',             'ops.mesh.extrude_region_shrink_fatten', ''),
                ('EXT IND',             'builtin.extrude_individual',       '',             'ops.mesh.extrude_faces_move',      ''),
                ('EXT CRS',             'builtin.extrude_to_cursor',        '',             'ops.mesh.dupli_extrude_cursor',    ''),

                ('INSET',               'builtin.inset_faces',              '',             'ops.mesh.inset',                   ''),
                ('BEVEL',               'builtin.bevel',                    '',             'ops.mesh.bevel',                   ''),
                ('LOOP CUT',            'builtin.loop_cut',                 '',             'ops.mesh.loopcut_slide',           ''),
                ('OFFSET',              'builtin.offset_edge_loop_cut',     '',             'ops.mesh.offset_edge_loops_slide', ''),
                ('KNIFE',               'builtin.knife',                    '',             'ops.mesh.knife_tool',              ''),
                ('BISECT',              'builtin.bisect',                   '',             'ops.mesh.bisect',                  ''),
                ('BUILD',               'builtin.poly_build',               '',             'ops.mesh.polybuild_hover',         ''),
                ('SPIN',                'builtin.spin',                     '',             'ops.mesh.spin',                    ''),
                ('SPIN DUB',            'builtin.spin_dublicates',          '',             'ops.mesh.spin.duplicate',          ''),
                ('SMTH',                'builtin.smooth',                   '',             'ops.mesh.vertices_smooth',         ''),
                ('RAND',                'builtin.randomize',                '',             'ops.transform.vertex_random',      ''),
                ('SLIDE E',             'builtin.edge_slide',               '',             'ops.transform.edge_slide',         ''),
                ('SLIDE V',             'builtin.vertex_slide',             '',             'ops.transform.vert_slide',         ''),
                ('SHRINK',              'builtin.shrink_fatten',            '',             'ops.transform.shrink_fatten',      ''),
                ('PUSH',                'builtin.push_pull',                '',             'ops.transform.push_pull',          ''),
                ('SHEAR',               'builtin.shear',                    '',             'ops.transform.shear',              ''),
                ('TO SPH',              'builtin.to_sphere',                '',             'ops.transform.tosphere',           ''),
                ('RIP REG',             'builtin.rip_region',               '',             'ops.mesh.rip',                     ''),
                ('RIP EDGE',            'builtin.rip_edge',                 '',             'ops.mesh.rip_edge',                '')
                ] 
Tools_Sculpt= [ 
                ('GRAB',                'builtin_brush.Grab',               '',             'brush.sculpt.grab',                ''),
                ('SHARP',               'builtin_brush.Draw Sharp',         '',             'brush.sculpt.draw_sharp',          ''),
                ('STRIPS',              'builtin_brush.Clay Strips',        '',             'brush.sculpt.clay_strips',         ''),
                ('LAYER',               'builtin_brush.Layer',              '',             'brush.sculpt.layer',               ''), 
                ('DRAW',                'builtin_brush.Draw',               '',             'brush.sculpt.draw',                ''),
                ('CLAY',                'builtin_brush.Clay',               '',             'brush.sculpt.clay',                ''),
                ('INFLATE',             'builtin_brush.Inflate',            '',             'brush.sculpt.inflate',             ''),
                ('CREASE',              'builtin_brush.Crease',             '',             'brush.sculpt.crease',              ''),
                ('PINCH',               'builtin_brush.Pinch',              '',             'brush.sculpt.pinch',               ''),
                ('SCRAPE',              'builtin_brush.Scrape',             '',             'brush.sculpt.scrape',              ''), 
                ('FLATTEN',             'builtin_brush.Flatten',            '',             'brush.sculpt.flatten',             ''),
                ('FILL',                'builtin_brush.Fill',               '',             'brush.sculpt.fill',                ''),
                ('SMTH',                'builtin_brush.Smooth',             '',             'brush.sculpt.smooth',              'SMOOTH'),
                ('MASK',                'builtin_brush.Mask',               '',             'brush.sculpt.mask',                ''),
                ('FSETS',               'builtin_brush.Draw Face Sets',     '',             'brush.sculpt.draw_face_sets',      ''),
                ('HIDE',                'builtin.box_hide',                 '',             'ops.sculpt.border_hide',           ''),
                ('BX',                  'builtin.box_trim',                 '',             'ops.sculpt.box_trim',              'BOX_TRIM'),
                ('LS',                  'builtin.lasso_trim',               '',             'ops.sculpt.lasso_trim',            'LASSO_TRIM'),
                ('TRANSFORM',           'builtin.transform',                '',             'ops.transform.transform',           ''),
                ('ELASTIC',             'builtin_brush.Elastic Deform',     '',             'brush.sculpt.elastic_deform',      'ELASTIC'),
                ('POSE',                'builtin_brush.Pose',               '',             'brush.sculpt.pose',                'POSE'),
                ('SNAKE_HOOK',          'builtin_brush.Snake Hook',         '',             'brush.sculpt.snake_hook',          'SNAKE_HOOK'),
                ('THUMB',               'builtin_brush.Thumb',              '',             'brush.sculpt.thumb',               'THUMB'),
                ('BLOB',                'builtin_brush.Blob',               '',             'brush.sculpt.blob',                'BLOB'), 
                ('CLAY_THUMB',          'builtin_brush.Clay Thumb',         '',             'brush.sculpt.clay_thumb',          'CLAY_THUMB'),
                ('MULTIPLANE_SCRAPE',   'builtin_brush.Multi-plane Scrape', '',             'brush.sculpt.multiplane_scrape',   'MULTIPLANE_SCRAPE'),
                ('CLOTH',               'builtin_brush.Cloth',              '',             'brush.sculpt.cloth',               'CLOTH'),                
                ('BX',                  'builtin.box_mask',                 '',             'ops.sculpt.border_mask',           'BOX_MASK'),
                ('LS',                  'builtin.lasso_mask',               '',             'ops.sculpt.lasso_mask',            'LASSO_MASK'),
                ('LN',                  'builtin.line_mask',                '',             'ops.sculpt.line_mask',             'LINE_MASK'),
                ('BOX_FACESET',         'builtin.box_face_set',             '',             'ops.sculpt.border_face_set',       'BOX_FACESET'),
                ('LASSO_FACESET',       'builtin.lasso_face_set',           '',             'ops.sculpt.lasso_face_set',        'LASSO_FACESET'),
                ('EDIT',                'builtin.face_set_edit',            '',             'ops.sculpt.face_set_edit',         'EDIT_FACESET'),
                ('MESH',                'builtin.mesh_filter',              '',             'ops.sculpt.mesh_filter',           ''),
                ('COLOR',               'builtin.color_filter',             '',             'ops.sculpt.color_filter',          ''),
                ('CLOTH',               'builtin.cloth_filter',             '',             'ops.sculpt.cloth_filter',          ''),
                ('PAINT',               'builtin_brush.Paint',              '',             'brush.sculpt.paint',               ''),
                ('SMEAR',               'builtin_brush.Smear',              '',             'brush.sculpt.smear',               ''),
                ]   
Tools_Texture= [ 
                ('DRAW',                'builtin_brush.Draw',               '',             'brush.paint_texture.draw',         ''), 
                ('SOFTEN',              'builtin_brush.Soften',             '',             'brush.paint_texture.soften',       ''),
                ('SMEAR',               'builtin_brush.Smear',              '',             'brush.paint_texture.smear',        ''),
                ('CLONE',               'builtin_brush.Clone',              '',             'brush.paint_texture.clone',        ''),
                ('FILL',                'builtin_brush.Fill',               '',             'brush.paint_texture.fill',         ''),
                ('MASK',                'builtin_brush.Mask',               '',             'brush.paint_texture.mask',         '')
                ]
Tools_Vertex= [ 
                ('DRAW',                'builtin_brush.Draw',               '',             'brush.paint_vertex.draw',          ''), 
                ('BLUR',                'builtin_brush.Blur',               '',             'brush.paint_vertex.blur',          ''),
                ('AVERAGE',             'builtin_brush.Average',            '',             'brush.paint_vertex.average',       ''),
                ('SMEAR',               'builtin_brush.Smear',              '',             'brush.paint_vertex.smear',         '')
                ] 
Tools_Weight= [ 
                ('DRAW',                'builtin_brush.Draw',               '',             'brush.paint_vertex.draw',          ''), 
                ('BLUR',                'builtin_brush.Blur',               '',             'brush.paint_vertex.blur',          ''),
                ('AVERAGE',             'builtin_brush.Average',            '',             'brush.paint_vertex.average',       ''),
                ('SMEAR',               'builtin_brush.Smear',              '',             'brush.paint_vertex.smear',         ''),
                ('GRADIENT',            'builtin.gradient',                 '',             'ops.paint.weight_gradient',        ''),
                ('SAMPLE',              'builtin.sample_weight',            '',             'ops.paint.weight_sample',          ''),
                ('SAMPLE GRP',          'builtin.sample_vertex_group',      '',             'ops.paint.weight_sample_group',    '')
                ]
Tools_GP_Draw= [ 
                ('PEN',                 'builtin_brush.Draw',               '',             'brush.gpencil_draw.draw',          ''),
                ('FILL',                'builtin_brush.Fill',               '',             'brush.gpencil_draw.fill',          ''),
                ('ERASE',               'builtin_brush.Erase',              '',             'brush.gpencil_draw.erase',         ''),
                ('TINT',                'builtin_brush.Tint',               '',             'brush.gpencil_draw.tint',          ''),
                ('CUTTER',              'builtin.cutter',                   '',             'ops.gpencil.stroke_cutter',        ''),
                ('SAMPLE',              'builtin.eyedropper',               '',             'ops.paint.eyedropper_add',         ''),
                ('LINE',                'builtin.line',                     '',             'ops.gpencil.primitive_line',       ''),
                ('POLYLINE',            'builtin.polyline',                 '',             'ops.gpencil.primitive_polyline'    ''),
                ('ARC',                 'builtin.arc',                      '',             'ops.gpencil.primitive_arc',        ''),
                ('CURVE',               'builtin.curve',                    '',             'ops.gpencil.primitive_curve',      ''),
                ('BOX',                 'builtin.box',                      '',             'ops.gpencil.primitive_box',        ''),
                ('CIRCLE',              'builtin.circle',                   '',             'ops.gpencil.primitive_circle',     ''),
                ('INTERPOLATE',         'builtin.interpolate',              '',             'ops.gpencil.primitive_line',       ''),
                ]

Tools_GP_Edit= [ 
                ('TWEAK',               'builtin.select',                   '',             'ops.generic.select',               ''), 
                ('BOX',                 'builtin.select_box',               '',             'ops.generic.select_box',           ''),
                ('CIRCLE',              'builtin.select_circle',            '',             'ops.generic.select_circle',        ''),
                ('LASSO',               'builtin.select_lasso',             '',             'ops.generic.select_lasso',         ''),
                ('CURSOR',              'builtin.cursor',                   '',             'ops.generic.cursor',               ''),
                ('MOVE',                'builtin.move',                     '',             'ops.transform.translate',          ''),
                ('ROTATE',              'builtin.rotate',                   '',             'ops.transform.rotate',             ''),
                ('SCALE',               'builtin.scale',                    '',             'ops.transform.resize',             ''),
                ('TRANSFORM',           'builtin.transform',                '',             'ops.transform.transform',          ''),
                ('EXTR',                'builtin.extrude',                  '',             'ops.gpencil.extrude_move',         ''),
                ('RAD',                 'builtin.radius',                   '',             'ops.gpencil.radius',               ''),
                ('BEND',                'builtin.bend',                     '',             'ops.gpencil.edit_bend',            ''),
                ('SHEAR',               'builtin.shear',                    '',             'ops.gpencil.edit_shear',           ''),
                ('SPH',                 'builtin.to_sphere',                '',             'ops.gpencil.edit_to_sphere',       ''),
                ('X FILL',              'builtin.transform_fill',           '',             'ops.gpencil.transform_fill',       ''),
                ('INTER',               'builtin.interpolate',              '',             'ops.gpencil.primitive_line',       ''),
                ]
Tools_GP_Sculpt= [ 
                ('SMOOTH',              'builtin_brush.Smooth',             '',             'ops.gpencil.sculpt_smooth',        ''), 
                ('THICKNESS',           'builtin_brush.Thickness',          '',             'ops.gpencil.sculpt_thickness',     ''),
                ('STRENGTH',            'builtin_brush.Strength',           '',             'ops.gpencil.sculpt_strength',      ''),
                ('RANDOMIZE',           'builtin_brush.Randomize',          '',             'ops.gpencil.sculpt_randomize',     ''),
                ('GRAB',                'builtin_brush.Grab',               '',             'ops.gpencil.sculpt_grab',          ''),
                ('PUSH',                'builtin_brush.Push',               '',             'ops.gpencil.sculpt_push',          ''),
                ('TWIST',               'builtin_brush.Twist',              '',             'ops.gpencil.sculpt_twist',         ''),
                ('PINCH',               'builtin_brush.Pinch',              '',             'ops.gpencil.sculpt_pinch',         ''),
                ('CLONE',               'builtin_brush.Clone',              '',             'ops.gpencil.sculpt_clone',         ''),
                ]
Tools_GP_Weight= [ 
                ('WEIGHT',              'builtin_brush.Weight',             '',             'ops.gpencil.sculpt_weight',        ''), 
                ]

#------------------------------------------------------------------------------------------------------------------------------------

#bpy.context.workspace.tools.from_space_view3d_mode(bpy.context.mode).idname
#bpy.context.tool_settings.sculpt.brush


