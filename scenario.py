# Fonction pour déterminer le commentaire à afficher
import random
from controller import get_leaderboard, calculate_points_needed

def get_commentary(points):
    if points < 1000:
        messages = [
            "- Sérieusement ? Tu rêves encore de 4000 points ? Réveille-toi...",
            "- T'es vraiment sûr que t'as bien compris le concept du jeu ?",
            "- Si tu continues à ce rythme, les 4000 points resteront un fantasme.",
            "- Peut-être qu'un jour tu atteindras les 1000 points, mais bon, faut pas rêver.",
            "- À ce rythme, c’est pas demain la veille que tu seras dans la course.",
            "- Va peut etre falloir rester dans le projet Centrale, les CTF c'est pas ça visiblement"
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


# Liste des templates de messages
TEMPLATES = [
    "💥 **{username}** frappe fort avec un gain de **{increment} points** grâce au challenge **{last_challenge}** ! 🚀",
    "🎯 **{username}** vient de marquer **{increment} points**. Le challenge **{last_challenge}** a été conquis avec style !",
    "🔥 Attention tout le monde ! **{username}** grimpe dans les classements avec un gain de **{increment} points** sur **{last_challenge}**.",
    "🏆 Bravo à **{username}** qui ajoute **{increment} points** à son compteur. Le challenge **{last_challenge}** n'a pas fait le poids !",
    "⚡ BOOM ! **{username}** fait exploser les scores avec un boost de **{increment} points** grâce à **{last_challenge}**.",
    "😱 Incroyable ! **{username}** vient de terminer **{last_challenge}** et empoche **{increment} points**. Qui pourra le rattraper ?",
    "😏 Pendant que certains dorment, **{username}** termine **{last_challenge}** et ajoute **{increment} points** à son score. 👏",
    "📈 **{username}** grimpe dans les classements avec **{increment} points** supplémentaires ! **{last_challenge}** maîtrisé comme un chef.",
    "🎉 **{username}**, toujours plus haut, ajoute **{increment} points** grâce à **{last_challenge}**. Une vraie légende !",
    "😂 Oops, les autres joueurs sont distancés par **{username}** qui vient de gagner **{increment} points** sur **{last_challenge}**. Trop facile !",
    "🤖 **{username}** semble être une machine à challenges. Encore **{increment} points** gagnés sur **{last_challenge}**. Respect !",
    "🎬 La performance de la journée revient à **{username}** qui ajoute **{increment} points** au compteur après avoir brisé **{last_challenge}**. 👏",
    "🎭 C'était dramatique, mais **{username}** l'a fait : **{increment} points** gagnés sur **{last_challenge}**. Les autres joueurs tremblent !",
    "🌟 Une étoile montante : **{username}** décroche **{increment} points** en terminant **{last_challenge}**. Quel talent !",
    "🔥 **{username}** n'a pas perdu de temps et a enchaîné **{increment} points** sur **{last_challenge}**. Un vrai maître !",
    "💡 Astuce du jour : **{username}** a débloqué **{increment} points** sur **{last_challenge}** en un clin d'œil. Imbattable !",
    "💪 **{username}** a pris de l'avance avec **{increment} points** sur **{last_challenge}**. À ce rythme, il ne va plus rien laisser à personne !",
    "🎮 **{username}** a montré qui est le boss avec **{increment} points** sur **{last_challenge}**. Bravo à lui !",
    "📊 **{username}** garde la tête haute avec **{increment} points** supplémentaires sur **{last_challenge}**. Le podium est dans sa ligne de mire !",
    "🥇 Félicitations à **{username}** qui remporte **{increment} points** sur **{last_challenge}**. Un champion !",
    "🌪️ **{username}** déchaîne tout avec **{increment} points** sur **{last_challenge}**. La tempête n'est pas près de s'arrêter !",
    "🎧 Pendant que les autres écoutent, **{username}** bosse et gagne **{increment} points** sur **{last_challenge}**. Un travailleur acharné !",
    "🧠 **{username}** fait preuve d'une intelligence redoutable avec **{increment} points** sur **{last_challenge}**. Genius !",
    "🔮 **{username}** a vu l'avenir et a sécurisé **{increment} points** sur **{last_challenge}**. Son ascension est inévitable !",
    "🌍 **{username}** s'impose mondialement avec **{increment} points** sur **{last_challenge}**. Qui pourra stopper sa progression ?",
    "🌈 **{username}** a trouvé le chemin de la victoire avec **{increment} points** sur **{last_challenge}**. C'est presque magique !",
    "🚀 **{username}** a fait décoller les scores avec **{increment} points** sur **{last_challenge}**. L'espace est sa prochaine destination !",
    "🧨 **{username}** a dynamité **{last_challenge}** et récupéré **{increment} points**. Pas de répit pour ses adversaires !",
    "💎 **{username}** brille comme une étoile avec **{increment} points** sur **{last_challenge}**. Chaque mouvement est un coup de maître !",
    "🔥 **{username}** a tout explosé avec **{increment} points** sur **{last_challenge}**. Un véritable raz-de-marée !",
    "💥 **{username}** fait vibrer la compétition avec **{increment} points** en plus ! Aucun défi ne lui résiste. 🚀",
    "🎯 **{username}** garde la visée parfaite et empoche **{increment} points** grâce à **{last_challenge}**. Tir sur cible !",
    "🎆 Une explosion de points pour **{username}** qui remporte **{increment} points** après avoir terminé **{last_challenge}**. 💥",
    "💬 **{username}** lâche une performance de ouf avec **{increment} points** sur **{last_challenge}**. Rien ne peut l'arrêter !",
    "🥳 Célébration en cours pour **{username}** avec **{increment} points** ! Il a brillamment dominé **{last_challenge}**.",
    "⚡ **{username}** s'impose avec **{increment} points** après avoir maîtrisé **{last_challenge}**. Un coup de maître !",
    "📊 **{username}** est en train de pulvériser tous les records avec **{increment} points** grâce à **{last_challenge}**. 🔥",
    "🎉 **{username}** grimpe comme un astronaute vers les étoiles avec **{increment} points**. **{last_challenge}** ? Facile !",
    "🎯 **{username}** n'a pas raté son tir et marque **{increment} points**. **{last_challenge}** est désormais une victoire !",
    "🎮 **{username}** est le champion du jour avec **{increment} points** sur **{last_challenge}**. Toujours plus fort !",
    "💣 **{username}** a fait sauter tous les obstacles avec **{increment} points** et remporte **{last_challenge}** haut la main !",
    "⏰ **{username}** prend de l'avance, remportant **{increment} points** sur **{last_challenge}**. Qui peut le rattraper ?",
    "🔥 **{username}** est en feu, il enchaîne les victoires avec **{increment} points** sur **{last_challenge}**. Incroyable !",
     "🚀 **{username}** vient de franchir la ligne d'arrivée avec **{increment} points** sur **{last_challenge}** ! Il a pris l'ascenseur pour le sommet. Qui peut le suivre ? 🤩",
    "🎉 **{username}** vient de pulvériser les attentes avec **{increment} points** grâce à **{last_challenge}**. Si c'était un film, ce serait un blockbuster à succès ! 🍿",
    "🌪️ Le vent souffle fort et il porte **{username}** jusqu'à **{increment} points** ! **{last_challenge}** ? C'est du gâteau pour lui. 🍰",
    "🔥 **{username}** ne fait pas dans la dentelle et sort **{increment} points** de son chapeau magique. Le challenge **{last_challenge}** ? Abandonné dans sa poussière ! 🎩✨",
    "🎲 **{username}** a joué sa chance et a remporté **{increment} points** sur **{last_challenge}** ! Quand la chance et le talent s'unissent, ça donne ça. 🍀🎰",
    "🕵️‍♂️ **{username}** a résolu le mystère du jour en encaissant **{increment} points** sur **{last_challenge}**. Sherlock n'a qu'à bien se tenir ! 🔍",
    "💥 Explosion de points pour **{username}** ! **{increment} points** remportés sur **{last_challenge}**. Plus rien ne l'arrête, il est sur orbite ! 🌌",
    "🥂 Santé à **{username}**, qui porte son score à **{increment} points** avec un gain monstrueux sur **{last_challenge}**. On dirait qu'il est déjà prêt pour la prochaine étape ! 🍸",
    "🛸 **{username}** vient de faire son entrée intergalactique avec **{increment} points** après avoir déchiffré **{last_challenge}**. Même les aliens veulent connaître son secret. 👽",
    "👑 **{username}** a enfilé sa couronne après avoir récupéré **{increment} points** sur **{last_challenge}**. Prêt pour régner sur le classement ! 🤴👸",
    "💡 **{username}** vient de faire un éclair de génie avec **{increment} points** sur **{last_challenge}**. Einstein aurait été jaloux ! ⚡",
    "🎢 Ça secoue ! **{username}** a fait un tour de montagnes russes et a pris **{increment} points** avec une maîtrise parfaite de **{last_challenge}**. 🎠",
    "⚔️ **{username}** a dégainé l'épée et tranché **{last_challenge}** en deux avec **{increment} points**. Ce chevalier n'a peur de rien ! 🏰",
    "💥 **{username}** a mis le turbo et a ajouté **{increment} points** à son total. **{last_challenge}** ? Simple formalité ! 🚗💨",
    "🏁 Le temps est écoulé et **{username}** a franchi la ligne avec **{increment} points** ! Un vrai champion qui enchaîne les victoires sans s'arrêter. 🏆",
    "🐉 **{username}** a dompté le dragon de **{last_challenge}** et s'en est sorti avec **{increment} points**. Un vrai héros légendaire ! 🏰",
    "⚡ **{username}** met le feu aux poudres avec **{increment} points** après avoir maîtrisé **{last_challenge}**. Une performance digne des meilleurs ! 🔥",
    "🧙‍♂️ **{username}** a jeté un sort magique pour s'emparer de **{increment} points** sur **{last_challenge}**. Qui osera l'affronter maintenant ? ✨",
    "⏳ **{username}** a fait le tour du chrono et a attrapé **{increment} points** dans la dernière seconde. La précision est son second prénom ! 🕰️",
    "🎉 **{username}** a lancé les confettis après avoir raflé **{increment} points** sur **{last_challenge}**. La fête est juste commencée ! 🥳",
    "⚡️ **{username}** électrise les classements avec **{increment} points** sur **{last_challenge}**. Un courant de génie traverse cette performance ! 🔋",
    "💎 **{username}** est comme un diamant : difficile à trouver, mais une fois découvert, il brille de mille feux avec **{increment} points** ! 💍",
    "🎯 Objectif atteint pour **{username}** qui a dégainé **{increment} points** avec précision sur **{last_challenge}**. Ça, c'est du tir parfait ! 🎯",
    "🌟 **{username}** a décroché les étoiles en ajoutant **{increment} points** à son score. Est-ce que ça commence à sentir la célébrité ? ⭐",
    "🥇 **{username}** est désormais sur la plus haute marche du podium avec **{increment} points**. Tout le monde est derrière lui à ce stade ! 🏆",
    "🚴‍♂️ **{username}** pédale à toute vitesse et gagne **{increment} points** sur **{last_challenge}**. S'il continue, il va battre tous les records ! ⏱️",
    "🔐 **{username}** a ouvert la porte du succès avec **{increment} points** sur **{last_challenge}**. Aucun code n'est assez compliqué pour lui ! 🗝️",
    "💨 **{username}** a pris la route la plus rapide pour ajouter **{increment} points** à son total. Qui peut le rattraper à ce rythme ? 🛣️",
    "🌈 **{username}** a créé un arc-en-ciel de **{increment} points** après avoir terminé **{last_challenge}**. Magique, non ? 🌟",
    "🍾 **{username}** vient de déboucher une bouteille de succès avec **{increment} points** après avoir brillamment résolu **{last_challenge}**. Champagne pour tout le monde ! 🥂"

]


TAUNTS_FOR_MAC = [
    "Ouch, <@688857965553516623>... on dirait que tu viens de prendre un bon coup dans la course au top 1. Peut-être qu'une pause serait utile... pour réfléchir à ta stratégie ? 😂",
    "<@688857965553516623>, pendant que tu regardes les autres briller, n'oublie pas que rêver, c'est gratuit. Mais rattraper le top 1 ? Pas avec tes stats actuelles. 😏",
    "Encore un challenge flaggé, et <@688857965553516623> s'éloigne de plus en plus. T'inquiète, il reste toujours la médaille du fair-play... si ça existe. 😅",
    "<@688857965553516623>, le top 1 t'envoie ses salutations. Enfin... si tu arrives à entendre depuis le bas du classement. 📉",
    "Félicitations à {winner_username}, mais prenons un moment pour penser à <@688857965553516623>, qui vient encore de perdre un peu plus de terrain. Courage, champion ! 🏅 (enfin, presque)",
    "Quand tu cours après le top 1 comme <@688857965553516623> mais que le top 1 prend l'avion. ✈️ Allez, accroche-toi, on croit (presque) en toi. 😂",
    "<@688857965553516623>, à ce rythme, le top 1 va te laisser un mot d'encouragement... depuis l'espace. 🪐",
    "<@688857965553516623>, tu vois ce chemin vers le top 1 ? Ouais, il est là... mais à 10 kilomètres de toi. Allez, tu peux encore rattraper ton retard… avec une fusée. 🚀",
    "T'as vu où est le top 1, <@688857965553516623> ? Si tu veux le rattraper, faudra peut-être songer à investir dans un jet privé. ✈️😂",
    "<@688857965553516623>, tes progrès sont si lents que le top 1 a eu le temps de se poser, faire un café, et revenir te dire bonjour. ☕📉",
    "C'est mignon de te voir essayer, <@688857965553516623>, mais à ce rythme, même une tortue te double. 🐢 #ObjectifTop1",
    "Salut <@688857965553516623>, je crois que tu viens de battre ton propre record... du plus long temps passé en dehors du top 1. 🏅📉",
    "Le top 1 t'a laissé un message : 'T'inquiète, on te garde une place tout en bas du classement. C'est là que les vrais champions s'entraînent !' 💪😂",
    "<@688857965553516623>, je crois qu'on devrait t'appeler 'Le spectateur officiel du top 1'. T'es là, mais trop loin pour participer. 🎬",
    "<@688857965553516623>, la bonne nouvelle ? Tu as officiellement battu ton record… d'être en retard sur la compétition. 😂🎯",
    "<@688857965553516623>, quand tu vois les autres franchir la ligne d'arrivée et toi tu viens à peine de la repérer. Peut-être une boussole serait utile ? 🧭",
    "<@688857965553516623>, le top 1 te laisse un peu d’avance… mais je pense qu’il se demande quand tu vas enfin arriver à sa hauteur. 🏁",
    "T’as un petit problème de vitesse, <@688857965553516623> ? Non, ne t’inquiète pas, le top 1 attendra. Enfin… pas trop longtemps. ⏳",
    "Si la compétition était une course de tortues, tu serais probablement en train de prendre la première place. 🐢",
    "<@688857965553516623>, à ce stade, on commence à se demander si tu cherches le top 1 ou si tu l’ignores volontairement. 😅",
    "Le top 1 t'attend, mais faut accélérer un peu… tu veux qu'on t'envoie un GPS ? 🗺️",
    "La prochaine fois, <@688857965553516623>, essaie peut-être d'utiliser un turbo. Parce que là, même les escargots ont pris de l'avance. 🐌💨",
    "En fait, <@688857965553516623>, tu devrais peut-être juste te concentrer sur le 'Top 10'. C’est plus réaliste, non ? 😉",
    "Oh <@688857965553516623>, t'as vu la place du top 1 ? C'est tout là-haut, tu sais… si tu veux, je peux t'expliquer comment y arriver. 😂",
    "Ne t'inquiète pas, <@688857965553516623>, on va t'envoyer une carte pour te montrer où se trouve le top 1. Spoiler : c’est pas à côté. 🗺️",
    "<@688857965553516623>, le top 1 va peut-être t’envoyer un trophée… pour ta persévérance à rester loin des premières places. 🏆",
    "Allez, courage <@688857965553516623>, on sait que tu t’es entraîné… mais là, il serait temps de commencer à jouer en mode ‘serieux’. 😆",
    "Ça va, <@688857965553516623> ? J’espère que tu as pris une bonne carte routière, parce que le top 1 ne t’attend pas. 🗺️📉",
    "C'est tellement triste de te voir jouer, <@688857965553516623>, qu'on dirait un documentaire sur la lente chute d'un champion. 🎬",
    "T'es sûr que tu ne confonds pas le top 1 avec ton lit, <@688857965553516623> ? Parce qu'à ce rythme, tu t’y rends plus vite. 🛏️",
    "Le top 1 commence à se demander si tu joues vraiment ou si tu fais une sieste sur le classement. 😴",
    "<@688857965553516623>, ton top 1 est aussi proche que mon compte en banque de gagner à la loterie. 😂💸",
    "Tu as déjà demandé à Siri où est le top 1 ? Peut-être qu'elle sait où il se cache. 📱",
    "Pas de panique <@688857965553516623>, on va t’envoyer une bouée de sauvetage. C’est dur d’être loin du top 1, non ? 🏖️",
    "Désolé, <@688857965553516623>, je crois que le top 1 est déjà passé... Mais t'inquiète, il te laisse une place à côté des trophées en papier. 🏆",
    "J'ai une idée, <@688857965553516623>, peut-être que si tu marches à reculons, tu arriveras plus vite vers le top 1. 🔄",
    "<@688857965553516623>, regarde le côté positif : au moins tu n’as pas à t’inquiéter de perdre ta place en haut du classement. 😜",
    "<@688857965553516623>, au lieu de courir après le top 1, pourquoi ne pas t'essayer à la marche ? C’est moins fatiguant. 🏃‍♂️",
    "Si t’as du mal à suivre le top 1, <@688857965553516623>, je crois qu’un cours de maths pourrait t’aider à comprendre où il est. ➗",
    "<@688857965553516623>, à ce rythme, tu seras officiellement un expert… en perte de place. 🥇",
    "Le top 1 est tellement loin que même Google Maps a abandonné en cherchant l’itinéraire. 📍",
    "<@688857965553516623>, à ce stade, je te conseille de commencer à développer une nouvelle stratégie : celle de ne pas perdre encore plus de terrain. 😅",
    "Je crois qu’on va t’appeler 'Le roi des places perdues'. 👑 Peut-être une place spéciale pour toi en bas du classement ?",
    "Oh <@688857965553516623>, même ton ombre est plus rapide que tes progrès dans cette compétition. 😂",
    "Si les classements étaient des courses de paresseux, tu serais déjà champion, <@688857965553516623>! 🦥",
    "<@688857965553516623>, à ce rythme, tu vas bientôt recevoir un certificat pour 'Participation Active au Fond du Classement'. 🎓",
    "Ouais, <@688857965553516623>, à force de regarder le top 1 de si loin, tu vas finir par avoir un torticolis. 👀",
    "T’es à ce point dans les bas fonds, <@688857965553516623>, que même un sous-marin te jalouse. 🌊",
    "<@688857965553516623>, si tu pouvais acheter un peu de vitesse, tu pourrais peut-être rattraper le top 1. Mais ça coûte cher, non ? 💸",
    "Tu sais, <@688857965553516623>, j’ai vu des escargots courir plus vite que toi dans cette compétition. 🐌💨",
    "<@688857965553516623>, t’es si loin du top 1 que même Google Maps t’a abandonné. 🗺️",
    "T'as plus de chances de rencontrer Bigfoot que de rattraper le top 1, <@688857965553516623>. 🦶",
    "C’est bizarre, <@688857965553516623>, je croyais que t'étais là pour jouer, pas pour faire office de décor. 🎭",
    "<@688857965553516623>, même un slow motion de film d’action semble plus rapide que ta progression. 🎬",
    "Tu sais ce qui serait encore plus impressionnant que tes stats, <@688857965553516623> ? Rien. 🤷‍♂️",
    "Si ta progression était une couleur, ce serait un gris déprimant. 🖤",
    "<@688857965553516623>, tu n'es même pas en train de courir après le top 1, tu fais de l'escapologie. 🤦‍♂️",
    "Le top 1 est si loin que je crois qu’il te fait une blague en te laissant dans la poussière. 😂💨",
    "Si tu continues comme ça, <@688857965553516623>, tu vas bientôt être derrière même les bots. 🤖",
    "<@688857965553516623>, le top 1 t'attend, mais c'est pas à la vitesse de ton Wi-Fi qu'il va te trouver. 🚶‍♂️",
    "Sérieusement, <@688857965553516623>, je crois que même un paresseux à un mètre par seconde irait plus vite que toi. 🦥⏳",
    "<@688857965553516623>, si tu continues à perdre du terrain, tu vas bientôt devenir une légende... mais dans la catégorie 'les plus lents'. 🏅",
    "Rien de plus divertissant que de te voir espérer atteindre le top 1, mais là, même ton optimisme est en fin de vie. 😂",
    "Si les stats étaient une compétition, tu serais champion du monde dans la catégorie 'le plus de distance entre moi et le top 1'. 🏆",
    "Hey <@688857965553516623>, à force de regarder les autres dans le rétroviseur, tu vas finir par les doubler… Ah non, désolé, c’est juste ton reflet. 😂",
    "Si le top 1 était un iceberg, tu serais le Titanic. Et non, tu n’as pas de chance de t'en sortir. 🚢❄️",
    "<@688857965553516623>, je commence à penser que tu fais exprès de rester aussi loin du top 1. Si c’est une tactique, c’est une mauvaise idée. 🤡",
    "Au rythme où tu vas, <@688857965553516623>, même un escargot en roller t’a déjà doublé. 🐌💨",
    "Tu veux qu'on t’envoie un GPS pour te guider vers le top 1, <@688857965553516623>? Parce que là, t’es perdu. 😂",
    "Même une tortue qui ferait une sieste t’aurait déjà devancé, <@688857965553516623>. 🐢💤",
    "Si tu cherches le top 1, <@688857965553516623>, il serait peut-être utile de sortir de ton rêve et d'ouvrir les yeux. 👀",
    "<@688857965553516623>, t'as sûrement perdu plus de terrain que ma connexion internet en mode 'réseau saturé'. 📶",
    "T’as pensé à une stratégie pour remonter, <@688857965553516623>? Parce que pour l’instant, t’es à fond dans la catégorie 'Aucune Ambition'. 🤷‍♂️",
    "<@688857965553516623>, franchement, même un fantôme pourrait te doubler tellement tu vas lentement. 👻",
    "Le top 1 t’envoie ses salutations… mais t’inquiète, il a déjà fait trois tours de circuit pendant que tu cherches encore ton chemin. 🏁",
    "À ce point, <@688857965553516623>, je pense que t’es plus un fan que vraiment un compétiteur. 📱🎮",
    "Oh <@688857965553516623>, tu sais ce qu’on dit : si tu restes trop longtemps derrière, tu finis par être oublié. Bienvenue dans l'oubli. 💀",

]





# Dictionnaire associant les usernames aux IDs Discord
DISCORD_USER_IDS = {
    "Mac-812606": 123456789012345678,  # Remplacez par l'ID réel de l'utilisateur
    "Drachh": 756178270830985286,     # Ajouter autant d'utilisateurs que nécessaire
    "Snaxx" : 445640456852865056,
    "NathanTmor" : 445640456852865056,
    "Kalith" : 441332639866028032,
    "Hioav2" : 261109633110900736,
    "RoiDechu" : 258989334537961472,
    "draune" : 905515340149194782,
    "AyWiZz" : 261164359269482498

    # Ajoutez d'autres mappings ici
}
def get_random_message(username, increment, last_challenge):
    """
    Sélectionne un message aléatoire parmi les templates et remplace les variables.
    Tag l'utilisateur sur Discord si son ID est connu.
    Ajoute un message de taunt pour Mac si quelqu'un avec plus de points flag un challenge.

    :param username: Nom de l'utilisateur
    :param increment: Points gagnés
    :param last_challenge: Dernier challenge réussi
    :return: Messages formatés à envoyer sur Discord
    """
    # Sélectionne un template pour le message principal
    template = random.choice(TEMPLATES)
    
    # Cherche l'ID Discord de l'utilisateur
    discord_id = DISCORD_USER_IDS.get(username)
    
    # Crée la mention pour l'utilisateur
    mention = f"<@{discord_id}>" if discord_id else username
    
    # Message principal
    primary_message = template.format(username=mention, increment=increment, last_challenge=last_challenge)
    
    leaderboard = get_leaderboard()

    # Recherche des points des deux utilisateurs
    mac_points = None
    user_points = None

    for username_leaderboard, points in leaderboard:
        if username_leaderboard == "Mac-812606":
            mac_points = points
        elif username_leaderboard == username:
            user_points = points


    # Si les points des deux utilisateurs sont trouvés
    if user_points is not None and mac_points is not None:
        # Calcul du nombre de points manquants pour chaque utilisateur
        points_needed_for_mac = calculate_points_needed(mac_points, user_points)
    
    # Si la personne n'est pas Mac et a plus de points que lui, ajoute un taunt
    taunt_message = None
    if username != "Mac-812606" and points_needed_for_mac > 0:
        taunt_template = random.choice(TAUNTS_FOR_MAC)
        taunt_message = taunt_template.format(winner_username=mention)
    
    # Retourne les messages (le taunt est optionnel)
    if taunt_message:
        # Retourne le message principal suivi du taunt sur une nouvelle ligne
        return f"{primary_message}\n{taunt_message}"
    else:
        return primary_message
