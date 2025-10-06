"""User repository for database operations related to users."""

from typing import Optional
from models import User
from database import DatabaseManager


class UserRepository:
    """Repository class handling user-related database operations."""
    
    def __init__(self):
        """Initialize repository with database manager."""
        self.db = DatabaseManager()
    
    def get_by_email(self, email: str) -> Optional[User]:
        """Retrieve a user by their email address."""
        with self.db.get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(
                    """
                    SELECT user_id, user_name, user_email, password_hash, 
                           created_at, updated_at 
                    FROM users 
                    WHERE user_email = %s
                    """,
                    (email,)
                )
                result = cursor.fetchone()
                
                if result:
                    return User(
                        user_id=result['user_id'],
                        user_name=result['user_name'],
                        user_email=result['user_email'],
                        password=result['password_hash'],
                        created_on=result['created_at'],
                        last_update=result['updated_at']
                    )
        return None
    
    def create(self, user: User) -> User:
        """Create a new user in the database."""
        with self.db.get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(
                    """
                    INSERT INTO users (user_id, user_name, user_email, password_hash) 
                    VALUES (%s, %s, %s, %s)
                    """,
                    (user.user_id, user.user_name, user.user_email, user.password)
                )
        return user
    
    def exists_by_email(self, email: str) -> bool:
        """Check if a user with the given email already exists."""
        user = self.get_by_email(email)
        return user is not None
