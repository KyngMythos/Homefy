#!/bin/bash

# GitHub-Repository-URL (ersetze <username> und <repository> mit deinem GitHub-Benutzernamen und Repository)
REPO_URL="https://github.com/KyngMythos/Homefy.git"

# Zielordner für das Projekt
HOMEFY_FOLDER="homefy"

# Schritt 1: Homefy-Ordner erstellen, falls nicht vorhanden
echo "Erstelle den Ordner $HOMEFY_FOLDER..."
mkdir -p $HOMEFY_FOLDER
cd $HOMEFY_FOLDER

# Schritt 2: Repository von GitHub klonen
echo "Klonen des Repositories von GitHub..."
git clone https://github.com/KyngMythos/Homefy

# Schritt 3: Abhängigkeiten installieren
echo "Installiere Abhängigkeiten..."
pip3 install -r requirements.txt

# Fertig
echo "Setup abgeschlossen!"
