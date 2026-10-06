from pathlib import Path
import sys

import pytest


ROOT = Path(__file__).resolve().parents[1]
SRC_DIR = ROOT / "src"
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))


@pytest.fixture(scope="session")
def project_root() -> Path:
    return ROOT


@pytest.fixture(scope="session")
def test_case_path():
    def _resolve(*parts: str) -> Path:
        return ROOT / "test-cases" / Path(*parts)

    return _resolve
