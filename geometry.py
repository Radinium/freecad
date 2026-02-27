# geometry.py
import FreeCAD as App
import Part
from FreeCAD import Vector
import settings

def create_and_export_geometry(params):
    if App.ActiveDocument is None:
        App.newDocument("Bracket_Model2")

    # Draw on the YZ plane (X=0)
    p1 = Vector(0, 0, 0)
    p2 = Vector(0, params['base_h'], 0)
    p3 = Vector(0, params['base_h'], params['base_t'] + params['arm_l'])
    p4 = Vector(0, params['base_h'] - params['arm_t'], params['base_t'] + params['arm_l'])
    p5 = Vector(0, params['base_h'] - params['arm_t'], params['base_t'])
    p6 = Vector(0, 0, params['base_t'])
    
    edges = [
        Part.makeLine(p1, p2),
        Part.makeLine(p2, p3),
        Part.makeLine(p3, p4),
        Part.makeLine(p4, p5),
        Part.makeLine(p5, p6),
        Part.makeLine(p6, p1)
    ]
    wire = Part.Wire(edges)
    face = Part.Face(wire)

    # Extrude symmetrically along X
    bracket = face.extrude(Vector(params['base_w']*2, 0, 0))
    bracket.translate(Vector(- params['base_w'], 0, 0)) 

    # Holes
    h1_y = params['hole_edge_offset']
    h2_y = params['hole_edge_offset'] + params['hole_pitch']

    hole1 = Part.makeCylinder(params['hole_d'] / 2.0, params['base_t'] + 10, Vector(0, h1_y, -5), Vector(0, 0, 1))
    hole2 = Part.makeCylinder(params['hole_d'] / 2.0, params['base_t'] + 10, Vector(0, h2_y, -5), Vector(0, 0, 1))
    bracket = bracket.cut(hole1).cut(hole2)

    # Rib corners
    r1 = Vector(0, 0, params['base_t'])                       
    r2 = Vector(0, params['base_h'] - params['arm_t'], params['base_t'])          
    r3 = Vector(0, params['base_h'] - params['arm_t'], params['base_t'] + params['rib_l'])  

    ctrl_1 = r3 + (r2 - r3) * params['tightness']
    ctrl_2 = r1 + (r2 - r1) * params['tightness']

    bezier = Part.BezierCurve()
    bezier.setPoles([r3, ctrl_1, ctrl_2, r1])
    curve_edge = bezier.toShape()

    rib_edges = [
        Part.makeLine(r1, r2),
        Part.makeLine(r2, r3),
        curve_edge              
    ]
    rib_wire = Part.Wire(rib_edges)
    rib_face = Part.Face(rib_wire)
    rib_shape = rib_face.extrude(Vector(params['rib_t'], 0, 0))

    left_rib = rib_shape.copy()
    left_rib.translate(Vector(-params['base_w'], 0, 0))
    right_rib = rib_shape.copy()
    right_rib.translate(Vector((params['base_w'] - params['rib_t'], 0, 0)))

    # Fuse and export
    final_part = bracket.fuse([left_rib, right_rib])
    final_part.exportStep(settings.step_file)
    print(f"Geometry successfully exported to {settings.step_file}")