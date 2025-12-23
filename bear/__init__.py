# bear/__init__.py
__version__ = "0.1.0"

def tick():
    from datetime import datetime
    return f"🧸 CryptoBear tick {datetime.now():%X}"