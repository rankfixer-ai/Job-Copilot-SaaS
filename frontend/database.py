# database.py
import sqlite3
import pandas as pd
from datetime import datetime

class Database:
    def __init__(self):
        self.conn = sqlite3.connect('jobcopilot.db', check_same_thread=False)
        self.create_tables()
    
    def create_tables(self):
        # Users table
        self.conn.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                email TEXT UNIQUE,
                name TEXT,
                password_hash TEXT,
                created_at TIMESTAMP,
                subscription_plan TEXT DEFAULT 'free'
            )
        ''')
        
        # Saved jobs table
        self.conn.execute('''
            CREATE TABLE IF NOT EXISTS saved_jobs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                job_title TEXT,
                job_url TEXT,
                saved_at TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users (id)
            )
        ''')
        
        # Applications table
        self.conn.execute('''
            CREATE TABLE IF NOT EXISTS applications (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                job_title TEXT,
                company TEXT,
                applied_date TIMESTAMP,
                status TEXT,
                notes TEXT,
                FOREIGN KEY (user_id) REFERENCES users (id)
            )
        ''')
        
        self.conn.commit()
    
    def register_user(self, email, name, password_hash):
        try:
            cursor = self.conn.cursor()
            cursor.execute(
                "INSERT INTO users (email, name, password_hash, created_at, subscription_plan) VALUES (?, ?, ?, ?, ?)",
                (email, name, password_hash, datetime.now(), 'free')
            )
            self.conn.commit()
            return cursor.lastrowid
        except sqlite3.IntegrityError:
            return None
    
    def get_user(self, email):
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM users WHERE email = ?", (email,))
        return cursor.fetchone()
    
    def save_job(self, user_id, job_title, job_url):
        cursor = self.conn.cursor()
        cursor.execute(
            "INSERT INTO saved_jobs (user_id, job_title, job_url, saved_at) VALUES (?, ?, ?, ?)",
            (user_id, job_title, job_url, datetime.now())
        )
        self.conn.commit()
        return cursor.lastrowid
    
    def get_saved_jobs(self, user_id):
        return pd.read_sql("SELECT * FROM saved_jobs WHERE user_id = ? ORDER BY saved_at DESC", 
                          self.conn, params=(user_id,))
    
    def close(self):
        self.conn.close()

# Initialize database
db = Database()