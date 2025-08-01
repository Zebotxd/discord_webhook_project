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
THUMBNAIL_URL = 'https://cdn.discordapp.com/attachments/1400838933960589422/1400840729085087855/Praktikanterne_logo.png?ex=688e1a18&is=688cc898&hm=eeb70914e72056e2bdf4a9f6b9e4f930dc6407f5d64bec51ebfd1c28bef66d&'

# --- Indhold fra Forventninger_og_Krav.py, opdelt i mindre dele ---
forventninger_krav_del1 = """
**Raidtider og Mål**
Vi raider onsdag og søndag fra 20:00-22:30. De første tre uger raider vi også tirsdag.

Vores mål er at opnå Cutting Edge (CE) og overgå vores tidligere præstationer.

Invites sendes ud kl. 19:45, og vi puller kl. 20:00. Tilmeld dig raids senest 24 timer før.
"""

forventninger_krav_del2 = """
**Krav til Raids**
For at sikre et effektivt raidmiljø har vi følgende krav til vores medlemmer:

Ugentlige keys: I uge 1 skal du have Keystone Master (2k rating). Fra uge 2 skal du have gennemført 4x +10 keys om ugen. Spillere, der ikke opfylder dette, vil blive nedprioriteret på loot og roster.

Forberedelse: Sæt dig ind i din class, læs op på boss-mekanikker, og hold dig opdateret om relevante raid-buffs.
"""

forventninger_krav_del3 = """
Gear: Sørg for at have de korrekte crafted items med embellishments, og at dit gear er fuldt enchanted og gemmed.

Consumsables: Medbring selv oils. Guilden står for feasts, cauldrons (flasks/potions) og vantus runes, men hav en backup i dine egne tasker.

Addons: Installer de nødvendige WeakAuras og addons. Tjek altid specifikke krav for individuelle bosser i de dedikerede tekstkanaler.
"""

forventninger_krav_del4 = """
BOEs: Eventuelle BOE-items trades til guildbanken via <@173786599140622336>. Det er muligt at købe et item til 30% af Auktionshusets markedspris, hvis det er en stor opgradering.
"""

# --- Indhold fra Loot.py, opdelt i mindre dele ---
loot_del1 = """
Loot Council består af <@169196574419714048>, <@194054862814576640>, og <@321639079492190208>.

**Loot-regler og fordeling**
Sims er et krav: Du skal simme din karakter inden raid for at LC har data at forholde sig til. Opdater altid din sim, når du får nyt gear. Sims prioriteres over alt andet i lootfordelingen.

Loot-prioritet: Vi fordeler loot primært ud fra de største DPS-upgrades. Hvor muligt vil vi også forsøge at fordele loot jævnt, men i starten vil tanks og healers blive nedprioriteret for at fokusere på DPS.
"""

loot_del2 = """
M+ krav: Hvis du ikke opfylder det ugentlige M+ krav, vil du blive nedprioriteret på loot.

Tier Sets: Tier sets fordeles 100% efter sims. Målet er at give alle deres 2-set bonus først, hvorefter vi fokuserer på 4-sets og upgrades.
"""

loot_del3 = """
**Vejledning til RC Loot Council**
BIS: Tryk, hvis et item er et "Best In Slot" på din liste og kun erstattes af samme item på et højere ilvl.

Upgrade: Tryk, hvis itemet er en opgradering – uanset om den er stor eller lille. Du skal tilføje en note.

Off-spec: Fordeles først til spillere med en officiel off-spec rolle (Cyd er tank, Fynbo er healer), derefter via roll.

Transmog: Vælg dette, hvis ingen andre har brug for itemet. Fordeles via roll.

Noter: Brug noter til at give LC en forklaring, især hvis du anmoder om et item, som ikke umiddelbart ser ud til at være en stor opgradering ifølge sims. Uden note vil LC ikke overveje din anmodning, hvis sim-dataen er uklar.
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

# Tilføj felter med opdelte tekster
main_embed.add_field(name="**Forventninger og Krav**", value=forventninger_krav_del1, inline=False)
main_embed.add_field(name=" ", value=forventninger_krav_del2, inline=False)
main_embed.add_field(name=" ", value=forventninger_krav_del3, inline=False)
main_embed.add_field(name="**Lootregler**", value=loot_del1, inline=False)
main_embed.add_field(name=" ", value=loot_del2, inline=False)
main_embed.add_field(name=" ", value=loot_del3, inline=False)

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
