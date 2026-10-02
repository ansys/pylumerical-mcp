# FDTD Workflow: Worked Example

A complete, step-by-step build of a straight silicon waveguide with TE
mode ports for S-parameter extraction. Read ``workflow`` and
``fdtd_workflow`` first -- the example is the worked counterpart to
those topics' rules, and it assumes you already understand the
chunked ``execute_python_code`` model, the ``_lum_get`` /
``_lum_print_json`` helpers, the "do NOT make assumptions" rules
(all in ``workflow``), and the FDTD-specific PML extension rule and
build-stage list (in ``fdtd_workflow``).

## User Request

"Silicon (n=3.48) waveguide, 500 nm wide x 220 nm tall x 10 um long,
on a 2 um SiO2 (n=1.44) substrate, air cladding, simulate at 1550 nm
with TE port source/monitors for S-parameters. Wait for confirmation
before running."

## Pre-Flight: Confirm Defaults Before Issuing Any Snippet

The user request above pins geometry, materials, wavelength, and the
source/monitor strategy, but leaves several solver-side knobs
implicit. Apply the ``workflow`` "Do NOT Make Assumptions" rules:
for **this** request, that means explicitly confirming or asking
about each of the following before issuing Step 1 -- do not silently
bake in a default.

- **Mesh accuracy** (integer 1-8 on ``addfdtd``). The Lumerical
  docs recommend **starting at 1-2** for a quick first run and
  raising it only as part of a convergence check; the FDTD solver
  reference defines accuracy 1 = 6 ppw, accuracy 2 = 10 ppw, and
  each step adds 4 ppw. Ask the user which accuracy they want
  rather than baking in an arbitrary "publication-grade" value.
- **Save path** for the ``.fsp``: ask. If the user says "anywhere",
  use ``/tmp/<session_name>.fsp`` (Linux/macOS) or
  ``%TEMP%\<session_name>.fsp`` (Windows) and tell them.
- **Wavelength point count**: "simulate at 1550 nm" means a single
  point unless the user asks for a sweep.
- **Air cladding**: the FDTD background defaults to ``n = 1``
  (vacuum). Either substitute vacuum and say so, or add a custom
  dielectric for air (see ``materials``) -- never substitute
  silently.

The example below assumes the user confirmed ``mesh_accuracy = 2``
(a reasonable first-run value; raise for convergence testing) and
provided ``save_path``. Both are bound as Python variables in
Step 2 so the choices live in one place.

## The Build

Each ``execute_python_code`` snippet is one chunk in the build.

**Step 1 -- open the session** (tool: ``open_session``).
Do NOT pass ``hide`` -- only set it on explicit user request:

```json
{"name": "straight_wg", "product": "fdtd"}
```

**Step 2 -- parameters and simulation region**
(tool: ``execute_python_code``):

```python
fdtd = _lum_get("straight_wg")

waveguide_width = 500e-9
waveguide_height = 220e-9
waveguide_length = 10e-6
substrate_thickness = 2e-6

core_index = 3.48
clad_index = 1.44

wavelength = 1550e-9
pml_extension = 1e-6

# Confirmed with user during pre-flight; referenced (not hard-coded)
# by later snippets so the choices live in exactly one place.
mesh_accuracy = 2                         # 1-8; start low
save_path = "/tmp/straight_wg.fsp"

sim_x_span = waveguide_length
sim_y_span = 3e-6
sim_z_min = -substrate_thickness * 0.5
sim_z_max = waveguide_height + 1e-6

fdtd.addfdtd({
    "x": 0, "x span": sim_x_span,
    "y": 0, "y span": sim_y_span,
    "z min": sim_z_min, "z max": sim_z_max,
    "mesh accuracy": mesh_accuracy,
})

_lum_print_json({"stage": "region", "ok": True,
                 "mesh_accuracy": mesh_accuracy,
                 "save_path": save_path})
```

**Step 3 -- geometry, extended into the PML on the propagation axis**
(see ``geometry`` for ``addX`` syntax and ``fdtd_workflow`` for the
PML extension rule):

```python
fdtd = _lum_get("straight_wg")

fdtd.addrect({
    "name": "substrate",
    "material": "SiO2 (Glass) - Palik",
    "x": 0, "x span": sim_x_span + 2 * pml_extension,
    "y": 0, "y span": sim_y_span + 2 * pml_extension,
    "z min": -substrate_thickness, "z max": 0,
})

fdtd.addrect({
    "name": "waveguide",
    "material": "Si (Silicon) - Palik",
    "x": 0, "x span": sim_x_span + 2 * pml_extension,
    "y": 0, "y span": waveguide_width,
    "z min": 0, "z max": waveguide_height,
})

_lum_print_json({"stage": "geometry", "ok": True})
```

**Step 4 -- global source / monitor settings and ports**
(see ``fdtd_sources_monitors`` for the port-direction convention):

```python
fdtd = _lum_get("straight_wg")

fdtd.setglobalsource("wavelength start", wavelength)
fdtd.setglobalsource("wavelength stop", wavelength)
fdtd.setglobalmonitor("use source limits", True)
fdtd.setglobalmonitor("frequency points", 1)

port_y_span = 2e-6
port_z_center = waveguide_height / 2
port_z_span = 1.5e-6

fdtd.addport({
    "name": "input_port",
    "injection axis": "x-axis",
    "direction": "Forward",
    "mode selection": "fundamental TE mode",
    "x": -sim_x_span / 2 + 0.5e-6,
    "y": 0, "y span": port_y_span,
    "z": port_z_center, "z span": port_z_span,
})

fdtd.addport({
    "name": "output_port",
    "injection axis": "x-axis",
    "direction": "Backward",
    "mode selection": "fundamental TE mode",
    "x": sim_x_span / 2 - 0.5e-6,
    "y": 0, "y span": port_y_span,
    "z": port_z_center, "z span": port_z_span,
})

# Pick which port mode actually injects on this run. The
# ``FDTD::ports`` group owns the injection state (``source port`` +
# ``source mode``); per-port ``"mode selection"`` above only chooses
# which mode each port analyses. Without this step the active source
# defaults silently to whichever port was added first.
fdtd.setnamed("FDTD::ports", "source port", "input_port")
fdtd.setnamed("FDTD::ports", "source mode", "mode 1")

_lum_print_json({"stage": "ports", "ok": True})
```

**Step 5 -- save**. ``save_path`` was bound during Step 2 from the
value the user confirmed at pre-flight, so the agent neither
hard-codes a path here nor invents one:

```python
import os
fdtd = _lum_get("straight_wg")
fdtd.save(save_path)
_lum_print_json({"stage": "saved", "path": save_path,
                 "exists": os.path.isfile(save_path)})
```

**Pause here and ask the user to confirm before running.**

**Step 6 -- run and pull S-parameters.** ``run()`` is called exactly
once; the call blocks until the simulation completes. The ports
group itself is **not** a result provider, so we discover first
(``fdtd.getresult()``) and then index per-port at
``FDTD::ports::<port_name>``. See ``fdtd_run_and_results`` for the
FDTD-specific ``run()`` calling conventions, the
dataset-is-a-dict contract, and the dump-before-index pattern, and
``s_parameter_sweep`` if the user later wants the full N x N
S-matrix.

```python
fdtd = _lum_get("straight_wg")
fdtd.run()
_lum_print_json(fdtd.getresult())
```

After confirming the result providers in the printed output, dump
the per-port dataset structure before indexing:

```python
fdtd = _lum_get("straight_wg")
_lum_print_json(fdtd.getresult("FDTD::ports::output_port", "S"))
```

**Step 7 -- close the session** (tool: ``close_session``) when the
results have been delivered:

```json
{"name": "straight_wg"}
```

See also: ``fdtd_workflow``, ``materials``, ``geometry``,
``fdtd_sources_monitors``, ``fdtd_run_and_results``.
