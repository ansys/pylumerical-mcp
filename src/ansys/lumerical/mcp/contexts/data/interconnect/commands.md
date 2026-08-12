# INTERCONNECT Commands Reference

This topic provides the INTERCONNECT-specific lumapi commands
grouped by category. These commands are called as methods on the
INTERCONNECT session handle (e.g., ``ic.library()``) or via
``ic.eval("<lsf>;")`` for script-only commands.

**Read ``workflow`` and ``interconnect_workflow`` first** for the
execution model, discover-before-configure workflow, and build/setup
stages.

## Element Library Commands

| Command | Description |
|---------|-------------|
| ``library()`` | Returns the installed element list, including custom elements. |
| ``addtolibrary()`` | Adds an element to the currently selected custom library. |
| ``customlibrary()`` | Returns the path of the custom library. |
| ``saveelement()`` | Saves an element to file. |
| ``loadelement()`` | Loads an element from file. |
| ``probe()`` | Places a probe analyzer at a specified port. |
| ``loadcustom()`` | Redirects the Custom folder path and reloads its contents. |
| ``replacelibrary()`` | Replaces all instances of the current library in the Element Library. |
| ``hideproperty()`` | Hides the property of a given element. |
| ``protectproperty()`` | Protects the property of a given element. |
| ``hidecategory()`` | Hides all properties of a given category of a given element. |
| ``annotateproperty()`` | Enables property annotation on a given element. |
| ``ispropertyactive()`` | Returns true if the property from an element is active. |
| ``parsebackannotation()`` | Parses the waveguide back annotation. |
| ``parsewaveguidebackannotation()`` | Parses waveguide back annotation at a given temperature. |

## Design Kit Commands

| Command | Description |
|---------|-------------|
| ``loaddesignkit()`` | Loads a design kit and directs its contents to a user-defined path. |
| ``enabledesignkit()`` | Enables a design kit in the Design Kits folder. |
| ``disabledesignkit()`` | Disables a design kit in the Design Kits folder. |
| ``removedesignkit()`` | Removes a design kit from the element library 'Design kits' folder. |
| ``reloaddesignkit()`` | Reloads a design kit from the element library Design kits folder. |
| ``packagedesignkit()`` | Creates a design kit file from a Custom folder. |
| ``installdesignkit()`` | Installs a ``.cml`` design kit to the Design Kits folder. |
| ``uninstalldesignkit()`` | Uninstalls a design kit from the Design Kits folder. |
| ``importlib()`` | Imports the .lib file for a CML in the Custom folder. |
| ``exportlib()`` | Exports the .lib file for a CML in the Custom folder. |
| ``renameport()`` | Renames the port name for a Compound or Scripted element. |
| ``removecustom()`` | Removes a folder in the Custom folder in Element Library. |

If a required compact model library is missing, install it with:

```python
ic.installdesignkit("dk.cml", "C:/Users/xxx", True)
```

``filename`` is the ``.cml`` file, ``path`` is the folder that holds
it, and ``overwrite=True`` replaces an existing kit with the same
name. With ``overwrite=False``, INTERCONNECT asks for confirmation
before replacing an existing kit.

## Measurement & Analyzer Commands

| Command | Description |
|---------|-------------|
| ``validate()`` | Reruns the analysis of an analyzer. |
| ``validateall()`` | Reruns the analysis of all analyzers in the simulation. |
| ``setresult()`` | Sets the result of a Scripted or a Compound element. |
| ``getresultdata()`` | Gets results from an analyzer as matrices. |
| ``getvalue()`` | Gets an internal value for an element internal parameter. |
| ``setvalue()`` | Sets an internal value for an element internal parameter. |

Use only commands verified in the deployed lumapi version. In
particular, do **not** assume convenience helpers such as
``getproperties()`` exist just because they appear in external
examples; in INTERCONNECT, property discovery is done with ``set()`` or
``setnamed(element)`` plus targeted ``getnamed(...)`` calls.

## Scripted Element / S-Parameter Commands

These commands are used for creating scripted elements and
S-parameter elements:

| Command | Description |
|---------|-------------|
| ``popportdata()`` | Extracts the first available data value from the input port. |
| ``pushportdata()`` | Sends the data to the output port. |
| ``cloneportdata()`` | Clones an existing data value. |
| ``popportframe()`` | Returns a frame structure for the input signal on a given port. |
| ``pushportframe()`` | Writes a frame structure for the output signal on a given port. |
| ``getmonitorframe()`` | Reads the available frames from an analyzer input port. |
| ``getmonitorwaveform()`` | Returns a waveform structure from an analyzer input port. |
| ``portdatasize()`` | Returns the number of data values available at the input port. |
| ``setsparameter()`` | Sets the S-parameter between output and input port. |
| ``importsparameter()`` | Imports Script-workspace S-parameter data into S-parameter elements. |
| ``setfir()`` | Initializes a FIR filter using the current S-parameters. |
| ``setiir()`` | Initializes an IIR filter using the current S-parameters. |
| ``getports()`` | Returns a list of ports in an element. |

## User-Defined Settings Commands

| Command | Description |
|---------|-------------|
| ``setsetting()`` | Sets the value of a user-defined setting. |
| ``getsetting()`` | Returns the value of a user-defined setting. |

## Optimization Commands

| Command | Description |
|---------|-------------|
| ``runoptimization()`` | Optimizes a chosen element property under specified conditions. |

## Export & Utility Commands

| Command | Description |
|---------|-------------|
| ``exportimage()`` | Exports an image of the current circuit schematic. |
| ``constructgeneratormatrix()`` | Constructs a symmetric coding generator matrix. |
| ``importtemperaturemap()`` | Imports an Icepak data file to an INTERCONNECT schematic design. |

## Result Extraction

**Never guess result/dataset names.** Use the discovery pattern:

1. ``getresult(element)`` with no second argument lists available
   dataset names.
2. ``getresult(element, dataset_name)`` returns the data as a dict.

Common analyzer result names (always verify with step 1):

| Analyzer | Typical dataset names |
|----------|----------------------|
| OSA | ``"sum/signal"``, ``"mode 1/signal"`` |
| ONA | ``"input 1/mode 1/gain"``, ``"input 1/mode 1/neff"`` |
| Eye Diagram | ``"measurement/BER"``, ``"measurement/Q factor"`` |

The returned dataset is a dict with keys like ``"Frequency"``,
``"power (dBm)"``, etc.

If ``getresult(element)`` lists a dataset but the returned payload is
empty or only contains a placeholder ``Lumerical_dataset`` envelope,
do not continue with blind indexing. Treat that as a data-health issue:
validate the signal chain, analyzer configuration, and whether the
analyzer is appropriate for the current workflow (for example, ONA is
often more informative than OSA for passive transfer-function checks).

See also: ``workflow``, ``interconnect_workflow``, ``sweeps``.
