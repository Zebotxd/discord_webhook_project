import discord
import requests
import os
import io

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

# --- Step 1: Create the embed object ---
main_embed = discord.Embed(
    title='I kan følge nedenstående guide til, hvordan i uploader jeres sims, som skal være uploadet inden raid for at få loot',
    description=description_text,
    color=discord.Color.blue()
)

main_embed.set_author(
    name="Beskrivelse af, hvordan man simmer som healer",
    icon_url='https://cdn.discordapp.com/embed/avatars/0.png'
)

# Opret en liste med embed-objektet
embeds_list = [main_embed]

# --- Step 2: Prepare the image files ---
files_to_send = {}
for i, url in enumerate(all_image_urls):
    try:
        response = requests.get(url)
        response.raise_for_status()
        
        # Opretter et fil-lignende objekt og tilføjer det til dictionary
        files_to_send[f"file{i}"] = (f"billede{i+1}.png", io.BytesIO(response.content))
        
    except requests.exceptions.RequestException as e:
        print(f"Failed to fetch image from URL {url}: {e}")

# --- Step 3: Send både embeds og billeder i en enkelt forespørgsel ---
try:
    response = requests.post(
        WEBHOOK_URL,
        data={'embeds': embeds_list[0].to_dict()}, # Send kun et enkelt embed-objekt her
        files=files_to_send,
    )
    response.raise_for_status()
    print("Successfully sent message with embed and images.")
except requests.exceptions.RequestException as e:
    print(f"Failed to send webhook message: {e}")
