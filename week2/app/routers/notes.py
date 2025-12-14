from __future__ import annotations

import sqlite3
from typing import List

from fastapi import APIRouter, Depends, HTTPException

from .. import db
from ..schemas import NoteCreate, NoteRead


router = APIRouter(prefix="/notes", tags=["notes"])


@router.post("", response_model=NoteRead)
def create_note(
    payload: NoteCreate, conn: sqlite3.Connection = Depends(db.get_db)
) -> NoteRead:
    content = payload.content.strip()
    if not content:
        raise HTTPException(status_code=400, detail="content is required")
    note_id = db.insert_note(conn, content)
    note = db.get_note(conn, note_id)
    if not note:
        raise HTTPException(status_code=500, detail="Failed to create note")
    return NoteRead.model_validate(note)


@router.get("/{note_id}", response_model=NoteRead)
def get_single_note(
    note_id: int, conn: sqlite3.Connection = Depends(db.get_db)
) -> NoteRead:
    row = db.get_note(conn, note_id)
    if row is None:
        raise HTTPException(status_code=404, detail="note not found")
    return NoteRead.model_validate(dict(row))


@router.get("", response_model=List[NoteRead])
def list_notes(conn: sqlite3.Connection = Depends(db.get_db)) -> List[NoteRead]:
    rows = db.list_notes(conn)
    return [NoteRead.model_validate(dict(row)) for row in rows]


