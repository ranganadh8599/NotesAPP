"""Note repository for database operations related to notes."""

from typing import List, Optional
from models import Note
from database import DatabaseManager


class NoteRepository:
    """Repository class handling note-related database operations."""
    
    def __init__(self):
        """Initialize repository with database manager."""
        self.db = DatabaseManager()
    
    def get_by_id(self, note_id: str) -> Optional[Note]:
        """Retrieve a note by its ID."""
        with self.db.get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(
                    """
                    SELECT note_id, user_id, note_title, note_content, 
                           created_at, updated_at 
                    FROM notes 
                    WHERE note_id = %s
                    """,
                    (note_id,)
                )
                result = cursor.fetchone()
                
                if result:
                    return Note(
                        note_id=result['note_id'],
                        user_id=result['user_id'],
                        note_title=result['note_title'],
                        note_content=result['note_content'],
                        created_on=result['created_at'],
                        last_update=result['updated_at']
                    )
        return None
    
    def get_by_user_id(self, user_id: str) -> List[Note]:
        """Retrieve all notes belonging to a specific user."""
        notes = []
        with self.db.get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(
                    """
                    SELECT note_id, user_id, note_title, note_content, 
                           created_at, updated_at 
                    FROM notes 
                    WHERE user_id = %s 
                    ORDER BY created_at DESC
                    """,
                    (user_id,)
                )
                results = cursor.fetchall()
                
                for result in results:
                    notes.append(Note(
                        note_id=result['note_id'],
                        user_id=result['user_id'],
                        note_title=result['note_title'],
                        note_content=result['note_content'],
                        created_on=result['created_at'],
                        last_update=result['updated_at']
                    ))
        return notes
    
    def create(self, note: Note) -> Note:
        """Create a new note in the database."""
        with self.db.get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(
                    """
                    INSERT INTO notes (note_id, user_id, note_title, note_content) 
                    VALUES (%s, %s, %s, %s)
                    """,
                    (note.note_id, note.user_id, note.note_title, note.note_content)
                )
        return note
    
    def update(self, note_id: str, title: str, content: str) -> None:
        """Update an existing note's title and content."""
        with self.db.get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(
                    """
                    UPDATE notes 
                    SET note_title = %s, note_content = %s 
                    WHERE note_id = %s
                    """,
                    (title, content, note_id)
                )
    
    def delete(self, note_id: str) -> None:
        """Delete a note from the database."""
        with self.db.get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute("DELETE FROM notes WHERE note_id = %s", (note_id,))
    
    def belongs_to_user(self, note_id: str, user_id: str) -> bool:
        """Check if a note belongs to a specific user."""
        note = self.get_by_id(note_id)
        return note is not None and note.user_id == user_id
