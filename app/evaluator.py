
import FreeCAD as App
import Part
import ObjectsFem
import settings
import geometry
import meshing
import fea_setup
import post_processing

def evaluate_design(params):
    #print("--- 1. Creating Geometry ---")
    geometry.create_and_export_geometry(params)

    #print("--- 2. Initializing FEA Document ---")
    doc = App.newDocument("Bracket_FEA")
    shape = Part.read(settings.step_file)
    part_obj = doc.addObject("Part::Feature", "Bracket")
    part_obj.Shape = shape
    analysis = ObjectsFem.makeAnalysis(doc, "Analysis")

    #print("--- 3. Applying Material ---")
    fea_setup.apply_material(doc, analysis)

    #print("--- 4. Generating Mesh ---")
    meshing.create_mesh(doc, part_obj, analysis)

    #print("--- 5. Applying Boundary Conditions ---")
    fea_setup.apply_boundary_conditions(doc, part_obj, analysis)

    #print("--- 6. Solving and Exporting ---")
    solve_success = fea_setup.solve_and_export(doc, analysis)

    mass_kg, volume_mm3 = post_processing.calculate_mass(part_obj.Shape, settings.density)

    if not solve_success:
        # Solver failed, return high penalty values
        return {
            "max_disp": 999.0,
            "max_stress": 9999.0,
            "mass": mass_kg,
            "volume": volume_mm3,
            "safety_factor": 0.01 
        }

    #print("--- 7. Extracting Results ---")
    max_disp, max_stress = post_processing.extract_max_values_from_vtk(settings.results_file)

    # --- Calculate Safety Factor ---
    # Handle potential division by zero if stress is 0
    if max_stress > 1e-9:
        safety_factor = settings.yield_strength / max_stress
    else:
        safety_factor = float('inf')
    
    return {
        "max_disp": max_disp,
        "max_stress": max_stress,
        "mass": mass_kg,
        "volume": volume_mm3,
        "safety_factor": safety_factor
    }
