# settings.py

# --- Geometry Parameters ---
base_h, base_w, base_t = 60.0, 15.0, 8.0
arm_l, arm_t = 52, 8.0
rib_t, rib_l = 5.0, 52
hole_d, hole_pitch, hole_edge_offset = 4.0, 20.0, 15.0
total_w = base_w * 2.0
tightness = 0.01

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