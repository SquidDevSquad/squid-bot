import functools

import Config
from log import LoggerFactory

log = LoggerFactory.get_logger(__name__)


def only_allowed_channels(f):
    @functools.wraps(f)
    async def wrapped(self, ctx, *args, **kwargs):
        if ctx.message.channel.id not in Config.ALLOWED_TEXT_CHANNEL_IDS:
            await ctx.send('Not allowed to operate on this channel')
            return
        else:
            await f(self, ctx, *args, **kwargs)

    return wrapped


def is_registration_open(f):
    @functools.wraps(f)
    async def wrapped(self, ctx, *args, **kwargs):
        if not self.client.global_variables.registration_opened:
            log.debug("Registrations are not open")
            await ctx.send(ctx.author.mention + " Registrations are not open yet")
            return
        else:
            await f(self, ctx, *args, **kwargs)

    return wrapped


def is_admin(f):
    @functools.wraps(f)
    async def wrapped(self, ctx, *args, **kwargs):
        if ctx.author.id not in Config.ADMIN_IDS:
            await ctx.send('You don\'t have the permissions to use this command')
            return
        else:
            await f(self, ctx, *args, **kwargs)

    return wrapped
