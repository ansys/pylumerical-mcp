# DEVICE Workflow (HEAT / CHARGE / FEEM / DGTD)

This topic covers the **build/setup and run/results** workflow for the
Lumerical finite-element design environment, which hosts the HEAT, CHARGE,
FEEM, and DGTD solvers.

**Read ``workflow`` first** for the generic execution model, snippet
structure, and the do-not-assume / do-not-invent rules.

For material creation, fetch ``device_materials``.
For simulation-region setup, fetch ``device_simulation_region``.
For geometry objects, fetch ``geometry``.

## Finite-Element Build Stages (Chunked)

Follow this order. Each stage maps to one ``execute_python_code`` snippet.

### Stage 1 -- Parameters

Declare all user-configurable values (solver type, domain extents, material
names, bias voltages, temperatures, mesh settings, etc.) with SI units.

### Stage 2 -- Create Model Materials

Build model materials before adding geometry. See ``device_materials``
for the full pattern. Key points:

- Use ``addmodelmaterial()`` then ``set("name", ...)`` to create the model.
- Attach property families with ``addmaterialproperties(family, db_name)``.
  Only add families the solver actually needs (``HT`` for thermal,
  ``CT`` for electrical, ``EM`` for optical).
- After each ``addmaterialproperties`` call, re-select the model material
  before adding the next family -- the selection shifts to the inserted
  property object.

```python
device.addmodelmaterial()
device.set("name", "silicon")
device.addmaterialproperties("HT", "Si (Silicon)")
device.select("materials::silicon")
device.addmaterialproperties("CT", "Si (Silicon)")
```

### Stage 3 -- Create Geometry

Use the shared ``geometry`` workflow (``addrect``, ``addcircle``, etc.).
Assign model materials to geometry objects with ``setnamed``:

```python
device.setnamed("Si_layer", "material", "silicon")
```

### Stage 4 -- Add Solver

Add the finite-element solver object with the appropriate ``add*`` command:

| Solver  | lumapi command  |
|---------|-----------------|
| HEAT    | ``addheatsolver()``   |
| CHARGE  | ``addchargesolver()`` |
| FEEM    | ``addfeemsolver()``   |
| DGTD    | ``adddgtdsolver()``   |

Solver objects have fixed names assigned by Lumerical and cannot be renamed.
After adding, configure its general settings directly using the fixed name:

```python
device.addheatsolver()
# The solver is accessible as "HEAT" -- do not attempt to rename it.
```

### Stage 5 -- Set Simulation Region

The simulation domain is a separate Simulation Region object, not the solver
itself. See ``device_simulation_region`` for the full pattern. Key points:

- New projects start with one Simulation Region already present.
- Set boundary types (``Open``, ``Closed``, or ``Shell``) per face independently.
- Set the solver's ``simulation region`` property to the exact region name:

```python
device.setnamed("HEAT", "simulation region", "HEAT simulation region")
```

### Stage 6 -- Add Doping (CHARGE only)

Doping profiles are required for CHARGE simulations and are added as children
of the CHARGE solver object. Skip this stage for HEAT, FEEM, and DGTD.

Common doping profiles and the corresponding constructors include
* constant: ``adddope()``
* diffusion: ``adddiffusion()``
* implant: ``addimplant()``

After adding, configure the doping region by name:

```python
device.adddope()
device.set("name", "p_doping")
device.setnamed("CHARGE::p_doping", "dopant type", "p")
device.setnamed("CHARGE::p_doping", "concentration", 1e23)  # in 1/m^3
```

### Stage 7 -- Add Boundary Conditions

Boundary conditions are children of the solver's ``boundary conditions``
sub-object. After adding a BC, it can be found under the solver's object tree and configured by
name.

```python
device.addtemperaturebc()
device.set("name", "Tbc")
device.setnamed("HEAT::boundary conditions::Tbc", "temperature", 330)
```

Some BC commands apply to multiple solvers. For example, ``addtemperaturebc()`` applies to both HEAT
and CHARGE. The correct solver needs to be defined in the syntax if multiple solvers are present.
For example, if both HEAT and CHARGE are present, the syntax is:

```python
device.addtemperaturebc("HEAT")  # when CHARGE solver is also present
```

Use ``device.getcommands()`` to discover the exact ``add*bc`` command
names available in the current session before adding any boundary condition.
Exception is device.addelectricalcontact() which is used to add electrical contact
boundary conditions for CHARGE solver. This command is only available when CHARGE solver is present
in the project.

### Stage 8 -- Add Monitors

Monitors are also children of the solver object. After adding a monitor,
it can be found under the solver's object tree and configured by name.

```python
device.addchargemonitor()
device.set("name", "charge_monitor")
device.setnamed("CHARGE::charge_monitor", "integrate total charge", True)
```

Monitors can also apply to multiple solvers. Set the solver name in the syntax when needed:

```python
device.addtemperaturemonitor("CHARGE")  # when HEAT, FEEM, or DGTD solver is also present
```

Use ``device.getcommands()`` to discover the exact ``add*monitor`` command
names available in the current session before adding any monitor.

### Stage 9 -- Save

```python
device.save(path)
```

### Stage 10 -- Run (requires explicit user confirmation)

```python
device.run("HEAT")          # pass the solver name
```

Do NOT call ``run()`` without explicit user confirmation. Finite-element
runs can be long and overwrite the project file.

### Stage 11 -- Collect Results

Results come from two sources:

1. **Monitors** -- call ``getresult(solver_name::monitor_name, dataset)`` on the monitor
   object.
2. **Solver object** -- the solver itself also exposes result datasets. Use
   ``getresult(solver_name, dataset)`` to access them.

Always inspect available datasets first:

```python
_lum_print_json({"monitor_results": device.getresult("temp_monitor"),
                 "solver_results": device.getresult("HEAT")})
```

Then index into specific fields only after confirming the dataset structure.

## Solver-Specific Notes

- **HEAT**: physics is thermal conduction / convection. BCs include
  fixed temperature, heat flux, and convection. Key result: temperature
  distribution.
- **CHARGE**: physics is drift-diffusion carrier transport. BCs include
  electrical contacts (Ohmic / Schottky). Key results: carrier densities,
  electric field, current density, band structure.
- **FEEM**: finite-element electromagnetic solver for waveguide modes.
  Workflow is similar but solver is optical; BCs are electromagnetic.
- **DGTD**: discontinuous Galerkin time-domain solver for broadband EM.
  Sources and monitors resemble FDTD but mesh and BCs are
  finite-element style.

## See Also

``device_materials``, ``device_simulation_region``, ``geometry``,
``workflow``.
