import os
import discord  # type: ignore

from dotenv import load_dotenv

from datetime import datetime
from discord.ext import tasks  # type: ignore
from discord.ext import commands  # type: ignore

from bot.scenario import get_commentary, get_random_message, DISCORD_USER_IDS
from bot.requester import fetch_and_parse_users
from bot.controller import (
    save_stats,
    get_all_user_data,
    init_db,
    detect_point_change,
    get_leaderboard,
    calculate_points_needed,
    get_user_data,
)

load_dotenv()

TOKEN = os.getenv("DISCORD_TOKEN")
CHANNEL_ID = int(os.getenv("CHANNEL_ID"))

intents = discord.Intents.default()
bot = commands.Bot(command_prefix="!", intents=intents)
intents.message_content = True
intents.typing = False
intents.presences = False

def translate_names(db_name):
    if db_name == "Mac-812606":
        return "Mac"
    elif db_name == "Onyx-852889":
        return "Onyx"
    else:
        return db_name


# Fonction pour envoyer un message privé à X lui rappelant son retard
async def send_reminder_to_user(user, target_user, points_needed):
    try:
        message = f"Désolé Erling, il te manque encore **{points_needed}** points pour rattraper **{target_user}**. N’abandonne pas… ou fais-le."
        target = await bot.fetch_user(
            user
        )  # On cherche l'utilisateur pour lui envoyer le message privé
        await target.send(message)  # Envoi du message
    except discord.DiscordException as e:
        print(f"Erreur lors de l'envoi du message à {user}: {e}")


# Fonction pour envoyer les rappels au démarrage du bot
async def send_race_reminders():
    # Définis ici les deux utilisateurs à comparer
    user1 = "Mac-812606"  # Utilisateur 1
    user2 = "Drachh"  # Utilisateur 2
    user3 = "Snaxx"

    discordUser1 = "688857965553516623"

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
    if (
        user1_points is not None
        and user2_points is not None
        and user3_points is not None
    ):
        # Calcul du nombre de points manquants pour chaque utilisateur
        points_needed_for_user1 = calculate_points_needed(user1_points, user2_points)
        points_needed_for_user1bis = calculate_points_needed(user1_points, user3_points)

        # Envoi des rappels si nécessaire
        if points_needed_for_user1 > 0:
            await send_reminder_to_user(discordUser1, user2, points_needed_for_user1)
        if points_needed_for_user1bis > 0:
            await send_reminder_to_user(discordUser1, user3, points_needed_for_user1bis)
        else:
            print(
                f"Erreur : Les utilisateurs {user1} ou {user2} ou {user3} n'ont pas été trouvés dans la base de données."
            )


@bot.command(name="commandes")
async def commandes(ctx):
    message = "```markdown\n"
    message += "🚀 BIENVENUE SUR LE BOT ROOT-ME 🚀\n"
    message += "Voici la liste des commandes disponibles :\n"
    message += "- !leaderboard : Affiche le classement des joueurs de la team\n"
    message += "- !stats : Affiche tes statistiques ROOT ME\n"
    message += "- !countdown : Affiche le nombre de jours avant le 1er avril 2025\n"
    message += "```"
    await ctx.send(message)


@bot.command(name="leaderboard")
async def leaderboard(ctx):
    leaderboard = get_leaderboard()

    if not leaderboard:
        await ctx.send("Il n'y a pas de données dans la base.")
        return

    # Création du tableau formaté
    message = "```markdown\n"
    message += "🏆 LEADERBOARD DES JOUEURS 🏆\n"
    message += f"{'Pos':<4} {'Utilisateur':<20} {'Points':>6} {'Commentaire':<30}\n"
    message += "-" * 64 + "\n"
    for i, user in enumerate(leaderboard, start=1):
        commentary = get_commentary(user[1]) if user[0] == "Mac-812606" else ""
        message += f"{i:<4} {translate_names(user[0]):<20} {user[1]:>6} {commentary:<30}\n"
    message += "```"

    # Envoi du message
    await ctx.send(message)


@bot.command(name="stats")
async def player_stats(ctx):
    # Retrieve user ID that ran the command
    user_id = ctx.author.id
    # Get the pseudo of the user that ran the command using DISCORD_USER_IDS
    user_pseudo = DISCORD_USER_IDS.get(str(user_id))
    stats = get_user_data(user_pseudo)

    if not stats:
        await ctx.send("Il n'y a pas de données dans la base.")
        return

    # Création du tableau formaté
    message = "```markdown\n"
    message += "🏆 STATS INDIVIDUELLES DU JOUEUR 🏆\n"
    if stats[0] == "Mac-812606" and stats[2] < 4000:
        message += "Gros pourri de merde, pas de 4000 pts : pas de stats !\n"
    else:
        message += f"Hey {translate_names(user_pseudo)}, tu es en train d'arracher ça, regarde-moi ces stats de fou :\n"
        message += f"{'Place':<12}: {stats[1]}/325710\n"
        message += f"{'Points':<12}: {stats[2]}\n"
        message += f"{'Challenges':<12}: {stats[3]}\n"
        message += f"{'Compromissions':<12}: {stats[4]}\n"
        message += f"{'Dernier challenge':<12}: {stats[5]}\n"
    message += "```"

    # Envoi du message
    await ctx.send(message)


@bot.command(name="refresh")
async def refresh(ctx):
    await ctx.send("Données en cours de mise à jour ...")
    await ctx.send(
        "Cela peut prendre quelques secondes, veuillez patienter (bot busy)..."
    )

    init_db()
    stats = await fetch_and_parse_users()
    point_change = detect_point_change(stats)

    if point_change:
        channel = bot.get_channel(CHANNEL_ID)
        if channel is not None:
            for user in point_change:
                # Générer un message aléatoire
                message = get_random_message(
                    username=user["Username"],
                    increment=user["Increment"],
                    last_challenge=user["Last Challenge"],
                )
                await channel.send(message)
        else:
            print(f"Channel with ID {CHANNEL_ID} not found.")
    save_stats(stats)
    all_data = get_all_user_data()

    if all_data:
        print("The data has been updated")
        for row in all_data:
            print(
                f"Username: {row[0]}, Place: {row[1]}, Points: {row[2]}, Challenges: {row[3]}, Compromissions: {row[4]}"
            )
        await ctx.send("Les données ont été mises à jour.")
    else:
        print("Aucune donnée enregistrée dans la base.")


@bot.command(name="countdown")
async def countdown(ctx):
    # Retrieve user ID that ran the command
    user_id = ctx.author.id
    # Get the pseudo of the user that ran the command using DISCORD_USER_IDS
    user_pseudo = DISCORD_USER_IDS.get(str(user_id))
    stats = get_user_data(user_pseudo)

    if not stats:
        await ctx.send("Il n'y a pas de données dans la base.")
        return

    # calcul le nombre de jours avant le 1 avril 2025
    date = datetime.now()
    date_1_avril_2025 = datetime(2025, 4, 1)
    delta = date_1_avril_2025 - date
    days = delta.days

    # Création du tableau formaté
    message = "```markdown\n"
    message += "COMPTE A REBOURS\n"
    if stats[0] == "Mac-812606":
        message += f"De toute façon, tu n'arriveras jamais à 4000 points mais bon si tu veux quand même savoir, il te reste : {days+1} jours pour y arriver\n"
    else:
        message += "Chill ya pas de compte à rebours pour toi, tu n'as pas de problèmes d'ego toi !\n"
        message += (
            f"Mais si tu veux savoir, il te reste : {days+1} jours avant le FIC2025\n"
        )

    message += "```"

    # Envoi du message
    await ctx.send(message)


@tasks.loop(minutes=5)
async def periodic_task():
    init_db()
    stats = await fetch_and_parse_users()
    point_change = detect_point_change(stats)

    if point_change:
        channel = bot.get_channel(CHANNEL_ID)
        if channel is not None:
            for user in point_change:
                # Générer un message aléatoire
                message = get_random_message(
                    username=(user["Username"]),
                    increment=user["Increment"],
                    last_challenge=user["Last Challenge"],
                )
                await channel.send(message)
        else:
            print(f"Channel with ID {CHANNEL_ID} not found.")

    save_stats(stats)
    all_data = get_all_user_data()

    if all_data:
        print("Data updated")
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
    channel_id = CHANNEL_ID  # Remplace par l'ID de ton channel
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
