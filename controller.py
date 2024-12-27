import sqlite3


def init_db():
    conn = sqlite3.connect("rootme_data.db")
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS user_data (
        username TEXT PRIMARY KEY,
        place INTEGER,
        points INTEGER,
        challenges INTEGER,
        compromissions INTEGER,
        last_challenge TEXT
    )
    """)
    conn.commit()
    conn.close()


def save_stats(stats):
    conn = sqlite3.connect("rootme_data.db")
    cursor = conn.cursor()

    for user in stats:
        username = user["Username"]
        place = int(user["Place"])
        points = int(user["Points"])
        challenges = int(user["Challenges"])
        compromissions = int(user["Compromissions"])
        last_challenge = user["Last Challenge"]

        cursor.execute(
            """
        INSERT INTO user_data (username, place, points, challenges, compromissions, last_challenge)
        VALUES (?, ?, ?, ?, ?, ?)
        ON CONFLICT(username) DO UPDATE SET
            place=excluded.place,
            points=excluded.points,
            challenges=excluded.challenges,
            compromissions=excluded.compromissions,
            last_challenge=excluded.last_challenge
        """,
            (username, place, points, challenges, compromissions, last_challenge),
        )

    conn.commit()
    conn.close()


# Connexion à la base de données
def get_leaderboard():
    conn = sqlite3.connect("rootme_data.db")
    cursor = conn.cursor()
    cursor.execute("SELECT username, points FROM user_data ORDER BY points DESC")
    leaderboard = cursor.fetchall()  # Récupère tous les utilisateurs triés par points
    conn.close()
    return leaderboard


def calculate_points_needed(x_points, y_points):
    return max(
        0, y_points - x_points
    )  # Si X est déjà devant Y, il ne manque aucun point


def get_user_data(username):
    conn = sqlite3.connect("rootme_data.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM user_data WHERE username = ?", (username,))
    user_data = cursor.fetchone()
    conn.close()
    return user_data


def get_all_user_data():
    conn = sqlite3.connect("rootme_data.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM user_data")
    all_data = cursor.fetchall()  # Récupère toutes les lignes de la table
    conn.close()
    return all_data


def detect_point_change(new_data):
    user_that_changed = []
    for user in new_data:
        old_data = get_user_data(user["Username"])
        if old_data is None:
            break
        if int(user["Points"]) != int(old_data[2]):
            user["Increment"] = int(user["Points"]) - int(old_data[2])
            user_that_changed.append(user)
    return user_that_changed


