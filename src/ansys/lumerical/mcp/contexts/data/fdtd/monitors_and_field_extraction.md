# FDTD Monitors and Field Extraction

This topic covers the FDTD monitor catalogue (which monitor to add
for which question), the ``override global monitor settings``
flag, mode-expansion analysis, and the **reduce-before-print**
pattern that keeps multi-megabyte field arrays from blowing through
the ``_lum_print_json`` truncation guard.

Related: ``fdtd_sources_monitors`` (global settings,
``setglobalmonitor``), ``fdtd_run_and_results`` (datasets-as-dicts
contract, ``getresult`` discovery, large-array safety),
``fdtd_far_field_and_grating`` (turning monitor data into a
far-field projection).

## Choosing a Monitor Type

- **Power / flux through a plane** -- ``addpower`` (alias of
  ``adddftmonitor``); frequency-domain, integrates E x H.
- **Field profile at a few frequencies** -- ``addprofile`` /
  ``adddftmonitor``; frequency-domain spatial fields.
- **Transient field history** -- ``addtime``; time-domain at a
  point or 1D / 2D slice.
- **Real-time animation** -- ``addmovie``; time-domain frames.
- **Index distribution** -- ``addindex``; snapshot of material
  indices on the mesh.
- **Modal content of a guided wave** -- ``addmodeexpansion``;
  decomposes monitor data into mode amplitudes.
- **S-parameters** -- ``addport`` (see ``fdtd_sources_monitors``).

In modern FDTD, ``addpower`` and ``addprofile`` are aliases for
specific configurations of the DFT monitor (``adddftmonitor``);
either form is acceptable. Prefer the explicit ``adddftmonitor``
when migrating to the modern UI / GUI.

## Override Global Monitor Settings

By default monitors inherit wavelength / frequency points from
``setglobalmonitor`` (set those globally first; see
``fdtd_sources_monitors``). Override per-monitor only when you
have a reason:

```python
fdtd.addprofile({
    "name": "high_res_profile",
    "monitor type": "2D Z-normal",
    "x": 0, "x span": 5e-6,
    "y": 0, "y span": 5e-6,
    "z": 0,
    "override global monitor settings": True,
    "use wavelength spacing": True,
    "use source limits": False,
    "wavelength center": 1.55e-6,
    "wavelength span": 50e-9,
    "frequency points": 51,
})
```

Common reasons to override:

- A field monitor needs finer spectral resolution than the power
  monitors used for the bulk of the spectrum.
- A monitor only cares about a sub-band of the source spectrum.
- A movie monitor needs a different time-window than other
  time-domain monitors.

Resonator simulations frequently override to use **apodization**
on time-domain monitors so that the long pulse tail (from a
high-Q cavity) does not artificially extend the DFT integration.

## Mode-Expansion Monitor

``addmodeexpansion`` attaches to a field monitor and decomposes
the recorded field into mode amplitudes. Used whenever you need:

- Power coupled into a specific waveguide mode (rather than total
  power through a plane).
- Per-mode S-parameters from a non-port monitor.

Workflow:

1. Add a 2D field monitor that spans the waveguide cross-section.
2. ``addmodeexpansion`` over the same plane; link it to the monitor
   via the ``"monitors for expansion"`` property.
3. Set the modal cross-section (``"mode selection"``) the same way
   a mode source picks its mode.
4. After ``run()``, read ``getresult("<mode_expansion_name>",
   "expansion for ...")`` and index ``"a"`` (forward) and ``"b"``
   (backward) amplitudes.

Ports already do this internally -- use mode expansion only when
you cannot use a port (e.g., multi-mode analysis at a non-port
plane).

## Reduce Before You Print

``_lum_print_json`` truncates arrays larger than ``max_array_size``
(200,000 by default) to a ``{"__truncated__": True, ...}`` stub
(see ``fdtd_run_and_results`` large-array safety). For 3D field
monitors **always reduce inside the subprocess** before printing:

```python
fdtd = _lum_get("device")
E = fdtd.getelectric("profile")            # ndarray (Nx, Ny, Nz, Nf, 3)
intensity_xy = (abs(E) ** 2).sum(axis=(2, -1))   # collapse z + vec
_lum_print_json({
    "intensity_xy": intensity_xy.tolist(),
    "x_nm": (fdtd.getdata("profile", "x") * 1e9).flatten().tolist(),
    "y_nm": (fdtd.getdata("profile", "y") * 1e9).flatten().tolist(),
})
```

Or save the heavy array to disk and only print the path:

```python
import numpy as np
fdtd = _lum_get("device")
E = fdtd.getelectric("profile")
out_path = "/tmp/E_profile.npz"
np.savez(out_path, E=E)
_lum_print_json({"saved": out_path, "shape": list(E.shape)})
```

**Never** raise ``max_array_size`` to "fix" a truncation; the
agent's context window cannot absorb a multi-megabyte array
anyway.

See also: ``fdtd_run_and_results``, ``fdtd_sources_monitors``,
``fdtd_far_field_and_grating``.
