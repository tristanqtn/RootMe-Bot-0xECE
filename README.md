# Bot Discord : Ultimate Root Me Bot

Ce projet est un bot Discord conçu pour suivre et notifier les événements liés aux scores des joueurs sur Root Me. Le bot tourne dans une structure Docker Compose et nécessite Python 3.12 et Poetry pour fonctionner.

---

## Fonctionnalités

### Commandes disponibles

- **!leaderboard** : Affiche le classement des joueurs de l'équipe.
- **!stats** : Affiche tes statistiques personnelles sur Root Me.
- **!countdown** : Affiche le nombre de jours avant le 1er avril 2025.

### Surveillance des points Root Me

- Le bot détecte automatiquement toutes les variations de points des joueurs enregistrés.
- Il envoie une notification sur le canal dès qu'un challenge est résolu.
- Les statistiques des joueurs sont mises à jour toutes les 5 minutes.

---

## Architecture des fichiers

- **/bot/main.py** : Contient le comportement principal du bot.
- **/bot/controller.py** : Gère les interactions avec la base de données SQLite3.
- **/bot/requester.py** : Responsable de la collecte des informations des joueurs et du parsing des données.
- **/bot/scenarios.py** : Contient les messages prédéfinis du bot.
- **/bot/reduce.py** : Fichier indépendant permettant de réduire les points des joueurs dans la base pour tester et déclencher les alertes.

---

## Installation et exécution

### Prérequis

- **Python 3.12**
- **Poetry** : Gestionnaire de dépendances Python
- **Docker** et **Docker Compose** (optionnel pour une exécution containerisée)

Assurez-vous de configurer Docker pour que le deamon démarré automatiquement au démarrage de votre machine.

```bash
sudo systemctl enable docker
sudo systemctl start docker
```

### Lancer le bot localement

Depuis la racine du projet (`/UltimateRootmeAPI`), exécutez les commandes suivantes :

```bash
poetry shell
poetry install
poetry run python -m bot.main
```

### Lancer le bot avec Docker

#### Créer une image Docker

```bash
docker build -t bot .
```

#### Exécuter le container Docker

```bash
docker run -it bot
```

### Lancer le bot avec Docker Compose

```bash
docker compose up
```

---

## Script de récurération des logs

Voici un script bash simple qui peut être utilisé avec une tâche cron pour lister les containers en cours d'exécution et enregistrer les journaux du container du bot dans un fichier.

[log_bot_container.sh](log_bot_container.sh)

### Étapes pour configurer la tâche cron

1. **Rendre le script exécutable** :

   ```bash
   chmod +x log_bot_container.sh
   ```

2. **Déplacer le script dans un emplacement accessible (par exemple `/usr/local/bin/`)** :

   ```bash
   sudo mv log_bot_container.sh /usr/local/bin/
   ```

3. **Configurer la tâche cron** :
   Ouvrez le crontab de l'utilisateur :

   ```bash
   crontab -e
   ```

   Ajoutez une ligne pour exécuter le script toutes les 10 minutes (ou une autre fréquence souhaitée) :

   ```bash
   0 * * * * /usr/local/bin/log_bot_container.sh
   ```

---

### Résultats

- Les journaux des containers en cours d'exécution seront enregistrés dans `/var/log/docker_bot_logs/`.
- Les journaux spécifiques au container `bot-annihilateur` seront séparés avec des horodatages pour faciliter leur suivi.
- Si le container du bot n'est pas actif, un message d'erreur sera ajouté à `error.log`.

N'hésitez pas à adapter les chemins ou les noms des fichiers selon vos besoins.
