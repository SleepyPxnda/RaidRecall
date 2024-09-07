from datetime import datetime

import discord

from commands.warcraftlogs.FormattingUtil import FormattingUtil
from src.utils import debug_red

def chunks(lst, n):
    """Yield successive n-sized chunks from lst."""
    for i in range(0, len(lst), n):
        yield lst[i:i + n]


class WLFormatter:
    def __init__(self, data : any):
        self.data = data

    def create_embed(self, code):
        embed = discord.Embed(
            title=self.read_embed_title(),
            description=self.read_embed_description(),
        )

        kill_value, boss_name = self.read_boss_lists()

        embed.add_field(name="Result", value="\n".join(kill_value), inline=True)
        embed.add_field(name="Boss", value="\n".join(boss_name), inline=True)

        embed.add_field(name="Useful Links", value="https://www.warcraftlogs.com/reports/" + code + " \n"
                                          + "https://www.wipefest.gg/report/" + code + " \n"
                                          + "https://wowanalyzer.com/report/" + code + " \n", inline=False)
        return embed

    def create_performance_embeds(self):
        performance_data = self.create_ranking_list()

        embeds = []

        for data in performance_data:
            embed = discord.Embed(
                title=data["boss_name"],
            )

            dps_strings = [FormattingUtil.get_role_icon_for_role(str(dps["role"])) + " " + str(dps["dmg_percent"]) + " " + str(dps["ilvl"]) +  " " + FormattingUtil.get_class_emoji_for_class(dps["class"]) + " " + dps["name"] for dps in data["dps"]]

            split_dps_strings = chunks(dps_strings, 5)

            embed.add_field(name="DPS", value="Role/Parse/ILvl/Class/Name", inline=True)
            for split_string in split_dps_strings:
                embed.add_field(name="", value="\n".join(split_string), inline=False)

            hps_strings = [FormattingUtil.get_role_icon_for_role(str(hps["role"])) + " " + str(hps["hps_percent"]) + " " + str(hps["ilvl"]) + " " + FormattingUtil.get_class_emoji_for_class(hps["class"]) + " " + hps["name"] for hps in data["hps"]]

            split_hps_strings = chunks(hps_strings, 5)

            embed.add_field(name="HPS", value="Role/Parse/ILvl/Class/Name", inline=True)
            for split_string in split_hps_strings:
                embed.add_field(name="", value="\n".join(split_string), inline=False)

            embeds.append(embed)

        return embeds

    def read_embed_description(self):
        source_starttime = self.data["reportData"]["report"]["startTime"]
        source_endtime = self.data["reportData"]["report"]["endTime"]

        start_time = datetime.fromtimestamp(float(source_starttime) / 1e3)
        end_time = datetime.fromtimestamp(float(source_endtime) / 1e3)

        duration = end_time - start_time

        hours, remainder = divmod(duration.total_seconds(), 3600)
        minutes, seconds = divmod(remainder, 60)

        zone_name = self.data["reportData"]["report"]["zone"]["name"]

        return "Duration: " + '{:02}:{:02}'.format(int(hours), int(minutes)) + "h \nZone: " + zone_name

    def read_embed_title(self):

        title = self.data["reportData"]["report"]["title"]
        date = datetime.fromtimestamp(float(self.data["reportData"]["report"]["startTime"]) / 1e3)

        difficulty = ",".join(set([str(fight["difficulty"]) for fight in self.data["reportData"]["report"]["fights"]])).replace("3","Normal").replace("4", "Heroic").replace("5", "Mythic")

        return title + " - " + str(date.date()) + " - " + difficulty

    def read_boss_lists(self):
        fights = self.data["reportData"]["report"]["fights"]
        encounters = self.data["reportData"]["report"]["zone"]["encounters"]

        boss_data = {}

        for fight in fights:
            for encounter in encounters:
                if not fight["encounterID"] == encounter["id"]: continue

                if boss_data.get(encounter["id"]) is None:
                    boss_data[encounter["id"]] = {"name": encounter["name"], "tries": 1, "best_percentage": fight["bossPercentage"], "kill": fight["kill"]}
                else:
                    boss_data[encounter["id"]]["tries"] += 1
                    if boss_data[encounter["id"]]["best_percentage"] > fight["bossPercentage"]:
                        boss_data[encounter["id"]]["best_percentage"] = fight["bossPercentage"]
                    if not boss_data[encounter["id"]]["kill"] and fight["kill"]:
                        boss_data[encounter["id"]]["kill"] = True


        boss_data = [value for value in boss_data.values()]
        boss_name = [boss["name"] for boss in boss_data]
        kill_value = [FormattingUtil.get_embed_value_for_fight_kill(boss["tries"], boss["kill"], boss["best_percentage"]) for boss in boss_data]

        return kill_value, boss_name

    def create_ranking_list(self):
        result = []
        fights = self.data["reportData"]["report"]["fights"]
        actors = self.data["reportData"]["report"]["masterData"]["actors"]
        dps_parses = self.data["reportData"]["report"]["dpsParses"]["data"]
        hps_parses = self.data["reportData"]["report"]["hpsParses"]["data"]

        unique_boss_ids = set([fight["encounterID"] for fight in fights])

        for boss_id in unique_boss_ids:
            fights_for_boss = [fight for fight in fights if fight["encounterID"] == boss_id]
            unique_players_in_boss_fight = {}

            for fight in fights_for_boss:
                for player_id in fight["friendlyPlayers"]:
                    if player_id not in unique_players_in_boss_fight:
                        player_data = [player for player in actors if player["id"] == player_id][0]

                        unique_players_in_boss_fight[player_id] = {"player": player_data, "participated_fights": 1}
                    else:
                        unique_players_in_boss_fight[player_id]["participated_fights"] += 1

            dps_parses_for_boss = [dps_data for dps_data in dps_parses if dps_data["encounter"]["id"] == boss_id]
            hps_parses_for_boss = [hps_data for hps_data in hps_parses if hps_data["encounter"]["id"] == boss_id]

            if len(dps_parses_for_boss) == 0:
                debug_red("RANKING", "No dps parses found for " + str(boss_id))
                continue

            if len(hps_parses_for_boss) == 0:
                debug_red("RANKING", "No hps parses found for " + str(boss_id))
                continue

            dmg_list = self.create_dps_list_for_boss(dps_parses_for_boss[0], unique_players_in_boss_fight)
            hps_list = self.create_hps_list_for_boss(hps_parses_for_boss[0], unique_players_in_boss_fight)

            dmg_list.sort(reverse=True, key=lambda entry: entry["dmg_percent"])
            hps_list.sort(reverse=True, key=lambda entry: entry["hps_percent"])

            boss_name = [boss["name"] for boss in self.data["reportData"]["report"]["zone"]["encounters"] if boss_id == boss["id"]][0]

            result.append({"boss_name": boss_name, "hps": hps_list, "dps": dmg_list})

        return result

    def create_dps_list_for_boss(self, dps_parses, players):
        result = []
        for player in players.values():
            for character in dps_parses["roles"]["tanks"]["characters"]:
                if character["name"] == player["player"]["name"]:
                    result.append({
                        "role": "tank",
                        "name": player["player"]["name"],
                        "class": character["class"],
                        "spec": character["spec"],
                        "dmg_percent": character["bracketPercent"],
                        "participated_fights": player["participated_fights"],
                        "ilvl": character["bracketData"]
                    })

            for character in dps_parses["roles"]["dps"]["characters"]:
                if character["name"] == player["player"]["name"]:
                    result.append({
                        "role": "dps",
                        "name": player["player"]["name"],
                        "class": character["class"],
                        "spec": character["spec"],
                        "dmg_percent": character["bracketPercent"],
                        "participated_fights": player["participated_fights"],
                        "ilvl": character["bracketData"]
                    })

            for character in dps_parses["roles"]["healers"]["characters"]:
                if character["name"] == player["player"]["name"]:
                    result.append({
                        "role": "healer",
                        "name": player["player"]["name"],
                        "class": character["class"],
                        "spec": character["spec"],
                        "dmg_percent": character["bracketPercent"],
                        "participated_fights": player["participated_fights"],
                        "ilvl": character["bracketData"]
                    })
        return result

    def create_hps_list_for_boss(self, hps_parses, players):
        result = []
        for player in players.values():
            for character in hps_parses["roles"]["tanks"]["characters"]:
                if character["name"] == player["player"]["name"]:
                    result.append({
                        "role": "tank",
                        "name": player["player"]["name"],
                        "class": character["class"],
                        "spec": character["spec"],
                        "hps_percent": character["bracketPercent"],
                        "participated_fights": player["participated_fights"],
                        "ilvl": character["bracketData"]
                    })

            for character in hps_parses["roles"]["dps"]["characters"]:
                if character["name"] == player["player"]["name"]:
                    result.append({
                        "role": "dps",
                        "name": player["player"]["name"],
                        "class": character["class"],
                        "spec": character["spec"],
                        "hps_percent": character["bracketPercent"],
                        "participated_fights": player["participated_fights"],
                        "ilvl": character["bracketData"]
                    })

            for character in hps_parses["roles"]["healers"]["characters"]:
                if character["name"] == player["player"]["name"]:
                    result.append({
                        "role": "healer",
                        "name": player["player"]["name"],
                        "class": character["class"],
                        "spec": character["spec"],
                        "hps_percent": character["bracketPercent"],
                        "participated_fights": player["participated_fights"],
                        "ilvl": character["bracketData"]
                    })
        return result

