import json
import os
from typing import List, Optional
from datetime import datetime
from app.models.note import Note, NoteCreate, NoteUpdate

class NoteRepository:
    def __init__(self, file_path: str = "data/notes.json"):
        self.file_path = file_path
        self._ensure_data_directory()
        self._ensure_file_exists()

    def _ensure_data_directory(self):
        """Créer le répertoire data s'il n'existe pas"""
        data_dir = os.path.dirname(self.file_path)
        if data_dir and not os.path.exists(data_dir):
            os.makedirs(data_dir)

    def _ensure_file_exists(self):
        """Créer le fichier JSON s'il n'existe pas"""
        if not os.path.exists(self.file_path):
            self._save_notes([])

    def _load_notes(self) -> List[dict]:
        """Charger les notes depuis le fichier JSON"""
        try:
            with open(self.file_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return []

    def _save_notes(self, notes: List[dict]):
        """Sauvegarder les notes dans le fichier JSON"""
        with open(self.file_path, 'w', encoding='utf-8') as f:
            json.dump(notes, f, ensure_ascii=False, indent=2, default=str)

    def _get_next_id(self, notes: List[dict]) -> int:
        """Obtenir le prochain ID disponible"""
        if not notes:
            return 1
        return max(note['id'] for note in notes) + 1

    def get_all(self) -> List[Note]:
        """Récupérer toutes les notes"""
        notes_data = self._load_notes()
        return [Note(**note) for note in notes_data]

    def get_by_id(self, note_id: int) -> Optional[Note]:
        """Récupérer une note par son ID"""
        notes_data = self._load_notes()
        for note_data in notes_data:
            if note_data['id'] == note_id:
                return Note(**note_data)
        return None

    def create(self, note_create: NoteCreate) -> Note:
        """Créer une nouvelle note"""
        notes_data = self._load_notes()
        now = datetime.now()
        
        new_note_data = {
            "id": self._get_next_id(notes_data),
            "title": note_create.title,
            "content": note_create.content,
            "created_at": now.isoformat(),
            "updated_at": now.isoformat()
        }
        
        notes_data.append(new_note_data)
        self._save_notes(notes_data)
        
        return Note(**new_note_data)

    def update(self, note_id: int, note_update: NoteUpdate) -> Optional[Note]:
        """Mettre à jour une note"""
        notes_data = self._load_notes()
        
        for i, note_data in enumerate(notes_data):
            if note_data['id'] == note_id:
                # Mettre à jour seulement les champs fournis
                if note_update.title is not None:
                    note_data['title'] = note_update.title
                if note_update.content is not None:
                    note_data['content'] = note_update.content
                
                note_data['updated_at'] = datetime.now().isoformat()
                notes_data[i] = note_data
                
                self._save_notes(notes_data)
                return Note(**note_data)
        
        return None

    def delete(self, note_id: int) -> bool:
        """Supprimer une note"""
        notes_data = self._load_notes()
        
        for i, note_data in enumerate(notes_data):
            if note_data['id'] == note_id:
                notes_data.pop(i)
                self._save_notes(notes_data)
                return True
        
        return False