"""Public package interface for the NX toolkit."""
import os
import sys

ugii_base_dir = os.environ.get("UGII_BASE_DIR")
if ugii_base_dir:
    sys.path.append(os.path.join(ugii_base_dir, "NXBIN", "python"))
    # os.add_dll_directory(os.path.join(ugii_base_dir, "NXBIN"))
    # os.environ["PYTHONPATH"] = os.path.join(ugii_base_dir, "NXBIN", "python") + os.pathsep + os.environ.get("PYTHONPATH", "")

import NXOpen

from .core import Body, Edge, Face, Feature, ICurve, Part, UFManager, DatumAxis, DatumPlane, CoordinateSystem, ISurface, DisplayableObject, NamedObject, TaggedObject, Point
from .modeling import BooleanBuilder, ExtrudeBuilder
from .maths import Vector3d
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
    "Vector3d"
    ]