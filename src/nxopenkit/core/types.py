
from typing import Union

from nxopenkit.core.datum_axis import DatumAxis
from nxopenkit.core.direction import Direction
from nxopenkit.maths.vector3d import Vector3d

Number = Union[int, float]
Angle = Union[int, float, str]
Double = Union[int, float, str]
VectorLike = Union[Vector3d, Direction, DatumAxis]