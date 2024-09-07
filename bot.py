import discord

from src.utils import clear, banner, extension_loader, get_bot_settings

bot = discord.Bot(intents=discord.Intents.all())

clear()
banner()
extension_loader(bot)

bot.run(get_bot_settings('token'))
