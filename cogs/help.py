import discord
from discord.ext import commands

class Paginator(discord.ui.View):
    def __init__(self, pages: list[discord.Embed], message: discord.Message, user: discord.User):
        super().__init__(timeout=30)
        self.pages = pages
        self.message = message
        self.user = user

        self.current = 0

    async def stop(self):
        for child in self.children:
            child.disabled = True
        super().stop()
        await self.message.edit(embed=self.pages[self.current], view=self)

    async def on_timeout(self):
        await self.stop()

    async def on_back(self):
        self.current -= 1
        if self.current < 0:
            self.current = len(self.pages) - 1

    async def on_next(self):
        self.current += 1
        if self.current >= len(self.pages):
            self.current = 0

    async def interaction_check(self, interaction: discord.Interaction) -> bool:
        return interaction.user == self.user

    @discord.ui.button(label="<", style=discord.ButtonStyle.primary)
    async def back_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self.on_back()
        await interaction.response.edit_message(embed=self.pages[self.current])

    @discord.ui.button(label=">", style=discord.ButtonStyle.primary)
    async def next_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self.on_next()
        await interaction.response.edit_message(embed=self.pages[self.current])

    @discord.ui.button(label="X", style=discord.ButtonStyle.danger)
    async def stop_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self.stop()
        await interaction.response.edit_message(embed=self.pages[self.current])

class myHelpCommand(commands.HelpCommand):
    async def generate_mapping_help(self, mapping: dict[commands.Cog, list[commands.Command]]):
        embeds: list[discord.Embed] = []
        for cog in reversed(mapping.keys()):
            if cog is not None:
                embed: discord.Embed = discord.Embed(title=cog.qualified_name, color=0x00ff00)
            else:
                embed: discord.Embed = discord.Embed(title="No Category", color=0x00ff00)

            filtered_commands = await self.filter_commands(mapping[cog])
            for command in filtered_commands:
                if len(embed.fields) == 25:
                    embeds.append(embed)
                    if cog is not None:
                        embed: discord.Embed = discord.Embed(title=cog.qualified_name, color=0x00ff00)
                    else:
                        embed: discord.Embed = discord.Embed(title="No Category", color=0x00ff00)

                if command.aliases != []:
                    embed.add_field(name=command.name + " " + command.signature, value=command.help + "\n\n**Aliases**: " + ", ".join(command.aliases), inline=False)
                else:
                    embed.add_field(name=command.name + " " + command.signature, value=command.help, inline=False)
            embeds.append(embed)
        return embeds

    async def send_bot_help(self, mapping):
        message = await self.get_destination().send("Loading help...")
        embeds = await self.generate_mapping_help(mapping)
        paginator = Paginator(embeds, message, self.context.author)
        await message.edit(content=None, embed=embeds[0], view=paginator)

    async def send_command_help(self, command):
        await self.context.send("This is help command")

    async def send_group_help(self, group):
        await self.context.send("This is help group")

    async def send_cog_help(self, cog):
        await self.context.send("This is help cog")

class Help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.bot.help_command = myHelpCommand()

async def setup(bot: commands.Bot):
    await bot.add_cog(Help(bot))