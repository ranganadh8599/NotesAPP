"""Note management routes for creating, reading, updating, and deleting notes."""

from fastapi import APIRouter, Depends

from models import NoteCreate, NoteUpdate, User
from services.note_service import NoteService
from dependencies import get_note_service, get_current_user


router = APIRouter(prefix="/notes", tags=["Notes"])


@router.post("/", summary="Create a new note")
async def create_note(
    note_data: NoteCreate,
    current_user: User = Depends(get_current_user),
    note_service: NoteService = Depends(get_note_service)
):
    """
    Create a new note for the authenticated user.
    
    - **note_title**: The title of the note
    - **note_content**: The content/body of the note
    """
    return note_service.create_note(note_data, current_user)


@router.get("/", summary="Get all notes for the current user")
async def get_notes(
    current_user: User = Depends(get_current_user),
    note_service: NoteService = Depends(get_note_service)
):
    """
    Retrieve all notes belonging to the authenticated user.
    
    Notes are returned in descending order by creation date.
    """
    return note_service.get_user_notes(current_user)


@router.get("/{note_id}", summary="Get a specific note by ID")
async def get_note(
    note_id: str,
    current_user: User = Depends(get_current_user),
    note_service: NoteService = Depends(get_note_service)
):
    """
    Retrieve a specific note by its ID.
    
    - **note_id**: The unique identifier of the note
    
    The user can only access notes they own.
    """
    return note_service.get_note_by_id(note_id, current_user)


@router.put("/{note_id}", summary="Update an existing note")
async def update_note(
    note_id: str,
    note_data: NoteUpdate,
    current_user: User = Depends(get_current_user),
    note_service: NoteService = Depends(get_note_service)
):
    """
    Update an existing note's title and/or content.
    
    - **note_id**: The unique identifier of the note
    - **note_title**: New title for the note (optional)
    - **note_content**: New content for the note (optional)
    
    The user can only update notes they own.
    """
    return note_service.update_note(note_id, note_data, current_user)


@router.delete("/{note_id}", summary="Delete a note")
async def delete_note(
    note_id: str,
    current_user: User = Depends(get_current_user),
    note_service: NoteService = Depends(get_note_service)
):
    """
    Delete a note by its ID.
    
    - **note_id**: The unique identifier of the note
    
    The user can only delete notes they own.
    """
    note_service.delete_note(note_id, current_user)
    return {"message": "Note deleted successfully"}