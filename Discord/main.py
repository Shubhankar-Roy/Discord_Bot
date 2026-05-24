import discord
from discord.ext import commands
import  logging
from dotenv import load_dotenv
import os

load_dotenv()
token = os.getenv("DISCORD_TOKEN")

handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix='!', intents=intents)

secret_role = "Sherrr"
#handling events

@bot.event
async def on_ready():
    print(f"We are ready to go!, {bot.user.name}")

# when new member join in
@bot.event
async def on_member_join(member: discord.Member):
    await member.send(f"Welcome to the server, {member.name}")

@bot.event
async def on_message(message: discord.Message):
    print(f"I just saw a message!, {message.author}: {message.content}")
    if message.author == bot.user:
        return

    if "shit" in message.content.lower():
        await message.delete()
        await message.channel.send(f"{message.author.mention} -don't use this word!")

    await bot.process_commands(message)

@bot.command()
async def hello(ctx):
    await ctx.send(f"Hello {ctx.author.mention}!")

@bot.command()
async def assign(ctx):
    role = discord.utils.get(ctx.guild.roles, name=secret_role)
    if role:
        await ctx.author.add_roles(role)
        await ctx.send(f"{ctx.author.mention} You are now assigned {secret_role}!")
    else:
        await ctx.send("Role doesn't exist!")

@bot.command()
async def remove(ctx):
    role = discord.utils.get(ctx.guild.roles, name=secret_role)
    if role:
        await ctx.author.remove_roles(role)
        await ctx.send(f"{ctx.author.mention} has had the {secret_role} role is removed!")
    else:
        await ctx.send("Role doesn't exist!")

@bot.command()
async def dm(ctx, *, msg):
    await ctx.author.send(f"You said {msg}!")

@bot.command()
async def reply(ctx):
    await ctx.reply("This is a reply to your message!")

@bot.command()
async def poll(ctx, *, questions):
    embed = discord.Embed(title="Poll!", color=discord.Color.green(), description=questions)
    poll_message = await ctx.send(embed=embed)
    await poll_message.add_reaction("👍")
    await poll_message.add_reaction("👎")

@bot.command()
@commands.has_role(secret_role)
async def secret(ctx):
    await ctx.send("Welcome to the club!")

@secret.error
async def secret_error(ctx, error):
    if isinstance(error, commands.MissingRole):
        await ctx.send("You do not have the permission to do that!")


bot.run(token, log_handler=handler, log_level=logging.DEBUG)