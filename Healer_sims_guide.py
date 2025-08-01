import discord
import requests
import os

# The script will now read the webhook URL from the environment variable set in the GitHub Action.
WEBHOOK_URL = os.environ.get("DISCORD_WEBHOOK_URL")

# Make sure the URL exists before trying to send the message.
if not WEBHOOK_URL:
    print("Error: DISCORD_WEBHOOK_URL environment variable is not set.")
    exit(1)

# List of all your image URLs
all_image_urls = [
    'https://i.imgur.com/HhdOUuI.png',
    'https://i.imgur.com/ymUsOko.png',
    'https://i.imgur.com/BAYoWDL.jpeg',
    'https://i.imgur.com/A6cLdgP.png',
    'https://i.imgur.com/e9aRuvJ.png',
    'https://i.imgur.com/whTKbhr.png',
    'https://i.imgur.com/QhzVeOH.png'
]

# Split the images into two groups
images_part1 = all_image_urls[:4]
images_part2 = all_image_urls[4:]

# The URL that will be shared by all embeds to group them.
shared_url = 'https://discord.com/channels/937428319295655966/1226225242285019286'

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

# --- Første embed (with text and first 4 images) ---
main_embed = discord.Embed(
    title='I kan følge nedenstående guide til, hvordan i uploader jeres sims, som skal være uploadet inden raid for at få loot',
    description=description_text,
    url=shared_url,
    color=discord.Color.blue()
)

main_embed.set_author(
    name="Beskrivelse af, hvordan man simmer som healer",
    icon_url='https://cdn.discordapp.com/embed/avatars/0.png'
)

# Set the first image for the gallery.
main_embed.set_image(url=images_part1[0])

embeds_list_part1 = [main_embed]
for url in images_part1[1:]:
    embeds_list_part1.append(
        discord.Embed(url=shared_url).set_image(url=url)
    )

# --- Anden embed (with remaining images) ---
# This embed will be sent as a separate message.
embeds_list_part2 = []
for url in images_part2:
    # We still need the shared_url to make it a gallery of images
    embeds_list_part2.append(
        discord.Embed(url=shared_url).set_image(url=url)
    )

# --- Send both webhooks separately ---
try:
    # Send the first message with the first gallery
    response1 = requests.post(
        WEBHOOK_URL,
        json={'embeds': [e.to_dict() for e in embeds_list_part1]},
        headers={'Content-Type': 'application/json'}
    )
    response1.raise_for_status()

    # Send the second message with the second gallery
    response2 = requests.post(
        WEBHOOK_URL,
        json={'embeds': [e.to_dict() for e in embeds_list_part2]},
        headers={'Content-Type': 'application/json'}
    )
    response2.raise_for_status()
    print("Successfully sent both webhook messages.")
except requests.exceptions.RequestException as e:
    print(f"Failed to send webhook message: {e}")
