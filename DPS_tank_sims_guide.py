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
Sims er et krav for at modtage loot. De bruges til at sikre, at loot går til dem, der får mest ud af det.

**Automatisk Upload (anbefales)**
1. Tag `/simc`-string i chatten og indsæt den i <#1249690921566601247>.
2. **Hvis teksten er for lang, skal du uploade den som en fil.**
3. Upload ST-sim først, derefter AoE.
4. Botten reagerer med ✅ ved succes.
5. Se YouTube-guiden for detaljer: https://www.youtube.com/watch?v=GSVXPuNl65o .

**Manuel Upload**
1. Tag din `/simc`-string ingame.
2. Gå til www.Raidbots.com, vælg **Droptimizer**, og kør to sims: ST (1 target) og AoE (5 targets).
3. Kopier linket, gå til **Wowaudit** på "Wishlist - Personal" og indsæt det.
"""

# Create the first embed with the title, author, and description.
main_embed = discord.Embed(
    title="",
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
