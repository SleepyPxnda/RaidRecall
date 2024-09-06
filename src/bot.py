import discord

from utils import extension_loader, get_bot_settings, clear, banner

bot = discord.Bot(intents=discord.Intents.all())

clear()
banner()
extension_loader(bot)

bot.run(get_bot_settings('token'))
