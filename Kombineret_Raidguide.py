import discord
import requests
import os

# Scriptet læser nu webhook-URL'en fra den GitHub Action environment variable.
WEBHOOK_URL = os.environ.get("DISCORD_WEBHOOK_URL")

# Sikrer, at URL'en eksisterer, før scriptet fortsætter.
if not WEBHOOK_URL:
    print("Error: DISCORD_WEBHOOK_URL environment variable is not set.")
    exit(1)

# Din thumbnail-URL (udskift dette med linket fra din Discord-kanal)
THUMBNAIL_URL = 'https://cdn.discordapp.com/attachments/1400838933960589422/1400840729085087855/Praktikanterne_logo.png?ex=688e1a18&is=688cc898&hm=eeb70914e72056e2bdf4a9f6b9e4f930f0dc6407f5d64bec51ebfd1c28bef66d&'

# --- Forkortet indhold til inline felter ---
forventninger_krav_kort = """
**Tilmeld dig raids** senest 24 timer før. **Invites** sendes ud kl. 19:45. Vi **puller** kl. 20:00.

**Krav:**
- **M+ Keys:** Keystone Master (2k) i uge 1. Fra uge 2: 4x +10 keys om ugen.
- **Forberedelse:** Sæt dig ind i class, læs op på boss-mekanikker og raid-buffs.
- **Gear:** Sørg for at gear er fuldt enchanted og gemmed.
- **Addons:** Installer de nødvendige WeakAuras & addons.

BOEs skal trades til guildbanken via <@173786599140622336>.
"""

loot_kort = """
**Loot Council** består af <@169196574419714048>, <@194054862814576640> og <@321639079492190208>.

**Sims er et krav:** Opdater altid din sim, når du får nyt gear. Sims prioriteres over alt andet i lootfordelingen.

**Loot-prioritet:** Loot fordeles primært ud fra de største DPS-upgrades.
**Tier Sets:** Fordeles 100% efter sims. Målet er, at alle får 2-set bonus først.

**Vejledning til RC Loot Council**
- **BIS:** Best In Slot.
- **Upgrade:** Stor eller lille opgradering. Kræver note.
- **Off-spec:** Fordeles via roll, efter officielle roller har fået.
- **Transmog:** Uddeles, hvis ingen andre har brug for itemet.
"""

# --- Opret det kombinerede embed ---
main_embed = discord.Embed(
    title="**Raid Guide: Forventninger & Loot**",
    description="Her finder du en samlet oversigt over forventninger til raidet og vores regler for loot.",
    color=discord.Color.purple()
)

main_embed.set_author(
    name="Praktikanterne Raids",
    icon_url='https://cdn.discordapp.com/embed/avatars/0.png'
)

# Tilføj dit thumbnail
main_embed.set_thumbnail(url=THUMBNAIL_URL)

# Tilføj det første inline felt
main_embed.add_field(
    name="**Forventninger og Krav**",
    value=forventninger_krav_kort,
    inline=True
)

# Tilføj det andet inline felt
main_embed.add_field(
    name="**Lootregler**",
    value=loot_kort,
    inline=True
)

# Opret en liste, der indeholder dit ene embed-objekt
embeds_list = [main_embed]

# --- Send embed'et til webhook'en ---
try:
    response = requests.post(
        WEBHOOK_URL,
        json={'embeds': [e.to_dict() for e in embeds_list]},
        headers={'Content-Type': 'application/json'}
    )
    response.raise_for_status()
    print("Successfully sent combined embed message.")
except requests.exceptions.RequestException as e:
    print(f"Failed to send webhook message: {e}")
