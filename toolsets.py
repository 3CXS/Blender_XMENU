import bpy

def Toolset():
    if bpy.context.mode == 'OBJECT':
        Toolset = Tools_Object
    if bpy.context.mode == 'SCULPT':
        Toolset = Tools_Sculpt
    if bpy.context.mode == 'PAINT_TEXTURE':
        Toolset = Tools_Texture
    if bpy.context.mode == 'PAINT_VERTEX':
        Toolset = Tools_Vertex
    return Toolset

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
                ('SCRAPE',              'builtin_brush.Scrape',             'Scrape/Peaks', 'brush.sculpt.scrape',              ''),
                ('POLISH',              'builtin_brush.Scrape',             'Polish',       'brush.sculpt.scrape',              ''), 
                ('FLATTEN',             'builtin_brush.Flatten',            '',             'brush.sculpt.flatten',             ''),
                ('FILL',                'builtin_brush.Fill',               '',             'brush.sculpt.fill',                ''),                                                                      
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
                ('SMTH',                'builtin_brush.Smooth',             '',             'brush.sculpt.smooth',              'SMOOTH'),
                ('MULTIPLANE_SCRAPE',   'builtin_brush.Multi-plane Scrape', '',             'brush.sculpt.multiplane_scrape',   'MULTIPLANE_SCRAPE'),
                ('CLOTH',               'builtin_brush.Cloth',              '',             'brush.sculpt.cloth',               'CLOTH'),                
                ('BX',                  'builtin.box_mask',                 '',             'ops.sculpt.border_mask',           'BOX_MASK'),
                ('LS',                  'builtin.lasso_mask',               '',             'ops.sculpt.lasso_mask',            'LASSO_MASK'),
                ('LN',                  'builtin.line_mask',                '',             'ops.sculpt.line_mask',             'LINE_MASK'),
                ('BOX_FACESET',         'builtin.box_face_set',             '',             'ops.sculpt.border_face_set',       'BOX_FACESET'),
                ('LASSO_FACESET',       'builtin.lasso_face_set',           '',             'ops.sculpt.lasso_face_set',        'LASSO_FACESET'),
                ('EDIT',                'builtin.face_set_edit',            '',             'ops.sculpt.face_set_edit',         'EDIT_FACESET'),
                ('FILTER',              'builtin.mesh_filter',              '',             'ops.sculpt.mesh_filter',           '')
                ]   

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
Tools_Texture= [ 
                ('DRAW',                'builtin_brush.Draw',                   '',             'brush.paint_texture.draw',               ''), 
                ('SOFTEN',                 'builtin_brush.Soften',               '',             'brush.paint_texture.soften',           ''),
                ('SMEAR',              'builtin_brush.Smear',            '',             'brush.paint_texture.smear',        ''),
                ('CLONE',               'builtin_brush.Clone',             '',             'brush.paint_texture.clone',         ''),
                ('FILL',              'builtin_brush.Fill',                   '',             'brush.paint_texture.fill',               ''),
                ('MASK',                'builtin_brush.Mask',                     '',             'brush.paint_texture.mask',          '')
                ]
Tools_Vertex= [ 
                ('DRAW',                'builtin_brush.Draw',                   '',             'brush.paint_vertex.draw',               ''), 
                ('BLUR',                 'builtin_brush.Blur',               '',             'brush.paint_vertex.blur',           ''),
                ('AVERAGE',              'builtin_brush.Average',            '',             'brush.paint_texture.average',        ''),
                ('SMEAR',               'builtin_brush.Smear',             '',             'brush.paint_texture.smear',         ''),
                ] 

#bpy.context.workspace.tools.from_space_view3d_mode(bpy.context.mode).idname
#bpy.context.tool_settings.sculpt.brush


