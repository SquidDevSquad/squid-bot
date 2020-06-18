import discord

ONLINE = "online"


def get_nick_or_name(player):
    if player.nick is not None:
        return player.nick
    else:
        return player.name


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
    return [p for p in players if p.status is not ONLINE]
