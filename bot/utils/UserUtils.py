import discord

ONLINE = "online"
IDLE = "idle"

sr_role_2_emoji_map = {
    "Silver 1500+ sr": "<:silver:597893469448437788>",
    "Gold 2000+ sr": "<:gold:597893476541268013>",
    "Platinum 2500+ sr": "<:platinum:597893481087631370>",
    "Diamond 3000+ sr": "<:diamond:597893483767791617>",
    "Master 3500+ sr": "<:master:597893481658187806>",
    "GrandMaster 4000+ sr": "<:grandmaster:597893486179647583>",
    "No SR": "<:doomfist:602169882112426013>"
}


def find_sr_role(roles):
    return next((role.name for role in roles if " sr" in role.name), "No SR")


def get_rank_emoji(roles):
    sr_role = find_sr_role(roles)
    return sr_role_2_emoji_map[sr_role]


def get_nick_or_name(player):
    rank_emoji = get_rank_emoji(player.roles)
    if player.nick is not None:
        return player.nick + " " + rank_emoji
    else:
        return player.name + " " + rank_emoji


def remove_players_from_list(list_to_remove, list_remove_from):
    for player_to_remove in list_to_remove:
        for player in list_remove_from:
            if player_to_remove.id == player.id:
                list_remove_from.remove(player)
                break


def print_players(players):
    if len(players) > 0:
        return ",".join([get_nick_or_name(p) for p in players])


def generate_player_list_embed(players, list_name):
    player_names = '\n'.join([get_nick_or_name(m) for m in players])
    return discord.Embed(title="{} member(s) in {}".format(len(players), list_name),
                         description=player_names,
                         color=discord.Color.blue())


def filter_spectators(players):
    return [p for p in players if p.status.value is not ONLINE]
