import discord
from utils import debug_green, EmbedBuilder
from discord.ext import commands

class HelpCommandCog(commands.Cog):
    """
    A class that represents the HelpCommand event handler.

    This class is a subclass of commands.Cog and it handles the help command.
    """

    def __init__(self, bot: discord.Bot):
        """
        The constructor for HelpCommandCog class.

        Parameters:
           bot (discord.Bot): The bot instance.
        """
        self.bot = bot
        debug_green("Extensions", "Command HelpCommandCog has been loaded successfully.")

    @commands.slash_command(
        name="help",
        description="Eine Liste aller existierenden Commands.",
    )
    @commands.guild_only()
    async def _help(self, ctx: discord.ApplicationContext):
        """
        The event listener for the help command.

        This method is called whenever the help command is used.
        It sends a message with a list of all existing commands.

        Parameters:
           ctx (discord.ApplicationContext): The context in which the command was used.
        """
        await ctx.defer(ephemeral=True)
        embed = EmbedBuilder.default_embed(
            title="",
            description="# Eine Liste aller existierenden Commands",
        )
        for command in self.bot.commands:
            embed.add_field(
                name=f"/{command.name}",
                value=command.description if command.description else "Keine Beschreibung",
                inline=False,
            )
        await ctx.followup.send(embed=embed, ephemeral=True)


def setup(bot):
    """
    The setup function for the HelpCommandCog class.

    This function is called when this cog is loaded by the bot.
    It adds an instance of HelpCommandCog to the bot.

    Parameters:
       bot (discord.Bot): The bot instance.
    """
    bot.add_cog(HelpCommandCog(bot))
