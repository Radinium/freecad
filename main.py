
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
for doc_name in App.listDocuments().keys():
    App.closeDocument(doc_name)

def  evaluate_design(params):
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
    fea_setup.solve_and_export(doc, analysis)

    #print("--- 7. Extracting Results ---")
    max_disp, max_stress = post_processing.extract_max_values_from_vtk(settings.results_file)
    mass_kg, volume_mm3 = post_processing.calculate_mass(part_obj.Shape, settings.density)
    #print("\n" + "="*30)
    #print("SIMULATION RESULTS SUMMARY:")
    '''if max_disp is not None:
        print(f"Max Displacement:   {max_disp:.9f} mm")
    if max_stress is not None:
        print(f"Max von Mises:      {max_stress:.9f} MPa")'''

    # --- Calculate Safety Factor ---
    safety_factor = settings.yield_strength / max_stress
    #print(f"Safety Factor:      {safety_factor:.2f}")
    
    # Add a quick structural warning
    '''if safety_factor < 1.0:
        print(">>> WARNING: PART WILL LIKELY FAIL (FoS < 1.0) <<<")
    elif safety_factor < 2.0:
        print(">>> CAUTION: Low margin of safety. <<<")'''
    #print("="*30 + "\n")
    #print(f"Volume:             {volume_mm3:.2f} mm^3")
    #print(f"Mass:               {mass_kg} kg")
    #print("="*35 + "\n")
    
    #print("--- Workflow Complete! ---")
    return {
        "max_disp": max_disp,
        "max_stress": max_stress,
        "mass": mass_kg,
        "volume": volume_mm3,
        "safety_factor": settings.yield_strength / max_stress
    }

# %%
if __name__ == "__main__":
    evaluate_design(settings.params)
'''     for t in [7, 8]:
        settings.params["base_t"] = t
        print(evaluate_design(settings.params))'''
#%%
ALLOWABLE_STRESS = 30  # MPa
MAX_DISP = 2.0         # mm

base_params = {
    "base_h": settings.base_h,
    "base_w": settings.base_w,
    "base_t": settings.base_t,
    "arm_l": settings.arm_l,
    "arm_t": settings.arm_t,
    "rib_t": settings.rib_t,
    "rib_l": settings.rib_l,
    "hole_d": settings.hole_d,
    "hole_pitch": settings.hole_pitch,
    "hole_edge_offset": settings.hole_edge_offset,
    "tightness": settings.tightness
}
def objective(x):

    params = base_params.copy()

    params["base_t"] = x[0]
    params["arm_t"]  = x[1]
    params["rib_t"]  = x[2]

    results = evaluate_design(params)

    penalty = 0.0

    if results["max_stress"] > ALLOWABLE_STRESS:
        penalty += 1000 * (results["max_stress"] / ALLOWABLE_STRESS)

    if results["max_disp"] > MAX_DISP:
        penalty += 1000 * (results["max_disp"] / MAX_DISP)

    return results["mass"] + penalty

#%%
bounds = [
    (6, 8),   # base_t
    (6, 8),   # arm_t
    (6, 8),   # rib_t
]
#%%
from scipy.optimize import differential_evolution

result = differential_evolution(
    objective,
    bounds,
    maxiter=15,
    popsize=5
)

print("Optimal variables:", result.x)
best_params = {
    "base_t": result.x[0],
    "arm_t": result.x[1],
    "rib_t": result.x[2],
}

final_results = evaluate_design(best_params)
print(final_results)
# %%
