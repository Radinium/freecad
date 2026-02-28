# fea_setup.py
import ObjectsFem
import femsolver.calculix.solver
from femtools import ccxtools
import feminout.importVTKResults
import settings
import meshio
import numpy as np
def apply_material(doc, analysis):
    material = ObjectsFem.makeMaterialSolid(doc, "SolidMaterial")
    mat_dict = material.Material
    mat_dict.update({
        'Name': settings.material_name,
        'YoungsModulus': settings.youngs_modulus,
        'PoissonRatio': settings.poisson_ratio,
        'Density': settings.density
    })
    material.Material = mat_dict
    analysis.addObject(material)

def apply_boundary_conditions(doc, part_obj, analysis):
    fixed = ObjectsFem.makeConstraintFixed(doc, "FixedConstraint")
    fixed.References = [(part_obj, "Face1")]
    analysis.addObject(fixed)

    force = ObjectsFem.makeConstraintForce(doc, "ForceConstraint")
    force.References = [(part_obj, "Face5")]
    force.Force = settings.force_magnitude
    force.Reversed = True
    analysis.addObject(force)

def solve_and_export(doc, analysis):
    solver = femsolver.calculix.solver.create(doc, "CalculiX")
    solver.GeometricalNonlinearity = 'linear'
    analysis.addObject(solver)
    doc.recompute()

    #print("Running CalculiX solver...")
    ccx = ccxtools.CcxTools(solver)
    error = ccx.run()
    print("CalculiX run error status:", error)

    result_obj = doc.getObject("CCX_Results")
    if result_obj is None:
        print("Solver failed: CCX_Results object not found.")
        return False
    
    feminout.importVTKResults.export([result_obj], settings.results_file)
    #print(f"Results exported to {settings.results_file}")
    return True
