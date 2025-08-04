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
    'https://media.discordapp.net/attachments/1400838933960589422/1401928556614779101/Healer_guide_1.png?ex=68920f36&is=6890bdb6&hm=57790bbfe970cedca743093fb941adfe83ede3d3bb9692a3c465d6f85d2f5e84&=&format=webp&quality=lossless&width=1708&height=856',
    'https://media.discordapp.net/attachments/1400838933960589422/1401928556304531567/Healer_guide_2.png?ex=68920f36&is=6890bdb6&hm=4d0155ea7ed673cebe67f657925318cf5259ce15712bcf217553bb0d67f67ac9&=&format=webp&quality=lossless&width=1656&height=856',
    'https://media.discordapp.net/attachments/1400838933960589422/1401928555692294274/Healer_guide_3.jpg?ex=68920f36&is=6890bdb6&hm=5c014abf54b50e03cc5caaf3a9cba008c7778a6aa67b063ec27a502f3bccc16d&=&format=webp&width=1062&height=856',
    'https://media.discordapp.net/attachments/1400838933960589422/1401928555323199660/Healer_guide_4.png?ex=68920f36&is=6890bdb6&hm=b961405fd12f28811dd796a3063d50fd1213a756a56d705f2eca7b5efcdb83b2&=&format=webp&quality=lossless',
    'https://media.discordapp.net/attachments/1400838933960589422/1401928554886987776/Healer_guide_5.png?ex=68920f36&is=6890bdb6&hm=e4e2fe0a005d49f4258c2a8bfd17241fd5bc670cf194036ab1230a2ab9425c5d&=&format=webp&quality=lossless',
    'https://media.discordapp.net/attachments/1400838933960589422/1401928554538602496/Healer_guide_6.png?ex=68920f35&is=6890bdb5&hm=9718b7b52b22d88fd5aaca6d0f5cd19e6f99d221bfdc64fd034b4745a8626036&=&format=webp&quality=lossless&width=1654&height=856',
    'https://media.discordapp.net/attachments/1400838933960589422/1401928554073161821/Healer_guide_7.png?ex=68920f35&is=6890bdb5&hm=e15ce928b62236032b074a506c87acab7ea91cfbd37e24f640086a3b6aae1594&=&format=webp&quality=lossless&width=1640&height=856'
]

description_text = """
**Sims og Lootfordeling**
Vi bruger sims til at fordele loot, så det giver mest muligt udbytte.

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
    icon_url='https://wow.zamimg.com/images/wow/icons/large/petbattle_health.jpg'
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
