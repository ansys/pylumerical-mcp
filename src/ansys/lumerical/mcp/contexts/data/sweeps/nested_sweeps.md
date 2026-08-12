# Lumerical Nested Sweeps

Nested sweeps are hierarchical: create the **inner sweep** first, then
wrap it with an **outer sweep** using ``insertsweep``. Use this when the
task needs **all combinations** of two swept parameters.

Read ``workflow`` first, then ``sweeps`` for the normal ``addsweep``
lifecycle. The only extra command here is ``insertsweep``.

## Core Rule

- create the inner sweep first
- wrap it with ``insertsweep("<child_name>")``
- add the child result to the parent sweep by result name only
- configure and run the outer sweep only
- use ``getsweepresult("<outer_name>", ...)`` on the outer sweep

When a parent sweep exposes a child sweep result, the ``Result`` field is
just the child result name. Do not prepend a hierarchical path such as
``::outer_sweep::inner_sweep::child_result``. Once the child result has been
added to the parent, the parent can access it directly.

## Compact Example

```python
fdtd = _lum_get("device")

fdtd.deletesweep("inner_sweep")
fdtd.addsweep(0)
fdtd.setsweep("sweep", "name", "inner_sweep")

fdtd.insertsweep("inner_sweep")
fdtd.setsweep("sweep", "name", "outer_sweep")

fdtd.addsweepresult("inner_sweep", {
    "Name": "R_inner",
    "Result": "::model::R::T",
})
fdtd.addsweepresult("outer_sweep", {
    "Name": "R",
    "Result": "R_inner"
})

# Propagate child results upward by name only, with no path prefix.
fdtd.runsweep("outer_sweep")
_lum_print_json(fdtd.getsweepresult("outer_sweep"))
```

For deeper nesting, repeat the same pattern one level at a time. If
``bottom_sweep`` defines ``bottom_result_1`` and ``bottom_result_2``, then
``mid_sweep`` should add results that point to ``bottom_result_1`` and
``bottom_result_2`` by name only. Then ``top_sweep`` should add results that
point to the mid-level result names, again by name only. None of these parent
assignments need a sweep path prefix.

Do not separately run the inner sweep after it has been wrapped.
The lower-level result must be added as a result on the parent sweep, and the
final collection happens from the top-level sweep only.


See also: ``workflow``, ``sweeps``, ``s_parameter_sweep``.
