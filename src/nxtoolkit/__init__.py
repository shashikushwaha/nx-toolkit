"""Public package interface for the NX toolkit."""
import sys
sys.path.append(r"C:\Program Files\Siemens\NX 12.0\NXBIN\python")
import NXOpen

from .core import Body, Edge, Face, Feature, Part

__version__ = "0.1.0"

__all__ = ["Body", "Edge", "Face", "Feature", "Part"]