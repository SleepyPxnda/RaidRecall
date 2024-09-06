import discord
from src.utils import debug_green, EmbedBuilder
from discord.ext import commands

from src.warcraftlogs.WLClient import WLClient
from src.warcraftlogs.WLFormatter import WLFormatter


class RaidCommandCog(commands.Cog):
    """
    A class that represents the RaidCommand event handler.

    This class is a subclass of commands.Cog and it handles the help command.
    """

    def __init__(self, bot: discord.Bot):
        """
        The constructor for RaidCommandCog class.

        Parameters:
           bot (discord.Bot): The bot instance.
        """
        self.bot = bot
        debug_green("Extensions", "Command RaidCommandCog has been loaded successfully.")

    @commands.slash_command(
        name="raid",
        description="Prints the log of a raid based on the warcraftlogs link",
    )
    @commands.guild_only()
    async def _raid(self, ctx: discord.ApplicationContext, warcraftlogs_link: discord.Option(str)):
        """
        The event listener for the raid command.

        This method is called whenever the raid command is used.
        It sends a message with a list of all existing commands.

        Parameters:
           ctx (discord.ApplicationContext): The context in which the command was used.
        """
        await ctx.defer(ephemeral=False)

        client = WLClient(warcraftlogs_link)

        result = await client.request_data()

        formatter = WLFormatter(result)

        embed = formatter.create_embed()

        await ctx.respond(ephemeral=False, embed=embed)


def setup(bot):
    """
    The setup function for the RaidCommandCog class.

    This function is called when this cog is loaded by the bot.
    It adds an instance of RaidCommandCog to the bot.

    Parameters:
       bot (discord.Bot): The bot instance.
    """
    bot.add_cog(RaidCommandCog(bot))
