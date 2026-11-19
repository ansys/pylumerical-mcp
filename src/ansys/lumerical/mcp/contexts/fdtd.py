# Copyright (C) 2026 Synopsys, Inc. and ANSYS, Inc. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""FDTD-specific guideline topics.

Owns every Lumerical FDTD-flavoured guideline:

- ``fdtd_workflow`` -- chunked **build/setup** stages, PML extension
  rule, disambiguation defaults.
- ``fdtd_workflow_example`` -- worked end-to-end build (straight
  silicon waveguide with TE port S-parameter extraction).
- ``fdtd_sources_monitors`` -- ``setglobalsource`` /
  ``setglobalmonitor`` rules, port-vs-mode-source decision,
  injection control via ``FDTD::ports``.
- ``fdtd_run_and_results`` -- FDTD-specific ``run()`` calling
  conventions (solver / resource type / resource name / CUDA /
  Cloud Burst), ``run()``-once + ``switchtolayout`` rule,
  dataset-as-dict contract, and ``getresult`` discovery.
- ``fdtd_boundary_conditions`` -- PML profiles (standard /
  stabilized / steep angle), symmetric / anti-symmetric, periodic,
  Bloch; decision guide.
- ``fdtd_mesh_and_convergence`` -- ``mesh accuracy`` semantics,
  conformal-mesh variants, mesh overrides, simulation time /
  auto-shutoff, divergence diagnostics.
- ``fdtd_source_types`` -- non-port source catalog: plane wave,
  BFAST, Gaussian, dipole, TFSF, imported source.
- ``fdtd_monitors_and_field_extraction`` -- monitor catalog,
  override-global pattern, mode expansion, reduce-before-print.
- ``fdtd_far_field_and_grating`` -- ``farfield2d/3d``,
  ``farfieldexact``, grating projections, NA filtering.

Cross-cutting topics that apply to several products live in their
own modules to avoid duplication.
"""

from __future__ import annotations

from importlib.resources import files


def get_guidelines_for_fdtd_workflow() -> str:
    """FDTD-specific build/setup workflow: stages, PML extension, disambiguation defaults."""
    return (
        files("ansys.lumerical.mcp.contexts.data.fdtd")
        .joinpath("workflow.md")
        .read_text(encoding="utf-8")
    )


def get_guidelines_for_fdtd_workflow_example() -> str:
    """Worked end-to-end FDTD example: straight silicon waveguide with TE ports."""
    return (
        files("ansys.lumerical.mcp.contexts.data.fdtd")
        .joinpath("workflow_example.md")
        .read_text(encoding="utf-8")
    )


def get_guidelines_for_fdtd_sources_monitors() -> str:
    """Global source/monitor settings and the port-vs-mode-source decision."""
    return (
        files("ansys.lumerical.mcp.contexts.data.fdtd")
        .joinpath("sources_monitors.md")
        .read_text(encoding="utf-8")
    )


def get_guidelines_for_fdtd_run_and_results() -> str:
    """FDTD run + results: solver args, run-once + ``switchtolayout``, datasets, ``getresult``."""
    return (
        files("ansys.lumerical.mcp.contexts.data.fdtd")
        .joinpath("run_and_results.md")
        .read_text(encoding="utf-8")
    )


def get_guidelines_for_fdtd_boundary_conditions() -> str:
    """FDTD boundary conditions: PML profiles, symmetric/anti-symmetric, periodic, Bloch."""
    return (
        files("ansys.lumerical.mcp.contexts.data.fdtd")
        .joinpath("boundary_conditions.md")
        .read_text(encoding="utf-8")
    )


def get_guidelines_for_fdtd_mesh_and_convergence() -> str:
    """FDTD mesh accuracy, conformal mesh, mesh overrides, auto-shutoff, divergence."""
    return (
        files("ansys.lumerical.mcp.contexts.data.fdtd")
        .joinpath("mesh_and_convergence.md")
        .read_text(encoding="utf-8")
    )


def get_guidelines_for_fdtd_source_types() -> str:
    """FDTD source-type catalog: plane wave, Gaussian, dipole, TFSF, import, BFAST."""
    return (
        files("ansys.lumerical.mcp.contexts.data.fdtd")
        .joinpath("source_types.md")
        .read_text(encoding="utf-8")
    )


def get_guidelines_for_fdtd_monitors_and_field_extraction() -> str:
    """FDTD monitor catalog + field-extraction patterns (override-global, reduce-before-print)."""
    return (
        files("ansys.lumerical.mcp.contexts.data.fdtd")
        .joinpath("monitors_and_field_extraction.md")
        .read_text(encoding="utf-8")
    )


def get_guidelines_for_fdtd_far_field_and_grating() -> str:
    """FDTD far-field and grating projection: farfield2d/3d, farfieldexact, NA filtering."""
    return (
        files("ansys.lumerical.mcp.contexts.data.fdtd")
        .joinpath("far_field_and_grating.md")
        .read_text(encoding="utf-8")
    )


__all__ = [
    "get_guidelines_for_fdtd_workflow",
    "get_guidelines_for_fdtd_workflow_example",
    "get_guidelines_for_fdtd_sources_monitors",
    "get_guidelines_for_fdtd_run_and_results",
    "get_guidelines_for_fdtd_boundary_conditions",
    "get_guidelines_for_fdtd_mesh_and_convergence",
    "get_guidelines_for_fdtd_source_types",
    "get_guidelines_for_fdtd_monitors_and_field_extraction",
    "get_guidelines_for_fdtd_far_field_and_grating",
]
