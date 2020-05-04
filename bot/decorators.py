import functools
import Config


def only_allowed_channels(f):
    @functools.wraps(f)
    async def wrapped(self, ctx, *args, **kwargs):
        if ctx.message.channel.id not in Config.ALLOWED_CHANNEL:
            await ctx.send('Not allowed to operate on this channel')
            return
        else:
            await f(self, ctx, *args, **kwargs)

    return wrapped


def is_admin(f):
    @functools.wraps(f)
    async def wrapped(self, ctx, *args, **kwargs):
        if ctx.author.id not in Config.ALLOWED_USER_TO_ADMIN_COMMANDS:
            await ctx.send('You don\'t have the permissions to use this command')
            return
        else:
            await f(self, ctx, *args, **kwargs)

    return wrapped
