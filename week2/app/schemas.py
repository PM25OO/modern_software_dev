from __future__ import annotations

from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel


class NoteBase(BaseModel):
    content: str


class NoteCreate(NoteBase):
    pass


class NoteRead(NoteBase):
    id: int
    created_at: Optional[str] = None  # SQLite returns strings for datetime

    class Config:
        from_attributes = True


class ActionItemBase(BaseModel):
    text: str
    done: bool = False


class ActionItemCreate(ActionItemBase):
    pass


class ActionItemUpdate(BaseModel):
    done: bool



class ActionItemRead(ActionItemBase):
    id: int
    note_id: Optional[int] = None
    created_at: Optional[str] = None

    class Config:
        from_attributes = True


class ExtractRequest(BaseModel):
    text: str
    save_note: bool = False


class ExtractResponse(BaseModel):
    note_id: Optional[int] = None
    items: List[ActionItemRead]
