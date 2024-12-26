import discord
from discord.ext import commands

TOKEN = "MTMyMTgzNDI4NzExNjMyMDgzOA.G0F6U7.mfTzYHAAjCuqKyaIHltNgHaCis5UoqxFldDrbw"

intents = discord.Intents.default()
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"{bot.user} is online!")

     # ID du channel où le bot doit envoyer le message
    channel_id = 1312171714272297065  # Remplace par l'ID de ton channel
    channel = bot.get_channel(channel_id)

    print(f"{bot.user} est connecté à {len(bot.guilds)} serveur(s) :")
    for guild in bot.guilds:
        print(f"- {guild.name} (ID: {guild.id})")
    
    if channel:
        await channel.send("Nathan pu du zob 🚀")
    else:
        print("Channel introuvable !")

bot.run(TOKEN)
