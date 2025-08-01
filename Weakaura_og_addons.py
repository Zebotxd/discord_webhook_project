import discord
import requests
import os

# The script will now read the webhook URL from the environment variable set in the GitHub Action.
WEBHOOK_URL = os.environ.get("DISCORD_WEBHOOK_URL")

# Make sure the URL exists before trying to send the message.
if not WEBHOOK_URL:
    print("Error: DISCORD_WEBHOOK_URL environment variable is not set.")
    exit(1)

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
# Tilføj et felt med en lang række af bindestreger.
# Dette felt vil være synligt, men det tvinger embed'et til at være bredere.
main_embed.add_field(name=" ", value="─" * 62, inline=False)
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
