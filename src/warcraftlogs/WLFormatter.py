from datetime import datetime

import discord

class WLFormatter:
    def __init__(self, data):
        self.data = data


    def create_embed(self):
        embed = discord.Embed(
            title=self.read_embed_title(),
            description=self.read_embed_description(),
        )

        boss_names, boss_tries, boss_first_kills = self.read_boss_lists()

        embed.add_field(name="First Try", value=boss_first_kills, inline=True)
        embed.add_field(name="Tries", value=boss_tries, inline=True)
        embed.add_field(name="Boss", value=boss_names, inline=True)

        return embed

    def read_embed_description(self):
        source_starttime = self.data["reportData"]["report"]["startTime"]
        source_endtime = self.data["reportData"]["report"]["endTime"]

        startTime = datetime.fromtimestamp(float(source_starttime) / 1e3)
        endTime = datetime.fromtimestamp(float(source_endtime) / 1e3)

        duration = endTime - startTime

        hours, remainder = divmod(duration.total_seconds(), 3600)
        minutes, seconds = divmod(remainder, 60)

        zone_name = self.data["reportData"]["report"]["zone"]["name"]

        return "Duration: " + '{:02}:{:02}'.format(int(hours), int(minutes)) + "h \nZone: " + zone_name
    def read_embed_title(self):

        title = self.data["reportData"]["report"]["title"]

        return title + " - " + str(datetime.now().date())

    def read_boss_lists(self):
        fights = self.data["reportData"]["report"]["fights"]
        encounters = self.data["reportData"]["report"]["zone"]["encounters"]

        boss_data = {};
        
        for fight in fights:
            for encounter in encounters:
                if not fight["encounterID"] == encounter["id"]: continue

                if boss_data.get(encounter["id"]) is None:
                    boss_data[encounter["id"]] = {"name":encounter["name"], "tries": 1, "first_kill": True}
                else:
                    boss_data[encounter["id"]]["tries"] += 1
                    boss_data[encounter["id"]]["first_kill"] = False

        boss_names = "\n".join([x["name"] for x in boss_data.values()])
        boss_tries = "\n".join([str(x["tries"]) for x in boss_data.values()])

        #TODO Make this into emotes
        boss_first_kills = "\n".join([str(x["first_kill"]) for x in boss_data.values()])

        return boss_names, boss_tries, boss_first_kills
