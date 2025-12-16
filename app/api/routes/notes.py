from fastapi import APIRouter, HTTPException, Depends, status
from typing import List
from app.models.note import Note, NoteCreate, NoteUpdate
from app.services.note_service import NoteService
from app.repositories.note_repository import NoteRepository

router = APIRouter(prefix="/notes", tags=["notes"])

# Dependency injection
def get_note_service() -> NoteService:
    note_repository = NoteRepository()
    return NoteService(note_repository)

@router.get("/", response_model=List[Note])
async def get_notes(note_service: NoteService = Depends(get_note_service)):
    """Récupérer toutes les notes"""
    return note_service.get_all_notes()

@router.get("/{note_id}", response_model=Note)
async def get_note(
    note_id: int, 
    note_service: NoteService = Depends(get_note_service)
):
    """Récupérer une note par son ID"""
    note = note_service.get_note_by_id(note_id)
    if not note:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Note avec l'ID {note_id} non trouvée"
        )
    return note

@router.post("/", response_model=Note, status_code=status.HTTP_201_CREATED)
async def create_note(
    note_create: NoteCreate,
    note_service: NoteService = Depends(get_note_service)
):
    """Créer une nouvelle note"""
    try:
        return note_service.create_note(note_create)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

@router.put("/{note_id}", response_model=Note)
async def update_note(
    note_id: int,
    note_update: NoteUpdate,
    note_service: NoteService = Depends(get_note_service)
):
    """Mettre à jour une note"""
    try:
        updated_note = note_service.update_note(note_id, note_update)
        if not updated_note:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Note avec l'ID {note_id} non trouvée"
            )
        return updated_note
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

@router.delete("/{note_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_note(
    note_id: int,
    note_service: NoteService = Depends(get_note_service)
):
    """Supprimer une note"""
    success = note_service.delete_note(note_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Note avec l'ID {note_id} non trouvée"
        )