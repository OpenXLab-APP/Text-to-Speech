# Copyright (c) 2023 Amphion.
#
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.

#################### Anti-aliasing ####################

import torch.nn as nn
from torch.nn import functional as F

from .filter import *

# This code is adopted from BigVGAN under the MIT License
# https://github.com/NVIDIA/BigVGAN

class UpSample1d(nn.Module):
    def __init__(self, ratio=2, kernel_size=None):
        super().__init__()
        self.ratio = ratio
        self.kernel_size = (
            int(6 * ratio // 2) * 2 if kernel_size is None else kernel_size
        )
        self.stride = ratio
        self.pad = self.kernel_size // ratio - 1
        self.pad_left = self.pad * self.stride + (self.kernel_size - self.stride) // 2
        self.pad_right = (
            self.pad * self.stride + (self.kernel_size - self.stride + 1) // 2
        )
        filter = kaiser_sinc_filter1d(
            cutoff=0.5 / ratio, half_width=0.6 / ratio, kernel_size=self.kernel_size
        )
        self.register_buffer("filter", filter)

    # x: [B, C, T]
    def forward(self, x):
        _, C, _ = x.shape

        x = F.pad(x, (self.pad, self.pad), mode="replicate")
        x = self.ratio * F.conv_transpose1d(
            x, self.filter.expand(C, -1, -1), stride=self.stride, groups=C
        )
        x = x[..., self.pad_left : -self.pad_right]

        return x


class DownSample1d(nn.Module):
    def __init__(self, ratio=2, kernel_size=None):
        super().__init__()
        self.ratio = ratio
        self.kernel_size = (
            int(6 * ratio // 2) * 2 if kernel_size is None else kernel_size
        )
        self.lowpass = LowPassFilter1d(
            cutoff=0.5 / ratio,
            half_width=0.6 / ratio,
            stride=ratio,
            kernel_size=self.kernel_size,
        )

    def forward(self, x):
        xx = self.lowpass(x)

        return xx
