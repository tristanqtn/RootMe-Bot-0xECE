import discord
import sqlite3


from discord.ext import tasks
from discord.ext import commands

from scenario import get_commentary, calculate_points_needed
from requester import fetch_and_parse_users
from controller import save_stats, get_all_user_data, init_db, detect_point_change, get_leaderboard 

TOKEN = "MTMyMTgzNDI4NzExNjMyMDgzOA.G0F6U7.mfTzYHAAjCuqKyaIHltNgHaCis5UoqxFldDrbw"

intents = discord.Intents.default()
bot = commands.Bot(command_prefix="!", intents=intents)
intents.message_content = True
intents.typing = False
intents.presences = False

# Fonction pour envoyer un message privé à X lui rappelant son retard
async def send_reminder_to_user(user, target_user, points_needed):
    try:
        message = f"Désolé Erling, il te manque encore **{points_needed}** points pour rattraper **{target_user}**. N’abandonne pas… ou fais-le."
        target = await bot.fetch_user(user)  # On cherche l'utilisateur pour lui envoyer le message privé
        await target.send(message)  # Envoi du message
    except discord.DiscordException as e:
        print(f"Erreur lors de l'envoi du message à {user}: {e}")

# Fonction pour envoyer les rappels au démarrage du bot
async def send_race_reminders():
    # Définis ici les deux utilisateurs à comparer
    user1 = "Mac-812606"  # Utilisateur 1
    user2 = "Drachh"     # Utilisateur 2
    user3 = "Snaxx"

    discordUser1 = "756178270830985286"
    
    leaderboard = get_leaderboard()

    # Recherche des points des deux utilisateurs
    user1_points = None
    user2_points = None

    for username, points in leaderboard:
        if username == user1:
            user1_points = points
        elif username == user2:
            user2_points = points
        elif username == user3:
            user3_points = points

    # Si les points des deux utilisateurs sont trouvés
    if user1_points is not None and user2_points is not None and user3_points is not None:
        # Calcul du nombre de points manquants pour chaque utilisateur
        points_needed_for_user1 = calculate_points_needed(user1_points, user2_points)
        points_needed_for_user1bis = calculate_points_needed(user1_points, user3_points)

        # Envoi des rappels si nécessaire
        if points_needed_for_user1 > 0:
            await send_reminder_to_user(discordUser1, user2, points_needed_for_user1)
        if points_needed_for_user1bis > 0:
            await send_reminder_to_user(discordUser1, user3, points_needed_for_user1bis)
        else:
            print(f"Erreur : Les utilisateurs {user1} ou {user2} ou {user3} n'ont pas été trouvés dans la base de données.")


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
    init_db()  # Initialize DB if necessary
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

    await send_race_reminders()


bot.run(TOKEN)
