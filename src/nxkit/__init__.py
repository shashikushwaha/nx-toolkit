"""Public package interface for the NX toolkit."""
import os
import sys

ugii_base_dir = os.environ.get("UGII_BASE_DIR")
if ugii_base_dir:
    sys.path.append(os.path.join(ugii_base_dir, "NXBIN", "python"))

import NXOpen

from .core import Body, Edge, Face, Feature, Part

__version__ = "0.1.0"

__all__ = ["Body", "Edge", "Face", "Feature", "Part"]