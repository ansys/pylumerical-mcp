# FDTD Run and Results

This topic covers the FDTD-specific **run and results** half of the
workflow: the ``run()`` calling conventions (solver / resource type
/ resource name / CUDA / Cloud Burst arguments documented for the
``run`` script command), the run-once + ``switchtolayout`` rule for
re-running, the dataset-is-a-dict contract for extracting data, and
the per-port S-parameter contract (and where the full N x N
S-matrix actually comes from).

The product-agnostic ``run()`` semantics (blocks, returns no data,
raises on failure; ``save()`` before ``run()``; ask the user before
invoking it) live in ``workflow``; the FDTD build/setup half (build
stages, PML extension, disambiguation defaults) lives in
``fdtd_workflow``.

## Running an FDTD Simulation

### Solver / Resource / GPU Arguments

The lsf positional arguments documented for the ``run`` script
command map 1:1 to Python positional arguments on the handle. All
forms are optional overrides for **a single call** -- they do not
mutate the project's saved solver / resource defaults.

```python
fdtd = _lum_get("project_name")
fdtd.run()                              # use project defaults
fdtd.run("FDTD")                        # pick the solver: "FDTD" or
                                        # "RCWA" (RCWA is CPU-only)
fdtd.run("FDTD", "GPU")                 # pick resource type:
                                        # "CPU" or "GPU"
fdtd.run("FDTD", "GPU", "my_cluster")   # also pick a named resource
                                        # set from the resource
                                        # configuration window
fdtd.run("FDTD", "GPU", "my_cluster",
         [0, 1])                        # pin specific GPUs via
                                        # CUDA_VISIBLE_DEVICES
                                        # (single value or list)
```

For Ansys Cloud Burst Compute submission (FDTD only). The
``getresource`` signature takes the resource **name** only -- not
the ``(solver, resource_type, name)`` triple used by ``run()``:

```python
burst_settings = fdtd.getresource("burst")
# ... edit fields on burst_settings as needed ...
fdtd.run("FDTD", "GPU", "burst", burst_settings)
```

For **2D FDTD**, prefer ``CPU`` instead of ``GPU``. If a user explicitly
asks for GPU on a 2D job, warn that the run may be unsupported or limited
on GPU in the current environment and confirm before proceeding.

### Run Once; ``switchtolayout`` to Re-run

FDTD's ``run()`` is meant to be called **once** per project state:

- After ``run()`` the project is in **analysis mode** and the
  layout is frozen. Mutating geometry, sources, or monitors at this
  point raises an lsf error.
- To re-run after editing the layout, drop back to layout mode via
  ``fdtd.switchtolayout()``. **This discards every single-run
  result** (per-port ``"S"``, monitor data); always extract first:

  ```python
  _lum_print_json(fdtd.getresult("FDTD::ports::output_port", "S"))
  fdtd.switchtolayout()
  # ... mutate parameters / objects ...
  fdtd.save(save_path)
  fdtd.run()
  ```

  Sweep results (``getsweepresult(...)``) survive a layout switch;
  single-run monitor / port data does not.

- **Only re-run when the user has explicitly asked for it.** A
  follow-up question about an existing result does not warrant
  another solver call.
- A single ``fdtd.run()`` excites **one port mode** -- whichever
  ``source port`` + ``source mode`` is currently selected on the
  ``FDTD::ports`` group (see ``fdtd_sources_monitors``). The
  per-port ``"S"`` dataset gives one column of the full S-matrix.
  For the full N x N S-matrix of a multi-port device, use the
  S-parameter matrix sweep (see ``s_parameter_sweep``); do not
  loop ``fdtd.run()`` manually with different active ports.

### Read the Error Message Before Changing the Model

If ``fdtd.run(...)`` fails, inspect the actual error text before changing
geometry, sources, or monitors.

- GPU limitation or unsupported-feature message: treat it as a resource
  issue first; for 2D FDTD, switch to ``CPU`` before changing the model.
- Named resource unavailable: retry with project defaults or confirm the
  requested resource name.
- Divergence or physics/setup error: debug the layout and solver setup,
  not the resource type.

## Datasets Are Dicts, Not Objects

Every Lumerical *dataset* (the thing returned by ``fdtd.getresult(...)``,
``fdtd.getdata(...)``, ``fdtd.getelectric(...)``, etc.) is surfaced by
PyLumerical as a **plain Python dict**. There is no attribute access:

```python
# WRONG -- these will raise AttributeError
result = fdtd.getresult("FDTD::ports::input", "S")
result.S          # AttributeError
result.lambda_    # AttributeError

# RIGHT -- index by string key
result = fdtd.getresult("FDTD::ports::input", "S")
s_column = result["S"]
wavelengths = result["lambda"]
```

## Discover Before You Reach (Always)

Do not guess monitor names, dataset names, or property keys. Use the
discovery primitives **first**, then drill down by string key:

```python
fdtd = _lum_get("straight_wg")

# 1. List every monitor / analysis group that has results. The
#    "FDTD::ports" group itself is NOT in this list -- the ports
#    group is a container, not a result provider (see below).
_lum_print_json(fdtd.getresult())

# 2. List the dataset names available on a specific port. The valid
#    path is "FDTD::ports::<port_name>", never just "FDTD::ports".
_lum_print_json(fdtd.getresult("FDTD::ports::input"))

# 3. Pull a specific dataset (then dump it before indexing).
_lum_print_json(fdtd.getresult("FDTD::ports::input", "S"))
```

For object properties (rather than results), use ``getnamed`` /
``setnamed``:

```python
fdtd = _lum_get("straight_wg")
_lum_print_json(fdtd.getnamed("input_port"))   # all properties of input_port
```

## Per-Port S Versus Full S-Matrix

Assuming an aggregate S-matrix exists where it does not is the most
common FDTD post-processing mistake. The rules:

- **``FDTD::ports`` is a group, not a result provider.** Calling
  ``fdtd.getresult("FDTD::ports", ...)`` raises
  ``LumApiError: 'FDTD::ports is not a result provider'``. The
  Lumerical KB is explicit: "results are available from the
  individual port objects inside the port group."
- **Per-port S** lives at ``FDTD::ports::<port_name>``. The ``"S"``
  dataset is a ``complex128`` ndarray of shape ``(N_freq, N_modes)``
  for that monitor port relative to whichever port was the source
  on the run that produced it. After a single ``fdtd.run()``, only
  the configured source port injects, so the S-values you can read
  are one column (and its reflection) of the full matrix -- never
  the matrix itself.
- **The full N x N S-matrix is a sweep result**, not a single-run
  result. It is produced by the S-parameter matrix sweep tool
  (``addsweep(3)`` + ``runsweep("s-parameter sweep")``) which
  launches N simulations, one per active source row. After the
  sweep runs, the matrix is read with
  ``fdtd.getsweepresult("s-parameter sweep", "S matrix")``. See
  ``s_parameter_sweep`` for the recipe.

Port names depend on how the build added ports; never hard-code
labels like ``"Through"`` / ``"Drop"`` / ``"Input"`` without first
confirming them via ``fdtd.getresult()``.

```python
fdtd = _lum_get("straight_wg")

# Step 1: dump it. ALWAYS dump first.
result = fdtd.getresult("FDTD::ports::output", "S")
_lum_print_json(result)
```

The agent reads the printed JSON, confirms the keys (``"S"``,
``"lambda"``, ``"f"``, ...) and shapes, and only **then** writes a
follow-up snippet that indexes them.

```python
import numpy as np
fdtd = _lum_get("straight_wg")

# Step 2: now that we know the shape, pull what we want. ``S`` is
# shape (N_freq, N_modes); for a single-mode port the only mode
# index is 0, so ``S[:, 0]`` is the per-frequency complex
# transmission from the source port to this port.
result = fdtd.getresult("FDTD::ports::output", "S")
_lum_print_json({
    "S21_abs": np.abs(result["S"][:, 0]).tolist(),
    "lambda_nm": (result["lambda"] * 1e9).flatten().tolist(),
})
```

Implications:

- For a per-port S column at one wavelength (a handful of complex
  numbers) you can dump the whole dataset and read it directly.
- For a 3D field monitor (``E``, ``H``) you will hit the truncation
  guard. **Don't** raise ``max_array_size`` to "fix" this -- the LLM
  context window cannot absorb a multi-MB field anyway. Instead,
  either:

  * Reduce in the subprocess before printing
    (``_lum_print_json({"intensity_at_z0": (abs(E)**2).sum(axis=-1).tolist()})``),
    or
  * Save the array to disk inside the subprocess
    (``np.savez(...)``) and only print the path / a small summary.

## End-to-End Example: Pull S-Parameters After ``run()``

This is the typical "after confirmation" snippet referenced from
``fdtd_workflow`` step 7. It runs once, dumps available result
providers and the per-port dataset structure first, and only then
indexes into ``"S"`` -- in three separate ``execute_python_code``
calls so the agent never indexes into a shape it has not actually
inspected.

```python
# First snippet: run + list every result provider.
fdtd = _lum_get("straight_wg")
fdtd.run()
_lum_print_json(fdtd.getresult())
```

```python
# Second snippet (after confirming the provider names): dump the
# per-port dataset structure for the monitor port.
fdtd = _lum_get("straight_wg")
_lum_print_json(fdtd.getresult("FDTD::ports::output_port", "S"))
```

```python
# Third snippet: pull the specific quantities the user asked for.
# ``S`` is a live numpy complex array of shape (N_freq, N_modes),
# so vectorised numpy works directly -- see ``workflow``'s
# "Printed JSON Is a Snapshot" callout.
import numpy as np
fdtd = _lum_get("straight_wg")
result = fdtd.getresult("FDTD::ports::output_port", "S")
S21 = result["S"][:, 0]
_lum_print_json({
    "lambda_nm": (result["lambda"] * 1e9).flatten().tolist(),
    "S21_dB": (20 * np.log10(np.abs(S21))).tolist(),
})
```

For the full N x N S-matrix of a multi-port device (Y-branch, MZI,
directional coupler, ...), one ``fdtd.run()`` is not enough; use
the S-parameter matrix sweep tool. See ``s_parameter_sweep``.

## Summary

- **Use FDTD-specific ``run()`` arguments** for one-off solver /
  resource / GPU overrides; see "Running an FDTD Simulation" above.
- **Call ``run()`` once.** Extract results first, then
  ``fdtd.switchtolayout()`` (which discards single-run results) to
  re-edit -- and only when the user has asked for another simulation.
- **Datasets are dicts.** No attribute access; index with string keys.
- **Always ``_lum_print_json(result)`` before indexing into an
  unfamiliar dataset.**
- **``FDTD::ports`` is not a result provider.** Use
  ``FDTD::ports::<port_name>`` for per-port S
  (shape ``(N_freq, N_modes)``), and the S-parameter matrix sweep
  tool for the full N x N S-matrix.
- **Use ``getresult()`` first** to list every real result provider --
  don't guess monitor or dataset names.
- **Heavy arrays must be reduced or saved to disk** in the subprocess
  before they leave through ``_lum_print_json``.

See also: ``workflow``, ``fdtd_workflow``, ``materials``,
``geometry``, ``fdtd_sources_monitors``, ``s_parameter_sweep``.
