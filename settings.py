# settings.py

# --- Geometry Parameters ---
params = {
    "base_w": 15.0,
    "base_h": 60.0,
    "arm_l": 52,
    "base_t": 8,
    "arm_t": 8,
    "rib_t": 5,
    "rib_l" : 52,
    "hole_d": 4,
    "hole_pitch": 20,
    "hole_edge_offset": 15,
    "tightness": 0.2 
} 
base_w= 15.0
base_h= 60.0
arm_l= 52
base_t= 8
arm_t= 8
rib_t= 5
rib_l= 52
hole_d= 4
hole_pitch= 20
hole_edge_offset= 15
tightness= 0.2 

# --- Material Properties ---
material_name = 'PLA'
youngs_modulus = '2740 MPa'
poisson_ratio = '0.36'
density = '1240 kg/m^3'
yield_strength = 60
# --- Mesh Parameters ---
mesh_char_length_max = 2
mesh_char_length_min = 1
mesh_element_order = "2nd"
mesh_optimize_std = True
mesh_curvature = 12

# --- Loading Parameters ---
force_magnitude = 1.0

# --- File Names ---
step_file = "bracket2.step"
mesh_file = "bracket_mesh2.vtk"
results_file = "analysis_results2.vtk"