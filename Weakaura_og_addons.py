import discord
import requests
import os

# Scriptet læser nu webhook-URL'en fra den GitHub Action environment variable.
WEBHOOK_URL = os.environ.get("DISCORD_WEBHOOK_URL")

# Henter tokenet fra en environment variable.
WOWUP_TOKEN = os.environ.get("WOWUP_TOKEN")

if not WEBHOOK_URL:
    print("Error: DISCORD_WEBHOOK_URL environment variable is not set.")
    exit(1)

# Din thumbnail-URL (udskift dette med linket fra din Discord-kanal)
THUMBNAIL_URL = 'https://cdn.discordapp.com/attachments/1400838933960589422/1400840729085087855/Praktikanterne_logo.png?ex=688e1a18&is=688cc898&hm=eeb70914e72056e2bdf4a9f6b9e4f930f0dc6407f5d64bec51ebfd1c28bef66d&'

# Den opdaterede beskrivelsestekst, der indsætter tokenet.
description_text = f"""
**Addons:**
Method Raid Tools (MRT)
RC Loot Council
BigWigs eller Deadly Boss Mods (DBM)
WeakAuras (WA)
Simulationcraft
Liquid Auraupdater (Se guide nedenfor) 

**WeakAuras:**
Liquid (Hentes via AuraUpdater)
Kaze MRT Timers: https://wago.io/n7l5uN3YM

**Liquid AuraUpdater Guide**
1. Installer WowUp fra **https://wowup.io/**.
2. Åbn WowUp > Options > Addons og indsæt denne token: **{WOWUP_TOKEN}**.
3. Gå til Get Addons > Install from URL og indsæt URL'en: **https://github.com/bart-dev-wow/AuraUpdater**.
4. In-game, skriv **/AU** for at opdatere Liquid WeakAuras.
"""

# Create a single embed with a title, description, and author.
main_embed = discord.Embed(
    title='**Til raid forventer vi, at i har:**',
    description=description_text,
    color=discord.Color.purple()
)

main_embed.set_author(
    name="Weakaura & Addons",
    icon_url='https://cdn.discordapp.com/embed/avatars/0.png'
)

# --- Tilføj dette for at gøre embed'et bredere ---
# Dette er den mest pålidelige måde at styre bredden på.
main_embed.set_thumbnail(url=THUMBNAIL_URL)
# --- Slut på tilføjelsen ---

# Create a list to hold the single embed object.
embeds_list = [main_embed]

# Now, send the embeds to the webhook.
try:
    response = requests.post(
        WEBHOOK_URL,
        json={'embeds': [e.to_dict() for e in embeds_list]},
        headers={'Content-Type': 'application/json'}
    )
    response.raise_for_status()
    print("Successfully sent webhook message.")
except requests.exceptions.RequestException as e:
    print(f"Failed to send webhook message: {e}")
