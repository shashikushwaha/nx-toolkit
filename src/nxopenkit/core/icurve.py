from abc import ABC, abstractmethod
from ctypes import cast

import NXOpen


class ICurve(ABC):
    
    @property
    @abstractmethod
    def nx_object(self) -> NXOpen.ICurve:
        cast(NXOpen.ICurve, super().nx_object)