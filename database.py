import sqlite3
import datetime
from typing import List, Dict

class Database:
    def __init__(self, db_name='meeting_scheduler.db'):
        self.db_name = db_name
        self.init_database()
    
    def init_database(self):
        """Initialize database with required tables"""
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        
        # Users table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                email TEXT UNIQUE NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Messages table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS messages (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                message TEXT NOT NULL,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users (id)
            )
        ''')
        
        # Meetings table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS meetings (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                date DATE NOT NULL,
                time TIME NOT NULL,
                participants TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Insert sample users and messages
        self.insert_sample_data(cursor)
        
        conn.commit()
        conn.close()
    
    def insert_sample_data(self, cursor):
        """Insert sample users and preloaded messages"""
        # Check if data already exists
        cursor.execute("SELECT COUNT(*) FROM users")
        if cursor.fetchone()[0] > 0:
            return
        
        # Sample users
        users = [
            ("Alice Johnson", "alice@email.com"),
            ("Bob Smith", "bob@email.com"),
            ("Carol Davis", "carol@email.com")
        ]
        
        cursor.executemany("INSERT INTO users (name, email) VALUES (?, ?)", users)
        
        # Sample messages with availability hints
        messages = [
            (1, "Hey everyone! Hope you're all doing well."),
            (2, "Hi Alice! Yes, all good here. How about you?"),
            (3, "Hello! I'm great, thanks for asking."),
            (1, "I was thinking we should have a team meeting soon to discuss the project."),
            (2, "That's a great idea! I'm available Monday to Wednesday next week."),
            (3, "Sounds good! I can do Tuesday or Wednesday afternoon."),
            (1, "I'm free on Tuesday and Wednesday as well. Tuesday afternoon works for me."),
            (2, "Perfect! Tuesday afternoon it is then."),
            (3, "Agreed! Let's schedule it.")
        ]
        
        cursor.executemany("INSERT INTO messages (user_id, message) VALUES (?, ?)", messages)
    
    def get_messages(self) -> List[Dict]:
        """Get all messages with user information"""
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT m.id, u.name, u.email, m.message, m.timestamp 
            FROM messages m 
            JOIN users u ON m.user_id = u.id 
            ORDER BY m.timestamp ASC
        ''')
        
        messages = []
        for row in cursor.fetchall():
            messages.append({
                'id': row[0],
                'user_name': row[1],
                'user_email': row[2],
                'message': row[3],
                'timestamp': row[4]
            })
        
        conn.close()
        return messages
    
    def add_message(self, user_name: str, user_email: str, message: str):
        """Add a new message"""
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        
        # Get or create user
        cursor.execute("SELECT id FROM users WHERE email = ?", (user_email,))
        user = cursor.fetchone()
        
        if not user:
            cursor.execute("INSERT INTO users (name, email) VALUES (?, ?)", (user_name, user_email))
            user_id = cursor.lastrowid
        else:
            user_id = user[0]
        
        # Add message
        cursor.execute("INSERT INTO messages (user_id, message) VALUES (?, ?)", (user_id, message))
        
        conn.commit()
        conn.close()
    
    def save_meeting(self, title: str, date: str, time: str, participants: List[str]):
        """Save meeting details"""
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        
        participants_str = ",".join(participants)
        cursor.execute(
            "INSERT INTO meetings (title, date, time, participants) VALUES (?, ?, ?, ?)",
            (title, date, time, participants_str)
        )
        
        conn.commit()
        conn.close()
    
    def get_users(self) -> List[Dict]:
        """Get all users"""
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        
        cursor.execute("SELECT name, email FROM users")
        users = [{'name': row[0], 'email': row[1]} for row in cursor.fetchall()]
        
        conn.close()
        return users
