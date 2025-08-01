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
**Addons:**
Method Raid Tools (MRT)
RC Loot Council
BigWigs eller Deadly Boss Mods (DBM)
WeakAuras (WA)
Simulationcraft
Liquid Auraupdater (Se guide nedenfor) 


**WeakAuras:**
Liquid Liberation of Undermine: https://wago.io/LiquidUndermine                                   
Liquid Weak Auras: https://wago.io/LiquidWeakAuras
Liquid Raid Anchors: https://wago.io/LiquidAnchors
Kaze MRT Timers: https://wago.io/n7l5uN3YM
Interrupt Anchor: https://wago.io/InterruptAnchor
"""

# Create a single embed with a title, description, and author.
main_embed = discord.Embed(
    title='**Til raid forventer vi, at i har:**',
    description=description_text,
    color=discord.Color.blue()
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
