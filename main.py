import discord
import asyncio
import requests
import os

# Ambil token dari environment variable Railway
TOKEN = os.getenv("DISCORD_TOKEN")

# Ganti dengan channel & role ID kamu
CHANNEL_ID = 1414397294890975397
ROLE_ID = 1414397105744908418

intents = discord.Intents.default()
client = discord.Client(intents=intents)

async def check_ugc():
    await client.wait_until_ready()
    channel = client.get_channel(CHANNEL_ID)

    while not client.is_closed():
        try:
            url = "https://catalog.roblox.com/v1/search/items/details?Category=13&SortType=3"
            response = requests.get(url)

            if response.status_code == 200:
                data = response.json()
                for item in data.get("data", []):
                    if item.get("price", 1) == 0:  # item gratis
                        embed = discord.Embed(
                            title=item["name"],
                            url=f"https://www.roblox.com/catalog/{item['id']}",
                            description="🎉 UGC FREE Baru Terdeteksi!",
                            color=discord.Color.blue()
                        )
                        embed.add_field(name="Price", value="FREE", inline=True)
                        embed.add_field(name="Creator", value=item.get("creatorTargetName", "Unknown"), inline=True)
                        embed.set_thumbnail(url=item.get("thumbnailUrl", ""))

                        role = f"<@&{ROLE_ID}>"  # ping role
                        await channel.send(content=role, embed=embed)

        except Exception as e:
            print(f"Error: {e}")

        await asyncio.sleep(60)  # cek tiap 60 detik

@client.event
async def on_ready():
    print(f"✅ Bot login sebagai {client.user}")

client.loop.create_task(check_ugc())
client.run(TOKEN)
