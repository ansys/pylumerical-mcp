# FDTD Workflow (Build & Setup)

This topic covers the FDTD-specific **build/setup** half of the
chunked ``execute_python_code`` workflow: the FDTD stage list, the
PML boundary-extension rule, and the FDTD-flavoured disambiguation
defaults. The matching **run + results** half (FDTD-specific
``run()`` calling conventions, ``run()``-once / ``switchtolayout``
rule, dataset-is-a-dict contract, ``getresult`` discovery) lives in
``fdtd_run_and_results``.

**Read ``workflow`` first** for the generic execution model
(``_lum_get`` / ``_lum_print_json`` helpers), snippet structure,
parameter management, and the "do NOT make assumptions / do NOT
invent or re-run" rules that apply to every Lumerical product.

## Disambiguation Defaults (FDTD)

Apply only when the user's request is ambiguous; if any parameter
is explicitly stated, follow the user. The product-agnostic
SI-units default lives in ``workflow``.

- **Geometry**: 3D unless the user explicitly asks for 2D.
- **Boundary conditions**: PML on all open boundaries (see "PML
  Boundary Extension" below).
- **Materials**: prefer built-in library entries (see ``materials``).

For **2D FDTD**, the simulation region is always **z-normal**, so the
computational plane is **XY**. Do not invent an arbitrary 2D plane
orientation. If the user asks for 2D, keep the pattern in XY and treat
out-of-plane extent as the Z axis.

## PML Boundary Extension

FDTD uses PML on all open boundaries. Any structure that should be
"infinitely extended" in a given direction (substrates, cladding
layers, waveguides continuing past the device) **must extend
comfortably past the inner PML boundary**, otherwise the material
interface coincides with the PML region and produces spurious
reflections.

Rules:

- The FDTD solver setting ``"extend structure through PML"`` is
  **on by default**, which automatically extends any structure
  that touches the inner PML edge through the PML layer. The
  manual extension pattern below is what makes the structure
  touch that inner edge in the first place, and is also required
  in the cases where you must turn this option **off**:
  - **Photonic crystals / periodic gratings** -- the periodic
    cell must end cleanly at the PML edge; turn auto-extend off.
  - **Metal layers near the PML** -- often the source of
    diverging simulations; truncate ~1 mesh cell short of the
    PML and disable auto-extend.
- **Calculate the extension from the simulation region span, not
  the nominal device dimension.** A 10 um waveguide inside a 12 um
  simulation region needs
  ``x span = sim_x_span + 2 * pml_extension``, not
  ``waveguide_length + 2 * pml_extension``.
- Apply only to the "infinite" axes. The waveguide's transverse
  width is finite and must NOT be extended.
- The exact ``pml_extension`` value is not critical; aim for
  something larger than the PML region thickness (which scales
  with PML-layer count and inversely with mesh size).

```python
sim_x_span = 12e-6           # simulation region span on the propagation axis
pml_extension = 1e-6         # how far past the sim region to extend

fdtd.addrect({               # waveguide: extended along x, finite in y/z
    "name": "waveguide",
    "x": 0, "x span": sim_x_span + 2 * pml_extension,
    "y": 0, "y span": waveguide_width,
    "z min": 0, "z max": waveguide_height,
})
```

See ``fdtd_workflow_example`` Step 4 for a worked substrate +
waveguide pair, and ``geometry`` for the dictionary-based ``addX``
syntax used here.

## FDTD Build Stages

Following ``workflow``'s chunking principle, an FDTD build
typically breaks into these stages -- one ``execute_python_code``
snippet each:

1. **Open session** -- ``open_session`` MCP tool with
   ``product="fdtd"``.
2. **Parameters + simulation region** -- declare dimensions,
   indices, wavelength, mesh accuracy, save path; call
   ``fdtd.addfdtd(...)``.
3. **Materials** -- only if custom materials are needed (see
   ``materials``).
4. **Geometry** -- substrate, waveguide, cladding, etc. See
   ``geometry`` for the dict-form ``addX`` syntax and the PML
   extension rule above.
5. **Sources and monitors** -- ``setglobalsource`` /
   ``setglobalmonitor``, ports vs. mode sources (see
   ``fdtd_sources_monitors``).
6. **Save** -- ``fdtd.save("<path>.fsp")``.
7. **Pause for user confirmation, then run and extract.** Final
   snippet calls ``fdtd.run()`` and pulls results via
   ``_lum_print_json(fdtd.getresult(...))``. The full FDTD-specific
   run + extraction guidance (solver / resource / GPU arguments,
   re-run rules, dataset-is-a-dict contract, the dump-before-index
   pattern) lives in ``fdtd_run_and_results``.

## Worked End-to-End Example

A full step-by-step build (straight silicon waveguide with TE port
S-parameter extraction) lives in ``fdtd_workflow_example``.

## Summary

- **Read ``workflow`` first** for the generic snippet / chunking /
  do-not-assume / wait-for-confirmation-before-run rules and the
  SI-units default.
- **Extend "infinite" structures past the sim region into the
  PML**, calculated from the sim region span (not the device
  dimension).
- **Datasets are dicts**: always
  ``_lum_print_json(<handle>.getresult(...))`` before indexing.
  See ``fdtd_run_and_results``.

See also: ``workflow``, ``fdtd_workflow_example``, ``materials``,
``geometry``, ``fdtd_sources_monitors``, ``fdtd_run_and_results``.
