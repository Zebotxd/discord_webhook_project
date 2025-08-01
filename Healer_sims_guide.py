import discord
import requests
import os
import io
import json
import time

# Scriptet læser nu webhook-URL'en fra den GitHub Action environment variable.
WEBHOOK_URL = os.environ.get("DISCORD_WEBHOOK_URL")

# Sikrer, at URL'en eksisterer, før scriptet fortsætter.
if not WEBHOOK_URL:
    print("Error: DISCORD_WEBHOOK_URL environment variable is not set.")
    exit(1)

# Din thumbnail-URL (udskift dette med linket fra din Discord-kanal)
THUMBNAIL_URL = 'https://cdn.discordapp.com/attachments/1400838933960589422/1400840729085087855/Praktikanterne_logo.png?ex=688e1a18&is=688cc898&hm=eeb70914e72056e2bdf4a9f6b9e4f930f0dc6407f5d64bec51ebfd1c28bef66d&'

# Liste over alle dine billed-URL'er fra Discord's CDN.
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
**Sims og Lootfordeling**
Vi bruger sims til at fordele loot, så det giver mest muligt udbytte. Har du spørgsmål, så kontakt loot-officer @bonkaboy.

**Sådan simmer du**
1. Tag din `/simc`-string i chatten med dit raid gear på.
2. Gå ind på https://questionablyepic.com/live/ og vælg "Upgrade finder".
3. Paste `/simc`-strengen ind i "Import gear".
4. Vælg "Heroic (Max)" og "Mythic (Max)".
5. Sæt "true" ved socket og tryk "Go".
6. Når sim er færdig, kopier linket og sæt det ind i din "Wishlist - Personal" på https://wowaudit.com/eu/silvermoon/praktikanterne/main/wishlists/personal.
"""

# --- Trin 1: Opret og send embed-beskeden ---
main_embed = discord.Embed(
    title='',
    description=description_text,
    color=discord.Color.blue()
)

main_embed.set_author(
    name="Beskrivelse af, hvordan man simmer som healer",
    icon_url='https://cdn.discordapp.com/embed/avatars/0.png'
)

# Tilføj dette for at gøre embed'et bredere
main_embed.set_thumbnail(url=THUMBNAIL_URL)

# Send den første besked med embed-objektet
try:
    response1 = requests.post(
        WEBHOOK_URL,
        json={'embeds': [main_embed.to_dict()]},
        headers={'Content-Type': 'application/json'}
    )
    response1.raise_for_status()
    print("Successfully sent embed message.")
except requests.exceptions.RequestException as e:
    print(f"Failed to send webhook message: {e}")
    exit(1)

# --- Trin 2: Forbered billederne og send den anden besked ---
# Indbyg en lille pause for at sikre at den første besked er færdig
print("Waiting for 2 seconds...")
time.sleep(2)

files_to_send = {}
for i, url in enumerate(all_image_urls):
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        
        files_to_send[f"file{i}"] = (f"billede{i+1}.png", io.BytesIO(response.content))
        
    except requests.exceptions.RequestException as e:
        print(f"Failed to fetch image from URL {url}: {e}")
        files_to_send = None 
        break

if files_to_send:
    try:
        response2 = requests.post(
            WEBHOOK_URL,
            files=files_to_send,
        )
        response2.raise_for_status()
        print("Successfully sent image messages.")
    except requests.exceptions.RequestException as e:
        print(f"Failed to send webhook message: {e}")
else:
    print("Could not send message due to failed image downloads.")
