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

# --- Step 1: Create and send the embed without images ---
main_embed = discord.Embed(
    title='I kan følge nedenstående guide til, hvordan i uploader jeres sims, som skal være uploadet inden raid for at få loot',
    description=description_text,
    color=discord.Color.blue()
)

main_embed.set_author(
    name="Beskrivelse af, hvordan man simmer som healer",
    icon_url='https://cdn.discordapp.com/embed/avatars/0.png'
)

embeds_list = [main_embed]

# --- Step 2: Prepare the image files for the second message ---
files_to_send = [] # Ændret til en liste for at håndtere filerne korrekt
for i, url in enumerate(all_image_urls):
    try:
        response = requests.get(url)
        response.raise_for_status()
        
        # Opretter et fil-lignende objekt fra billedets indhold
        file_data = io.BytesIO(response.content)
        
        # Tilføj filen til listen i det korrekte format
        files_to_send.append((f"billede{i+1}.png", file_data, 'image/png'))
        
    except requests.exceptions.RequestException as e:
        print(f"Failed to fetch image from URL {url}: {e}")

# --- Step 3: Send both messages separately ---
try:
    # Send the first message with the embed
    response1 = requests.post(
        WEBHOOK_URL,
        json={'embeds': [e.to_dict() for e in embeds_list]},
        headers={'Content-Type': 'application/json'}
    )
    response1.raise_for_status()
    print("Successfully sent embed message.")

    # Send the second message with the image attachments
    response2 = requests.post(
        WEBHOOK_URL,
        files=files_to_send,
    )
    response2.raise_for_status()
    print("Successfully sent image messages.")
    
except requests.exceptions.RequestException as e:
    print(f"Failed to send webhook message: {e}")
