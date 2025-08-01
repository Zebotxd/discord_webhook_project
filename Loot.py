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
Loot Council består af <@169196574419714048>, <@194054862814576640>, og <@321639079492190208>.

**Loot-regler og fordeling**
Sims er et krav: Du skal simme din karakter inden raid for at LC har data at forholde sig til. Opdater altid din sim, når du får nyt gear. Sims prioriteres over alt andet i lootfordelingen.

Loot-prioritet: Vi fordeler loot primært ud fra de største DPS-upgrades. Hvor muligt vil vi også forsøge at fordele loot jævnt, men i starten vil tanks og healers blive nedprioriteret for at fokusere på DPS.

M+ krav: Hvis du ikke opfylder det ugentlige M+ krav, vil du blive nedprioriteret på loot.

Tier Sets: Tier sets fordeles 100% efter sims. Målet er at give alle deres 2-set bonus først, hvorefter vi fokuserer på 4-sets og upgrades.

**Vejledning til RC Loot Council**
BIS: Tryk, hvis et item er et "Best In Slot" på din liste og kun erstattes af samme item på et højere ilvl.

Upgrade: Tryk, hvis itemet er en opgradering – uanset om den er stor eller lille. Du skal tilføje en note.

Off-spec: Fordeles først til spillere med en officiel off-spec rolle (Cyd er tank, Fynbo er healer), derefter via roll.

Transmog: Vælg dette, hvis ingen andre har brug for itemet. Fordeles via roll.

Noter: Brug noter til at give LC en forklaring, især hvis du anmoder om et item, som ikke umiddelbart ser ud til at være en stor opgradering ifølge sims. Uden note vil LC ikke overveje din anmodning, hvis sim-dataen er uklar.
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
