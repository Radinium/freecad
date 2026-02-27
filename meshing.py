# meshing.py
import ObjectsFem
from femmesh.gmshtools import GmshTools
import settings

def create_mesh(doc, part_obj, analysis):
    gmsh_mesh = ObjectsFem.makeMeshGmsh(doc, "GmshMesh")
    gmsh_mesh.Shape = part_obj
    
    # Apply mesh properties from settings
    gmsh_mesh.CharacteristicLengthMax = settings.mesh_char_length_max
    gmsh_mesh.CharacteristicLengthMin = settings.mesh_char_length_min
    gmsh_mesh.ElementOrder = settings.mesh_element_order                
    gmsh_mesh.OptimizeStd = settings.mesh_optimize_std              
    gmsh_mesh.MeshSizeFromCurvature = settings.mesh_curvature      
    
    analysis.addObject(gmsh_mesh)
    doc.recompute()
    
    gmsh_runner = GmshTools(gmsh_mesh)
    error = gmsh_runner.create_mesh()
    print("Gmsh meshing error status:", error)

    # Export mesh
    gmsh_mesh.FemMesh.write(settings.mesh_file)
    print(f"Mesh exported to {settings.mesh_file}")
    
    return gmsh_mesh