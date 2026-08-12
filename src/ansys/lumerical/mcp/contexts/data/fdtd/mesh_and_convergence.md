# FDTD Mesh and Convergence

This topic covers the four levers that determine FDTD accuracy and
runtime: the global ``mesh accuracy`` knob, **conformal mesh**
refinement variants, **mesh override** regions for local
refinement, and the **simulation time / auto-shutoff** controls
plus divergence diagnostics.

## Global Mesh Accuracy

The FDTD solver's ``"mesh accuracy"`` property is an integer
1-8 that sets the auto-mesh's points-per-wavelength (ppw) in the
highest-index material:

- ``1`` -> ~6 ppw (very coarse; fast smoke test)
- ``2`` -> ~10 ppw (sensible starting point)
- each step adds 4 ppw, so ``3`` -> 14, ..., ``8`` -> 30+

Guidance from the Lumerical docs:

- **Start at 1-2.** Get a working build, then raise accuracy as
  part of a convergence test (rerun at successively higher values
  and watch the metric of interest stop changing).
- Memory and runtime scale with the cube (3D) of mesh density, so
  jumping straight to 6+ can be very expensive.
- The auto-mesh sees only **dielectric** index; for metals or
  thin features you almost always need a local override (below).

## Conformal Mesh Refinement

The "Mesh refinement" pull-down on the FDTD solver picks how
sub-cell material boundaries are handled. Useful options:

- **Staircase** -- no sub-cell treatment; each Yee cell takes one
  material. Fastest, least accurate; use only for sanity checks.
- **Conformal variant 0** (default) -- the conformal mesh
  technology (CMT) on dielectrics only; metals and PEC fall back
  to staircase. Good default for most photonic structures.
- **Conformal variant 1** -- CMT on everything **except** PEC and
  interfaces involving a metal. Enables sub-cell accuracy for
  most dispersive metals; verify with a convergence test before
  trusting it.
- **Conformal variant 2** -- CMT on all materials including
  metals. Most accurate sub-cell treatment, but can be less stable
  on lossy / dispersive interfaces.
- **Dielectric volume average** -- averages permittivity over the
  cell; reasonable for slowly varying dielectrics.

## Mesh Override Regions

Drop an ``addmesh`` block over a sub-region whenever the auto-mesh
can't see the feature you care about (thin metal layer, small gap,
sub-wavelength corner). Override regions force a finer grid only
inside their bounds:

```python
fdtd.addmesh({
    "name": "metal_film_override",
    "x": 0, "x span": 2e-6,
    "y": 0, "y span": 2e-6,
    "z": metal_z, "z span": metal_thickness + 2 * dx,
    "dx": 5e-9, "dy": 5e-9, "dz": 2e-9,
    "based on a structure": False,
})
```

Tips:

- Always cover the full physical feature **plus** ~1-2 mesh cells
  on each side; clipping the override is a common mistake.
- For thin (< lambda/100) layers, target ``dz`` to give at least
  2 cells across the layer; otherwise the material is invisible
  to the solver.
- Override regions can also be "based on a structure" so they
  follow geometry edits.

## Simulation Time and Auto-Shutoff

Two FDTD-solver fields cap the run:

- ``"simulation time"`` (fs) -- hard wall-clock-equivalent
  upper bound. Default is generous; halve it for quick sanity
  checks.
- ``"auto shutoff min"`` -- the solver stops early when the
  remaining field energy drops below this fraction of the peak.
  Default ``1e-5`` is fine for transmission/reflection;
  resonators and cavities may need ``1e-6`` or smaller to capture
  long ring-down tails.

The ``STATUS`` integer result on the FDTD solver after ``run()``
tells you which one fired:

- ``1`` -- ran to ``simulation time`` (no shutoff). Often means
  the simulation hadn't decayed enough; lower ``auto shutoff min``
  or extend ``simulation time``.
- ``2`` -- auto-shutoff fired (the healthy case).
- ``3`` -- diverged (see below).

## Divergence Diagnostics

If a run diverges (NaNs, fields blowing up), the most common
causes documented in the Lumerical KB:

- **Material interfaces cut through PML** -> switch the offending
  face to the ``stabilized`` PML profile (see
  ``fdtd_boundary_conditions``).
- **Metals touching PML** -> truncate the metal ~1 mesh cell short
  of the inner PML edge and disable ``"extend structure through
  PML"`` on the solver.
- **Under-resolved metals / corners** -> add a local mesh override
  (above) or raise global accuracy.
- **Anisotropic / dispersive material outside its valid range** ->
  re-fit the material model or restrict the source bandwidth.

After a diverging run, ``fdtd.getresult("FDTD", "simulationdata")``
exposes diagnostics (field-energy log, mesh stats); use them
before re-running blindly.

See also: ``fdtd_workflow``, ``fdtd_boundary_conditions``,
``fdtd_run_and_results``.
