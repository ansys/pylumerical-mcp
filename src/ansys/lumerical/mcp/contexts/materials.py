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

"""Material-selection guidance shared by FDTD and MODE (``materials`` topic).

Both products use the same material database and ``addmaterial``/``setmaterial``
lumapi calls. The markdown below is therefore neutral
in its handle naming (``fdtd`` shown for brevity, ``mode`` works
identically).
"""

from __future__ import annotations

from importlib.resources import files


def get_guidelines_for_materials() -> str:
    """Built-in versus custom materials, anisotropic input. Applies to FDTD and MODE."""
    return (
        files("ansys.lumerical.mcp.contexts.data.materials")
        .joinpath("materials.md")
        .read_text(encoding="utf-8")
    )


__all__ = ["get_guidelines_for_materials"]
