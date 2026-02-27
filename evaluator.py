# evaluator.py
import main
import settings
import numpy as np

def evaluate(design_variables):
    """
    Evaluator function for the optimization.

    Args:
        design_variables (list): A list of design variables.

    Returns:
        tuple: A tuple containing the objective function value and a list of constraint values.
    """
    # 1. Update the settings with the new design variables
    #    This part needs to be implemented.
    #    For example:
    #    settings.base_h, settings.arm_t, settings.rib_t = design_variables
    
    # 2. Run the simulation workflow
    max_disp, max_stress, mass_kg, volume_mm3 = main.run_workflow()

    # 3. Define the objective function
    objective = mass_kg

    # 4. Define the constraints
    #    Constraint: max_stress <= yield_strength / safety_factor
    #    The constraint function should be <= 0 for SciPy's 'SLSQP' method.
    safety_factor = 2.5 
    constraint_stress = max_stress - (settings.yield_strength / safety_factor)

    constraints = [constraint_stress]

    print(f"Objective (Mass): {objective:.4f} kg")
    print(f"Constraint (Stress): {constraint_stress:.4f}")

    return objective, constraints

if __name__ == '__main__':
    # Example usage of the evaluator function
    # Use the default values from settings.py as a starting point
    example_design_variables = [settings.base_h, settings.arm_t, settings.rib_t]
    evaluate(example_design_variables)
