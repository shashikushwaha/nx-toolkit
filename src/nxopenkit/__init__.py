"""Public package interface for the NX toolkit."""
import os
import sys

ugii_base_dir = os.environ.get("UGII_BASE_DIR")
if ugii_base_dir:
    sys.path.append(os.path.join(ugii_base_dir, "NXBIN", "python"))
    # os.add_dll_directory(os.path.join(ugii_base_dir, "NXBIN"))
    # os.environ["PYTHONPATH"] = os.path.join(ugii_base_dir, "NXBIN", "python") + os.pathsep + os.environ.get("PYTHONPATH", "")

import NXOpen

from .core.body import Body 
from .core.edge import Edge
from .core.face import Face
from .core.feature import Feature
from .core.icurve import ICurve
from .core.part import Part 
from .core.uf_manager import UFManager
from .core.datum_axis import DatumAxis 
from .core.datum_plane import DatumPlane
from .core.coordinate_system import CoordinateSystem
from .core.isurface import ISurface
from .core.displayable_object import DisplayableObject
from .core.named_object import NamedObject
from .core.tagged_object import TaggedObject
from .core.point import Point
from .modeling.boolean_builder import BooleanBuilder
from .modeling.extrude_builder import  ExtrudeBuilder
from .maths.vector3d import Vector3d
from .maths.point3d import Point3d 
from .maths.matrix3x3 import Matrix3X3

__version__ = "0.1.0"

__all__ = [
    "Body", 
    "Edge",
    "Face", 
    "Feature", 
    "ICurve", 
    "ISurface",
    "NamedObject",
    "TaggedObject",
    "CoordinateSystem", 
    "DatumPlane", 
    "DatumAxis", 
    "DisplayableObject", 
    "Part", 
    "Point", 
    "UFManager", 
    "BooleanBuilder",
    "ExtrudeBuilder", 
    "Vector3d",
    "Point3d",
    "Matrix3X3"
    ]