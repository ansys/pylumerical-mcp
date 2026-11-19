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

"""DEVICE finite-element IDE guideline topics.

Owns guidelines for the Lumerical finite-element solver environment (DEVICE IDE),
which hosts HEAT, CHARGE, FEEM, and DGTD:

- ``device_workflow`` -- chunked build/setup stages shared across all
  finite-element solvers: materials, geometry, solver addition, simulation
  region, boundary conditions, monitors, run, and results.
- ``device_materials`` -- model-material creation, property-family
  assignment (EM / CT / HT), and database discovery.
- ``device_simulation_region`` -- simulation-region ownership model,
  boundary types (Open / Closed / Shell), and solver linkage.
"""

from __future__ import annotations

from importlib.resources import files


def get_guidelines_for_device_workflow() -> str:
    """Finite-element IDE workflow shared by HEAT, CHARGE, FEEM, and DGTD."""
    return (
        files("ansys.lumerical.mcp.contexts.data.device")
        .joinpath("workflow.md")
        .read_text(encoding="utf-8")
    )


def get_guidelines_for_device_materials() -> str:
    """Material-library creation and database discovery for DEVICE finite-element solvers."""
    return (
        files("ansys.lumerical.mcp.contexts.data.device")
        .joinpath("materials.md")
        .read_text(encoding="utf-8")
    )


def get_guidelines_for_device_simulation_region() -> str:
    """Simulation-region setup shared by HEAT, CHARGE, FEEM, DGTD, and peers."""
    return (
        files("ansys.lumerical.mcp.contexts.data.device")
        .joinpath("simulation_region.md")
        .read_text(encoding="utf-8")
    )


__all__ = [
    "get_guidelines_for_device_workflow",
    "get_guidelines_for_device_materials",
    "get_guidelines_for_device_simulation_region",
]
