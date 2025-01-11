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

def add_user_to_fetch(database_path, pseudo):
    """
    Ajoute un pseudo dans la table rootme_users pour le fetch.

    :param database_path: Chemin vers la base de données SQLite.
    :param pseudo: Nom d'utilisateur Root-Me à ajouter.
    :return: Un message indiquant si l'ajout a été effectué ou si le pseudo existe déjà.
    """
    try:
        # Connexion à la base de données
        conn = sqlite3.connect(database_path)
        cursor = conn.cursor()

        # Vérifier si la table existe, sinon la créer
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS rootme_users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                pseudo TEXT UNIQUE NOT NULL
            )
        ''')

        # Vérifier si le pseudo existe déjà
        cursor.execute("SELECT pseudo FROM rootme_users WHERE pseudo = ?", (pseudo,))
        existing_user = cursor.fetchone()

        if existing_user:
            return f"Le pseudo '{pseudo}' existe déjà dans la base de données."

        # Insérer le nouveau pseudo
        cursor.execute("INSERT INTO rootme_users (pseudo) VALUES (?)", (pseudo,))
        conn.commit()

        return f"Le pseudo '{pseudo}' a été ajouté avec succès."

    except sqlite3.Error as e:
        return f"Erreur SQLite : {e}"

    finally:
        if conn:
            conn.close()


def remove_user_from_db(database_path: str, stats_path: str, username: str) -> str:
    """
    Supprime un utilisateur des bases de données des utilisateurs et des statistiques.

    Args:
        database_path (str): Chemin vers la base de données des utilisateurs.
        stats_path (str): Chemin vers la base de données des statistiques.
        username (str): Nom de l'utilisateur à supprimer.

    Returns:
        str: Message indiquant le résultat de l'opération.
    """
    import sqlite3

    try:
        # Connexion à la base de données des utilisateurs
        conn = sqlite3.connect(database_path)
        cursor = conn.cursor()

        # Suppression de l'utilisateur
        cursor.execute("DELETE FROM rootme_users WHERE pseudo = ?", (username,))
        users_deleted = cursor.rowcount
        cursor.execute("SELECT * FROM rootme_users")
        conn.commit()
        conn.close()

        # Connexion à la base de données des statistiques
        conn = sqlite3.connect(stats_path)
        cursor = conn.cursor()

        # Suppression des données de l'utilisateur
        cursor.execute("DELETE FROM user_data WHERE username = ?", (username,))
        stats_deleted = cursor.rowcount
        cursor.execute("SELECT * FROM user_data")
        conn.commit()
        conn.close()

        
        if users_deleted > 0 or stats_deleted > 0:
            return f"L'utilisateur '{username}' a été supprimé des bases de données. "   
        else:
            return f"L'utilisateur '{username}' n'a pas été trouvé dans les bases de données.'{users_deleted}' entrées ont été sup'{stats_deleted}' entrées ont été supprimées des statistiques."

    except Exception as e:
        return f"Une erreur s'est produite lors de la suppression de l'utilisateur : {e}"