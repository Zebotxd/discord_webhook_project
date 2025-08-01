import discord
import requests
import os
import io
import json
import time

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

# Opret payload for embed-beskeden
payload = {
    'embeds': [main_embed.to_dict()]
}

# --- Step 2: Prepare the image files ---
files_to_send = {}
for i, url in enumerate(all_image_urls):
    try:
        response = requests.get(url, timeout=10) # Tilføj en timeout
        response.raise_for_status()
        
        files_to_send[f"file{i}"] = (f"billede{i+1}.png", io.BytesIO(response.content))
        
        # Indbyg en lille pause for at undgå at blive blokeret af Imgur
        time.sleep(1)
        
    except requests.exceptions.RequestException as e:
        print(f"Failed to fetch image from URL {url}: {e}")
        # Fejlhåndtering: Hvis en download fejler, skal vi stoppe
        files_to_send = None 
        break

# --- Step 3: Send både embeds og billeder i en enkelt forespørgsel ---
if files_to_send:
    try:
        response = requests.post(
            WEBHOOK_URL,
            data={'payload_json': json.dumps(payload)}, # Korrekt måde at sende JSON og filer
            files=files_to_send
        )
        response.raise_for_status()
        print("Successfully sent message with embed and images.")
    except requests.exceptions.RequestException as e:
        print(f"Failed to send webhook message: {e}")
else:
    print("Could not send message due to failed image downloads.")
