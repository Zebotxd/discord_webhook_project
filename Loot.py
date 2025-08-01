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

Loot council består af loot-officer <@169196574419714048> samt vores raiders <@194054862814576640> og <@321639079492190208>

Man skal simme inden raid, før man kan få loot, ellers har LC ikke noget data at gå ud fra. For hjælp til at simme, se vore sim guides. Sørg for at forny din sim, hvis du udskifter eller opgraderer et item. LC kan se, hvilke items man har simmet med, og hvis det ikke stemmer overens med det, man har på, kan man ikke få tildelt det item, da de ikke har de rigtige sims at gå ud fra. Sim i god tid inden raid, da botten kan få travlt lige inden, ellers læg dem ind manuelt.

Der uddeles loot efter, hvad der er BIS i raid og ikke m+. M+ kommer i 2. række. Brug noten i RCLC.

Der uddeles loot med fokus på DPS-upgrades, men samtidig vil vi også forsøge at fordele loot jævnt ud mellem alle raiders, så alle får. Dog skal tanks og healers forvente at blive nedprioriteret på loot til fordel for DPS'ere i starten som altid...

Hvis man ikke har opfyldt m+-kravet ugen før, vil man blive nedprioriteret på loot for at gøre det fair for dem, som gør en stor indsats på holdet.

Tier sets fordeles 100% efter sims, og vi går efter at give alle 2-set først, fordi med catalyst og m+ score/AOTC burde alle kunne ramme 4-set hurtigst muligt. Efter alle har fået 2-set, uddeles 4-set og upgrades til tier set.
 
-
Hvad betyder knapperne i RC Loot Council: 

BIS: Trykkes ved loot, som man ikke vil erstatte med andet end samme item på et højere ilvl. Altså kun på loot, som står på jeres overall BIS-liste.

Upgrade:  Trykkes ved loot, som er en upgrade både stor og lille. Man SKAL skrive en note til.

Off-spec: Off-spec gear fordeles til dem, der har en officiel off-spec rolle i raidet først, og derefter uddeles det via roll igennem RCLCs eget roll system. Off-spec tank i raid er Cyd. Off-spec healer i raid er Fynbo.

Transmog:  Uddeles, hvis ingen får en upgrade ud af et item. Uddeles med RCLCs eget roll system, så alle har lige chance.

Note:  Brug noten effektivt. Giv en forklaring eller uddybning - især hvis du trykker upgrade eller BIS uden, at det på sims ser ud til at være en stor upgrade. Hvis der ikke er noteret en note, og sims ikke siger, det er en upgrade, vil LC ikke betragte det som en upgrade.
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
