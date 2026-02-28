# Cantilever Bracket Analysis & Optimization (FreeCAD + FEM)

This repository is a portfolio project that automates a **cantilever bracket** workflow:

1. Generate a parametric 3D bracket geometry in FreeCAD.
2. Run finite element analysis (FEA) with CalculiX.
3. Evaluate mass, stress, and displacement.
4. Optimize key geometric variables using differential evolution.

---

## Why this project

The goal is to demonstrate practical engineering automation skills:

- Parametric CAD modeling
- FEM simulation setup in code
- Post-processing simulation results
- Design optimization under constraints

---

## Tech stack

- **Python**
- **FreeCAD API** (Part / FEM workbench modules)
- **CalculiX** (solver)
- **Gmsh** (meshing)
- **SciPy** (`differential_evolution`)
- **VTK / NumPy** (result extraction)

---

## Repository structure

```text
.
├── main.py                 # Entry point
├── app/
│   ├── geometry.py         # Parametric bracket generation + STEP export
│   ├── meshing.py          # Gmsh mesh generation
│   ├── fea_setup.py        # Material, BCs, solver execution
│   ├── post_processing.py  # Extract max displacement/stress, compute mass
│   ├── evaluator.py        # End-to-end single design evaluation
│   ├── optimize.py         # Differential evolution optimization loop
│   └── settings.py         # Geometry, material, mesh, and file parameters
└── opt_log.txt             # Optimization log output
```

---

## How it works

### 1) Parametric geometry
The bracket profile is created on the YZ plane, extruded, drilled with two bolt holes, and reinforced with two ribs.

### 2) FEA setup
The script applies:
- a fixed boundary condition on one face,
- an external force on another face,
- linear static analysis with CalculiX.

### 3) Results extracted
For each design candidate, the pipeline computes:
- maximum displacement,
- maximum von Mises stress,
- volume and mass,
- safety factor (`yield_strength / max_stress`).

### 4) Optimization objective
The optimizer minimizes mass while applying penalties when stress or displacement exceed allowed limits.

---

## Getting started

### Prerequisites

You need a Python environment with FreeCAD FEM dependencies available. Typical requirements:

- FreeCAD (with FEM modules)
- CalculiX
- Gmsh
- Python packages: `scipy`, `vtk`, `numpy`, `meshio`

> Note: Running this project usually requires launching Python from an environment where FreeCAD modules are importable.

### Run

```bash
python main.py
```

This will run the optimization and print the best variables and final performance metrics.

---

## Key parameters to customize

Open `app/settings.py` and tune:

- **Geometry:** `base_t`, `arm_t`, `rib_t`, etc.
- **Material:** `youngs_modulus`, `density`, `yield_strength`
- **Mesh:** characteristic lengths, element order
- **Load case:** `force_magnitude`
- **Output files:** STEP / mesh / result paths

Optimization bounds are currently set in `app/optimize.py`.

---

## Current status / roadmap

### Implemented
- End-to-end scripted CAD → FEM → optimization loop
- Automatic extraction of mass/stress/displacement

### Planned improvements
- Multiple load cases
- Manufacturability constraints
- Better objective formulation (multi-objective / Pareto front)
- Result visualization and report generation
- Unit tests and robust error handling

---

## Portfolio highlights

This project demonstrates the ability to:

- Build simulation-driven design workflows,
- Integrate CAD + CAE + optimization tools,
- Translate engineering goals into code and objective functions.

---

## License

Add a license file (`MIT`, `Apache-2.0`, etc.) depending on how you want others to use this code.
