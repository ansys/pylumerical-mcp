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

"""S-parameter matrix sweep guidance shared by FDTD and MODE (``s_parameter_sweep``).

Both products expose ``addsweep(3)`` and the same
``runsweep``/``getsweepresult``/``exportsweep`` lifecycle for
extracting a full N x N S-matrix; the per-task property set differs
(documented inline). Snippets use the ``fdtd`` handle name for
brevity. The ``mode`` handle works identically (substitute the
appropriate name).
"""

from __future__ import annotations

from importlib.resources import files


def get_guidelines_for_s_parameter_sweep() -> str:
    """S-parameter matrix sweep recipe and Y-branch example for FDTD and MODE."""
    return (
        files("ansys.lumerical.mcp.contexts.data.s_parameter_sweep")
        .joinpath("s_parameter_sweep.md")
        .read_text(encoding="utf-8")
    )


__all__ = ["get_guidelines_for_s_parameter_sweep"]
