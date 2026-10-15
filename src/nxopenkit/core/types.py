import NXOpen
import NXOpen.Features
import NXOpen.GeometricUtilities
from typing import Union

from nxopenkit.core.datum_axis import DatumAxis
from nxopenkit.core.direction import Direction
from nxopenkit.maths.vector3d import Vector3d
CylinderType = NXOpen.Features.CylinderBuilder.Types
BooleanType = NXOpen.GeometricUtilities.BooleanOperation.BooleanType
SphereType = NXOpen.Features.SphereBuilder.Types
PointOnCurveLocationOption = NXOpen.PointCollection.PointOnCurveLocationOption


Number = Union[int, float]
Angle = Union[int, float, str]
Double = Union[int, float, str]
VectorLike = Union[Vector3d, Direction, DatumAxis]