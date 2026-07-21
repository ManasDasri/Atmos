import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[1]))

from backend.main import app


def test_fastapi_app_is_initialized():
    assert app.title == "Atmos"
