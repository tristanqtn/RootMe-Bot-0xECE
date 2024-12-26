import requests
from bs4 import BeautifulSoup
import sqlite3

BASE_URL = "https://www.root-me.org"
USERNAME = "RoiDechu"

def init_db():
    conn = sqlite3.connect("rootme_data.db")
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS user_data (
        username TEXT PRIMARY KEY,
        place INTEGER,
        points INTEGER,
        challenges INTEGER,
        compromissions INTEGER
    )
    """)
    conn.commit()
    conn.close()

def get_user_info(username):
    url = f"{BASE_URL}/{username}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.text
    else:
        print(f"Failed to get user info for {username} (Status code: {response.status_code})")
        return None

def parse_user_data(html):
    soup = BeautifulSoup(html, 'html.parser')
    divs = soup.find_all("div", class_="small-6 medium-3 columns text-center")

    results = {}
    for div in divs:
        value = div.find("h3").get_text(strip=True).split("\u00a0")[-1]
        label = div.find("span", class_="gras").get_text(strip=True)
        results[label] = value

    return results

def save_user_data(username, results):
    conn = sqlite3.connect("rootme_data.db")
    cursor = conn.cursor()

    place = int(results["Place"])
    points = int(results["Points"])
    challenges = int(results["Challenges"])
    compromissions = int(results["Compromissions"])

    cursor.execute("""
    INSERT INTO user_data (username, place, points, challenges, compromissions)
    VALUES (?, ?, ?, ?, ?)
    ON CONFLICT(username) DO UPDATE SET
        place=excluded.place,
        points=excluded.points,
        challenges=excluded.challenges,
        compromissions=excluded.compromissions
    """, (username, place, points, challenges, compromissions))

    conn.commit()
    conn.close()

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

# Script principal
init_db()
data = get_user_info(USERNAME)

if data:
    results = parse_user_data(data)
    save_user_data(USERNAME, results)

    # Vérifier les données enregistrées
    user_data = get_user_data(USERNAME)
    if user_data:
        print(f"Données pour {USERNAME} : {user_data}")

    all_data = get_all_user_data()
    if all_data:
        print("Toutes les données enregistrées :")
        for row in all_data:
            print(f"Username: {row[0]}, Place: {row[1]}, Points: {row[2]}, Challenges: {row[3]}, Compromissions: {row[4]}")
    else:
        print("Aucune donnée enregistrée dans la base.")
