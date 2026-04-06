# Copyright 2026 NVIDIA CORPORATION & AFFILIATES
#
# Licensed under the NVIDIA Software and Model Evaluation License (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
# SPDX-License-Identifier: LicenseRef-NvidiaProprietary

"""Mock experiments with realistic wall-clock execution time for workflow testing."""

from .resonator_spectroscopy import resonator_spectroscopy
from .qubit_spectroscopy import qubit_spectroscopy
from .rabi_oscillation import rabi_oscillation
from .t1_measurement import t1_measurement
from .ramsey_measurement import ramsey_measurement

__all__ = [
    "resonator_spectroscopy",
    "qubit_spectroscopy",
    "rabi_oscillation",
    "t1_measurement",
    "ramsey_measurement",
]
