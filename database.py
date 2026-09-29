import sqlite3
from pathlib import Path
from datetime import datetime

DB_FILE = Path("financeflow.db")


def get_connection():
    conn = sqlite3.connect(DB_FILE, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn


def init_database():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            salt TEXT NOT NULL,
            role TEXT NOT NULL DEFAULT 'user',
            is_active INTEGER NOT NULL DEFAULT 1,
            budget REAL NOT NULL DEFAULT 100000,
            created_at TEXT NOT NULL
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS transactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            date TEXT NOT NULL,
            type TEXT NOT NULL,
            category TEXT NOT NULL,
            description TEXT,
            amount REAL NOT NULL,
            created_at TEXT NOT NULL,
            FOREIGN KEY(user_id) REFERENCES users(id)
        )
    """)

    conn.commit()
    conn.close()


# =========================================================
# USERS
# =========================================================

def create_user(name, email, password_hash, salt, role="user"):
    conn = get_connection()

    try:
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO users
            (name, email, password_hash, salt, role, is_active, budget, created_at)
            VALUES (?, ?, ?, ?, ?, 1, 100000, ?)
        """, (
            name,
            email.lower().strip(),
            password_hash,
            salt,
            role,
            datetime.now().isoformat()
        ))

        conn.commit()
        return cursor.lastrowid

    except sqlite3.IntegrityError:
        return None

    finally:
        conn.close()


def get_user_by_email(email):
    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM users WHERE email = ?",
        (email.lower().strip(),)
    )

    user = cursor.fetchone()

    conn.close()

    return dict(user) if user else None


def get_user_by_id(user_id):
    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM users WHERE id = ?",
        (user_id,)
    )

    user = cursor.fetchone()

    conn.close()

    return dict(user) if user else None


def get_all_users():
    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            id,
            name,
            email,
            role,
            is_active,
            budget,
            created_at
        FROM users
        ORDER BY id DESC
    """)

    users = [dict(row) for row in cursor.fetchall()]

    conn.close()

    return users


def update_user_status(user_id, status):
    conn = get_connection()

    conn.execute(
        "UPDATE users SET is_active = ? WHERE id = ?",
        (1 if status else 0, user_id)
    )

    conn.commit()
    conn.close()


def update_budget(user_id, budget):
    conn = get_connection()

    conn.execute(
        "UPDATE users SET budget = ? WHERE id = ?",
        (budget, user_id)
    )

    conn.commit()
    conn.close()


def count_users():
    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute(
        "SELECT COUNT(*) FROM users"
    )

    count = cursor.fetchone()[0]

    conn.close()

    return count


def count_active_users():
    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute(
        "SELECT COUNT(*) FROM users WHERE is_active = 1"
    )

    count = cursor.fetchone()[0]

    conn.close()

    return count


# =========================================================
# TRANSACTIONS
# =========================================================

def add_transaction(
    user_id,
    transaction_date,
    transaction_type,
    category,
    description,
    amount
):
    conn = get_connection()

    conn.execute("""
        INSERT INTO transactions
        (user_id, date, type, category, description, amount, created_at)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (
        user_id,
        transaction_date,
        transaction_type,
        category,
        description,
        amount,
        datetime.now().isoformat()
    ))

    conn.commit()
    conn.close()


def get_user_transactions(user_id):
    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            id,
            date,
            type,
            category,
            description,
            amount
        FROM transactions
        WHERE user_id = ?
        ORDER BY date DESC, id DESC
    """, (user_id,))

    transactions = [dict(row) for row in cursor.fetchall()]

    conn.close()

    return transactions


def delete_transaction(transaction_id, user_id):
    conn = get_connection()

    conn.execute("""
        DELETE FROM transactions
        WHERE id = ? AND user_id = ?
    """, (
        transaction_id,
        user_id
    ))

    conn.commit()
    conn.close()


def count_transactions():
    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute(
        "SELECT COUNT(*) FROM transactions"
    )

    count = cursor.fetchone()[0]

    conn.close()

    return count


def total_income():
    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute("""
        SELECT COALESCE(SUM(amount), 0)
        FROM transactions
        WHERE type = 'Income'
    """)

    value = cursor.fetchone()[0]

    conn.close()

    return value


def total_expenses():
    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute("""
        SELECT COALESCE(SUM(amount), 0)
        FROM transactions
        WHERE type = 'Expense'
    """)

    value = cursor.fetchone()[0]

    conn.close()

    return value


def get_all_transactions():
    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            transactions.id,
            transactions.date,
            transactions.type,
            transactions.category,
            transactions.description,
            transactions.amount,
            users.name,
            users.email
        FROM transactions
        JOIN users
        ON transactions.user_id = users.id
        ORDER BY transactions.date DESC
    """)

    transactions = [dict(row) for row in cursor.fetchall()]

    conn.close()

    return transactions