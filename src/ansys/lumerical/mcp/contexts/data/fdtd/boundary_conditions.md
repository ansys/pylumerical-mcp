# FDTD Boundary Conditions

This topic covers the four boundary-condition (BC) families used by
the FDTD solver: **PML** (absorbing, open boundaries), **symmetric
/ anti-symmetric** (mirror-plane speed-up), **periodic** (unit-cell
simulation under normal incidence), and **Bloch** (unit-cell under
angled / phase-shifted excitation). PML-extension geometry rules
live in ``fdtd_workflow``; this topic explains how to pick the
right BC and its key sub-options.

## PML (absorbing, open boundaries)

PML is the default for open boundaries -- it absorbs outgoing light
with minimal reflection. The FDTD simulation region exposes four
predefined PML **profiles** (set on the Boundary Conditions tab):

- **Standard** -- best overall absorption with few layers; default.
  Use whenever no material interface cuts through the PML region.
- **Stabilized** -- use when a material interface cuts through PML
  (substrates, claddings ending mid-PML, metal stacks). Suppresses
  the localised exponential-growth instability that the standard
  profile can develop at such interfaces, at the cost of needing
  more PML layers.
- **Steep Angle** -- use when PML is combined with periodic / Bloch
  BCs (gratings, metasurfaces), where light scatters at angles
  nearly parallel to the PML surface.
- **Custom** -- exposes every PML parameter (LAYERS, KAPPA, SIGMA,
  ALPHA, polynomial orders). Reach for it only after the predefined
  profiles fail.

PML profiles can be set **per-boundary**: uncheck
``"same settings on all boundaries"`` on the FDTD solver object,
then only the offending boundary needs the heavier ``stabilized``
profile. This avoids paying the layer-count cost on every face.

Increasing the layer count lowers reflection on any profile;
diverging or noisy simulations are often fixed by switching to
``stabilized`` or raising the layer count on a single boundary.

## Symmetric / Anti-Symmetric (mirror-plane speed-up)

If the EM fields have a plane of symmetry, replace the open BC on
that plane with a symmetry BC and shrink the sim region accordingly.
Each plane gives a 2x speed-up (4x or 8x for multiple symmetries).

Picking the right one is **source-driven**, not just structure-
driven:

- ``"symmetric"`` -- the source's **electric field polarisation is
  tangential** to the symmetry plane (Lumerical colour code: blue
  arrow along the blue BC face).
- ``"anti-symmetric"`` -- the electric polarisation is **normal**
  to the plane (blue arrow into the green BC face).

Common gotchas:

- A wrong choice produces silently incorrect results -- there is no
  warning. Always validate by re-running once without symmetry and
  comparing.
- **Do not shrink the sim region manually**; the GUI greys out the
  half that won't be simulated. In a script just set the BC and
  leave the span alone -- the solver handles unfolding.
- ``getdata`` / ``getelectric`` / ``getmagnetic`` auto-unfold the
  fields back to the full region; monitors entirely inside the
  greyed half record no data.

## Periodic (unit-cell, normal incidence)

For genuinely periodic structures excited at normal incidence,
set the lateral BCs to ``"periodic"`` and draw exactly one unit
cell. The solver simply copies the field at one face to the
opposite face.

Both the **structure** and the **fields** must be periodic. If a
plane wave hits the cell at an angle, fields differ by a phase
between cells -- periodic BCs are then wrong; use Bloch instead.
A single dipole inside a periodic cell (e.g. OLED) is also
non-periodic in the field sense and should not use periodic BCs.

Extend the structure through the periodic boundary so the material
in the one-mesh-cell BC region is correct.

## Bloch (unit-cell, angled / phase-shifted excitation)

Bloch BCs generalise periodic by applying a phase correction
``exp(-i k_bloch * a)`` between opposite faces. Use them for:

- **Periodic structures under angled plane-wave illumination**
  (gratings, metasurfaces, angle-of-incidence sweeps).
- **Bandstructure** calculations, where ``kx`` / ``ky`` / ``kz`` is
  swept manually.

Key flags and costs:

- ``"set based on source angle"`` is on by default and computes the
  Bloch vector from the plane-wave source's angle. Disable it only
  for bandstructure work where ``kx`` is set manually.
- Bloch uses **complex-valued time-domain fields**, so memory and
  runtime can roughly double, and time-domain field / movie
  monitors record complex values (take the real part if needed).
- For **broadband angled** sweeps, the ordinary plane-wave + Bloch
  combination has a frequency-dependent angle; switch to the
  ``BFAST`` source instead (BFAST manages BCs internally and
  overrides Bloch).

## Choosing the Right BC at a Glance

- Free-space scattering / radiation -> PML on all open faces.
- Symmetric structure + suitably polarised source -> add symmetric
  or anti-symmetric on the mirror plane (one per plane).
- Infinite periodic array, normal incidence -> periodic on lateral
  faces + PML on top/bottom (use ``steep angle`` PML).
- Infinite periodic array, angled incidence (single freq) ->
  Bloch on lateral faces + PML on top/bottom.
- Infinite periodic array, broadband angled incidence -> BFAST
  source (its built-in BCs replace Bloch).

See also: ``fdtd_workflow``, ``fdtd_sources_monitors``,
``fdtd_run_and_results``.
