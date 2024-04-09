import discord
from discord.ext import commands

import sqlite3
import os
from dotenv import load_dotenv

load_dotenv(".env")

token = os.getenv("TOKEN")

bot = commands.Bot(command_prefix='!', intents=discord.Intents.all())

@bot.event
async def on_ready():
    print(f"{bot.user} has connected to Discord!")
    print(f"Username is {bot.user.name}")
    print(f"ID is {bot.user.id}")
    print(f"Keep this window open to keep the bot running.")

    # extensions
    await load_extensions()

async def load_extensions():
    if __name__ == "__main__":

        status = {}
        for extension in os.listdir("./cogs"):
            if extension.endswith(".py"):
                status[extension] = "X"
        errors = []

        for extension in status:
            if extension.endswith(".py"):
                try:
                    await bot.load_extension(f"cogs.{extension[:-3]}")
                    status[extension] = "L"
                except Exception as e:
                    errors.append(e)

        maxlen = max(len(str(extension)) for extension in status)
        for extension in status:
            print(f" {extension.ljust(maxlen)} | {status[extension]}")
        print(errors) if errors else print("no errors during loading")

@bot.command(help="Load a cog")
@commands.is_owner()
async def load(ctx, name):
    name = name.lower()
    status = {}
    for extension in os.listdir(f"./{name}"):
        if extension.endswith(".py"):
            status[extension] = "X"
    errors = []

    for extension in status:
        if extension.endswith(".py"):
            try:
                await bot.load_extension(f"{name}.{extension[:-3]}")
                status[extension] = "L"
            except Exception as e:
                errors.append(e)

    maxlen = max(len(str(extension)) for extension in status)
    extensionstatus = ""
    for extension in status:
        extensionstatus += (f" {extension.ljust(maxlen)} | {status[extension]}\n")
    embed = discord.Embed(title=f"load report of {name}", description=extensionstatus, color=0x00ff00 if not errors else 0xFF0000)
    if errors:
        embed.add_field(name="Errors", value=str(errors))
    await ctx.send(embed=embed)


@bot.command(help="Unload a cog")
@commands.is_owner()
async def unload(ctx, name):
    name = name.lower()
    status = {}
    for extension in os.listdir(f"./{name}"):
        if extension.endswith(".py"):
            status[extension] = "X"
    errors = []

    for extension in status:
        if extension.endswith(".py"):
            try:
                await bot.unload_extension(f"{name}.{extension[:-3]}")
                status[extension] = "U"
            except Exception as e:
                errors.append(e)

    maxlen = max(len(str(extension)) for extension in status)
    extensionstatus = ""
    for extension in status:
        extensionstatus += (f" {extension.ljust(maxlen)} | {status[extension]}\n")
    embed = discord.Embed(title=f"Unload report of {name}", description=extensionstatus, color=0x00ff00 if not errors else 0xFF0000)
    if errors:
        embed.add_field(name="Errors", value=str(errors))
    await ctx.send(embed=embed)


@bot.command(help="Reload a cog")
@commands.is_owner()
async def reload(ctx, name):
    name = name.lower()
    status = {}
    for extension in os.listdir(f"./{name}"):
        if extension.endswith(".py"):
            status[extension] = "X"
    errors = []

    for extension in status:
        if extension.endswith(".py"):
            try:
                await bot.reload_extension(f"{name}.{extension[:-3]}")
                status[extension] = "R"
            except Exception as e:
                errors.append(e)

    maxlen = max(len(str(extension)) for extension in status)
    extensionstatus = ""
    for extension in status:
        extensionstatus += (f" {extension.ljust(maxlen)} | {status[extension]}\n")
    embed = discord.Embed(title=f"Reload report of {name}", description=extensionstatus, color=0x00ff00 if not errors else 0xFF0000)
    if errors:
        embed.add_field(name="Errors", value=str(errors))
    await ctx.send(embed=embed)

@bot.command(help="Show all loaded cogs")
@commands.is_owner()
async def loaded(ctx):
    embed = discord.Embed(title="Loaded cogs", description="\n".join(bot.cogs), color=0x00ff00)
    await ctx.reply(embed=embed, mention_author=False)

bot.run(token)