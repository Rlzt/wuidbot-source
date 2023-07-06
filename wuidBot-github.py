import discord
from datetime import datetime
import random
from discord.ext import commands
import asyncio
import warnings
import aiohttp
from discord import Client
import os
import json


bot = discord.Bot()

intents = discord.Intents.default()
intents.members = True
XP_FILE = 'xp_data.json'

@bot.slash_command(name = "hello", description = "Say hello to the bot")
async def hi(ctx):
    await ctx.send("Hey!")

@bot.slash_command(name = "version", description = "Check Bot Version")
async def ver(ctx):
    await ctx.send("Version 1.0.5 - Beta Branch - By <@895788406347558922>")

def add_xp_to_user(guild_id, user_id, xp_amount):
    xp_data = load_xp_data()

    if str(guild_id) not in xp_data:
        xp_data[str(guild_id)] = {}

    guild_data = xp_data[str(guild_id)]

    if str(user_id) not in guild_data:
        guild_data[str(user_id)] = 0

    guild_data[str(user_id)] += xp_amount

    save_xp_data(xp_data)

def remove_xp_from_user(guild_id, user_id, xp_amount):
    xp_data = load_xp_data()

    if str(guild_id) not in xp_data:
        return

    guild_data = xp_data[str(guild_id)]

    if str(user_id) not in guild_data:
        return

    guild_data[str(user_id)] -= xp_amount

    if guild_data[str(user_id)] <= 0:
        del guild_data[str(user_id)]

    save_xp_data(xp_data)

def reset_guild_xp(guild_id):
    xp_data = load_xp_data()

    if str(guild_id) in xp_data:
        del xp_data[str(guild_id)]

    save_xp_data(xp_data)

def load_xp_data():
    try:
        with open(XP_FILE, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return {}

def save_xp_data(xp_data):
    with open(XP_FILE, 'w') as file:
        json.dump(xp_data, file)

def get_user_xp(guild_id, user_id):
    xp_data = load_xp_data()
    guild_data = xp_data.get(str(guild_id), {})
    return guild_data.get(str(user_id), 0)

def process_message(message):
    if not message.author.bot:
        add_xp_to_user(message.guild.id, message.author.id, 10)

@bot.event
async def on_ready():
        await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.playing, name="This Bot Is Meant to Be used with wuidBot."))
        print(f'Logged in as {bot.user.name} ({bot.user.id})')





@bot.command()
async def welcome_embedv0(ctx):
    embed = discord.Embed(
        title="Welcome!",
        description="Welcome to The Server! Here is a List of channels you should read up on!",
        color=discord.Colour.blurple(), # Pycord provides a class with default colors you can choose from
    )
    embed.add_field(name="Gen Chat!", value="**<#1120578724677570673>**")

    embed.add_field(name="Rules?", value="no", inline=True)
    embed.add_field(name="Announced Something?", value="<#1120831816094470204>", inline=True)
 
    embed.set_footer(text="by wuid") # footers can have icons too
    embed.set_author(name="by <@895788406347558922>", icon_url="https://pfps.gg/assets/pfps/1268-girl-pfp-1.png")
    embed.set_thumbnail(url="https://pfps.gg/assets/pfps/1268-girl-pfp-1.png")
    embed.set_image(url="https://pfps.gg/assets/banners/3332-90s-clouds.png")
 
    await ctx.respond("For Newbies!", embed=embed) # Send the embed with some text


@bot.command(description="Sends the bot's latency.") # this decorator makes a slash command
async def ping(ctx): # a slash command will be created with the name "ping"
        response_message = f"{ctx.author.mention} {bot.latency}"
    
        await ctx.respond(response_message)

@bot.slash_command(name = "add", description = "Adds Two Sums together.")
# pycord will figure out the types for you
async def add(ctx, first: discord.Option(int), second: discord.Option(int)):
  # you can use them as they were actual integers
  sum = first + second
  await ctx.respond(f"The sum of {first} and {second} is {sum}.")


class MyView(discord.ui.View): # Create a class called MyView that subclasses discord.ui.View
    async def on_timeout(self):
        self.disable_all_items()
        await self.message.edit(content="You Took too long! Disabled Buttons!",  view=self)
    @discord.ui.button(label="Bot Invite Link", style=discord.ButtonStyle.red) # Create a button with the label "😎 Click me!" with color Blurple
    async def button_callback(self, button, interaction):
        await interaction.response.send_message("<https://discord.com/api/oauth2/authorize?client_id=1122881752633979090&permissions=8&scope=bot>")
    
    @discord.ui.button(label="Support Server Link", row=1, style=discord.ButtonStyle.red)
    async def second_button_callback(self, button, interaction):
        await interaction.response.send_message("https://dsc.gg/mcarchive")

@bot.slash_command() # Create a slash command
async def bothelp(ctx):
    await ctx.respond("Click It!", view=MyView()) # Send a message with our View class that contains the button

@bot.command()
async def credits(ctx):
    embed = discord.Embed(
        title="Credits",
        description="Credits",
        color=discord.Colour.red(), # Pycord provides a class with default colors you can choose from
    )
    embed.add_field(name="Creator", value="<@895788406347558922>")

    embed.add_field(name="Helped", value="<@795736872109604864>")

 
    await ctx.respond("Info!", embed=embed) # Send the embed with some text

@bot.slash_command()
async def serverinfo(ctx):

    guild = ctx.guild
    member_count = guild.member_count
    guild_owner_id = guild.owner_id
    guild_owner = await guild.fetch_member(guild_owner_id) if guild_owner_id else None
    owner_name = guild_owner.name if guild_owner else "Unknown"
    
    if guild.icon is not None:
        icon_url = guild.icon.url
    else:
        icon_url = "https://i.imgur.com/gFIDu2z.png"
    embed = discord.Embed(
        title="Server Info",
        description=" Server Info!!",
        color=discord.Colour.red(), # Pycord provides a class with default colors you can choose from
    )
    embed.add_field(name="Name :", value= f"{ctx.guild.name}")

    embed.add_field(name="Created On :", value= ctx.guild.created_at.strftime("%b %d %Y"), inline = True)
    embed.add_field(name="Owner :", value=owner_name, inline=False)
    embed.add_field(name="Bot Ping :", value=f'{bot.latency}', inline = True)
    embed.add_field(name="Member Count", value=f'{ctx.guild.member_count}', inline = True)
 
    embed.set_footer(text="ServerInfo") # footers can have icons too
    embed.set_author(name="By .wuid", icon_url="https://pfps.gg/assets/pfps/1268-girl-pfp-1.png")
    embed.set_thumbnail(url=icon_url)
 
    await ctx.respond("Info!", embed=embed)
@bot.slash_command(name = "avatar", description = "get some random persons avatar")
async def avatar(ctx, member: discord.Member = None):
    if member is None:
        member = ctx.author
    
    avatar_url = member.avatar.url
    
    embed = discord.Embed()
    embed.set_image(url=avatar_url)
    embed.set_footer(text=f"Avatar of {member}")
    
    await ctx.respond(embed=embed)
@bot.slash_command(name = "say", description = "says whatever you want it to!")
async def say(ctx, message=None):
        response_message = {message} + "etyetf"
    
        await ctx.respond(response_message)


class MyV1ew(discord.ui.View): # Create a class called MyView that subclasses discord.ui.View
    async def on_timeout(self):
        self.disable_all_items()
        await self.message.edit(content="Button Timeout.",  view=self)
    @discord.ui.button(label="Github Link", style=discord.ButtonStyle.red) # Create a button with the label "😎 Click me!" with color Blurple
    async def button_callback(self, button, interaction):
        await interaction.response.send_message("https://github.com/Rlzt/Basic-discord-bot")
    

@bot.slash_command() # Create a slash command
async def github(ctx):
    await ctx.respond("Bot Source Code", view=MyV1ew())

@bot.slash_command(name = "icon", description = "Gets Guild Icon for vbucks")
async def fuxkmedaddxy(ctx):
    guild = ctx.guild
    if guild.icon is not None:
        icon_url = guild.icon.url
    else:
        icon_url = "https://media.tenor.com/Lby-i8SJI2QAAAAM/placeholder-bluelearn.gif"

    rm = f"{ctx.author.mention} Guild Icon Found {icon_url}!"
    
    await ctx.respond(rm)
        





@bot.command()
async def doge(ctx):
    goodjobwuid = ["https://www.allthingsdogs.com/wp-content/uploads/2019/06/Fun-Dog-Meme.jpg", "https://www.allthingsdogs.com/wp-content/uploads/2019/06/Border-Collie-Joke.jpg", "https://www.allthingsdogs.com/wp-content/uploads/2019/06/Dog-Eating-Food-Pun.jpg",  "https://www.allthingsdogs.com/wp-content/uploads/2019/06/Dog-Paw-Meme.jpg", "https://www.allthingsdogs.com/wp-content/uploads/2019/06/Joke-About-Puggles.jpg", "https://media3.giphy.com/media/3otPovknltwgrSHJDO/200w.webp?cid=ecf05e47onblm1gfyn2yi0sind4e8m1dxxhd719hwww9dqkq&ep=v1_gifs_search&rid=200w.webp&ct=g", "https://media.giphy.com/media/eG4Y2ROCoYIEIKbbJV/giphy.gif", "https://media.giphy.com/media/SgA1dDaADW1Uuo5MZG/giphy.gif", "https://media.giphy.com/media/gIupdT6dMUHSOrYieB/giphy.gif", "https://media.giphy.com/media/26uTru9zaMy7SFuQU/giphy.gif", "https://media.giphy.com/media/3otPorBqSZrB0sVPHi/giphy.gif", "https://media.giphy.com/media/bCm4v4wy0LSfdz72Mr/giphy.gif", "https://media.giphy.com/media/3otPou7Ug1KjTOYeje/giphy.gif", "https://media.giphy.com/media/UWtZTgC9zhlTqxEelf/giphy.gif", "https://media.giphy.com/media/pn1e1I4nAVtSMo1h7y/giphy.gif", "https://media.giphy.com/media/P1fiDLzvru9FetvtKC/giphy.gif", "https://media.giphy.com/media/IF0a7qASuTexF2kRc9/giphy.gif", "https://media.giphy.com/media/lzP4HBHI9P8gHV8lHq/giphy.gif", "https://media.giphy.com/media/lCY522fPY3faVDvj2R/giphy.gif", "https://media0.giphy.com/media/fvM5D7vFoACAM/200.webp?cid=ecf05e47869lndklovq7bpj1xfsy6vlrl7iudwjvzpezebb5&ep=v1_gifs_search&rid=200.webp&ct=g", "https://media.giphy.com/media/oBQZIgNobc7ewVWvCd/giphy.gif", "https://media.giphy.com/media/8FUmlOoL72HB3rR7wm/giphy.gif", "https://media.giphy.com/media/xT9DPEPymVhAwi0mJy/giphy.gif", "https://media.giphy.com/media/dKKu8jJaontS3Yyka8/giphy.gif", "https://media.giphy.com/media/CqogJHPYMv6oiBO31a/giphy.gif", "https://media.giphy.com/media/21sybnVhC2Xpm/giphy.gif", "https://media.giphy.com/media/D6InoH7TLxMsM/giphy.gif", "https://media.giphy.com/media/ATjmo8oCmY2btUckpV/giphy.gif", "https://media.giphy.com/media/k2hh0zJzIBvY4/giphy.gif", "https://media1.giphy.com/media/Eh9JKXQg1EpUqP8l5Y/giphy.webp?cid=ecf05e476m6kd8f722o2tkfa8g6m37hfxkgbldmgm3dz2kiv&ep=v1_gifs_search&rid=giphy.webp&ct=g", "https://media0.giphy.com/media/9cWrk07kjAJdC6jHta/200w.webp?cid=ecf05e476m6kd8f722o2tkfa8g6m37hfxkgbldmgm3dz2kiv&ep=v1_gifs_search&rid=200w.webp&ct=g", "https://media4.giphy.com/media/SS4qzUNG3SlQHqQX2u/giphy.webp?cid=ecf05e47n3d8weq9epd9qls9ayuiv76rwmdr4hbuby3e5fpy&ep=v1_gifs_search&rid=giphy.webp&ct=g", "https://media0.giphy.com/media/OQBoOB4CQvSSpVYSCA/200.webp?cid=ecf05e47n3d8weq9epd9qls9ayuiv76rwmdr4hbuby3e5fpy&ep=v1_gifs_search&rid=200.webp&ct=g", "https://media0.giphy.com/media/cEYFeDHvTlS4zmRmPU4/200w.webp?cid=ecf05e47n3d8weq9epd9qls9ayuiv76rwmdr4hbuby3e5fpy&ep=v1_gifs_search&rid=200w.webp&ct=g", "https://media2.giphy.com/media/4QFd9B1jMRZDVbMYAg/200.webp?cid=ecf05e47n3d8weq9epd9qls9ayuiv76rwmdr4hbuby3e5fpy&ep=v1_gifs_search&rid=200.webp&ct=g"]
    senddoggos = random.choice(goodjobwuid)
    embed = discord.Embed()
    embed.set_thumbnail(url=senddoggos)

    response_message = f"{ctx.author.mention} used the /doge command! Here's a doggo for you:"

    await ctx.respond(response_message, embed=embed)








# restrict bot to one guild.
def only_this_guild(guild_id: int):
    async def predicate(ctx):
        if ctx.guild is None:
            raise commands.NoPrivateMessage() 
        return ctx.guild.id == guild_id           

    return commands.check(predicate)

@bot.slash_command(
    name="infomc",
    description="info about a second discord server"
)
@only_this_guild(1122020440202817587)
async def xDGamerMCYTtesting3957406(ctx):

    response_message = f"{ctx.author.mention} hello!"
    
    await ctx.respond(response_message)



import discord
from discord.ext import commands

@bot.command()
@commands.has_permissions(administrator=True)
async def slowmode(ctx, channel: discord.TextChannel, time: int):
    response_message = f"{ctx.author.mention} Set Slowmode To {time} in {channel.mention}"
    await channel.edit(slowmode_delay=time)
    await ctx.respond(response_message)




@bot.command()
async def flipcoin(ctx):
    coin = random.choice(['Heads', 'Tails'])
    response_message = f"{ctx.author.mention} Flipped a Coin : It Landed on ***{coin}***!"
    await ctx.respond(response_message)


@bot.command()
async def quote(ctx):

    try:
        with open("quotes.json", "r") as r:
            j = json.load(r)
            all_quotes = j["quotes"]
    except:
        await ctx.send("No quotes stored! Add it using the quotes command")
        return
    
    await ctx.respond(random.choice(all_quotes))


@bot.command()
async def addq(ctx, quote_):
    def add_quote(quote, file="quotes.json"):
        with open(file, "r+") as fw:
            j = json.load(fw)
            j["quotes"].append(quote)
            with open(file, "w+") as wp:
                wp.write(json.dumps(j))

    try:
        with open("quotes.json", "r"):
            pass
    except:
        with open("quotes.json", "w+") as wp:
            wp.write('{"quotes" : []}')
    finally:
        add_quote(quote_)
    response_message1 = "Done!"
    await ctx.respond(response_message1)

import requests

@bot.command()
async def joke(ctx):
    response = requests.get("https://official-joke-api.appspot.com/random_joke")
    joke_data = response.json()
    joke_setup = joke_data['setup']
    joke_punchline = joke_data['punchline']
    
    embed = discord.Embed(title="Joke Time!",
                          description=f"{joke_setup}\n\n{joke_punchline}",
                          color=discord.Color.blue())
    
    await ctx.respond(embed=embed)

@bot.command(name = "rolldice", description = "after using /rolldice say a message afterwards to continue with the command")
async def rolldice(ctx):
    def check(message):
        return message.author == ctx.author and message.channel == ctx.channel

    try:
        await ctx.send("Rolling the dice! 🎲")
        message = await bot.wait_for("message", check=check, timeout=30.0)
        await ctx.send(f"You rolled: {random.randint(1, 6)}")
    except asyncio.TimeoutError:
        await ctx.send("Timeout! You took too long to respond.")


@bot.event
async def on_ready():
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name="the best song ever"))
    print(f"{bot.user} is ready and online!!!")



@bot.slash_command(name="announce", description="Make an announcement in a channel")
@commands.has_permissions(administrator=True)
async def announce(ctx: commands.Context, channel: discord.TextChannel, message: str):
    await ctx.respond("Sending announcement now!")
    
    embed = discord.Embed(title="Announcement", description=message, color=discord.Color.blue())
    await channel.send(embed=embed)


@bot.slash_command(name="purge", description="Purge a specified number of messages in a channel")
@commands.has_permissions(manage_messages=True)
async def purge(ctx: commands.Context, limit: int):
    channel = ctx.channel
    await ctx.respond(f"Purging {limit} messages...")
    
    messages = await channel.history(limit=limit + 1).flatten()
    await channel.delete_messages(messages)
    
    await ctx.respond(f"Purged {limit} messages!")


@bot.slash_command(name = "timeout", description = "timesout/mutes a user noone likes lmaoo")
@commands.has_permissions(manage_messages=True)
async def timeout(ctx, member: discord.Member, duration: int, *, reason=None):
    if duration < 0:
        await ctx.send("Duration cannot be negative.")
        return

    # Mute the member
    muted_role = discord.utils.get(ctx.guild.roles, name="Muted")  # Assuming there is a role named "Muted"
    await member.add_roles(muted_role, reason=reason)
    await ctx.respond(f'{member.name} has been muted for {duration} seconds.')

    # Wait for the specified duration
    await asyncio.sleep(duration)

    # Unmute the member after the duration has passed
    await member.remove_roles(muted_role, reason="Timeout expired")
    await ctx.respond(f'{member.name} has been unmuted after the timeout.')

@timeout.error
async def command_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.respond("You don't have permission to use this command.")
  


@bot.slash_command()
@commands.has_permissions(manage_messages=True)
async def ban(ctx, member: discord.Member, *, reason=None):
    await member.ban(reason=reason)
    await ctx.send(f'{member.name} has been banned.')

@bot.slash_command()
@commands.has_permissions(manage_messages=True)
async def kick(ctx, member: discord.Member, *, reason=None):
    await member.kick(reason=reason)
    await ctx.send(f'{member.name} has been kicked.')

@ban.error
@kick.error
async def command_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("You don't have permission to use this command.")




@bot.command()
async def truth(ctx):
    with open("questions.json", "r") as file:
        questions = json.load(file)
        truth_list = questions["truth"]
        truth = random.choice(truth_list)
        await ctx.respond(truth)

@bot.command()
async def dare(ctx):
    with open("questions.json", "r") as file:
        questions = json.load(file)
        dare_list = questions["dare"]
        dare = random.choice(dare_list)
        await ctx.respond(dare)



@bot.command()
async def dareadd(ctx, *, new_dare):
    with open("questions.json", "r+") as file:
        questions = json.load(file)
        dare_list = questions["dare"]
        dare_list.append(new_dare)
        file.seek(0)
        json.dump(questions, file, indent=4)
        await ctx.respond("New dare has been added!")


@bot.command()
async def truthadd(ctx, *, new_truth):
    with open("questions.json", "r+") as file:
        questions = json.load(file)
        truth_list = questions["truth"]
        truth_list.append(new_truth)
        file.seek(0)
        json.dump(questions, file, indent=4)
        await ctx.respond("New truth question has been added!")



























bot.run("TOKEN")
