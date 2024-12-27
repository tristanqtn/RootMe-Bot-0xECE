# Fonction pour déterminer le commentaire à afficher
import random
import discord
from discord.ext import commands
from controller import get_leaderboard, calculate_points_needed

def get_commentary(points):
    if points < 1000:
        messages = [
            "- Sérieusement ? Tu rêves encore de 4000 points ? Réveille-toi...",
            "- T'es vraiment sûr que t'as bien compris le concept du jeu ?",
            "- Si tu continues à ce rythme, les 4000 points resteront un fantasme.",
            "- Peut-être qu'un jour tu atteindras les 1000 points, mais bon, faut pas rêver.",
            "- À ce rythme, c’est pas demain la veille que tu seras dans la course."
        ]
    elif points < 1500:
        messages = [
            "- Ouf, t'as dépassé les 1000, bravo... mais tu es encore loin du sommet.",
            "- On dirait bien que tu viens de découvrir que le jeu existe.",
            "- T'es pas encore à la vitesse d'un escargot, mais c'est pas loin.",
            "- Tu te rapproches... mais t’es encore bien derrière.",
            "- Si tu fais un petit effort, tu finiras par faire partie de la course... un jour."
        ]
    elif points < 2000:
        messages = [
            "- Tu commences à atteindre la vitesse d'un escargot en manque d'énergie. Allez, encore un effort...",
            "- Ah, tu bouges ! Mais t’es toujours pas dans le top.",
            "- C’est bien, mais faudrait peut-être accélérer un peu si tu veux jouer dans la cour des grands.",
            "- T’es toujours là, mais tu n'es même pas encore à mi-chemin de 4000 points.",
            "- T'es sur la bonne voie, mais faut vraiment te bouger si tu veux rivaliser."
        ]
    elif points < 2500:
        messages = [
            "- Presque... Mais la barre des 4000 est encore à des années-lumière.",
            "- T'es plus proche, mais encore un peu trop lent pour les vrais champions.",
            "- T'as atteint un certain niveau, mais t’es encore trop loin des meilleurs.",
            "- Tu commences à comprendre, mais la route est encore longue.",
            "- Avec un peu de chance, tu finiras bien par rattraper les autres."
        ]
    elif points < 3000:
        messages = [
            "- Ah, tu n'es plus qu'à un petit effort. Peut-être que tu y arriveras si tu arrêtes de procrastiner.",
            "- Un peu plus de travail, et tu seras dans la course. Mais attention, ça chauffe derrière.",
            "- Presque là ! Mais est-ce que tu as ce qu'il faut pour franchir la ligne d’arrivée ?",
            "- L'effort commence à payer, mais faut pas lâcher maintenant !",
            "- Encore un petit coup de collier et tu peux prétendre à un vrai classement."
        ]
    elif points < 3500:
        messages = [
            "- C'est mieux, mais t'es encore trop faible pour rivaliser avec les vrais champions.",
            "- T'es dans la course, mais faut vraiment appuyer sur l'accélérateur.",
            "- Bien joué, mais ce n’est pas encore suffisant pour prétendre au podium.",
            "- C’est mieux, mais tu dois encore dépasser les autres. Ça va être difficile.",
            "- T'as fait du progrès, mais faudrait vraiment que tu te lèves pour aller chercher les 4000."
        ]
    elif points < 4000:
        messages = [
            "- Ça y est, tu commences à rentrer dans la course... mais il y a encore du pain sur la planche.",
            "- Bien joué, tu fais enfin honneur à la compétition, mais t’es encore trop loin des top joueurs.",
            "- T'es presque là, mais les autres sont déjà en train de te dépasser.",
            "- T’es au niveau, mais y’a encore de la marge pour les vrais champions.",
            "- Tu as bien progressé, mais faut te bouger encore un peu pour atteindre la ligne d’arrivée."
        ]
    else:
        messages = [
            "- Top niveau, mais on est presque sûr que tu triches. 💪",
            "- T'as atteint le sommet... mais c’est sûrement grâce à des raccourcis, non ?",
            "- Bravo, t'es au top... mais je parie que tu as payé un service pour y arriver.",
            "- T'es un champion, mais on sait tous que tu triches.",
            "- Félicitations, t'es un modèle... mais pour les autres à ne pas suivre."
        ]
    
    # Retourne un message choisi aléatoirement parmi ceux de la tranche
    return random.choice(messages)

# Fonction pour envoyer un message privé à X lui rappelant son retard
async def send_reminder_to_user(user, target_user, points_needed):
    try:
        message = f"Désolé **{user}**, il te manque encore **{points_needed}** points pour rattraper **{target_user}**. N’abandonne pas… ou fais-le."
        target = await bot.fetch_user(user)  # On cherche l'utilisateur pour lui envoyer le message privé
        await target.send(message)  # Envoi du message
    except discord.DiscordException as e:
        print(f"Erreur lors de l'envoi du message à {user}: {e}")

# Fonction pour envoyer les rappels au démarrage du bot
async def send_race_reminders():
    # Définis ici les deux utilisateurs à comparer
    user1 = "Mac-812606"  # Utilisateur 1
    user2 = "Drachh"     # Utilisateur 2

    discordUser1 = "drachh_"
    
    leaderboard = get_leaderboard()

    # Recherche des points des deux utilisateurs
    user1_points = None
    user2_points = None

    for username, points in leaderboard:
        if username == user1:
            user1_points = points
        elif username == user2:
            user2_points = points

    # Si les points des deux utilisateurs sont trouvés
    if user1_points is not None and user2_points is not None:
        # Calcul du nombre de points manquants pour chaque utilisateur
        points_needed_for_user1 = calculate_points_needed(user1_points, user2_points)

        # Envoi des rappels si nécessaire
        if points_needed_for_user1 > 0:
            await send_reminder_to_user(discordUser1, user2, points_needed_for_user1)

    else:
        print(f"Erreur : Les utilisateurs {user1} ou {user2} n'ont pas été trouvés dans la base de données.")