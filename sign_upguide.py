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
# Udskift med dine faktiske billed-links fra en Discord-kanal.
image_urls = [
    'https://cdn.discordapp.com/attachments/.../image1.png',
    'https://cdn.discordapp.com/attachments/.../image2.png',
    'https://cdn.discordapp.com/attachments/.../image3.png',
    'https://cdn.discordapp.com/attachments/.../image4.png'
]

# The URL that will be shared by all embeds to group them.
shared_url = 'https://discord.com/channels/937428319295655966/1226225242285019286'

# Opdateret beskrivelse med den kortere version.
description_text = """
**Tilmeldingsguide**
- **Første gang:** Vælg status (Present/Absent/Late) og følg linket fra WoWaudit-botten for at linke din konto. Herefter kan du tilmelde dig fra enhver enhed.

- **Deadline:** Du skal tilmelde dig senest 24 timer før raidstart. Rosteren sættes ca. 24 timer før.

- **Afbud:** Sæt din status til "Absent", hvis du ikke kan deltage. Ved afbud efter deadline skal du kontakte en officer med det samme.
- **Kontakt ved forsinkelse:** Kontakt direkte <@173786599140622336> eller <@231862976502562816> ved forsinkelse eller fravær efter rosteren er sat. Udeblivelse uden varsel er uacceptabelt.
"""

# Create the first embed with the title, author, and description.
main_embed = discord.Embed(
    title='Til raid sign-up bruger vi WoWaudit, som findes i kanalen <#1226225242285019286>',
    description=description_text,
    url=shared_url,
    color=discord.Color.green()
)

# Add the author attribute. You can replace the name and icon_url.
main_embed.set_author(
    name="Sign up-guide",
    icon_url='https://cdn.discordapp.com/embed/avatars/0.png'
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
