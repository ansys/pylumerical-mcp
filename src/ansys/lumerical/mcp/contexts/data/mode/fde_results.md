# MODE FDE Results

This topic covers solving FDE modes, extracting common mode properties,
and classifying TE-like and TM-like modes in MODE.

Read ``workflow`` first, then ``mode_fde_workflow`` for setup. This topic
assumes the geometry and FDE object already exist and the user has agreed
to solve.

## Solving Modes

For FDE mode solving, prefer ``findmodes()``. Do not assume that generic
``run()`` is the right entry point for cross-sectional mode extraction.

```python
mode = _lum_get("mode_fde")
num_modes = mode.findmodes()
_lum_print_json({"stage": "modes_found", "num_modes": num_modes})
```

If group index is required, enable ``calculate group index`` before the
solve. Save before solving so the results have a stable project file.

Each solved mode is stored as a D-card named ``mode1``, ``mode2``, and so
on under the FDE solver result tree.

## Analysis Mode After Solve

After ``findmodes()`` the project behaves like analysis mode. Do not assume
that the same saved file is safe to mutate for a sweep. Reopen the clean
pre-run setup file when changing geometry or solver settings across sweep
points.

## FDE Analysis Commands

The key analysis commands the agent should know are:

- ``findmodes()`` to calculate the supported modes
- ``selectmode(...)`` to choose which solved mode or modes subsequent
  analysis should act on
- ``setanalysis("property", value)`` to configure FDE analysis-tab
  settings such as mode tracking and detailed dispersion calculation
- ``getanalysis("property")`` to inspect the current analysis settings
  before changing them
- ``frequencysweep()`` to run the frequency sweep using the current
  analysis settings

Use ``setnamed("FDE", ...)`` for solver-object setup in layout mode, and
use ``setanalysis(...)`` / ``getanalysis(...)`` for analysis-tab settings
after the mode solve context is available. Do not mix these two property
surfaces.

## Mode Selection Before Analysis

``selectmode(...)`` can target a mode by index, by name, or by a list of
selected modes. Use it before ``frequencysweep()`` when the sweep should
track a specific mode or mode set.

Representative Python pattern:

```python
mode = _lum_get("mode_fde")
mode.findmodes()
mode.selectmode(1)
mode.setanalysis("track selected mode", 1)
mode.setanalysis("detailed dispersion calculation", 1)
_lum_print_json({"stage": "mode_selected", "selected_mode": 1})
```

Do not assume the desired sweep target is always the first raw mode index.
When needed, classify the modes first and then select the physically
intended one.

## Frequency Sweep

``frequencysweep()`` performs a frequency sweep using the current FDE
analysis settings. It does not return data directly. Instead, it creates a
result object named ``frequencysweep`` under the FDE solver result tree.

Representative Python pattern:

```python
mode = _lum_get("mode_fde")
mode.findmodes()
mode.selectmode(1)
mode.setanalysis("track selected mode", 1)
mode.setanalysis("detailed dispersion calculation", 1)
mode.frequencysweep()
_lum_print_json({"stage": "frequency_sweep_done", "ok": True})
```

## Result Discovery Under FDE

After ``findmodes()``, the solved mode data is available under result paths
such as ``FDE::data::mode1``, ``FDE::data::mode2``, and so on. After
``frequencysweep()``, sweep data is available under
``FDE::data::frequencysweep``.

In the CAD or LSF prompt, selecting the FDE solver and using
``?getresult;`` reveals the available result objects under ``FDE``. Use
that discovery step when the exact result containers are unclear.

In Python lumapi, once the result path is known, pull fields from those
objects with ``getdata(...)``.

## Common Result Fields

For a solved mode card such as ``mode1``, commonly-used ``getdata()``
fields include:

- ``neff``
- ``loss``
- ``TE polarization fraction``
- ``ng`` when group index was enabled

Representative extraction pattern:

```python
mode = _lum_get("mode_fde")
payload = {
    "mode1_neff": mode.getdata("mode1", "neff"),
    "mode1_loss": mode.getdata("mode1", "loss"),
    "mode1_te_fraction": mode.getdata("mode1", "TE polarization fraction"),
}
_lum_print_json(payload)
```

Solved modes do not necessarily appear as ordinary layout objects in a
generic object-tree listing. Use the mode-card result getters directly
instead of assuming they are discoverable from the layout tree alone.

Representative Python extraction patterns:

```python
mode = _lum_get("mode_fde")
payload = {
  "mode1_neff": mode.getdata("FDE::data::mode1", "neff"),
  "mode1_loss": mode.getdata("FDE::data::mode1", "loss"),
}
_lum_print_json(payload)
```

```python
mode = _lum_get("mode_fde")
payload = {
  "dispersion": mode.getdata("FDE::data::frequencysweep", "D"),
  "dispersion_frequency": mode.getdata("FDE::data::frequencysweep", "f_D"),
  "neff_sweep": mode.getdata("FDE::data::frequencysweep", "neff"),
  "frequency": mode.getdata("FDE::data::frequencysweep", "f"),
}
_lum_print_json(payload)
```

## TE/TM Classification

Do not rely on mode index stability across bend radius or other sweeps.
``mode1`` at one parameter point is not guaranteed to represent the same
polarization family at another point.

Prefer this classification rule:

1. extract ``TE polarization fraction`` for the candidate solved modes
2. split the family into TE-like and TM-like modes using that fraction
3. within each family, select the physically relevant mode by highest
   ``neff`` or by the user-requested criterion

This is the robust pattern for bent-waveguide sweeps where ordering shifts.

## Bent-Waveguide Notes

For bent-waveguide FDE results:

- ``neff`` is the bent-waveguide effective index tied to the chosen radius
- ``loss`` is usually reported per length, not per angle
- mode ordering can change as radius changes

If the user needs the angular propagation quantity rather than the usual
effective index/loss pair, inspect the available result fields before
assuming a specific card name.

## Result Extraction Style

Keep snippets compact. Prefer explicit assignments over long loop-heavy
blocks when working in the persistent subprocess. If a result-extraction
snippet starts accumulating loops and formatting complexity, split it into
another ``execute_python_code`` call.

## Reporting Guidance

When the user asks for the fundamental TE and TM modes, report the exact
selection rule you used, for example: "highest-neff TE-like mode by
TE polarization fraction". This avoids silently treating a raw mode index
as a physical label.

## See Also

Use ``mode_fde_workflow`` for setup and sweep-safe file reuse. Use
``mode_eme_workflow`` when the task is device propagation, taper-length
optimization, or user S-matrix extraction rather than cross-sectional mode
analysis.
