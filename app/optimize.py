
import logging
from scipy.optimize import differential_evolution
import settings
from evaluator import evaluate_design

# --- Optimization Settings ---
ALLOWABLE_STRESS = 30  # MPa
MAX_DISP = 2.0         # mm

logging.basicConfig(filename="opt_log.txt", level=logging.INFO, filemode='w')

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

bounds = [
    (6, 8),   # base_t
    (6, 8),   # arm_t
    (4, 6),   # rib_t
]

def objective(x):
    params = base_params.copy()
    params["base_t"] = x[0]
    params["arm_t"]  = x[1]
    params["rib_t"]  = x[2]

    results = evaluate_design(params)

    # --- FIX: Convert FreeCAD Quantities to floats ---
    mass = results['mass'].Value if hasattr(results['mass'], 'Value') else float(results['mass'])
    stress = float(results['max_stress'])
    disp = float(results['max_disp'])

    penalty = 0.0
    
    logging.info(
        f"x={list(x)} | "
        f"Mass={mass:.4f} | "
        f"Stress={stress:.4f}"
    )
    if stress > ALLOWABLE_STRESS:
        penalty += 1000 * (stress / ALLOWABLE_STRESS)

    if disp > MAX_DISP:
        penalty += 1000 * (disp / MAX_DISP)

    return mass + penalty

def run_optimization():
    print("Starting differential evolution optimization...")
    result = differential_evolution(
        objective,
        bounds,
        maxiter=3,
        popsize=2,
    )

    print("\nOptimization Complete!")
    print("Optimal variables:", result.x)
    
    best_params = base_params.copy()
    best_params["base_t"] = result.x[0]
    best_params["arm_t"] = result.x[1]
    best_params["rib_t"] = result.x[2]
    
    print("\nEvaluating final optimal design...")
    final_results = evaluate_design(best_params)
    
    print("\nFinal Performance:")
    for key, value in final_results.items():
        val = value.Value if hasattr(value, 'Value') else value
        # Format floats to 4 decimal places for cleaner output
        if isinstance(val, float):
            print(f"  {key}: {val:.4f}")
        else:
            print(f"  {key}: {val}")
