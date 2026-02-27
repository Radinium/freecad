
#%%
# # post_processing.py
import vtk
from vtk.util.numpy_support import vtk_to_numpy
import numpy as np
import FreeCAD as App
def extract_max_values_from_vtk(vtk_filename):
    """
    Reads a VTK file and extracts the maximum displacement magnitude 
    and maximum von Mises stress.
    """
    # Initialize the VTK reader
    reader = vtk.vtkUnstructuredGridReader()
    reader.SetFileName(vtk_filename)
    reader.Update()
    
    # Get the grid and point data
    grid = reader.GetOutput()
    point_data = grid.GetPointData()
    
    # --- 1. Extract Displacement ---
    # FreeCAD FEM typically exports this as "Displacement"
    disp_array = point_data.GetArray("Displacement")
    # Convert VTK array to a standard NumPy array
    disp_data = vtk_to_numpy(disp_array)
    # Calculate the magnitude (Euclidean norm) of each XYZ displacement vector
    disp_magnitudes = np.linalg.norm(disp_data, axis=1)
    max_disp = np.max(disp_magnitudes)
    # --- 2. Extract von Mises Stress ---
    # Depending on your FreeCAD version, this is named "vonMises" or "VonMisesStress"
    vm_array = point_data.GetArray("von Mises Stress")
    vm_data = vtk_to_numpy(vm_array)
    max_vm_stress = np.max(vm_data)
    return max_disp, max_vm_stress

def calculate_mass(shape, density_str):
    """
    Calculates the volume and mass of a FreeCAD shape based on a density string.
    """
    # FreeCAD calculates volume in its native unit (mm^3)
    volume_mm3 = shape.Volume
    
    # Use FreeCAD's unit system to convert the density string into kg/mm^3
    # This prevents us from having to do manual unit conversions!
    density_val = App.Units.Quantity(density_str).getValueAs('kg/mm^3')
    
    # Calculate mass (Volume * Density)
    mass_kg = volume_mm3 * density_val
    
    return mass_kg, volume_mm3