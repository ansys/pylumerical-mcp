# Device Simulation Region

This topic covers simulation-region setup for HEAT, CHARGE, FEEM, and DGTD.

Read ``workflow`` first for the generic execution model and do-not-assume
rules, and ``device_workflow`` for the DEVICE-specific build stages.

## What Matters For MCP Workflows

- The simulation region is a separate object from the solver.
- A solver does not define its computational domain by itself.
- Link each solver to a region explicitly by name.

Use this topic whenever the task depends on domain size, boundary behavior,
or background material.

## Region Definition (Script-Facing)

Define the region with explicit geometry and boundary intent:

- choose dimension (2D or 3D) (Note that default is 2D Y-Normal)
- set per-face boundary behavior (``Open``, ``Closed``, ``Shell``)
- set region extents explicitly (center + span or min/max)
- set background material when using a fully closed domain

Do not infer domain extents from nearby solids. Set region geometry directly.

## Solver-To-Region Linkage

Bind each solver to the intended region via the solver's
``simulation region`` property:

```python
device.setnamed("CHARGE", "simulation region", "CHARGE simulation region")
```

Use the same pattern for HEAT, FEEM, DGTD, and any additional finite-element
solver in the project.

## Quick Validation Checks

- Verify solver-to-region mapping first.
- Verify boundary mode on each face (especially mixed boundary setups).
- Verify background material is consistent with solver physics and boundary
  choice.

## See Also

``workflow`` for the generic execution model. ``device_materials`` for shared model-material
creation and database discovery. ``device_workflow`` for HEAT / CHARGE / FEEM / DGTD solver
configuration, simulation region setup, boundary conditions, monitors, and results.
