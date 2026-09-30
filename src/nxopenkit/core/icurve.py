from abc import ABC, abstractmethod
from ctypes import cast

import NXOpen


class ICurve(ABC):
    
    @property
    @abstractmethod
    def to_nx(self) -> NXOpen.ICurve:
        cast(NXOpen.ICurve, super().to_nx)