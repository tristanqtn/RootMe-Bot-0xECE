import asyncio
from parser import fetch_and_parse_users
from store_data import save_stats, get_all_user_data, init_db



# Run the async tasks
init_db()
stats = asyncio.run(fetch_and_parse_users())
save_stats(stats)
all_data = get_all_user_data()
if all_data:
    print("Toutes les données enregistrées :")
    for row in all_data:
        print(f"Username: {row[0]}, Place: {row[1]}, Points: {row[2]}, Challenges: {row[3]}, Compromissions: {row[4]}")
else:
    print("Aucune donnée enregistrée dans la base.")
