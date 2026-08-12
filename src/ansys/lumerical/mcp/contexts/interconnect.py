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

"""INTERCONNECT-specific guideline topics.

Owns every Lumerical INTERCONNECT-flavoured guideline:

- ``interconnect_workflow`` -- chunked build/setup stages for photonic
  circuit simulation: element addition, naming, selection, connection,
  compound elements, and property discovery.
- ``interconnect_simulation`` -- root element simulation configuration
  (time-domain vs. frequency-domain modes, ``"simulation input"``
  selector, ONA frequency-domain workflow), and ``getresult``
  discovery pattern for analyzers.
- ``interconnect_commands`` -- reference of INTERCONNECT-specific lumapi
  commands grouped by category (element library, design kits,
  measurements, scripted elements).
"""

from __future__ import annotations

from importlib.resources import files


def get_guidelines_for_interconnect_workflow() -> str:
    """INTERCONNECT-specific build/setup workflow: stages, element management, simulation config."""
    return (
        files("ansys.lumerical.mcp.contexts.data.interconnect")
        .joinpath("workflow.md")
        .read_text(encoding="utf-8")
    )


def get_guidelines_for_interconnect_simulation() -> str:
    """INTERCONNECT simulation config: root element, time/freq domain, result extraction."""
    return (
        files("ansys.lumerical.mcp.contexts.data.interconnect")
        .joinpath("simulation.md")
        .read_text(encoding="utf-8")
    )


def get_guidelines_for_interconnect_commands() -> str:
    """INTERCONNECT-specific lumapi command reference by category."""
    return (
        files("ansys.lumerical.mcp.contexts.data.interconnect")
        .joinpath("commands.md")
        .read_text(encoding="utf-8")
    )


__all__ = [
    "get_guidelines_for_interconnect_commands",
    "get_guidelines_for_interconnect_simulation",
    "get_guidelines_for_interconnect_workflow",
]
