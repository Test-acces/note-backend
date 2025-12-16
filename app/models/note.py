from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class NoteBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=200, description="Titre de la note")
    content: str = Field(..., min_length=1, description="Contenu de la note")

class NoteCreate(NoteBase):
    pass

class NoteUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=200)
    content: Optional[str] = Field(None, min_length=1)

class Note(NoteBase):
    id: int = Field(..., description="Identifiant unique de la note")
    created_at: datetime = Field(default_factory=datetime.now, description="Date de création")
    updated_at: datetime = Field(default_factory=datetime.now, description="Date de dernière modification")

    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }