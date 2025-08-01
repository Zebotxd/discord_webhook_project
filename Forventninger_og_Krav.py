import discord
import requests
import os

# The script will now read the webhook URL from the environment variable set in the GitHub Action.
WEBHOOK_URL = os.environ.get("DISCORD_WEBHOOK_URL")

# Make sure the URL exists before trying to send the message.
if not WEBHOOK_URL:
    print("Error: DISCORD_WEBHOOK_URL environment variable is not set.")
    exit(1)

# Din thumbnail-URL (udskift dette med linket fra din Discord-kanal)
THUMBNAIL_URL = 'https://cdn.discordapp.com/attachments/1400838933960589422/1400840729085087855/Praktikanterne_logo.png?ex=688e1a18&is=688cc898&hm=eeb70914e72056e2bdf4a9f6b9e4f930f0dc6407f5d64bec51ebfd1c28bef66d&'

description_text = """
**Raidtider og Mål**
Vi raider onsdag og søndag fra 20:00-22:30. De første tre uger raider vi også tirsdag. Vores mål er Cutting Edge (CE). Invites kl. 19:45, og vi puller kl. 20:00. Tilmeld dig raids senest 24 timer før.

**Krav til Raids**
**Ugentlige Keys:** 2k rating i uge 1. Derefter 4x +10 keys om ugen. Manglende opfyldelse giver nedprioritering på loot og roster.

**Forberedelse:** Du skal kende din class og have læst op på boss-mekanikker,  Tjek altid specifikke krav for bosser i de dedikerede tekstkanaler.

**Gear:** Sørg for at have de korrekte crafted items, enchants og gems.

**Consumables:** Medbring selv oils. Guilden står for feasts og cauldrons, men hav en backup i dine tasker.

**Addons:** Installer de nødvendige WeakAuras og addons.

**BOEs:** Trades til guildbanken via <@173786599140622336>. De kan købes til 30% af AH-markedsprisen, hvis det er en stor opgradering.
"""

# Create a single embed with a title, description, and author.
main_embed = discord.Embed(
    title='**THE WAR WITIHIN SEASON 3**',
    description=description_text,
    color=discord.Color.red()
)

main_embed.set_author(
    name="Vores forventninger og krav til raidet og til jer",
    icon_url='https://wow.zamimg.com/images/wow/icons/large/inv_misc_book_09.jpg'
)

# Tilføj dette for at gøre embed'et bredere
main_embed.set_thumbnail(url=THUMBNAIL_URL)

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
