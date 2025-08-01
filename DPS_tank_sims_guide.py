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

# List of image URLs you want to include.
# Replace these with your actual image links.
image_urls = [
    'https://i.imgur.com/x4HgLaJ.png',
    'https://i.imgur.com/QzuePy2.png',
]

# The URL that will be shared by all embeds to group them.
shared_url = 'https://discord.com/channels/937428319295655966/1226225242285019286' # Use a link relevant to your guild or project.

# This is the text you provided, formatted for the embed description.
# The triple quotes allow for multi-line text with formatting.
description_text = """
**Sims og Lootfordeling**
Vi bruger sims til at sikre, at loot bliver fordelt til dem, der får mest ud af det. For at modtage loot er det derfor et krav, at dine sims er uploadet inden raid. Har du spørgsmål eller udfordringer, skal du kontakte <@173786599140622336>.

**Automatisk upload (anbefalet)**
Tag dit raid-gear på & skriv /simc i chatten og kopier teksten

Indsæt teksten i Discord-kanalen <#1249690921566601247>. Hvis teksten er for lang, skal du uploade den som en fil.

Upload Single Target (ST) sim først, og derefter AoE-sim, hvis du ønsker at uploade for begge.

Botten reagerer med ⏳, og når den er færdig, vises ✅ for succes eller ⛔ ved fejl.
Upload i god tid, da botten kan være belastet op til raid.

Tip: Få en mere detaljeret, pædagogisk forklaring i denne YouTube-guide, der viser hele processen med at bruge botten: https://www.youtube.com/watch?v=GSVXPuNl65o .

**Manuel upload**
Tag dit raid-gear på & skriv /simc i chatten og kopier teksten.

Gå til www.Raidbots.com og vælg Droptimizer.

Paste din /simc-streng, vælg det relevante raid, og kør to separate sims:

Single Target (ST): Patchwork, 1 target, 5 min.
AoE: Patchwork, 5 targets, 5 min.

Når dine sims er færdige, kopierer du linket.

Gå til https://wowaudit.com/eu/silvermoon/praktikanterne/main/wishlists/personal.

Indsæt Raidbots-linket under "Wishlist - Personal" og vælg, om det er en "Single Target" eller "AOE" sim.
"""

# Create the first embed with the title, author, and description.
main_embed = discord.Embed(
    title="Beskrivelse af, hvordan man simmer som DPS'er og tank.",
    description=description_text,
    url=shared_url,
    color=discord.Color.orange()
)

# Add the author attribute. You can replace the name and icon_url.
main_embed.set_author(
    name="DPS/Tank Sims-guide",
    icon_url='https://cdn.discordapp.com/embed/avatars/0.png' # You can put a URL to a guild icon here.
)

# Tilføj dette for at gøre embed'et bredere
main_embed.set_thumbnail(url=THUMBNAIL_URL)

# Set the first image for the gallery.
main_embed.set_image(url=image_urls[0])

# Create a list to hold all the embed objects.
embeds_list = [main_embed]

# Loop through the remaining images and create a new embed for each.
for url in image_urls[1:]:
    # Create a new embed with the same shared_url and only the image.
    embeds_list.append(
        discord.Embed(url=shared_url).set_image(url=url)
    )

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
