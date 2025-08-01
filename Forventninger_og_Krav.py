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
Vi raider Onsdag og Søndag fra 20:00-22:30.
De 3 første uger køre vi dog også Tirsdag

Vores mål for dette tier er CE, samt at vi selvfølgelig skal slå os selv fra season 2!

**Vores krav:**

Man signer op til raid senest 24 timer før raid i ⁠sign-up (meget gerne før).

Raid starter kl. 20. Invites går ud ca. 19:45, så vi kan være klar til pulle kl. 20:00.

M+-krav i uge 1: Opnå Keystone Master (2k rating).

M+-krav fra uge 2: 4x +10 keys om ugen. Man bliver nedprioriteret på loot og roster, hvis man ikke har opfyldt m+-kravet ugen forinden (Kravet bliver fjernet slut tier nå det ikke giver mening længere).

Man har sat sig ind i sin class, læst op på changes, boss mechanics og holdt sig opdateret med eventuelle tilgængelige raid buffs.

Man har crafted items med embellishments, når det er muligt. Sim jeres char eller spørg efter hjælp, hvis i er tvivl om, hvad der giver mest mening at crafte først.

Man har enchanted sit gear til raid (minimum rank 2 fra start, og rank 3 når vi begynder på mythic).

Man skal have socket og gems i neck og rings (på hero- og mythictrack gear)

I skal selv medbringe oils. Vi sørger for feasts, repair-hammers, cauldrons med flasks og potions og vantus runes. Hav gerne lige lidt backup i jeres egne bags, hvis i skulle misse et feast eller en cauldron.

Man skal have installeret de Weakauras & addons, som man finder i tråden nedenunder. Der kan være krav til specifikke WeakAuras & Addons på nogle bosser, og disse vil fremgå i tekstkanaler med bossens navn. Husk at orientér jer heri inden raid.

BOEs går til guildbanken. De skal trades til <@173786599140622336> (zebåt i raidet). Det er muligt at købe et BOE-item, hvis det er en stor upgrade eller et BIS-item til 30% af AH-markedsprisen..
"""

# Create a single embed with a title, description, and author.
main_embed = discord.Embed(
    title='**THE WAR WITIHIN SEASON 3**',
    description=description_text,
    color=discord.Color.red()
)

main_embed.set_author(
    name="Vores forventninger og krav til raidet og til jer",
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
