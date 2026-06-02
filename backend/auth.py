from fastapi import APIRouter
from pydantic import BaseModel

import sqlite3
import os

router = APIRouter()

# ============================================
# DATABASE
# ============================================

BASE_DIR = os.path.dirname(
    os.path.abspath(__file__)
)

DB_PATH = os.path.join(
    BASE_DIR,
    "auth.db"
)

conn = sqlite3.connect(
    DB_PATH,
    check_same_thread=False
)

cursor = conn.cursor()

# ============================================
# CREATE TABLE
# ============================================

cursor.execute(
    """
    CREATE TABLE IF NOT EXISTS users (

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        username TEXT UNIQUE,

        email TEXT,

        password TEXT
    )
    """
)

conn.commit()

# ============================================
# MODELS
# ============================================

class SignupRequest(BaseModel):

    username: str
    email: str
    password: str


class LoginRequest(BaseModel):

    username: str
    password: str


# ============================================
# SIGNUP
# ============================================

@router.post("/signup")
def signup(data: SignupRequest):

    try:

        cursor.execute(

            """
            INSERT INTO users
            (username, email, password)

            VALUES (?, ?, ?)
            """,

            (
                data.username,
                data.email,
                data.password
            )
        )

        conn.commit()

        return {

            "status": "success",

            "message":
            "Account created successfully"
        }

    except Exception as e:

        print("SIGNUP ERROR:", str(e))

        return {

            "status": "error",

            "message":
            str(e)
        }


# ============================================
# LOGIN
# ============================================

@router.post("/login")
def login(data: LoginRequest):

    cursor.execute(

        """
        SELECT * FROM users

        WHERE username = ?
        AND password = ?
        """,

        (
            data.username,
            data.password
        )
    )

    user = cursor.fetchone()

    if not user:

        return {

            "status": "error",

            "message":
            "Invalid credentials"
        }

    return {

        "status": "success",

        "message":
        "Login successful"
    }