from abc import ABC, abstractmethod
from ctypes import cast

import NXOpen


class ISurface(ABC):
    
    @property
    @abstractmethod
    def nx_object(self) -> NXOpen.ISurface:
        cast(NXOpen.ISurface, super().nx_object)