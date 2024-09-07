from discord.ext import commands
import discord

from src.utils import debug_yellow, debug_stats, get_bot_settings


class OnReadyCog(commands.Cog):
    """
    A class that represents the OnReady event handler.

    This class is a subclass of commands.Cog and it handles the on_ready event.
    """

    def __init__(self, bot: discord.Bot):
        """
        The constructor for OnReadyCog class.

        Parameters:
           bot (discord.Bot): The bot instance.
        """
        self.bot = bot
        debug_yellow("Extensions", "Event OnReadyCog has been loaded successfully.")

    @commands.Cog.listener('on_ready')
    async def on_ready(self):
        """
        The event listener for the on_ready event.

        This method is called when the bot has successfully connected to the Discord API.
        It logs a message and sets the bot's presence.

        """
        await self.bot.change_presence(activity=discord.Game(name=get_bot_settings("status")))
        debug_stats(self.bot)
        print()


def setup(bot):
    """
    The setup function for the OnReadyCog class.

    This function is called when this cog is loaded by the bot.
    It adds an instance of OnReadyCog to the bot.

    Parameters:
       bot (discord.Bot): The bot instance.
    """
    bot.add_cog(OnReadyCog(bot))
