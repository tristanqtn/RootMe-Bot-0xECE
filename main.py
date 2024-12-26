import discord
import sqlite3

from discord.ext import tasks
from discord.ext import commands

from requester import fetch_and_parse_users
from controller import save_stats, get_all_user_data, init_db, detect_point_change

TOKEN = "MTMyMTgzNDI4NzExNjMyMDgzOA.G0F6U7.mfTzYHAAjCuqKyaIHltNgHaCis5UoqxFldDrbw"

intents = discord.Intents.default()
bot = commands.Bot(command_prefix="!", intents=intents)
intents.message_content = True
intents.typing = False
intents.presences = False


# Connexion à la base de données
def get_leaderboard():
    conn = sqlite3.connect("rootme_data.db")
    cursor = conn.cursor()
    cursor.execute("SELECT username, points FROM user_data ORDER BY points DESC")
    leaderboard = cursor.fetchall()  # Récupère tous les utilisateurs triés par points
    conn.close()
    return leaderboard


# Fonction pour déterminer le commentaire à afficher
def get_commentary(points):
    if points < 1000:
        return "- encore vachement loin des 4000"
    elif points < 2000:
        return "- tu commences à t'approcher des 4000 !"
    elif points < 3000:
        return "- presque au top, encore un peu d'effort !"
    elif points < 4000:
        return "- ça y est, tu es dans la course !"
    else:
        return "- Top niveau ! 💪"


# Commande !leaderboard
@bot.command(name="leaderboard")
async def leaderboard(ctx):
    leaderboard = get_leaderboard()

    if not leaderboard:
        await ctx.send("Il n'y a pas de données dans la base.")
        return

    # Création du message à envoyer
    message = "🏆 **Leaderboard des utilisateurs** 🏆\n"
    message += "\n".join(
        [
            f"{i+1}. **{user[0]}** - {user[1]} points  {get_commentary(user[1]) if user[0] == 'Mac-812606' else ''}"
            for i, user in enumerate(leaderboard)
        ]
    )

    # Envoi du message
    await ctx.send(message)


@tasks.loop(minutes=10)  # Set to 30 minutes interval
async def periodic_task():
    await init_db()  # Initialize DB if necessary
    stats = await fetch_and_parse_users()  # Fetch and parse user data
    detect_point_change(stats)
    await save_stats(stats)  # Save fetched stats
    all_data = get_all_user_data()

    if all_data:
        print("Toutes les données enregistrées :")
        for row in all_data:
            print(
                f"Username: {row[0]}, Place: {row[1]}, Points: {row[2]}, Challenges: {row[3]}, Compromissions: {row[4]}"
            )
    else:
        print("Aucune donnée enregistrée dans la base.")


@bot.event
async def on_ready():
    print(f"{bot.user} is online!")

    periodic_task.start()

    # ID du channel où le bot doit envoyer le message
    channel_id = 1312171714272297065  # Remplace par l'ID de ton channel
    channel = bot.get_channel(channel_id)

    print(f"{bot.user} est connecté à {len(bot.guilds)} serveur(s) :")
    for guild in bot.guilds:
        print(f"- {guild.name} (ID: {guild.id})")

    if channel:
        await channel.send("Nathan pu du zob 🚀")
    else:
        print("Channel introuvable !")


bot.run(TOKEN)
