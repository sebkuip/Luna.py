import random
import time
import typing

import discord
from discord.ext import commands


class Utils(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(
        help="Shows the Avatar of a User that is given",
        aliases=["av", "pfp", "profilepic", "profilepicture"],
    )
    async def avatar(self, ctx, user: discord.User = None):
        if user is None:
            user = ctx.author
        await ctx.send(user.avatar.url)

    @commands.command(help="Shows the latency the bot is experiencing")
    async def ping(self, ctx):
        before = time.perf_counter()
        msg = await ctx.reply("testing...", mention_author=False)
        await msg.edit(
            content=f"pong!\nbot latency: {round((time.perf_counter() - before) * 1000)}ms\nwebsocket latency: {round(self.bot.latency * 1000)}ms"
        )

    @commands.command(help="Send a message as the bot")
    @commands.is_owner()
    async def echo(
        self, ctx, channel: typing.Optional[discord.TextChannel] = None, *, text
    ):
        if channel is None:
            channel = ctx.channel
        await channel.send(text)
        await ctx.message.delete()

    @commands.command(help="Roll the dice", aliases=["rtd", "rollthedice"])
    async def dice(self, ctx, *, dice: typing.Optional[str] = None):
        if dice and "d" in dice:
            dice = dice.split("d")
            if len(dice) == 2:
                dice[0] = int(dice[0])
                dice[1] = int(dice[1])
                if dice[0] > 0 and dice[1] > 0:
                    result = 0
                    for _ in range(dice[0]):
                        result += random.randint(1, dice[1])
                    await ctx.reply(f"You rolled {dice[0]}d{dice[1]} and got {result}")
            else:
                await ctx.reply("Invalid dice format")
        elif dice is not None:
            try:
                await ctx.reply(f"You rolled {random.randint(1, int(dice))}")
            except ValueError:
                await ctx.reply("Invalid dice format")
        else:
            await ctx.reply(f"You rolled {random.randint(1, 6)}")


async def setup(bot: commands.Bot):
    await bot.add_cog(Utils(bot))
