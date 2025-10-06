"""Database connection module with class-based approach for MySQL operations."""

import pymysql
from pymysql.cursors import DictCursor
from contextlib import contextmanager
import os
from dotenv import load_dotenv
from typing import Optional

load_dotenv()


class DatabaseManager:
    """
    Singleton Database Manager class for handling MySQL connections.
    Provides connection pooling and automatic resource management.
    """
    
    _instance: Optional['DatabaseManager'] = None
    
    def __new__(cls):
        """Ensure only one instance of DatabaseManager exists (Singleton pattern)."""
        if cls._instance is None:
            cls._instance = super(DatabaseManager, cls).__new__(cls)
            cls._instance._initialized = False
        return cls._instance
    
    def __init__(self):
        """Initialize database configuration."""
        if self._initialized:
            return
            
        self.config = {
            'host': os.getenv('DB_HOST', 'localhost'),
            'port': int(os.getenv('DB_PORT', 3306)),
            'user': os.getenv('DB_USER', 'root'),
            'password': os.getenv('DB_PASSWORD', ''),
            'database': os.getenv('DB_NAME', 'notes_db'),
            'charset': 'utf8mb4',
            'cursorclass': DictCursor
        }
        self._initialized = True
    
    @contextmanager
    def get_connection(self):
        """
        Context manager for database connections.
        Automatically handles connection, commit, rollback, and close operations.
        
        Usage:
            db = DatabaseManager()
            with db.get_connection() as conn:
                with conn.cursor() as cursor:
                    cursor.execute("SELECT * FROM users")
                    results = cursor.fetchall()
        """
        conn = None
        try:
            conn = pymysql.connect(**self.config)
            yield conn
            conn.commit()
        except Exception as e:
            if conn:
                conn.rollback()
            raise e
        finally:
            if conn:
                conn.close()
    
    def initialize_database(self):
        """Initialize the database and create necessary tables."""
        temp_config = self.config.copy()
        db_name = temp_config['database']
        print("db_name:", db_name)
        try:
            # Create database if it doesn't exist
            with pymysql.connect(**temp_config) as conn:
                with conn.cursor() as cursor:
                    cursor.execute(f"CREATE DATABASE IF NOT EXISTS {db_name}")
                    print(f"Database '{db_name}' is ready")
            
            # Create tables
            with self.get_connection() as conn:
                with conn.cursor() as cursor:
                    # Users table
                    cursor.execute("""
                        CREATE TABLE IF NOT EXISTS users (
                            user_id VARCHAR(36) PRIMARY KEY,
                            user_name VARCHAR(255) NOT NULL,
                            user_email VARCHAR(255) UNIQUE NOT NULL,
                            password_hash VARCHAR(255) NOT NULL,
                            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
                        )
                    """)
                    
                    # Notes table
                    cursor.execute("""
                        CREATE TABLE IF NOT EXISTS notes (
                            note_id VARCHAR(36) PRIMARY KEY,
                            user_id VARCHAR(36) NOT NULL,
                            note_title VARCHAR(255) NOT NULL,
                            note_content TEXT,
                            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
                            FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE,
                            INDEX idx_user_id (user_id)
                        )
                    """)
                    
                    print("Database tables created successfully")
                    
        except Exception as e:
            print(f"Database initialization error: {e}")
            raise
    
    def test_connection(self) -> bool:
        """Test the database connection."""
        try:
            with self.get_connection() as conn:
                with conn.cursor() as cursor:
                    cursor.execute("SELECT 1")
                    result = cursor.fetchone()
                    print("Database connection test: OK")
                    return True
        except Exception as e:
            print(f"Database connection test failed: {e}")
            return False
    
    def execute_query(self, query: str, params: tuple = None):
        """
        Execute a query and return results.
        
        Args:
            query: SQL query to execute
            params: Query parameters (optional)
            
        Returns:
            Query results
        """
        with self.get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(query, params)
                return cursor.fetchall()
    
    def execute_one(self, query: str, params: tuple = None):
        """
        Execute a query and return a single result.
        
        Args:
            query: SQL query to execute
            params: Query parameters (optional)
            
        Returns:
            Single query result
        """
        with self.get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(query, params)
                return cursor.fetchone()
