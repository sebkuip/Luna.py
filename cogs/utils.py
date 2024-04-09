import discord
from discord.ext import commands

class Utils(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(help="Shows the Avatar of a User that is given", aliases=['av', 'pfp', 'profilepic', 'profilepicture'])
    async def avatar(self, ctx, user: discord.User = None):
        if user is None:
            user = ctx.author
        await ctx.send(user.avatar.url)

async def setup(bot: commands.Bot):
    await bot.add_cog(Utils(bot))