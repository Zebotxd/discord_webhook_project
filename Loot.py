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
Loot Council: <@169196574419714048>, <@194054862814576640> og <@321639079492190208>.

**Regler:**
- **Sims er et krav:** Opdater altid din sim, når du får nyt gear. Sims er topprioritet for loot.
- **Loot-prioritet:** Fokuserer på de største DPS-upgrades. Tanks og healers nedprioriteres i starten.
- **M+ krav:** Manglende opfyldelse af M+ kravet fører til nedprioritering på loot.
- **Tier Sets:** Fordeles 100% efter sims. Målet er 2-set til alle først.

**Vejledning til RCLC:**
- **BIS:** "Best In Slot" på din BIS-liste.
- **Upgrade:** En opgradering, stor som lille. **Kræver note.**
- **Off-spec:** Fordeles til officielle off-spec roller først (Cyd & Fynbo), derefter via roll.
- **Transmog:** Fordeles via roll, hvis ingen andre har brug for itemet.
- **Noter:** Brug noter til at forklare din anmodning, især hvis sim-dataen er uklar.
"""

# Create a single embed with a title, description, and author.
main_embed = discord.Embed(
    title="""Loot fordeles af loot council (LC) ved hjælp af RC Loot Council addon (RCLC)""",
    description=description_text,
    color=discord.Color.gold()
)

main_embed.set_author(
    name="Lootregler",
    icon_url='https://cdn.discordapp.com/embed/avatars/0.png'
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
