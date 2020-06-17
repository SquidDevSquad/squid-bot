def get_nick_or_name(player):
    if player.nick is not None:
        return player.nick
    else:
        return player.name


def find(player_id, players):
    return next((p for p in players if p.id == player_id), False)


def print_players(players):
    if len(players) > 0:
        return ",".join([get_nick_or_name(p) for p in players])
