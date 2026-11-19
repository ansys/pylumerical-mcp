# Device Materials

This topic covers material handling in the DEVICE finite-element solver environment used by
finite-element solvers such as HEAT, CHARGE, FEEM, and DGTD.
Unlike FDTD and MODE, these workflows should not assume that a built-in database
material is assigned directly to a geometry object.

Read ``workflow`` first for the generic execution model and do-not-assume rules,
and ``device_workflow`` for the DEVICE-specific build stages. Use this topic whenever
the task involves building or inspecting material models in the DEVICE
solver or IDE.

## Material Model Pattern

In the DEVICE environment, create a model material in the materials object
library first, then attach the required property families to that material.

The standard pattern is:

1. call ``device.addmodelmaterial()``
2. call ``device.set("name", ...)`` to name the model material
3. add the needed property families with ``device.addmaterialproperties(family, db_name)``
4. re-select the model material with ``device.select("materials::<name>")`` before each
   additional property insertion, because the selection shifts to the inserted property
5. assign the model material to geometry with ``device.setnamed(obj, "material", name)``

Representative pattern:

```python
device.addmodelmaterial()
device.set("name", "silicon")
device.addmaterialproperties("EM", "Si (Silicon) - Palik")
device.select("materials::silicon")
device.addmaterialproperties("CT", "Si (Silicon)")
device.select("materials::silicon")
device.addmaterialproperties("HT", "Si (Silicon)")
```

## Property Families

The main property families imported from the DEVICE material databases are:

- ``EM`` for optical or electromagnetic properties
- ``CT`` for conductive or electrical transport properties
- ``HT`` for thermal or heat-transport properties

Only add the families that the requested solver workflow actually needs. For
example, a thermal-only HEAT task may only need ``HT``, while an electro-thermal
CHARGE task may need both ``CT`` and ``HT`` and may also carry ``EM`` data when
the model is coupled to upstream optical workflows.

## Exploring Available Database Entries

Do not guess material names from memory when the task depends on the exact name
present in the DEVICE databases. Use ``addmaterialproperties`` without a
material name to query what is available for each property family. Note that the
query only works when a model material is selected.

In this environment, the query result can come back either as a Python list or
as one newline-delimited string. Normalize it before filtering so the workflow
does not accidentally treat one long string as one material name.

```python
em_names = device.addmaterialproperties("EM")
ct_names = device.addmaterialproperties("CT")
ht_names = device.addmaterialproperties("HT")
if isinstance(em_names, str):
    em_names = em_names.splitlines()
if isinstance(ct_names, str):
    ct_names = ct_names.splitlines()
if isinstance(ht_names, str):
    ht_names = ht_names.splitlines()
_lum_print_json({"EM": em_names, "CT": ct_names, "HT": ht_names})
```

This is the DEVICE analogue of ``getmaterial()`` in the FDTD and MODE
material workflow.

## Selection Hygiene

After ``addmaterialproperties(...)`` the selection moves from the model material
to the inserted property object. Re-select the material model before adding the
next property family.

```python
device.select("materials::silicon")
device.addmaterialproperties("CT", "Si (Silicon)")
```

If a snippet fails while adding multiple properties, the first cheap check is to
inspect whether the selection is still on the material model rather than on one
of its child properties.

## When To Query Versus When To Reuse

Prefer querying the database names when:

- the user names a material loosely rather than with the exact database string
- the workflow needs to know whether a property family exists for a given
  material in ``EM``, ``CT``, or ``HT``
- a shared model material is being assembled from several databases and name
  mismatches would be easy to miss
- the database query returned one newline-delimited string and needs
  ``splitlines()`` before exact-name filtering

Reuse an already-known exact database string only when it has already been
confirmed in the current session or is explicitly given by the user.

## See Also

``workflow`` for the generic execution model. ``device_workflow`` for HEAT / CHARGE / FEEM / DGTD
solver setup. ``device_simulation_region`` for simulation-region and boundary setup.
