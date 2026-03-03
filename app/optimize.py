
import logging
from scipy.optimize import differential_evolution
from . import settings, evaluator
# --- Optimization Settings ---
ALLOWABLE_STRESS = 17600000  # MPa
MAX_DISP = 2.0         # mm

logging.basicConfig(filename="opt_log.txt", level=logging.INFO, filemode='w', format='%(message)s')

base_params= settings.params.copy()
bounds = [
    (3, 8),   # base_t
    (3, 8),   # arm_t
    (3, 8),   # rib_t
]

def objective(x):
    params = base_params.copy()
    params["base_t"] = x[0]
    params["arm_t"]  = x[1]
    params["rib_t"]  = x[2]

    results = evaluator.evaluate_design(params)

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
        maxiter=2,
        popsize=1,
    )

    print("\nOptimization Complete!")
    print("Optimal variables:", result.x)
    
    best_params = base_params.copy()
    best_params["base_t"] = result.x[0]
    best_params["arm_t"] = result.x[1]
    best_params["rib_t"] = result.x[2]
    
    print("\nEvaluating final optimal design...")
    final_results = evaluator.evaluate_design(best_params)
    
    print("\nFinal Performance:")
    for key, value in final_results.items():
        val = value.Value if hasattr(value, 'Value') else value
        # Format floats to 4 decimal places for cleaner output
        if isinstance(val, float):
            print(f"  {key}: {val:.4f}")
        else:
            print(f"  {key}: {val}")
