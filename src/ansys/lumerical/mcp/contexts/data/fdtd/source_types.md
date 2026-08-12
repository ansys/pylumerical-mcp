# FDTD Source Types

This topic catalogues the FDTD source families beyond ports and
mode sources (``fdtd_sources_monitors`` covers those). Pick the
source that matches the physics, not the source you happen to
know best.

## Decision Tree

- **Guided mode** (waveguide cross-section, want S-parameters) ->
  ``addport()`` (or ``addmode()`` if S-params not needed). See
  ``fdtd_sources_monitors``.
- **Plane wave at normal or fixed angle, single frequency** ->
  ``addplane`` (planar wave source).
- **Plane wave, broadband and angled** -> ``addbfastplanewave`` /
  BFAST source -- the only correct broadband-angled source.
- **Focused free-space beam (lens, fiber tip)** -> ``addgaussian``
  (paraxial) or the scalar/vector "thin lens" mode.
- **Isolated scatterer cross-section** (RCS, absorption,
  scattering efficiency) -> ``addtfsf`` (Total-Field
  Scattered-Field).
- **Point emitter** (LED active region, Purcell factor, antenna) ->
  ``adddipole``.
- **Field profile recorded elsewhere or computed externally** ->
  ``addimportedsource``.

## Plane Wave (``addplane``)

A finite-sized plane wave injected through one face of the sim
region. Pair with periodic or Bloch lateral BCs for true
infinite-array behaviour.

Gotchas:

- **Edge effects.** A finite plane wave inside the sim region has
  diffraction at its edges; either size it larger than every
  monitor of interest, or use periodic / Bloch BCs to enforce
  laterally infinite injection.
- **Angled injection of a broadband pulse** suffers from the
  frequency-dependent-angle problem (each frequency component
  refracts to a different angle when combined with Bloch BCs).
  Use BFAST instead.

## BFAST (``addbfastplanewave``)

Broadband Fixed Angle Source Technique. A specialised plane-wave
source for broadband angled sweeps that internally enforces the
correct fixed-angle injection at every frequency in the band.
BFAST automatically overrides Bloch BCs on the lateral faces.

Use BFAST whenever you need a transmission / reflection spectrum
at an oblique angle of incidence.

## Gaussian / Thin-lens beam (``addgaussian``)

Focused beam with user-set waist radius and beam center. Paraxial
form is the default; the "thin lens" option produces a more
accurate vector beam at high NA.

Common applications: fiber-to-chip coupling efficiency, focused
spot inside a metasurface, microscope illumination.

## Dipole (``adddipole``)

Idealised electric or magnetic point dipole, optionally with a
fixed polarisation vector. Required source for:

- **LED / OLED** quantum efficiency (sweep dipole position /
  orientation to integrate over the emissive layer).
- **Purcell factor** vs free-space dipole.
- **Antenna** input impedance and radiation pattern (combine with
  far-field projection, see ``fdtd_far_field_and_grating``).

In an inhomogeneous environment the dipole couples to nearby
structure; always validate with a homogeneous-medium reference
run (Lumerical KB: *Testing FDTD dipole sources in homogeneous
materials*).

## TFSF (``addtfsf``)

Total-Field / Scattered-Field source: a closed box that injects a
plane wave **inside** while subtracting the incident field
**outside**. Power monitors outside the box record only scattered
fields; monitors inside record total fields.

Standard use cases:

- Scattering cross-section / RCS of an isolated particle.
- Absorption cross-section of a nanostructure on a substrate.

Gotcha: TFSF assumes the background outside the box is what is
**inside** the TFSF boundary at simulation start. Avoid having
the TFSF box cross a material interface; substrates that pierce
the box produce spurious scattered fields. The Lumerical KB
includes a dedicated *Tips and best practices when using the FDTD
TFSF source* article -- consult it for any non-trivial geometry.

## Imported Source (``addimportedsource``)

Injects a spatial field profile recorded by a monitor (typically
from a smaller FDE / MODE simulation) or loaded from an external
file. Use when:

- You want to inject a mode computed by a different simulation
  (multi-stage workflow).
- You want a custom illumination profile that none of the analytic
  sources match (engineered wavefront, measured aperture).

The companion KB articles document the spatial-profile import
(monitor-data and equation forms) and the **custom time signal**
mechanism for shaping the pulse temporal envelope.

## Source-Bandwidth and Global Settings

Wavelength / frequency range and pulse length are controlled by
``setglobalsource``. Per-source overrides are documented but rarely
needed -- see ``fdtd_sources_monitors`` for the global vs.
per-source rules. For very-narrow-band or very-broadband sources,
``setglobalsource("optimize for short pulse", False)`` improves
spectral accuracy at the cost of a longer source signal.

See also: ``fdtd_sources_monitors``, ``fdtd_boundary_conditions``,
``fdtd_far_field_and_grating``, ``fdtd_workflow``.
