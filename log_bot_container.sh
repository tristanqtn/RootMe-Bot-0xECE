#!/bin/bash

# Répertoire pour stocker les journaux
LOG_DIR="/var/log/docker_bot_logs"
BOT_CONTAINER_NAME="bot-annihilateur"
DATE=$(date +"%Y-%m-%d_%H-%M-%S")

# Créer le répertoire des journaux s'il n'existe pas
mkdir -p $LOG_DIR

# Lister les containers en cours d'exécution
docker ps > $LOG_DIR/running_containers_$DATE.log

# Vérifier si le container du bot est en cours d'exécution
if docker ps --filter "name=$BOT_CONTAINER_NAME" --format '{{.Names}}' | grep -q "^$BOT_CONTAINER_NAME$"; then
    # Si le container est actif, enregistrer ses logs
    docker logs $BOT_CONTAINER_NAME > $LOG_DIR/${BOT_CONTAINER_NAME}_logs_$DATE.log 2>&1
else
    # Sinon, enregistrer un message d'erreur
    echo "[$DATE] Le container '$BOT_CONTAINER_NAME' n'est pas en cours d'exécution." >> $LOG_DIR/error.log
fi

# Purger les journaux plus anciens que 14 jours
find $LOG_DIR -type f -mtime +14 -exec rm -f {} \;
