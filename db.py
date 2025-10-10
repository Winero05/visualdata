"""Mini-module de gestion SQLite pour stocker l'historique des fichiers chargés.

Fichier DB placé dans le même dossier que `PyQt5_Complete_App.py`.

Tables créées:
- files(id, name, path, type, imported_at, metadata)
- embeddings (simple placeholder)
"""
import sqlite3
import os
import json
import datetime

DB_PATH = os.path.join(os.path.dirname(__file__), 'app_data.sqlite')

def get_conn():
    # Enable row access by name if needed
    conn = sqlite3.connect(DB_PATH)
    return conn

def init_db():
    """Create tables if they don't exist."""
    with get_conn() as conn:
        c = conn.cursor()
        c.execute('''
            CREATE TABLE IF NOT EXISTS files (
                id INTEGER PRIMARY KEY,
                name TEXT,
                path TEXT,
                type TEXT,
                imported_at TEXT,
                metadata TEXT
            )
        ''')
        c.execute('''
            CREATE TABLE IF NOT EXISTS embeddings (
                id INTEGER PRIMARY KEY,
                file_id INTEGER,
                method TEXT,
                params TEXT,
                vector BLOB,
                created_at TEXT,
                FOREIGN KEY(file_id) REFERENCES files(id)
            )
        ''')
        conn.commit()

def insert_file(file_data: dict) -> int:
    """Insert a file record and return its DB id.

    The function will serialise a minimal metadata JSON (variables, shape).
    """
    metadata = {}
    try:
        df = file_data.get('data')
        if hasattr(df, 'shape'):
            metadata['shape'] = df.shape
            metadata['variables'] = list(df.columns)
        else:
            metadata['variables'] = file_data.get('variables', [])
    except Exception:
        metadata['variables'] = file_data.get('variables', [])

    name = file_data.get('name')
    path = file_data.get('path')
    typ = file_data.get('type')
    imported_at = datetime.datetime.utcnow().isoformat()

    with get_conn() as conn:
        c = conn.cursor()
        c.execute('''
            INSERT INTO files (name, path, type, imported_at, metadata)
            VALUES (?, ?, ?, ?, ?)
        ''', (name, path, typ, imported_at, json.dumps(metadata, ensure_ascii=False)))
        conn.commit()
        return c.lastrowid

def update_file(file_data: dict) -> bool:
    """Update the metadata for an existing file using file_data['db_id'] if present.

    Returns True if updated, False otherwise.
    """
    db_id = file_data.get('db_id')
    if not db_id:
        return False

    metadata = {}
    try:
        df = file_data.get('data')
        if hasattr(df, 'shape'):
            metadata['shape'] = df.shape
            metadata['variables'] = list(df.columns)
        else:
            metadata['variables'] = file_data.get('variables', [])
    except Exception:
        metadata['variables'] = file_data.get('variables', [])

    with get_conn() as conn:
        c = conn.cursor()
        c.execute('''
            UPDATE files SET name=?, path=?, type=?, metadata=? WHERE id=?
        ''', (
            file_data.get('name'),
            file_data.get('path'),
            file_data.get('type'),
            json.dumps(metadata, ensure_ascii=False),
            db_id
        ))
        conn.commit()
        return c.rowcount > 0

def get_all_files():
    with get_conn() as conn:
        c = conn.cursor()
        c.execute('SELECT id, name, path, type, imported_at, metadata FROM files ORDER BY imported_at DESC')
        rows = c.fetchall()
        results = []
        for r in rows:
            try:
                meta = json.loads(r[5]) if r[5] else {}
            except Exception:
                meta = {}
            results.append({
                'id': r[0],
                'name': r[1],
                'path': r[2],
                'type': r[3],
                'imported_at': r[4],
                'metadata': meta
            })
        return results

def reset_db():
    """Danger: removes the DB file entirely. Use for testing."""
    try:
        if os.path.exists(DB_PATH):
            os.remove(DB_PATH)
            return True
    except Exception:
        return False
    return True
