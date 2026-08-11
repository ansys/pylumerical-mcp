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

"""Product-agnostic sweep guidance (``sweeps`` and ``nested_sweeps`` topics).

Owns the generic lifecycle of any analysis task created with
``addsweep`` and configured via the matching ``setsweep`` /
``addsweepparameter`` / ``runsweep`` / ``getsweepresult`` /
``deletesweep`` lsf commands. Applies to FDTD, MODE, and INTERCONNECT.
The S-parameter matrix sweep flavour (``addsweep(3)``) has additional
product-specific rules and a Y-branch worked example in
:mod:`ansys.lumerical.mcp.contexts.s_parameter_sweep`.
"""

from __future__ import annotations

from importlib.resources import files


def get_guidelines_for_sweeps() -> str:
    """Product-agnostic sweep lifecycle: addsweep/setsweep/runsweep/getsweepresult."""
    return (
        files("ansys.lumerical.mcp.contexts.data.sweeps")
        .joinpath("sweeps.md")
        .read_text(encoding="utf-8")
    )


def get_guidelines_for_nested_sweeps() -> str:
    """Product-agnostic nested sweep workflow based on ``insertsweep``."""
    return (
        files("ansys.lumerical.mcp.contexts.data.sweeps")
        .joinpath("nested_sweeps.md")
        .read_text(encoding="utf-8")
    )


__all__ = ["get_guidelines_for_sweeps", "get_guidelines_for_nested_sweeps"]
