
#%%
# # main.py
import FreeCAD as App
import Part
import ObjectsFem
import settings
import geometry
import meshing
import fea_setup
import post_processing
def run_workflow():
    print("--- 1. Creating Geometry ---")
    geometry.create_and_export_geometry()

    print("--- 2. Initializing FEA Document ---")
    doc = App.newDocument("Bracket_FEA")
    shape = Part.read(settings.step_file)
    part_obj = doc.addObject("Part::Feature", "Bracket")
    part_obj.Shape = shape
    analysis = ObjectsFem.makeAnalysis(doc, "Analysis")

    print("--- 3. Applying Material ---")
    fea_setup.apply_material(doc, analysis)

    print("--- 4. Generating Mesh ---")
    meshing.create_mesh(doc, part_obj, analysis)

    print("--- 5. Applying Boundary Conditions ---")
    fea_setup.apply_boundary_conditions(doc, part_obj, analysis)

    print("--- 6. Solving and Exporting ---")
    fea_setup.solve_and_export(doc, analysis)

    print("--- 7. Extracting Results ---")
    max_disp, max_stress = post_processing.extract_max_values_from_vtk(settings.results_file)
    mass_kg, volume_mm3 = post_processing.calculate_mass(part_obj.Shape, settings.density)
    print("\n" + "="*30)
    print("SIMULATION RESULTS SUMMARY:")
    if max_disp is not None:
        print(f"Max Displacement:   {max_disp:.9f} mm")
    if max_stress is not None:
        print(f"Max von Mises:      {max_stress:.9f} MPa")

    # --- Calculate Safety Factor ---
    safety_factor = settings.yield_strength / max_stress
    print(f"Safety Factor:      {safety_factor:.2f}")
    
    # Add a quick structural warning
    if safety_factor < 1.0:
        print(">>> WARNING: PART WILL LIKELY FAIL (FoS < 1.0) <<<")
    elif safety_factor < 2.0:
        print(">>> CAUTION: Low margin of safety. <<<")
    print("="*30 + "\n")
    print(f"Volume:             {volume_mm3:.2f} mm^3")
    print(f"Mass:               {mass_kg} kg")
    print("="*35 + "\n")
    
    print("--- Workflow Complete! ---")
    return max_disp, max_stress, mass_kg, volume_mm3


if __name__ == "__main__":
    run_workflow()

# %%
