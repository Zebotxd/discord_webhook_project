import discord
import requests
import os

# The script will now read the webhook URL from the environment variable set in the GitHub Action.
WEBHOOK_URL = os.environ.get("DISCORD_WEBHOOK_URL")

# Make sure the URL exists before trying to send the message.
if not WEBHOOK_URL:
    print("Error: DISCORD_WEBHOOK_URL environment variable is not set.")
    exit(1)

# List of image URLs you want to include.
# Replace these with your actual image links.
image_urls = [
    'https://i.imgur.com/HhdOUuI.png',
    'https://i.imgur.com/ymUsOko.png',
    'https://i.imgur.com/BAYoWDL.jpeg',
    'https://i.imgur.com/A6cLdgP.png',
    'https://i.imgur.com/e9aRuvJ.png',
    'https://i.imgur.com/whTKbhr.png',
    'https://i.imgur.com/QhzVeOH.png'
]

# The URL that will be shared by all embeds to group them.
shared_url = 'https://discord.com/channels/937428319295655966/1226225242285019286' # Use a link relevant to your guild or project.

# This is the text you provided, formatted for the embed description.
# The triple quotes allow for multi-line text with formatting.
description_text = """
Vi bruger sims til at fordele lootet ud til de personer, som får mest ud af det.
Hvis der er nogle spørgsmål eller udfordringer, så hiv gerne fat i loot-officer, @bonkaboy.

**Sådan simmer du:**
Tag jeres "/Simc"-string ingame med jeres raid gear på.
Gå ind på https://questionablyepic.com/live/ og vælg "Upgrade finder" (Se billede 1)
Paste jeres "/Simc"-string ind i "Import gear" (Se billede 2).
Vælg "Heroic (Max)" og "Mythic (Max)" (se billede 3).
Tryk på "true" ved socket (se billede 4 og 5).
Tryk på "Go" (se billede 6).
Når jeres sim er færdig, kopierer i linket og smider det ind under "Wishlist - Personal" på https://wowaudit.com/eu/silvermoon/praktikanterne/main/wishlists/personal (Se billede 7).
"""

# Create the first embed with the title, author, and description.
main_embed = discord.Embed(
    title='I kan følge nedenstående guide til, hvordan i uploader jeres sims, som skal være uploadet inden raid for at få loot',
    description=description_text,
    url=shared_url,
    color=discord.Color.blue()
)

# Add the author attribute. You can replace the name and icon_url.
main_embed.set_author(
    name="Beskrivelse af, hvordan man simmer som healer",
    icon_url='https://cdn.discordapp.com/embed/avatars/0.png' # You can put a URL to a guild icon here.
)

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
