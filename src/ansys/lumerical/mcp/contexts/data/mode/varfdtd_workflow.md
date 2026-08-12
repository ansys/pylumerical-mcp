# MODE varFDTD Workflow

This topic covers the MODE variational FDTD (varFDTD) workflow for planar
integrated photonic devices that can be modeled with a 2.5D effective-index
approximation. varFDTD reduces a 3D structure to a 2D propagation problem by
deriving effective material properties from a reference vertical slab mode.

Read ``workflow`` first. Pair this topic with ``geometry`` and ``materials``.
Use FDE first when the user still needs cross-sectional mode design inputs;
use varFDTD for the larger planar propagation problem after those inputs are
known.

## When To Use varFDTD

Use varFDTD for slab and ridge waveguides, ring resonators, and other planar
photonic components where the vertical physics is well represented by a chosen
reference slab mode and coupling between supported vertical slab modes is
limited.

Prefer varFDTD over full 3D FDTD when the device fits that 2.5D assumption and
the main goal is efficient guided-wave propagation through a planar structure.

Do not use varFDTD as a substitute for FDE mode solving, and do not treat it as
an exact replacement for full 3D FDTD when the vertical approximation is weak.
Its accuracy depends directly on whether the selected slab mode and
polarization are physically representative of the actual device.

## Information Required Before Setup

Before building the model, obtain or confirm:

- geometry dimensions and layout
- material assignments and any required dispersive models
- simulation-region position and spans
- background index
- simulation time and acceptable auto-shutoff behavior
- wavelength or frequency range of interest
- the slab-mode position and polarization or mode choice for the effective
  index model

Do not invent these values. The wavelength range matters not only for sources
and monitors, but also for effective-material generation, meshing behavior, and
bandwidth-dependent fitting.

## Recommended Workflow

1. Confirm the device is suitable for the 2.5D varFDTD approximation.
2. Build the geometry and assign the intended material models.
3. Add the varFDTD simulation region and set its position, spans, background
   index, and simulation time.
4. Configure the Effective Index settings carefully, especially slab-mode
   position, polarization or explicit mode selection, and bandwidth model.
5. Inspect the generated effective materials using test points or an effective
   index monitor before relying on the setup.
6. Add supported sources and the monitors needed for field, power, or
   mode-expansion analysis.
7. Save the setup file and ask before running.
8. Validate the setup with convergence checks and effective-material sanity
   checks before trusting production results.

## Effective Index Settings

The Effective Index tab is the solver-specific core of the workflow because it
defines how the original 3D structure is converted into the 2D effective-index
model.

Key settings include:

- slab-mode position: place this sample point inside the intended core region so
  the reference vertical slab mode is computed from the right part of the
  device
- polarization or explicit mode selection: this choice directly affects the
  generated effective indices
- effective-index method: use the solver's supported formulation instead of
  assuming one method is always correct
- simulation bandwidth mode: choose narrowband for single-frequency or very
  narrowband studies, and broadband when a dispersive effective-material fit is
  required over a wavelength range
- test points: use them to inspect generated effective materials in selected
  parts of the structure
- clamp to physical material properties: enable this when the effective-index
  procedure produces clearly nonphysical values such as an artificial negative
  imaginary index

If the geometry is made of z-extruded structures with vertical sidewalls, use
the available meshing optimization for that case when appropriate.

## Mesh And Boundary Conditions

varFDTD uses a rectangular Cartesian mesh. A practical starting point is auto
non-uniform meshing with mesh accuracy 1 or 2 for quick initial checks, then
increase resolution during convergence testing.

The meshing algorithm refines automatically in high-index and highly absorbing
regions, but that does not remove the need for user-driven convergence checks.

Supported boundary conditions include:

- PML
- PEC or metal
- PMC
- periodic
- Bloch
- symmetric and anti-symmetric

Choose boundaries that match the physical problem and the source symmetry. Do
not assume a symmetry or periodic boundary is safe unless it is justified by the
actual device and excitation.

## Sources And Monitors

Most standard FDTD sources are available in varFDTD, but import source and port
objects are not supported. Do not suggest port-based setup for varFDTD.

Most standard monitor types behave similarly to their FDTD counterparts. The
effective index monitor is specific to this workflow and reports the generated
2D effective-index profile associated with the chosen slab mode and test-point
configuration.

Typical analysis monitors include:

- field monitors
- power monitors
- mode-expansion monitors
- optional effective index monitors for validating the generated materials

These are commonly used to extract field profiles, transmission, and related
guided-wave metrics.

## Validation And Physicality Checks

Reliable varFDTD results require convergence testing on:

- mesh density
- bandwidth settings
- boundary conditions

Also verify that the selected slab mode and polarization are physically
appropriate for the device under study.

Use test points or an effective index monitor to inspect the generated effective
indices and compare them with the expected material-property bounds of the
original structure. If the generated values are nonphysical, enable clamping to
physical material properties and recheck the effective-material results before
continuing.

## Layout / Analysis Behavior

The generic workflow rules still apply here: ask before running, and after a
run only switch back to layout if the user has explicitly confirmed that
discarding results is acceptable.

## See Also

Use ``mode_fde_workflow`` and ``mode_fde_results`` when the task is still at
the cross-sectional design stage. Use FDTD topics only when the user needs full
3D simulation rather than the MODE varFDTD approximation.
