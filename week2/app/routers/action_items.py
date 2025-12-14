from __future__ import annotations

import sqlite3
from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException

from .. import db
from ..schemas import ActionItemRead, ActionItemUpdate, ExtractRequest, ExtractResponse
from ..services.extract import extract_action_items, extract_action_items_llm


router = APIRouter(prefix="/action-items", tags=["action-items"])


@router.post("/extract", response_model=ExtractResponse)
def extract(
    payload: ExtractRequest, conn: sqlite3.Connection = Depends(db.get_db)
) -> ExtractResponse:
    text = payload.text.strip()
    if not text:
        raise HTTPException(status_code=400, detail="text is required")

    note_id: Optional[int] = None
    if payload.save_note:
        note_id = db.insert_note(conn, text)

    items = extract_action_items(text)
    ids = db.insert_action_items(conn, items, note_id=note_id)
    
    response_items = []
    for i, t in zip(ids, items):
        response_items.append(ActionItemRead(id=i, text=t, note_id=note_id, done=False))
        
    return ExtractResponse(note_id=note_id, items=response_items)


@router.post("/extract-llm", response_model=ExtractResponse)
def extract_llm(
    payload: ExtractRequest, conn: sqlite3.Connection = Depends(db.get_db)
) -> ExtractResponse:
    text = payload.text.strip()
    if not text:
        raise HTTPException(status_code=400, detail="text is required")

    note_id: Optional[int] = None
    if payload.save_note:
        note_id = db.insert_note(conn, text)

    items = extract_action_items_llm(text)
    ids = db.insert_action_items(conn, items, note_id=note_id)
    
    response_items = []
    for i, t in zip(ids, items):
        response_items.append(ActionItemRead(id=i, text=t, note_id=note_id, done=False))
        
    return ExtractResponse(note_id=note_id, items=response_items)


@router.get("", response_model=List[ActionItemRead])
def list_all(
    note_id: Optional[int] = None, conn: sqlite3.Connection = Depends(db.get_db)
) -> List[ActionItemRead]:
    rows = db.list_action_items(conn, note_id=note_id)
    return [ActionItemRead.model_validate(dict(r)) for r in rows]


@router.post("/{action_item_id}/done", response_model=ActionItemRead)
def mark_done(
    action_item_id: int,
    payload: ActionItemUpdate,
    conn: sqlite3.Connection = Depends(db.get_db),
) -> ActionItemRead:
    db.mark_action_item_done(conn, action_item_id, payload.done)
    # Fetch the updated item to return it
    # Since we don't have a get_action_item function, we can just construct the response
    # or add a get_action_item function to db.py. For now, let's assume success.
    # Ideally we should fetch it.
    # Let's add a quick fetch or just return what we have if we trust the update.
    # But to be correct with the schema, we need the other fields.
    # Let's query it.
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM action_items WHERE id = ?", (action_item_id,))
    row = cursor.fetchone()
    if not row:
        raise HTTPException(status_code=404, detail="Action item not found")
    return ActionItemRead.model_validate(dict(row))


