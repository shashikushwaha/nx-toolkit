import NXOpen as nx
from nxopenkit.core.direction import Direction
from nxopenkit.maths.vector3d import Vector3d

from .datum_axis import DatumAxis
from .part import Part
from .types import VectorLike

def to_nx_axis(axis: VectorLike, is_mandatory : bool = True):

    work_part = Part.work_part().to_nx

    if not is_mandatory and axis is None:
        return None
    if isinstance(axis, DatumAxis):
        direction1 = work_part.Directions.CreateDirection(axis.to_nx, nx.Sense.Forward, nx.SmartObject.UpdateOption.WithinModeling)    
        axis1 = work_part.Axes.CreateAxis(nx.Point.Null, direction1, nx.SmartObject.UpdateOption.WithinModeling)
        return axis1
    
    if isinstance(axis, Vector3d):
        nx_direction = (
                work_part.Directions.CreateDirection(
                nx.Point3d(0.0, 0.0, 0.0),
                axis.to_nx,
                nx.SmartObject.UpdateOption.WithinModeling,
            )
        )

        nx_axis = (
                work_part.Axes.CreateAxis(
                nx.Point.Null,
                nx_direction,
                nx.SmartObject.UpdateOption.WithinModeling,
            )
        )

        return nx_axis

    if isinstance(axis, Direction):

        nx_axis = (
                work_part.Axes.CreateAxis(
                nx.Point.Null,
                axis.to_nx,
                nx.SmartObject.UpdateOption.WithinModeling,
            )
        )

        return nx_axis

    raise TypeError("direction must be DatumAxis, Direction, or Vector3d.")