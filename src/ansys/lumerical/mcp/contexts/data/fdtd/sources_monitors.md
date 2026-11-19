# FDTD Sources and Monitors

This topic covers two related conventions: using global source/monitor
settings instead of per-object configuration, and preferring ports over
mode sources whenever S-parameters are needed.

## Use Global Source and Monitor Settings

Lumerical FDTD provides global settings for sources and monitors that
apply to all objects of that type. **Always use global settings**
instead of configuring wavelength/frequency parameters on individual
sources and monitors.

### Guidelines

- Set wavelength range using ``setglobalsource`` for sources and
  ``setglobalmonitor`` for monitors.
- Individual sources and monitors should inherit from global settings
  by default.
- Only override global settings on individual objects when there is a
  specific reason (see exceptions below).

### When to override global source settings

- Multiple sources with different wavelength ranges are required.
- A specific source needs different frequency points than others.

### When to override global monitor settings

- Multiple monitors need to record at different frequency resolutions.
- A specific monitor needs a different wavelength range than the global
  setting.
- Power monitors vs. field monitors have different frequency
  requirements.

### Important: no dict syntax for global setters

Unlike most lumapi functions, ``setglobalsource`` and
``setglobalmonitor`` do **not** support dictionary-based initialization.
You must use individual ``set``-style calls for each property.

### Example: setting global source and monitor properties

```python
# Set global source properties (applies to all sources)
# NOTE: setglobalsource does NOT support dict syntax - use individual calls
fdtd.setglobalsource("wavelength start", 1.5e-6)
fdtd.setglobalsource("wavelength stop", 1.6e-6)

# Set global monitor properties (applies to all monitors)
# NOTE: setglobalmonitor does NOT support dict syntax - use individual calls
fdtd.setglobalmonitor("use source limits", True)   # Use same wavelength range as source
fdtd.setglobalmonitor("frequency points", 101)     # Number of frequency points to record

# Sources and monitors will automatically use these global settings
# No need to specify wavelength on individual objects
fdtd.addmode({
    "name": "source",
    "x": source_x,
    "y": 0,
    "y span": source_y_span,
    "z": source_z,
    "z span": source_z_span,
    "injection axis": "x-axis",
    "direction": "Forward"
    # wavelength settings inherited from global source
})

fdtd.addpower({
    "name": "transmission",
    "monitor type": "2D X-normal",
    "x": monitor_x,
    "y": 0,
    "y span": monitor_y_span,
    "z": monitor_z,
    "z span": monitor_z_span
    # frequency settings inherited from global monitor
})
```

## Use Ports Instead of Mode Sources

For any waveguide excitation where S-parameters are needed (single
waveguides, directional couplers, splitters, multi-port devices),
use ``addport()`` instead of ``addmode()``. A port is a combined
mode source + monitor with built-in S-parameter extraction; after
``fdtd.run()`` each port exposes its own ``"S"`` dataset at
``FDTD::ports::<port_name>`` (shape ``(N_freq, N_modes)``). For
the full N x N S-matrix across every active port, use the
S-parameter matrix sweep tool (see ``s_parameter_sweep``) --
``FDTD::ports`` itself is a group, not a result provider, and
``getresult("FDTD::ports", "S")`` raises
``'FDTD::ports is not a result provider'``.

### Injection control: the ``FDTD::ports`` group, not the port

Per-port ``"mode selection"`` (e.g. ``"fundamental TE mode"``)
chooses **which mode each port analyses**. Which port mode actually
**injects** on a given ``fdtd.run()`` is owned by the
``FDTD::ports`` group via its ``source port`` and ``source mode``
properties; only one port mode injects per run. Always set this
explicitly rather than relying on whichever port was added first:

```python
fdtd.setnamed("FDTD::ports", "source port", "input_port")
fdtd.setnamed("FDTD::ports", "source mode", "mode 1")
```

For the full N x N matrix the S-parameter sweep tool rotates this
source-port selection through every active port automatically;
do not loop ``fdtd.run()`` manually.

### Other FDTD source types

``addport()`` and ``addmode()`` are not the only sources. Reach
for the others when ports/modes don't apply:

- ``addplane`` -- plane-wave (free-space scattering, transmission
  / reflection through gratings or thin films).
- ``addgaussian`` -- focused Gaussian / scalar beam.
- ``adddipole`` -- point electric / magnetic dipole (LED, antenna,
  Purcell-factor problems).
- ``addtfsf`` -- total-field / scattered-field plane wave for
  isolated scatterer cross-sections (RCS, absorption).
- ``addimportedsource`` -- field profile imported from a
  monitor or external file.

A port is the right choice whenever the structure has a clean
waveguide cross-section at the source plane; the source types
above are for plane-wave illumination, free-space radiation, and
non-waveguide problems.

### Port ``direction`` convention

For S-parameter extraction with ports at opposite ends of a
waveguide, the ports must **face into the simulation domain**:

- **Input port** at the low-coordinate end of the propagation axis
  (e.g. ``x = -L/2``) is the active source, injecting light toward
  the device. Its ``direction`` is ``"Forward"``.
- **Output port** at the high-coordinate end (e.g. ``x = +L/2``) is
  passive (transmission monitor). Its ``direction`` is
  ``"Backward"`` -- the port surface normal points back into the
  simulation, which is what makes a wave travelling in ``+x``
  register as "incoming" for that port and gives the right sign
  convention for ``S21``.

A common mistake is to set both ports to ``"Forward"``. The
simulation will still run and per-port ``getresult`` calls (e.g.
``getresult("FDTD::ports::output_port", "S")``) will still return
numbers, but the "incident vs. transmitted" labelling at the output
port is wrong, so the resulting S-parameters do not have the
conventional meaning.

### Example: using ports for S-parameter measurement

```python
# Input port: active TE source + reflection (S11) monitor.
# Direction "Forward" so it injects light in +x toward the device.
fdtd.addport({
    "name": "input_port",
    "injection axis": "x-axis",
    "direction": "Forward",
    "mode selection": "fundamental TE mode",
    "x": input_x,
    "y": 0,
    "y span": port_y_span,
    "z": port_z_center,
    "z span": port_z_span
})

# Output port: transmission (S21) monitor.
# Direction "Backward" so the port faces into the simulation domain
# and a wave travelling in +x registers as "incoming" for this port.
fdtd.addport({
    "name": "output_port",
    "injection axis": "x-axis",
    "direction": "Backward",
    "mode selection": "fundamental TE mode",
    "x": output_x,
    "y": 0,
    "y span": port_y_span,
    "z": port_z_center,
    "z span": port_z_span
})

# After simulation, per-port S-parameters can be extracted using:
# S = fdtd.getresult("FDTD::ports::output_port", "S")
# (See ``fdtd_run_and_results`` for the dataset-is-a-dict contract
# and the dump-before-index pattern.) For the full N x N S-matrix
# across every active port, see ``s_parameter_sweep``.
```

See also: ``fdtd_workflow``, ``materials``, ``geometry``,
``fdtd_run_and_results``, ``s_parameter_sweep``.
