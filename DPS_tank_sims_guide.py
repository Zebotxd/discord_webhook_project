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
I kan følge nedenstående guides "Automatisk/Manuel" til, hvordan i uploader jeres sims, som skal være uploadet inden raid for at få loot.
Vi bruger sims til at fordele loot til lige de personer, som får mest ud af det.
Hvis der er nogle spørgsmål eller udfordringer, så hiv gerne fat i <@173786599140622336> .

**Automatisk:**
Tag jeres "/Simc"-string ingame med jeres raid gear på.
Sæt jeres "/Simc"-string ind i kanalen <#1249690921566601247>.
Her er det muligt, den brokker sig, hvortil i skal vælge at uploade "simc" som en fil.
Vigtigt! Husk, at uploade ST først og derefter AOE, såfremt i vil uploade for begge muligheder. 
Botten reagerer nu med "⏳", og hertil kan der gå op til 10min, før den reagerer med " ✅ / ⛔ "
Reagerer den med " ✅ " er alt fint, og jeres sims er uploadet, som de skal.
Reagere den med " ⛔ " er der gået noget galt. Herefter kan i tage fat i <@173786599140622336>. 
(Husk at uploade i god tid, da botten kan være presset lige op til raid).
Man kan også se denne YouTube-video, hvor Wossti forklarer det for os meget pædagogisk: https://www.youtube.com/watch?v=GSVXPuNl65o 

**Manuel:**
Tag jeres "/Simc"-string ingame med jeres raid gear på.
Gå ind på www.Raidbots.com og vælg Droptimizer.
Paste jeres "/Simc"-string og vælg det pågældende raid. (Se eksempel: Billede 1)
Duplikér jeres vindue, så i har to. Der skal nemlig køres to Droptimizers med følgende:
Patchwork, 1 targets, 5 min fight.
Patchwork, 5 targets, 5 min fight.
Når disse sims er færdige, kopierer i linket og smider det ind under "Wishlist - Personal" på https://wowaudit.com/eu/silvermoon/praktikanterne/main/wishlists/personal
Her står der, at i kan uploade jeres raidbots link, hvor i oppe i toppen af højre hjørne skal vælge, om det er "Single Target" eller "AOE" (Se billede 2)
Single Target - Patchwork, 1 targets, 5 min fight.
AOE           - Patchwork, 5 targets, 5 min fight.
"""

# Create the first embed with the title, author, and description.
main_embed = discord.Embed(
    title="Beskrivelse af, hvordan man simmer som DPS'er og tank.",
    description=description_text,
    url=shared_url,
    color=discord.Color.blue()
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
