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
    'https://i.imgur.com/DCXga87.png',
    'https://i.imgur.com/8WUzMz7.png',
    'https://i.imgur.com/IV6rg0l.png',
    'https://i.imgur.com/cldUdeP.png'
]

# The URL that will be shared by all embeds to group them.
shared_url = 'http://example.com' # Use a link relevant to your guild or project.

# This is the text you provided, formatted for the embed description.
# The triple quotes allow for multi-line text with formatting.
description_text = """
Første gang man signer up, skal man gøre følgende:
Vælg present, absent eller late.
Klik på det link, som WoWaudit botten sender til dig for at linke din konto med WoWaudit (se billede 1).
Når du er logget ind, og du har linket din konto, kan du fremover bruge kanalen ⁠sign-up til at signe up til raid fra alle enheder, hvor du er logget ind på Discord (se billede 2).

Man skal have signet op senest 24 timer før, men vi ser gerne, at man signer op hurtigst muligt og gerne i god tid.
Vi forventer, at alle signer. Hvis man ikke kan komme, signer man sig selvfølgelig som absent.
Vi sætter roster ca. 24 timer før raid start. Når rosteret er sat, får i en lille besked herom i ⁠<#1226225068892487822>, og så kan man se, hvilke bosser man er inde på ved at kigge på billedet i øverste højre hjørne af det pågældende event (se billede 3 og 4).

Hvis der skulle opstå en situation under 24 timer før raid, altså efter der er sat roster, så er det vigtigt, at man kontakter en officer! Hvis man bliver forsinket, eller man er nødt til helt at udeblive fra raid, så kræver vi, at man skriver direkte til <@173786599140622336>eller <@231862976502562816>.
At blive forsinket eller udeblive fra raid efter roster er sat - uden at give lyd fra sig - er et totalt no-go.
"""

# Create the first embed with the title, author, and description.
main_embed = discord.Embed(
    title='Til raid sign-up bruger vi WoWaudit, som findes i kanalen <#1226225242285019286>',
    description=description_text,
    url=shared_url,
    color=discord.Color.blue()
)

# Add the author attribute. You can replace the name and icon_url.
main_embed.set_author(
    name="Sign up-guide"
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
