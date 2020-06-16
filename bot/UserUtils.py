def get_nick_or_name(player):
    if player.nick is not None:
        return player.nick
    else:
        return player.name
