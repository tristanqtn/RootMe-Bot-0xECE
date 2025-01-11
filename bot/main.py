import os
import discord  # type: ignore
import logging  # type: ignore

from dotenv import load_dotenv

from datetime import datetime
from discord.ext import tasks  # type: ignore
from discord.ext import commands  # type: ignore
from bot.requester import fetch_and_parse_users
from bot.controller import (
    add_user_to_fetch,
    remove_user_from_db,
    save_stats,
    get_all_user_data,
    init_db,
    get_leaderboard,
)

# Configure logging
logging.basicConfig(
    format="[%(asctime)s] [%(levelname)s] | %(message)s",
    level=logging.DEBUG,  # You can change this to INFO, WARNING, ERROR, etc.
)

load_dotenv()

TOKEN = os.getenv("DISCORD_TOKEN")
CHANNEL_ID = int(os.getenv("CHANNEL_ID"))
ENV = os.getenv("ENV")

intents = discord.Intents.default()
bot = commands.Bot(command_prefix="/", intents=intents)
intents.message_content = True
intents.typing = False
intents.presences = False


def translate_names(db_name):
    if db_name == "Mac-812606":
        return "Mac"
    elif db_name == "Onyx-852889":
        return "Onyx"
    elif db_name == "Xeroxx75":
        return "Xeroxx"
    else:
        return db_name


def inverse_translate_names(db_name):
    if db_name == "Mac":
        return "Mac-812606"
    elif db_name == "Onyx":
        return "Onyx-852889"
    elif db_name == "Xeroxx":
        return "Xeroxx75"
    else:
        return db_name



@bot.command(name="status")
async def status(ctx):
    await ctx.send(f"Je suis en ligne !\nJe tourne depuis l'env de {ENV}🚀")


@bot.command(name="commandes")
async def commandes(ctx):
    message = "```markdown\n"
    message += "🚀 BIENVENUE SUR LE BOT ROOT-ME 🚀\n"
    message += "Voici la liste des commandes disponibles :\n"
    message += "- /commandes : Affiche la liste des commandes disponibles\n"
    message += "- /status : Affiche le statut du bot\n"
    message += "- /leaderboard : Affiche le classement des joueurs de la team\n"
    message += "- /lastchallenge : Affiche les derniers challenges de la team\n"
    message += "```"
    await ctx.send(message)

@bot.command(name="add")
async def add_user(ctx, pseudo: str):
    """
    Ajoute un pseudo utilisateur à la base de données Root-Me.

    Args:
        ctx: Le contexte de la commande.
        pseudo (str): Le pseudo Root-Me de l'utilisateur.
    """
    # Validation basique du pseudo
    if not pseudo:
        await ctx.send("Veuillez fournir un pseudo valide.")
        return
    if not pseudo.isalnum() or len(pseudo) < 3:
        await ctx.send("Le pseudo fourni n'est pas valide. Assurez-vous qu'il est alphanumérique et contient au moins 3 caractères.")
        return

    # Traduction du pseudo si nécessaire
    db_pseudo = inverse_translate_names(pseudo)

    # Ajout à la base de données via la fonction add_user_to_fetch
    database_path = "users.db"  # Remplacez par le chemin réel de votre base
    try:
        result = add_user_to_fetch(database_path, db_pseudo)
        await ctx.send(result)  # Message renvoyé par la fonction add_user_to_fetch

        # Appel de la fonction refresh pour mettre à jour les données
        await ctx.send("Les données vont maintenant être mises à jour...")
        await refresh(ctx)  # Appelle la fonction refresh en passant le contexte
    except Exception as e:
        logging.error(f"Erreur lors de l'ajout du pseudo {pseudo} : {e}")
        await ctx.send("Une erreur interne s'est produite. Veuillez réessayer plus tard.")

@bot.command(name="remove")
async def remove_user(ctx, pseudo: str):
    """
    Supprime un utilisateur des tables user_data et rootme_users.

    Args:
        ctx: Le contexte de la commande.
        pseudo (str): Le pseudo Root-Me de l'utilisateur.
    """
    # Validation basique du pseudo
    if not pseudo:
        await ctx.send("Veuillez fournir un pseudo valide.")
        return

    # Suppression de l'utilisateur dans la base de données
    database_path = "users.db"
    stats_path = "rootme_data.db"
    result = remove_user_from_db(database_path,stats_path, pseudo)
    await ctx.send(result)


@bot.command(name="classement")
async def leaderboard(ctx):
    leaderboard = get_leaderboard()

    if not leaderboard:
        await ctx.send("Il n'y a pas de données dans la base.")
        return

    # Création du tableau formaté
    message = "```markdown\n"
    message += "🏆 LEADERBOARD DES JOUEURS 🏆\n"
    message += f"{'Pos':<4} {'Utilisateur':<20} {'Points':>6}\n"
    message += "-" * 64 + "\n"
    for i, user in enumerate(leaderboard, start=1):
        message += (
            f"{i:<4} {translate_names(user[0]):<20} {user[1]:>6}\n"
        )
    message += "```"

    # Envoi du message
    await ctx.send(message)


@bot.command(name="refresh")
async def refresh(ctx):
    await ctx.send(
        "Données en cours de mise à jour cela peut prendre quelques secondes..."
    )

    init_db()
    stats = await fetch_and_parse_users()
    save_stats(stats)
    all_data = get_all_user_data()

    if all_data:
        logging.info("The data has been updated")
        for row in all_data:
            logging.info(
                f"Username: {row[0]}, Place: {row[1]}, Points: {row[2]}, Challenges: {row[3]}, Compromissions: {row[4]}"
            )
        await ctx.send("Les données ont été mises à jour.")
    else:
        logging.info("Aucune donnée enregistrée dans la base.")


@bot.command(name="lastchallenge")
async def lastchallenge(ctx):
    # display all the last challenges of the team
    user_data = get_all_user_data()
    message = "```markdown\n"
    message += "🏆 DERNIERS CHALLENGES DE LA TEAM 🏆\n"
    message += f"{'Utilisateur':<20} {'Dernier challenge':<30}\n"
    message += "-" * 64 + "\n"
    for user in user_data:
        message += f"{translate_names(user[0]):<20} {user[5]:<30}\n"
    message += "```"

    # Envoi du message
    await ctx.send(message)


@tasks.loop(minutes=15)
async def periodic_task():
    init_db()
    stats = await fetch_and_parse_users()

    save_stats(stats)
    all_data = get_all_user_data()

    if all_data:
        logging.info("Data updated")
        for row in all_data:
            logging.info(
                f"Username: {row[0]}, Place: {row[1]}, Points: {row[2]}, Challenges: {row[3]}, Compromissions: {row[4]}, Last Challenge: {row[5]}"
            )
    else:
        logging.info("Aucune donnée enregistrée dans la base.")


@bot.event
async def on_ready():
    logging.info(f"{bot.user} is online!")

    periodic_task.start()

    # ID du channel où le bot doit envoyer le message
    channel_id = CHANNEL_ID  # Remplace par l'ID de ton channel
    channel = bot.get_channel(channel_id)

    logging.info(f"{bot.user} est connecté à {len(bot.guilds)} serveur(s) :")
    for guild in bot.guilds:
        logging.info(f"- {guild.name} (ID: {guild.id})")

    if channel:
        await channel.send("Yo, je suis la V2 🚀")
        await channel.send(f"Je tourne depuis l'env de {ENV}🚀\nPour voir la liste des commandes disponibles, tapez !commandes")
    else:
        logging.error("Channel introuvable !")



bot.run(TOKEN)
