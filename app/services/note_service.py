from typing import List, Optional
from app.models.note import Note, NoteCreate, NoteUpdate
from app.repositories.note_repository import NoteRepository

class NoteService:
    def __init__(self, note_repository: NoteRepository):
        self.note_repository = note_repository

    def get_all_notes(self) -> List[Note]:
        """Récupérer toutes les notes"""
        return self.note_repository.get_all()

    def get_note_by_id(self, note_id: int) -> Optional[Note]:
        """Récupérer une note par son ID"""
        return self.note_repository.get_by_id(note_id)

    def create_note(self, note_create: NoteCreate) -> Note:
        """Créer une nouvelle note"""
        # Validation métier supplémentaire si nécessaire
        if not note_create.title.strip():
            raise ValueError("Le titre ne peut pas être vide")
        
        if not note_create.content.strip():
            raise ValueError("Le contenu ne peut pas être vide")
        
        return self.note_repository.create(note_create)

    def update_note(self, note_id: int, note_update: NoteUpdate) -> Optional[Note]:
        """Mettre à jour une note"""
        # Vérifier que la note existe
        existing_note = self.note_repository.get_by_id(note_id)
        if not existing_note:
            return None
        
        # Validation métier
        if note_update.title is not None and not note_update.title.strip():
            raise ValueError("Le titre ne peut pas être vide")
        
        if note_update.content is not None and not note_update.content.strip():
            raise ValueError("Le contenu ne peut pas être vide")
        
        return self.note_repository.update(note_id, note_update)

    def delete_note(self, note_id: int) -> bool:
        """Supprimer une note"""
        return self.note_repository.delete(note_id)