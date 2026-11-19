# MODE EME Workflow

This topic covers the MODE Eigenmode Expansion (EME) workflow for taper,
converter, and multi-section propagation devices: EME setup, cell-group
configuration, analysis-mode propagation, and result interpretation.

Read ``workflow`` first. Pair this topic with ``geometry`` and
``materials`` for shared build conventions.

## When To Use EME

Use EME for longitudinal devices where propagation through multiple cells,
cell groups, or ports matters: tapers, spot-size converters, bends,
periodic sections, and user S-matrix extraction.

Use FDE instead when the task is only cross-sectional mode properties.

## MODE EME Build Stages

Prefer these stages as separate snippets:

1. Parameters: wavelength, geometry, port intent, number of cell groups,
   group spans, cells per group, and modes per group.
2. Add geometry.
3. Add the EME object.
4. Configure the EME setup in layout mode.
5. Save the setup file.
6. Ask before the mode-calculation / propagation step.
7. After the user confirms, run the EME calculation to enter analysis mode.
8. In analysis mode, use ``emepropagate()`` / ``emesweep()`` and extract
   the user S-matrix or other requested results.

## Layout Mode Versus Analysis Mode

This is the most important EME rule.

- In layout mode, configure geometry, ports, and cell groups.
- Running the EME calculation moves the project into analysis mode.
- ``emepropagate()`` and propagation sweeps belong to analysis mode.
- Geometry and most object edits are blocked in analysis mode.

If you need to modify ports, geometry, or solver setup after a run, call
``switchtolayout()`` only after the user confirms that existing analysis
results may be discarded.

## Cell Groups And Group Spans

The longitudinal extent is controlled by cell-group settings, not by
assuming a direct ``x span`` edit on the EME solver object in every state.

Common setup keys include:

- ``number of cell groups``
- ``group spans``
- ``cells``
- ``number of modes for all cell groups``
- ``allow custom eigensolver settings`` when group-specific settings are
  required

For ``group spans`` and ``cells``, do not assume plain Python lists are the
accepted payload. MODE commonly expects matrix-shaped values. When a list is
rejected, switch to the matrix format that the live object accepts.

## Coordinate Updates And Alignment

When changing EME longitudinal spans, do not assume the solver center stays
fixed. Updating ``group spans`` can shift the region center. If the device
must stay centered, explicitly re-apply the intended ``x`` position after
the span update and verify the final bounds.

This matters for taper-length sweeps: set the span-defining properties
first, then re-center, then verify the EME bounds before propagating.

## Ports

Inspect the actual port objects present in the saved project before using
the user S-matrix as a two-port metric. Disposable probe ports can mutate a
live session and leave extra enabled ports behind.

Before reporting port-to-port transmission:

1. verify the expected port count
2. verify which modes are enabled at each port
3. remove unintended ports in layout mode if necessary
4. rerun the EME calculation before trusting the user S-matrix

## Propagation And Sweeps

Use ``emepropagate()`` for the current analysis configuration. Use
``emesweep()`` for propagation-length or wavelength sweeps after the EME
mode solve has been performed.

Keep in mind:

- propagation sweep settings can use internal enum values rather than
  free-form strings
- propagation changes can often be made in analysis mode without
  recalculating the modes
- changing geometry or port definitions requires returning to layout mode

## EME Analysis Commands

The key EME analysis commands the agent should know are:

- ``setemeanalysis("property", value)`` to configure the EME analysis
  window in analysis mode
- ``getemeanalysis("property")`` to inspect the current EME analysis
  settings before changing or using them
- ``emepropagate()`` to run the current propagation analysis
- ``emesweep()`` or ``emesweep("...")`` to run a configured sweep
- ``getemesweep("...")`` to retrieve sweep datasets
- ``exportemesweep("filename", "format")`` to export wavelength-sweep
  data for downstream use, including INTERCONNECT

If the valid analysis-window properties are unclear, discover them first
instead of guessing. In lumapi Python, use explicit getters/setters such as
``mode.getemeanalysis("group spans")`` and
``mode.setemeanalysis("group spans", value)``.

Supported EME sweep modes include:

- ``emesweep()`` or ``emesweep("propagation sweep")``
- ``emesweep("wavelength sweep")``
- ``emesweep("mode convergence sweep")``

## Python Examples

Representative Python lumapi patterns:

```python
mode = _lum_get("eme_device")

# Inspect current analysis settings before changing them.
group_spans = mode.getemeanalysis("group spans")
_lum_print_json({"group_spans": group_spans})
```

```python
mode = _lum_get("eme_device")

# Run the current propagated analysis state.
mode.emepropagate()
result = mode.getresult("EME", "user s matrix")
_lum_print_json(result)
```

```python
mode = _lum_get("eme_device")

# Configure and run a propagation sweep in analysis mode.
mode.setemeanalysis("propagation sweep", 1)
mode.setemeanalysis("parameter", "group span 2")
mode.setemeanalysis("start", 10e-6)
mode.setemeanalysis("stop", 200e-6)
mode.setemeanalysis("number of points", 10)
mode.emesweep()
dataset = mode.getemesweep("S")
_lum_print_json(dataset)
```

```python
mode = _lum_get("eme_device")

# Configure and run a wavelength sweep, then export it.
mode.setemeanalysis("wavelength sweep", 1)
mode.setemeanalysis("start wavelength", 1.5e-6)
mode.setemeanalysis("stop wavelength", 1.6e-6)
mode.setemeanalysis("number of wavelength points", 31)
mode.setemeanalysis("calculate group delays", 1)
mode.emesweep("wavelength sweep")
mode.exportemesweep("s_param", "touchstone")
_lum_print_json({"stage": "wavelength_sweep_exported", "ok": True})
```

```python
mode = _lum_get("eme_device")

# Run a mode convergence sweep and retrieve its dataset.
mode.setemeanalysis("mode convergence sweep", 1)
mode.setemeanalysis("start mode", 4)
mode.setemeanalysis("mode interval", 1)
mode.emesweep("mode convergence sweep")
dataset = mode.getemesweep("S_mode_convergence_sweep")
_lum_print_json(dataset)
```

Keep these mode-specific distinctions in mind:

- ``emepropagate()`` is for the current propagated analysis state, not for
  parameter sweeps
- propagation, wavelength, and mode-convergence sweeps are configured with
  ``setemeanalysis(...)`` and run with ``emesweep(...)``
- wavelength-sweep export uses ``exportemesweep(...)`` and applies to the
  EME analysis wavelength sweep result

## Results To Prefer

The most decision-useful result for a taper or converter is typically the
``user s matrix`` or ``power normalized user s matrix`` after confirming the
port configuration. Do not assume that overlap, ``Pmatrix``, or other
normalized helper results are the correct loss metric for every task.

Always inspect the returned result payload before indexing into it, and say
which S-matrix element you are treating as the transmission metric.

## Analysis-Mode Hygiene

Keep exploratory probes side-effect free where possible. Avoid adding
disposable ports or helper objects to a live session unless you are also
cleaning them up deliberately. If the session has been heavily probed, a
fresh session opened from the saved file is often the safer base for the
production run.

## See Also

Use ``s_parameter_sweep`` when the task is the formal S-parameter matrix
sweep utility shared by FDTD and MODE. Use ``mode_fde_workflow`` and
``mode_fde_results`` for cross-sectional mode solving rather than device
propagation.
