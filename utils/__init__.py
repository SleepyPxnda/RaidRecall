import asyncio
import datetime
import random

import aiohttp
import discord
import json
import os

from dateutil import parser


class Stats:
    loaded_commands = 0
    loaded_events = 0
    loaded_tasks = 0


class color:
    """
    A class to store color codes for the terminal.
    """
    RED = '\033[91m'
    LIGHT_RED = '\033[31m'
    GREEN = '\033[92m'
    LIGHT_GREEN = '\033[32m'
    YELLOW = '\033[93m'
    LIGHT_YELLOW = '\033[33m'
    ORANGE = '\033[33m'
    LIGHT_ORANGE = '\033[33m'
    BLUE = '\033[94m'
    LIGHT_BLUE = '\033[34m'
    PURPLE = '\033[95m'
    LIGHT_PURPLE = '\033[35m'
    CYAN = '\033[96m'
    LIGHT_CYAN = '\033[36m'
    PINK = '\033[95m'
    LIGHT_PINK = '\033[35m'
    GRAY = '\033[90m'
    LIGHT_GRAY = '\033[37m'
    RESET = '\033[0m'


def clear():
    """
    Clear the console.
    """
    os.system('cls' if os.name == 'nt' else 'clear')


def banner():
    """
    Print the bot's banner.
    """
    print(color.LIGHT_BLUE + r"""
 /$$$$$$$              /$$  /$$$$$$$$                                /$$             /$$              
| $$__  $$            | $$ |__  $$__/                               | $$            | $$              
| $$  \ $$  /$$$$$$  /$$$$$$  | $$  /$$$$$$  /$$$$$$/$$$$   /$$$$$$ | $$  /$$$$$$  /$$$$$$    /$$$$$$ 
| $$$$$$$  /$$__  $$|_  $$_/  | $$ /$$__  $$| $$_  $$_  $$ /$$__  $$| $$ |____  $$|_  $$_/   /$$__  $$
| $$__  $$| $$  \ $$  | $$    | $$| $$$$$$$$| $$ \ $$ \ $$| $$  \ $$| $$  /$$$$$$$  | $$    | $$$$$$$$
| $$  \ $$| $$  | $$  | $$ /$$| $$| $$_____/| $$ | $$ | $$| $$  | $$| $$ /$$__  $$  | $$ /$$| $$_____/
| $$$$$$$/|  $$$$$$/  |  $$$$/| $$|  $$$$$$$| $$ | $$ | $$| $$$$$$$/| $$|  $$$$$$$  |  $$$$/|  $$$$$$$
|_______/  \______/    \___/  |__/ \_______/|__/ |__/ |__/| $$____/ |__/ \_______/   \___/   \_______/
                                                          | $$                                        
                                                          | $$                                        
                                                          |__/                                               
""" + color.RESET)


def debug_yellow(type: str, args: str):
    """
    Debugging function that prints the current time and the provided argument.
    """
    time = datetime.datetime.now().strftime("%H:%M:%S")
    print(
        f'{color.GRAY}[{color.YELLOW}{type}{color.GRAY}] {color.GRAY}({color.LIGHT_GRAY}{time}{color.GRAY}) {color.RESET}{args}')


def debug_red(type: str, args: str):
    """
    Debugging function that prints the current time and the provided argument in red.
    """
    time = datetime.datetime.now().strftime("%H:%M:%S")
    print(
        f'{color.GRAY}[{color.RED}{type}{color.GRAY}] {color.GRAY}({color.LIGHT_GRAY}{time}{color.GRAY}) {color.RESET}{args}')


def debug_green(type: str, args: str):
    """
    Debugging function that prints the current time and the provided argument in green.
    """
    time = datetime.datetime.now().strftime("%H:%M:%S")
    print(
        f'{color.GRAY}[{color.GREEN}{type}{color.GRAY}] {color.GRAY}({color.LIGHT_GRAY}{time}{color.GRAY}) {color.RESET}{args}')


def debug_blue(type: str, args: str):
    """
    Debugging function that prints the current time and the provided argument in blue.
    """
    time = datetime.datetime.now().strftime("%H:%M:%S")
    print(
        f'{color.GRAY}[{color.BLUE}{type}{color.GRAY}] {color.GRAY}({color.LIGHT_GRAY}{time}{color.GRAY}) {color.RESET}{args}')


def debug_stats(bot: discord.Bot):
    """
    Debugging function that prints the current time and the provided argument in blue.
    """
    bot_name = str(bot.user)
    bot_id = str(bot.application_id)
    loaded_commands = str(Stats.loaded_commands)
    loaded_tasks = str(Stats.loaded_tasks)
    loaded_events = str(Stats.loaded_events)
    ping = str(round(bot.latency * 1000)) + "ms"

    max_len = max(len(bot_name), len(bot_id), len(loaded_commands), len(loaded_tasks), len(loaded_events), len(ping))

    print()
    print(
        color.LIGHT_GRAY + f"╭{'─' * (max_len + 2)}┬{'─' * (max_len + 2)}┬{'─' * (max_len + 2)}┬{'─' * (max_len + 2)}┬{'─' * (max_len + 2)}┬{'─' * (max_len + 2)}╮")
    print(
        color.LIGHT_GRAY + f"│ {'Bot':>{max_len}} │ {'ID':>{max_len}} │ {'Commands':>{max_len}} │ {'Tasks':>{max_len}} │ {'Events':>{max_len}} │ {'Ping':>{max_len}} │")
    print(
        color.LIGHT_GRAY + f"│{'─' * (max_len + 2)}┼{'─' * (max_len + 2)}┼{'─' * (max_len + 2)}┼{'─' * (max_len + 2)}┼{'─' * (max_len + 2)}┼{'─' * (max_len + 2)}┼")
    print(
        f"│ {color.LIGHT_GREEN}{bot_name:>{max_len}} {color.LIGHT_GRAY}│ {color.LIGHT_BLUE}{bot_id:>{max_len}} {color.LIGHT_GRAY}│ {color.LIGHT_PINK}{loaded_commands:>{max_len}} {color.LIGHT_GRAY}│ {color.YELLOW}{loaded_tasks:>{max_len}} {color.LIGHT_GRAY}│ {color.PINK}{loaded_events:>{max_len}} {color.LIGHT_GRAY}│ {color.ORANGE}{ping:>{max_len}} {color.LIGHT_GRAY}│")
    print(
        color.LIGHT_GRAY + f"╰{'─' * (max_len + 2)}┴{'─' * (max_len + 2)}┴{'─' * (max_len + 2)}┴{'─' * (max_len + 2)}┴{'─' * (max_len + 2)}┴{'─' * (max_len + 2)}╯")


def extension_loader(bot: discord.Bot):
    """
    Load all extensions (commands, events) for the provided bot.
    """
    for path in ["events", "commands", "tasks"]:
        for filename in os.listdir(path):
            if "#" in filename:
                if path == "commands":
                    debug_red("Extensions", f"Skipping command {filename.replace("#", "")} because it is disabled.")
                elif path == "events":
                    debug_red("Extensions", f"Skipping event {filename.replace("#", "")} because it is disabled.")
                elif path == "tasks":
                    debug_red("Extensions", f"Skipping task {filename.replace("#", "")} because it is disabled.")
                continue
            if filename.endswith(".py"):
                if path == "events":
                    bot.load_extension(path + "." + filename[:-3])
                    Stats.loaded_events += 1
                elif path == "commands":
                    bot.load_extension(path + "." + filename[:-3])
                    Stats.loaded_commands += 1
                elif path == "tasks":
                    bot.load_extension(path + "." + filename[:-3])
                    Stats.loaded_tasks += 1
    debug_green("Extensions", "All extensions loaded successfully.")


def get_bot_settings(key: str):
    """
    Get the value of the provided key from the bot's settings.
    """

    if os.path.exists("utils/settings_debug.json"):
        # Open the file
        with open("utils/settings_debug.json", "r") as file:
            settings = json.load(file)
            if key in settings:
                return settings[key]
            else:
                debug_yellow("BotSettings", f"Key {key} not found in settings_debug.json")
                return None
    else:
        with open("utils/settings_operational.json", "r") as file:
            settings = json.load(file)
            if key in settings:
                return settings[key]
            else:
                debug_yellow("BotSettings", f"Key {key} not found in settings_operational.json")
                return None


class EmbedBuilder:
    """
    A class to build embeds for discord messages.
    """

    @staticmethod
    def default_embed(title: str, description: str):
        """
        Build a default embed with the provided title, description, thumbnail_url, and image_url.
        """
        embed = discord.Embed(title=title, description=description, color=int(get_bot_settings('hex_color'), 16))
        embed.set_author(icon_url=get_bot_settings('avatar_url'), name=get_bot_settings('bot_name'))
        embed.set_image(url=get_bot_settings('footer_image_url'))
        return embed

    @staticmethod
    def error_embed(title: str, description: str):
        """
        Build an error embed with the provided title, description, thumbnail_url, and image_url.
        """
        embed = discord.Embed(title=title, description=description, color=0xff0000)
        embed.set_author(icon_url=get_bot_settings('avatar_url'), name=get_bot_settings('bot_name'))
        embed.set_image(url=get_bot_settings('footer_image_url'))
        return embed


async def has_permissions(ctx: discord.ApplicationContext, user: discord.Member, permission: str):
    """
    Check if the provided user has the provided permission in the provided context.
    If the user does not have the permission, send an error embed.
    """
    permissions = user.guild_permissions
    if getattr(permissions, permission):
        pass
    else:
        embed = EmbedBuilder.error_embed(title="",
                                         description=f"# Keine Permissions\nDir fehlt die Berechtigung `{permission}`, um diese Aktion auszuführen.")
        await ctx.respond(embed=embed, ephemeral=True)
        return


async def has_role(user: discord.Member, role: int):
    """
    Check if the provided user has the provided role in the provided context.
    If the user does not have the role, send an error embed.
    """
    # Check role by id
    if role in [role.id for role in user.roles]:
        return True
    else:
        return False
