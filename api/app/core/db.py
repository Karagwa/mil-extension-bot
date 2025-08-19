from typing import Any, Dict, List
from app.core.config import settings

# Try to import Supabase client only when needed.
def _real_supabase():
    from supabase import create_client
    return create_client(settings.supabase_url, settings.supabase_key)

# ---------- In-memory fallback for tests / mock ----------
class _Result:
    def __init__(self, data): self.data = data

class _MemTable:
    def __init__(self): self.rows: List[Dict[str, Any]] = []
    def insert(self, row: Dict[str, Any]):
        self.rows.append(row); return _Result([row])
    def select(self, *cols: str):
        self._cols = cols or None; return self
    def eq(self, key: str, val: Any):
        self._filtered = [r for r in self.rows if r.get(key) == val]; return self
    def execute(self):
        return _Result(getattr(self, "_filtered", self.rows))

class _MemDB:
    def __init__(self): self._tables: Dict[str, _MemTable] = {}
    def table(self, name: str) -> _MemTable:
        if name not in self._tables: self._tables[name] = _MemTable()
        return self._tables[name]

_memdb = _MemDB()

def get_db():
    """
    Returns a DB-like object.
    - MOCK_MODE: in-memory DB (fast, deterministic tests).
    - REAL: Supabase client (when creds provided).
    """
    if settings.mock_mode or not (settings.supabase_url and settings.supabase_key):
        return _memdb
    return _real_supabase()
