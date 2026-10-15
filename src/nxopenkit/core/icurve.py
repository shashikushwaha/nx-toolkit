from __future__ import annotations
from abc import ABC, abstractmethod
from ctypes import cast
from typing import Sequence

import NXOpen


class ICurve(ABC):
    
    @property
    @abstractmethod
    def to_nx(self) -> NXOpen.ICurve:
        cast(NXOpen.ICurve, super().to_nx)

    