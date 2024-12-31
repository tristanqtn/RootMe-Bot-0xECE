import sqlite3

def reduce_points(username, points_to_deduct):
    """
    Réduit les points d'un utilisateur spécifique dans la base de données SQLite.

    :param username: Nom de l'utilisateur (str)
    :param points_to_deduct: Nombre de points à déduire (int)
    """
    # Connexion à la base de données SQLite
    conn = sqlite3.connect("rootme_data.db")  # Remplacez par le chemin de votre base de données SQLite
    cursor = conn.cursor()

    # Vérifie si l'utilisateur existe
    cursor.execute("SELECT points FROM user_data WHERE username = ?", (username,))
    user = cursor.fetchone()
    
    if not user:
        print(f"Utilisateur '{username}' non trouvé.")
        conn.close()
        return

    # Récupère les points actuels
    current_points = user[0]
    new_points = max(current_points - points_to_deduct, 0)  # Ne pas descendre en dessous de 0

    # Met à jour les points dans la base de données
    cursor.execute("UPDATE user_data SET points = ? WHERE username = ?", (new_points, username))
    conn.commit()

    print(f"Points de '{username}' mis à jour : {new_points} points restants.")

    # Fermeture de la connexion
    conn.close()

# Exemple d'utilisation
reduce_points("Snaxx", 10)
reduce_points("NathanTmor", 10)
reduce_points("Kalith", 10)
reduce_points("Hioav2", 10)
reduce_points("Drachh", 10)
reduce_points("RoiDechu", 10)