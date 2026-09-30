from abc import ABC, abstractmethod
from ctypes import cast

import NXOpen


class ISurface(ABC):
    
    @property
    @abstractmethod
    def to_nx(self) -> NXOpen.ISurface:
        cast(NXOpen.ISurface, super().to_nx)