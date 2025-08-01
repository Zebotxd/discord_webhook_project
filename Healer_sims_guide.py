import discord
import requests
import os
import io
import json

# The script will now read the webhook URL from the environment variable set in the GitHub Action.
WEBHOOK_URL = os.environ.get("DISCORD_WEBHOOK_URL")

# Make sure the URL exists before trying to send the message.
if not WEBHOOK_URL:
    print("Error: DISCORD_WEBHOOK_URL environment variable is not set.")
    exit(1)

# List of all your image URLs from Discord's CDN.
# (Udskift disse med de links, du har kopieret fra din Discord-kanal)
all_image_urls = [
    'https://cdn.discordapp.com/attachments/1397519593764814889/1400823597143953419/Healer_guide_1.png?ex=688e0a23&is=688cb8a3&hm=af21235a48e9f347789de21d73760e5c38a9930c26ae78eb7ef1042e541a004d&',
    'https://cdn.discordapp.com/attachments/1397519593764814889/1400823596485447730/Healer_guide_2.png?ex=688e0a23&is=688cb8a3&hm=d2620363a7757ce7d4e3f69c983eb32e79b40222a5f0bd4609fbf3d35891fc9d&',
    'https://cdn.discordapp.com/attachments/1397519593764814889/1400823595797577870/Healer_guide_3.jpg?ex=688e0a23&is=688cb8a3&hm=ece87e3a5299ccd1005b1affd912b3bb24e9901b0fa46f2d8e202928eae8e34e&',
    'https://cdn.discordapp.com/attachments/1397519593764814889/1400823595315363890/Healer_guide_4.png?ex=688e0a23&is=688cb8a3&hm=b697cecaaadd8635d7b72acd7d0bd16f417194ded7b484d596e228236c581317&',
    'https://cdn.discordapp.com/attachments/1397519593764814889/1400823594686353490/Healer_guide_5.png?ex=688e0a23&is=688cb8a3&hm=37595a5d00b3babb6b51c8a5c71bf73986faa9b8d75b942f08dfcca8e38e445e&',
    'https://cdn.discordapp.com/attachments/1397519593764814889/1400823594220781609/Healer_guide_6.png?ex=688e0a22&is=688cb8a2&hm=8acd36dad965e4213843dfa1c1b4ec24fbb05d7567e3b67d288e411712667b0c&',
    'https://cdn.discordapp.com/attachments/1397519593764814889/1400823593796894810/Healer_guide_7.png?ex=688e0a22&is=688cb8a2&hm=5abbffb07b74687abcc21a40dad3f83bd97c794109bee198ead80355b94a4d76&'
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
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        
        files_to_send[f"file{i}"] = (f"billede{i+1}.png", io.BytesIO(response.content))
        
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
            data={'payload_json': json.dumps(payload)},
            files=files_to_send
        )
        response.raise_for_status()
        print("Successfully sent message with embed and images.")
    except requests.exceptions.RequestException as e:
        print(f"Failed to send webhook message: {e}")
else:
    print("Could not send message due to failed image downloads.")
