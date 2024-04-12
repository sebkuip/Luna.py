import traceback

import discord
from discord.ext import commands


class ErrorHandler(commands.Cog):
    def __init__(self, bot):
        self.bot = bot  # This is the bot instance, it lets us interact with most things

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if hasattr(ctx.command, "on_error"):
            return

        error = getattr(error, "original", error)

        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(
                f"Command usage: `>{ctx.command.name} {ctx.command.signature}`"
            )
            return

        # elif isinstance(error, FileNotFoundError):
        #     pass
        # elif isinstance(error, commands.NotOwner):
        #     pass
        # elif isinstance(error, commands.MemberNotFound):
        #     pass
        # elif isinstance(error, commands.BadArgument):
        #     pass
        # elif isinstance(error, commands.CommandNotFound):
        #     pass
        # lif isinstance(error, commands.MissingPermissions):
        #     pass
        # elif isinstance(error, commands.BotMissingPermissions):
        #    pass
        # elif isinstance(error, commands.DisabledCommand):
        #     pass
        # elif isinstance(error, commands.PrivateMessageOnly):
        #    pass
        # elif isinstance(error, discord.Forbidden):
        #     embed.add_field(
        #         name=f"**Forbidden**",
        #         value=f"Looks like the bot is missing permissions to execute this command.",
        #     )
        # elif isinstance(error, discord.ext.commands.errors.CommandInvokeError):
        # embed.add_field(name=f'**CommandInvokeError**',
        # value=f'Looks like something is wrong with the command. This could be because the page '
        # f'does not exist.')

async def setup(bot):
    await bot.add_cog(ErrorHandler(bot))
