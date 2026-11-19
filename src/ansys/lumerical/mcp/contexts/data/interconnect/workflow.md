# INTERCONNECT Workflow (Build & Setup)

This topic covers the INTERCONNECT-specific **build/setup** workflow
for photonic circuit simulation: the chunked stage list, element
management (adding, naming, selecting, connecting), compact-model
library discovery, property discovery, analyzer/result discovery, and
root-element simulation configuration.

**Read ``workflow`` first** for the generic execution model
(``_lum_get`` / ``_lum_print_json`` helpers), snippet structure,
parameter management, and the "do NOT make assumptions / do NOT
invent or re-run" rules that apply to every Lumerical product.

## INTERCONNECT Build Stages (Chunked)

Follow this order. Each stage is one ``execute_python_code`` snippet:

1. **Parameters** -- declare all user-configurable values (bitrate,
  wavelengths, modulation depth, analyzer settings, bias points,
  etc.) with SI units where applicable.
2. **Discover before configure** -- call ``ic.library()`` and verify
  the exact installed element names before adding anything. For any
  unfamiliar element, inspect its ports and properties before trying
  to wire or configure it. If a required compact model library is
  missing, install the needed ``.cml`` design kit first with
  ``installdesignkit(filename, path, overwrite)``.
3. **Add elements and position them** -- ``addelement`` + immediate
  ``get("name")`` to capture the auto-assigned instance name.
  Immediately set ``"x position"`` and ``"y position"`` on each
  element in the same snippet so elements are never stacked at the origin.
  Verify each ``addelement`` succeeded before proceeding (see "Handling
  addelement Failures" below).
4. **Discover ports and connection roles** -- use ``getports()`` for
  every element to build the connection plan and identify any
  digital-to-electrical bridges needed.
5. **Connect elements** -- wire compatible ports with ``connect()``.
6. **Configure elements and root mode** -- set element properties only
  after confirming the exact property names, active state, and enum
  choices. Set the root element's ``simulation input`` mode before
  configuring time-domain properties that depend on it.
7. **Save** -- ``ic.save(path)``.
8. **Run** -- ``ic.run()`` (only after user confirmation).
9. **Extract results** -- discover dataset names first, then extract
  analyzer outputs and inspect the returned payload before indexing
  into it.

## Element Library Discovery

Use ``library()`` to get a complete list of elements available in
the currently installed element libraries. This returns all
primitive elements (sources, modulators, detectors, analyzers) as
well as any installed foundry PDK elements.

For foundry compact models, **do not assume the user-facing shorthand
matches the installed leaf name**. Lumfoundry-style models often show
up with a ``lum_`` prefix or another library-specific prefix, and the
exact installed spelling varies across design kits. Always search the
current ``library()`` output and use the exact discovered name.

```python
ic = _lum_get("wdm_tx")
lib_list = ic.library()
print(lib_list)
```

## Adding Elements

Use ``addelement("element_name")`` to add an element to the
schematic. The element name must match the **exact** library name
(case-insensitive, but whitespace-sensitive).

**IMPORTANT**: Always call ``ic.library()`` first and verify that the
element name exists in the output before calling ``addelement``. Do
NOT guess element names -- installed libraries vary across
installations and PDK configurations, and compact-model aliases in one
environment may be absent in another.

## Element Naming Convention

After ``addelement``, INTERCONNECT auto-assigns an abbreviated name
with an incrementing suffix, for example ``"CW Laser"`` → ``CWL_1``.

**Always call ``get("name")`` immediately after ``addelement``** to
capture the auto-assigned name, then use ``setnamed(..., "name", ...)``
if you need a deterministic instance name.

If no ``addelement`` name argument is given, a compound element is
added by default.

## Element Positioning (Schematic Layout)

Set ``"x position"`` and ``"y position"`` on every element in the
same snippet where it is added so the schematic stays readable. Do not
leave elements stacked at the origin.

## Handling addelement Failures

If ``addelement("name")`` fails (e.g., wrong library name), do
**NOT** call ``get("name")`` afterward -- it will return the
previously-selected element's name (stale state), and any
subsequent ``setnamed`` rename will corrupt an unrelated element.

Safe pattern: call ``get("name")`` only after a successful
``addelement``.

If a batch of ``addelement`` calls fails mid-way, the safest
recovery is to clear the circuit (``ic.selectall()`` +
``ic.delete()``) and rebuild from scratch rather than trying to
fix corrupted naming state in-place.

## Connecting Elements

Use ``connect("element1", "port1", "element2", "port2")`` to wire
ports together. Get an element's port names using
``getports("element_name")``.

``getports()`` is the universal port-discovery mechanism for both
primitive elements and compact-model-library elements. Prefer it over
trying to infer ports from ``getnamed(element, "ports")`` or other
property dumps.

**Port type matching**: always connect same-type ports. There are
3 common port types: electrical, optical, digital. Use
``getports("element", "port type")`` to list ports of a specific
type:

```python
optical_ports = ic.getports("RING_1", "optical")
electrical_ports = ic.getports("RING_1", "electrical")
digital_ports = ic.getports("PRBS_1", "digital")
```

**Always discover port types before connecting.** A common pattern is
PRBS ``output`` = digital, NRZ ``modulation`` = digital, and NRZ
``output`` = electrical.

## Signal Chain: Driving Electrically-Modulated Elements

PRBS generators produce **digital** output, but modulators (ring,
MZM) expect **electrical** modulation input. You cannot connect
digital to electrical directly.

Use an **NRZ Pulse Generator** as the digital→electrical bridge:

```
PRBS (digital out) → NRZ Pulse Generator (digital in, electrical out) → Modulator (electrical in)
```

```python
ic.connect("PRBS_1", "output", "NRZ_1", "modulation")  # digital→digital
ic.connect("NRZ_1", "output", "RING_1", "modulation")   # electrical→electrical
```

The NRZ Pulse Generator converts digital bit patterns to an
electrical voltage waveform. In the reference docs, ``amplitude`` is
the output peak amplitude before bias is added, and ``bias`` is the DC
offset added afterward. For an NRZ-driven electrical signal, treat the
low level as the bias and the high level as ``bias + amplitude``.

## Hierarchical Circuits

For hierarchical circuits, use ``::`` paths for internal elements and
remember that compound external ports map to internal ``RELAY_n``
elements in the order returned by ``getports(compound_name)``.

## Compound Elements / Compact Models

Select core elements / children with ``select`` and ``shiftselect``,
then call ``createcompound()`` to turn the selection into a compound element.
Add ports explicitly with ``addport(element, name, type, data)`` — each call
creates a ``RELAY_N`` inside the compound in order. Connect relays to internal
element ports using ``COMPOUND::RELAY_N`` path syntax.

## Property Discovery

There is **no** ``getproperties()`` method in INTERCONNECT's lumapi.
To discover element properties:

- **Option 1**: select the element and call ``set()`` with no
  arguments -- this prints all available properties.
- **Option 2**: call ``setnamed("element_name")`` with no second
  argument -- same effect without needing to select first.

```python
props = ic.setnamed("RING_1")
```

To get a property value: ``ic.getnamed("element_name", "property")``
To set a property value: ``ic.setnamed("element_name", "property", value)``

Before writing a property, verify all of the following locally:

1. The property name exists exactly as written.
2. The property is currently active for the element's current mode.
3. If it is an enum, the value is one of the allowed choices.
4. If it is numeric, the supplied units/range match the property table.

Use ``ic.ispropertyactive(element, property_name)`` when available to
check whether a property is currently writable in the active mode.

If a prompt asks for ``notes`` and the field is empty or absent, fall
back to the element ``description``, the library path/name, and the
verified property table rather than fabricating notes.

## Expression-Locked Properties

Some element properties are bound to the root element via
expressions and **cannot** be directly overwritten with
``setnamed``. For example, the PRBS bitrate is typically tied to
the root element's bitrate.

Preferred fix: set the controlling value on ``"::Root Element"``.
Only clear the expression with ``setexpression(...)`` if you truly need
per-element control.

See also: ``workflow``, ``sweeps``, ``interconnect_commands``,
``interconnect_simulation``.
