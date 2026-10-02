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

"""Dictionary-based ``addX`` syntax shared by FDTD, MODE, and DEVICE.

All three products use the same lumapi calls (``addrect``,
``addcircle``, ``addsphere``, ...) and the same dictionary form.
Substitute the appropriate handle name (``fdtd``, ``mode``,
``device``) for the snippets below.
"""

from __future__ import annotations

from importlib.resources import files


def get_guidelines_for_geometry() -> str:
    """Dictionary-based ``addX`` syntax for Lumerical layout objects (FDTD/MODE/DEVICE)."""
    return (
        files("ansys.lumerical.mcp.contexts.data.geometry")
        .joinpath("geometry.md")
        .read_text(encoding="utf-8")
    )


__all__ = ["get_guidelines_for_geometry"]
