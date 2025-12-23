# bear/__init__.py
import yaml, os
from pathlib import Path
from datetime import datetime

_CONFIG_PATH = Path(__file__).parent.parent / "config" / "settings.yaml"
config = yaml.safe_load(_CONFIG_PATH.read_text())

def tick():
    return f"🧸 CryptoBear tick {datetime.now():%X}"