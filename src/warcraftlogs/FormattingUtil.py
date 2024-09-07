class FormattingUtil:

    @staticmethod
    def get_class_emoji_for_class(class_name):
        if class_name.lower() == 'warrior':
            return "<:ClassIcon_warrior:1038504922225844265>"
        if class_name.lower() == 'warlock':
            return "<:ClassIcon_warlock:1038504923861618840>"

        if class_name.lower() == 'rogue':
            return "<:ClassIcon_rogue:1038504927015743508>"
        if class_name.lower() == 'demonhunter':
            return "<:ClassIcon_demon_hunter:1038504919897997414>"
        if class_name.lower() == 'deathknight':
            return "<:ClassIcon_deathknight:1038504921189863455>"
        if class_name.lower() == 'hunter':
            return "<:ClassIcon_hunter:1038504934481596457>"
        if class_name.lower() == 'priest':
            return "<:ClassIcon_priest:1038504928114651277>"
        if class_name.lower() == 'shaman':
            return "<:ClassIcon_shaman:1038504925405118476>"
        if class_name.lower() == 'mage':
            return "<:ClassIcon_mage:1038504933202346054>"
        if class_name.lower() == 'monk':
            return "<:ClassIcon_monk:1038504931386216458>"
        if class_name.lower() == 'druid':
            return "<:ClassIcon_druid:1038504935869919393>"
        if class_name.lower() == 'paladin':
            return "<:ClassIcon_paladin:1038504929775587328>"
        if class_name.lower() == 'evoker':
            return "🐉"
        return "<:read_the_error:508733110154690560>"

    @staticmethod
    def get_embed_value_for_fight_kill(tries, kill, best_percentage):
        if tries == 1 and kill:
            return "⭐"
        if kill:
            return "✅"

        if not kill:
            return str(best_percentage) + " %"