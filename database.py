import sqlite3, bcrypt

def create_database():
    conn = sqlite3.connect("game.db")
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL,
        highscore INTEGER DEFAULT 0,
        max_level INTEGER DEFAULT 0
    );
    """)

    conn.commit()
    conn.close()

def register_user(username, password):
    conn = sqlite3.connect("game.db")
    cursor = conn.cursor()

    # Hash the password before storing it in the database
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    try:
        cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, hashed_password))
        conn.commit()
        user_id = cursor.lastrowid
    except sqlite3.IntegrityError:
        print("Username already exists.")
        conn.close()
        return False, None

    conn.close()
    return True, user_id

def login_user(username, password):
    conn = sqlite3.connect("game.db")
    cursor = conn.cursor()
    cursor.execute("SELECT id, password FROM users WHERE username=?", (username,))

    result = cursor.fetchone()
    conn.close()

    if result:
        user_id, hashed_password = result
        if bcrypt.checkpw(password.encode('utf-8'), hashed_password):
            return True, user_id
        else:
            return False, None
    else:
        return False, None

def update_user_highscore_and_level(user_id, highscore, max_level):
    conn = sqlite3.connect('game.db')
    c = conn.cursor()
    c.execute('''
        UPDATE users SET highscore = ?, max_level = ? WHERE id = ?;
    ''', (highscore, max_level, user_id))
    conn.commit()
    conn.close()

def get_user_highscore_and_level(user_id):
    conn = sqlite3.connect('game.db')
    c = conn.cursor()
    c.execute('SELECT highscore, max_level FROM users WHERE id = ?', (user_id,))
    result = c.fetchone()
    conn.close()
    if result:
        return result[0], result[1]
    return 0, 0
