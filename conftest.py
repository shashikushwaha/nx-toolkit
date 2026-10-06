import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SRC_DIR = ROOT / "src"
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

# _nx_dll_directory_handles = []
# _ugii_base_dir = os.environ.get("UGII_BASE_DIR")
# if _ugii_base_dir:
#     _nx_python_dir = os.path.join(_ugii_base_dir, "NXBIN", "python")
#     if not os.path.isdir(_nx_python_dir):
#         raise FileNotFoundError(f"NX Python directory does not exist: {_nx_python_dir}")
#     if _nx_python_dir not in sys.path:
#         sys.path.insert(0, _nx_python_dir)

#     if hasattr(os, "add_dll_directory"):
#         for _directory in ("NXBIN", "NXBIN\\python", "UGII", "UGOPEN"):
#             _dll_directory = os.path.join(_ugii_base_dir, _directory)
#             if not os.path.isdir(_dll_directory):
#                 raise FileNotFoundError(f"NX DLL directory does not exist: {_dll_directory}")
#             _nx_dll_directory_handles.append(os.add_dll_directory(_dll_directory))
