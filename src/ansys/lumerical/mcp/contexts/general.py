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

"""Product-agnostic Lumerical workflow guidance (``workflow`` topic).

Owns the generic execution model, snippet structure, chunking principle,
parameter management, and "do NOT make assumptions / do NOT invent or
re-run" rules that apply to every Lumerical product (FDTD, MODE, DEVICE,
INTERCONNECT). Product-specific topics live in
:mod:`ansys.lumerical.mcp.contexts.fdtd` (and future
``mode``/``device``/``interconnect`` modules).
"""

from __future__ import annotations

from importlib.resources import files


def get_guidelines_for_workflow() -> str:
    """Product-agnostic execution model, snippet structure, chunking, do-not rules."""
    return (
        files("ansys.lumerical.mcp.contexts.data.general")
        .joinpath("workflow.md")
        .read_text(encoding="utf-8")
    )


__all__ = ["get_guidelines_for_workflow"]
