print("Importing librarys")
import os
import shutil
import yaml
import lyricsgenius
import eyed3
from pyrogram import Client, filters
print("successfully imported")

# Konfigurationsdatei laden
def load_config(config_file="config.yaml"):
    with open(config_file, "r") as file:
        return yaml.safe_load(file)

print("loading config")
config = load_config()
print("successfully loaded")
# API-Daten aus der Konfiguration
api_id = config["telegram"]["api_id"]
api_hash = config["telegram"]["api_hash"]

# Genius API-Token aus der Konfiguration
print("contacting Genius")
genius_api_token = config["genius"]["api_token"]
genius = lyricsgenius.Genius(genius_api_token)
print("Api Token Valid")

# Temporärer Ordner für Downloads (im selben Ordner wie das Skript)
download_folder = os.path.join("./temp")  # Temp-Ordner im Skript-Verzeichnis
os.makedirs(download_folder, exist_ok=True)  # Ordner erstellen, falls er nicht existiert

# Finaler Ordner aus der Konfiguration
final_folder = config["paths"]["final_folder"]
os.makedirs(final_folder, exist_ok=True)  # Ordner wird erstellt, falls er nicht existiert

# Erstelle den Pyrogram-Client
app = Client("my_account", api_id=api_id, api_hash=api_hash)

@app.on_message(filters.audio & filters.chat("@deezload2bot"))  # Filter für Mediendateien und Deezloadbot
def download_audio(client, message):
    if message.audio:
        # Verwende den Titel der Audiodatei als Dateinamen
        file_name = f"{message.audio.title}.mp3" if message.audio.title else "unknown_audio.mp3"
        
        # Vollständiger Pfad für den Download
        file_path = os.path.join(download_folder, file_name)

        # Lade die Datei herunter
        downloaded_file_path = message.download(file_name=file_path)

        # Überprüfe, ob die Datei existiert und keine .temp-Datei ist
        if os.path.exists(downloaded_file_path) and not downloaded_file_path.endswith(".temp"):
            print(f"Audio-Datei erfolgreich heruntergeladen: {downloaded_file_path}")

            # Holen der Lyrics von Genius (nur, wenn der Titel vorhanden ist)
            if message.audio.title:
                song = genius.search_song(message.audio.title)
                if song:
                    lyrics = song.lyrics
                    print(f"Lyrics gefunden: {lyrics[:100]}...")  # Nur einen Teil der Lyrics ausgeben

                    # MP3-Datei mit Lyrics versehen
                    add_lyrics_to_mp3(downloaded_file_path, lyrics)

                    # Verschiebe die Datei in den finalen Ordner
                    move_file(downloaded_file_path)
                else:
                    print(f"Keine Lyrics für {message.audio.title} gefunden.")
            else:
                print("Kein Titel für das Lied vorhanden, keine Lyrics hinzugefügt.")
        else:
            print("Fehler beim Herunterladen der Datei.")

def add_lyrics_to_mp3(file_path, lyrics):
    """
    Fügt die Lyrics als ID3-Tags zu einer MP3-Datei hinzu.
    """
    audio_file = eyed3.load(file_path)
    if audio_file and audio_file.tag:
        audio_file.tag.lyrics.set(lyrics)  # Lyrics hinzufügen
        audio_file.tag.save()
        print("Lyrics erfolgreich zu MP3 hinzugefügt.")
    else:
        print("Fehler: MP3-Datei konnte nicht geladen werden.")

def move_file(file_path):
    """
    Verschiebt die heruntergeladene MP3-Datei in einen anderen Ordner.
    """
    file_name = os.path.basename(file_path)
    new_path = os.path.join(final_folder, file_name)
    shutil.move(file_path, new_path)
    print(f"Datei verschoben: {new_path}")

app.run()