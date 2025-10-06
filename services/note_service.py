"""Note service handling business logic for note operations."""

from datetime import datetime, timezone
from typing import List
from fastapi import HTTPException

from models import Note, NoteCreate, NoteUpdate, NoteResponse, User, generate_id
from repositories.note_repository import NoteRepository


class NoteService:
    """Service class handling note-related business logic."""
    
    def __init__(self, note_repository: NoteRepository):
        self.note_repository = note_repository
    
    def create_note(self, note_data: NoteCreate, current_user: User) -> NoteResponse:
        """Create a new note for the authenticated user."""
        now = datetime.now(timezone.utc)
        note = Note(
            note_id=generate_id(),
            user_id=current_user.user_id,
            note_title=note_data.note_title,
            note_content=note_data.note_content,
            created_on=now,
            last_update=now
        )
        
        self.note_repository.create(note)
        
        return self._convert_to_response(note)
    
    def get_user_notes(self, current_user: User) -> List[NoteResponse]:
        """Get all notes for the authenticated user."""
        notes = self.note_repository.get_by_user_id(current_user.user_id)
        return [self._convert_to_response(note) for note in notes]
    
    def get_note_by_id(self, note_id: str, current_user: User) -> NoteResponse:
        """Get a specific note by ID, ensuring user ownership."""
        note = self.note_repository.get_by_id(note_id)
        
        if not note:
            raise HTTPException(status_code=404, detail="Note not found")
        
        if not self._verify_note_ownership(note, current_user):
            raise HTTPException(
                status_code=403, 
                detail="Not authorized to access this note"
            )
        
        return self._convert_to_response(note)
    
    def update_note(self, note_id: str, note_data: NoteUpdate, current_user: User) -> NoteResponse:
        """Update an existing note, ensuring user ownership."""
        note = self.note_repository.get_by_id(note_id)
        
        if not note:
            raise HTTPException(status_code=404, detail="Note not found")
        
        if not self._verify_note_ownership(note, current_user):
            raise HTTPException(
                status_code=403, 
                detail="Not authorized to update this note"
            )
        
        # Update note fields if provided
        if note_data.note_title is not None:
            note.note_title = note_data.note_title
        if note_data.note_content is not None:
            note.note_content = note_data.note_content
        
        self.note_repository.update(note_id, note.note_title, note.note_content)
        
        # Get the updated note
        updated_note = self.note_repository.get_by_id(note_id)
        return self._convert_to_response(updated_note)
    
    def delete_note(self, note_id: str, current_user: User) -> None:
        """Delete a note, ensuring user ownership."""
        note = self.note_repository.get_by_id(note_id)
        
        if not note:
            raise HTTPException(status_code=404, detail="Note not found")
        
        if not self._verify_note_ownership(note, current_user):
            raise HTTPException(
                status_code=403, 
                detail="Not authorized to delete this note"
            )
        
        self.note_repository.delete(note_id)
    
    def _verify_note_ownership(self, note: Note, user: User) -> bool:
        """Verify that a note belongs to the given user."""
        return note.user_id == user.user_id
    
    def _convert_to_response(self, note: Note) -> NoteResponse:
        """Convert a Note model to NoteResponse."""
        return NoteResponse(
            note_id=note.note_id,
            note_title=note.note_title,
            note_content=note.note_content,
            user_id=note.user_id,
            created_on=note.created_on,
            last_update=note.last_update
        )