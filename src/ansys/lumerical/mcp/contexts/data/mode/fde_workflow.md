# MODE FDE Workflow

This topic covers the MODE Finite-Difference Eigenmode (FDE) solver
workflow for waveguide cross-sections, including bent-waveguide setup,
safe property-setting patterns, and sweep-safe project reuse.

Read ``workflow`` first for the generic snippet model and do-not-assume
rules. Pair this topic with ``geometry`` and ``materials`` for shared
layout/material conventions, and with ``mode_fde_results`` for the
``findmodes()`` / extraction half.

## When To Use FDE

Use FDE when the task is to solve waveguide cross-sectional modes,
effective index, loss, polarization, group index, or bent-waveguide
mode properties. FDE solves a cross-sectional eigenvalue problem; it is
not the right solver for full-device taper propagation or EME-style
port-to-port transmission.

## MODE FDE Build Stages

Prefer these stages as separate ``execute_python_code`` snippets:

1. Parameters: wavelength, materials, cladding/substrate, solver span,
   boundary conditions, number of trial modes, and bend settings if any.
2. Add the geometry and materials.
3. Add a bare ``FDE`` object.
4. Configure the FDE object incrementally with ``setnamed()``.
5. Save the setup file.
6. Stop and ask before solving; the solve/extract half lives in
   ``mode_fde_results``.

## Safe Object-Creation Pattern

For MODE FDE, prefer a bare ``addfde()`` followed by one-property-at-a-time
``setnamed("FDE", ...)`` calls. In practice, valid properties can be
rejected when they are packed into the constructor dict, while the same
properties succeed after the object exists.

Safe pattern:

```python
mode = _lum_get("mode_fde")
mode.addfde()
mode.setnamed("FDE", "solver type", "2D Z normal")
mode.setnamed("FDE", "wavelength", wavelength_m)
mode.setnamed("FDE", "number of trial modes", trial_modes)
_lum_print_json({"stage": "fde_configured", "ok": True})
```

Avoid assuming that constructor-time ``addfde({...})`` accepts the same
property surface or activation state as later ``setnamed()`` calls.

## Common FDE Property Names

Commonly-needed keys include:

- ``solver type``
- ``wavelength``
- ``number of trial modes``
- ``x``, ``x span``, ``y``, ``y span``
- boundary keys such as ``x min bc``, ``x max bc``, ``y min bc``,
  ``y max bc``
- ``bent waveguide``
- ``bend radius``
- ``bend orientation``
- ``calculate group index``

Do not assume that a visible alternate spelling such as
``center wavelength`` is active just because it appears in a property dump.
If a property is rejected as inactive, inspect the object state and switch
to the active canonical key.

## Bent Waveguide Setup

The FDE solver can solve bent waveguides directly. For bent-waveguide
tasks:

- set ``bent waveguide`` to enable the bent solver
- set ``bend radius`` explicitly
- set ``bend orientation`` explicitly when the bend plane matters
- use PML boundaries when bend radiation loss must escape the region

The bent-waveguide effective index depends on the chosen bend radius,
while the angular propagation constant is the radius-independent quantity.
Reported ``loss`` is the net waveguide loss in the chosen setup, not a
separate bend-only delta.

## Boundary Conditions

Metal is a common default in FDE, but it is usually the wrong default for
open bent-waveguide loss calculations. If the user asks for radiation or
bend loss, ask before silently leaving metal boundaries in place. Use PML
only when that matches the intended physics.

## Save-Before-Solve And Sweep-Safe Reuse

Always save a clean setup file before solving. After ``findmodes()`` or a
GUI run, MODE enters analysis mode. A solved project can then reject later
geometry or solver edits.

For parameter sweeps, keep a pre-run setup file and reopen that clean
layout-state file for each sweep point instead of mutating a saved
post-solve file.

## Property Discovery

If you need to inspect a property surface, probe locally and keep the probe
side-effect free. Prefer reading the existing FDE object over disposable
object creation that mutates the live project unnecessarily.

## See Also

Use ``mode_fde_results`` for ``findmodes()``, ``getdata()``, and TE/TM
reporting. Use ``mode_eme_workflow`` for taper, converter, and multi-cell
propagation devices where the EME solver is the right abstraction.
