# INTERCONNECT Simulation Configuration and Results

This topic covers INTERCONNECT **simulation configuration** and
**result extraction**: root element setup (time-domain modes and the
``"simulation input"`` selector), frequency-domain workflow via the
Optical Network Analyzer (ONA), and the ``getresult`` discovery
pattern for analyzers.

**Read ``workflow`` and ``interconnect_workflow`` first** for the
generic execution model, the discover-before-configure workflow, and
the build/setup stages.

## Root Element / Simulation Configuration

The INTERCONNECT root element controls global simulation settings.
Access it as ``"::Root Element"``.

**WARNING**: Do NOT use FDTD-style property names:
- ~~``"simulation window"``~~ → use ``"time window"``
- ~~``"bit rate"``~~ → use ``"bitrate"``

**Setting up time domain simulation**: the root element exposes a
``"simulation input"`` selector that determines which global property
set is active. The optimizer domain context documents the allowed
values as ``"time window"``, ``"sequence length"``, and
``"sample rate"``. Only the active mode's dependent properties are
settable; inactive properties raise errors.

- **``"sequence length"`` mode**: ``"bitrate"`` +
  ``"samples per bit"`` + ``"sequence length"``
- **``"time window"`` mode**: ``"time window"`` +
  ``"number of samples"``
- **``"sample rate"`` mode**: ``"sample rate"`` + the complementary
  root settings needed by the active solver setup

You **cannot** safely mix properties from different modes. Set
``"simulation input"`` first, then configure the dependent properties.
If you get "property is inactive", the root element is in another
mode.

```python
# Sequence-length mode: define via bitrate parameters
ic.setnamed("::Root Element", "simulation input", "sequence length")
ic.setnamed("::Root Element", "bitrate", 25e9)
ic.setnamed("::Root Element", "samples per bit", 64)
ic.setnamed("::Root Element", "sequence length", 128)

# Time-window mode: define duration directly
ic.setnamed("::Root Element", "simulation input", "time window")
ic.setnamed("::Root Element", "time window", 5.12e-9)
ic.setnamed("::Root Element", "number of samples", 8192)
```

In practice, ``"samples per bit"`` is a common inactive-property trap:
if it fails, verify that ``"simulation input"`` is set to
``"sequence length"`` before retrying.

Common starting values are ``sequence length = 128`` and
``samples per bit = 64``.

## Frequency Domain Simulation

Frequency domain simulation is performed using an **Optical Network
Analyzer (ONA)**. The ONA output port acts as the source and its
input port(s) collect optical signals from the circuit as results.

Typical pattern: ONA ``output`` drives the device under test and one or
more ONA ``input n`` ports collect the response.

For ONA simulations, ``"simulation bandwidth"`` is the practical
analogue of the Root Element ``"sample rate"``; ideally, set
``"simulation bandwidth"`` to inherit the Root ``"sample rate"`` via
an expression ``%sample rate%`` so ONA and any other active sources
(for example, DC sources) stay synchronized.

## Result Extraction (Discovery Pattern)

**Never guess result/dataset names.** Always discover first:

```python
datasets = ic.getresult("OSA_1")
result = ic.getresult("OSA_1", "sum/signal")
_lum_print_json(result)
```

Common analyzer result names (always verify with discovery first):

- OSA: ``"sum/signal"``, ``"mode 1/signal"``, ``"sum/spectrogram"``
- Eye Diagram: ``"measurement/BER"`` plus other
  ``"measurement/..."`` outputs

Treat listed result names as discoverable hints, not guarantees that
the dataset is populated. An analyzer can expose a result name yet
still return an empty or unusable dataset if the signal chain is
broken or the analyzer has no valid data. Always inspect the returned
payload with ``_lum_print_json(...)`` before indexing into nested keys.

See also: ``workflow``, ``interconnect_workflow``,
``interconnect_commands``, ``sweeps``.
