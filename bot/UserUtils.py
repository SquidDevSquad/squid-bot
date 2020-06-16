def get_nick_or_name(player):
    if player.nick is not None:
        return player.nick
    else:
        return player.name


def find(player_id, players):
    return next((p for p in players if p.id == player_id), False)
