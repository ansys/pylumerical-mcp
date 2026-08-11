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

"""MODE-specific guideline topics."""

from __future__ import annotations

from importlib.resources import files


def get_guidelines_for_mode_fde_workflow() -> str:
    """MODE FDE build/setup workflow for straight and bent-waveguide tasks."""
    return (
        files("ansys.lumerical.mcp.contexts.data.mode")
        .joinpath("fde_workflow.md")
        .read_text(encoding="utf-8")
    )


def get_guidelines_for_mode_fde_results() -> str:
    """MODE FDE solve/result extraction guidance."""
    return (
        files("ansys.lumerical.mcp.contexts.data.mode")
        .joinpath("fde_results.md")
        .read_text(encoding="utf-8")
    )


def get_guidelines_for_mode_eme_workflow() -> str:
    """MODE EME build/setup and analysis workflow."""
    return (
        files("ansys.lumerical.mcp.contexts.data.mode")
        .joinpath("eme_workflow.md")
        .read_text(encoding="utf-8")
    )


def get_guidelines_for_mode_varfdtd_workflow() -> str:
    """MODE varFDTD build/setup workflow."""
    return (
        files("ansys.lumerical.mcp.contexts.data.mode")
        .joinpath("varfdtd_workflow.md")
        .read_text(encoding="utf-8")
    )


__all__ = [
    "get_guidelines_for_mode_eme_workflow",
    "get_guidelines_for_mode_fde_results",
    "get_guidelines_for_mode_fde_workflow",
    "get_guidelines_for_mode_varfdtd_workflow",
]
