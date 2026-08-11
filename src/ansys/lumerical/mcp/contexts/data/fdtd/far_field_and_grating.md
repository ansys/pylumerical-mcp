# FDTD Far-Field and Grating Projections

This topic covers turning **near-field** monitor data (recorded on
a plane inside the sim region) into:

- **Far-field projections** -- the angular intensity distribution
  many wavelengths away from the source (antennas, scatterers,
  fiber-coupling efficiency).
- **Grating projections** -- the per-order diffraction efficiency
  of a periodic structure (gratings, metasurfaces).

Read ``fdtd_monitors_and_field_extraction`` first for the monitor
that feeds these projections; read ``fdtd_boundary_conditions``
for the periodic / Bloch setup that grating projections require.

## Far-Field Projection (free-space radiation)

The fast path uses the script commands ``farfield2d`` (line
monitor) or ``farfield3d`` (plane monitor) on a frequency-domain
field monitor:

```python
fdtd = _lum_get("antenna")

# Discover what's on the monitor first (see fdtd_run_and_results
# 'datasets-are-dicts' contract).
_lum_print_json(fdtd.getresult("upper_hemisphere"))

# Project to the far-field hemisphere at a single frequency.
# Last argument controls angular resolution: number of samples in
# the angular grid. Larger -> finer angular detail, more memory.
import numpy as np
# Default is 1 for the first frequency point; adjust if the monitor
# records a custom spectrum.
freq_idx = 1
n_pts = 201
ff = fdtd.farfield3d("upper_hemisphere", freq_idx, n_pts)
_lum_print_json({"farfield_shape": list(np.shape(ff))})
```
# Warning: Do not try to get the farfield result using getresult()
# it is not a dataset and will not be visible until after you run the projection command.
# Always run the projection command first, then inspect the result with getresult()
# If you try to get the farfield result before running the projection command,
# the tool may go into a state where it waits for user input via the GUI
# and does not respond to further commands until you click "OK" on the GUI prompt.

Useful companions:

- ``farfield3dintegrate`` -- integrates the far-field pattern over
  an arbitrary cone (NA, divergence, fraction of power into a
  given solid angle).
- ``farfieldexact`` -- replaces the FFT-based default with an
  exact Green's-function integral. Slower but needed for tilted
  hemispheres, high-NA collection, or when the FFT-based result
  shows artefacts.
- ``farfieldfilter`` / ``farfieldspherical`` -- map the result
  onto a numerical-aperture cone or a (theta, phi) sphere.

Setup tips (Lumerical KB *Far-field projections in FDTD overview*):

- Place the monitor **outside** the immediate near-field of the
  emitter (>= a few wavelengths away) but **inside** the inner
  PML edge.
- For sources above a substrate, the substrate must extend through
  the monitor plane; otherwise the projection assumes the wrong
  background medium.
- A single monitor projects into the half-space facing it; use
  multiple monitors (or a bounding box of six) for full-sphere
  patterns.

## Grating Projection (periodic structures)

For a periodic device under plane-wave (or BFAST) illumination,
the far field is a discrete set of diffraction orders. Compute
them with ``gratingn1`` / ``gratingn2`` (order indices) and
``gratingbloch1`` / ``gratingbloch2`` (Bloch-vector components),
combined with grating-projection helpers:

```python
fdtd = _lum_get("grating")

# Order indices visible in the upper half-space.
n1 = fdtd.gratingn1("T_monitor")     # in-plane order along axis 1
n2 = fdtd.gratingn2("T_monitor")     # in-plane order along axis 2

# Per-order power (transmission) -- normalised diffraction
# efficiency.
T_orders = fdtd.grating("T_monitor")
_lum_print_json({"n1": n1.tolist(),
                 "n2": n2.tolist(),
                 "T_orders": T_orders.tolist()})
```

Companion commands:

- ``gratingpolar`` -- per-order amplitude split into TE / TM
  polarisations.
- ``gratingangle`` -- elevation / azimuth angle of each order
  versus frequency (useful for sweeping incidence angle).
- ``gratingvector`` -- the full diffraction-order k-vectors.

Setup requirements:

- Lateral BCs must be **periodic** (normal incidence) or **Bloch**
  / **BFAST** (angled incidence) -- see
  ``fdtd_boundary_conditions``.
- The monitor must span exactly one unit cell.
- The source must be a plane wave (or BFAST plane wave); finite
  beams produce a continuum, not discrete orders.

## NA / Angular Filtering for Coupling Efficiency

For fiber-coupling or microscope-objective efficiency, project
to the far field then filter by numerical aperture:

```python
fdtd = _lum_get("gc")
ff = fdtd.farfield3d("up", 0, 401)
# Fraction of radiated power inside NA=0.4 cone, centred on +z.
T_NA = fdtd.farfield3dintegrate(ff, 401, 401, 0.4, 0, 0)
_lum_print_json({"T_into_NA": float(T_NA)})
```

See also: ``fdtd_monitors_and_field_extraction``,
``fdtd_boundary_conditions``, ``fdtd_sources_monitors``,
``s_parameter_sweep``.
