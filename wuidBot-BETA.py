import discord
from datetime import datetime


bot = discord.Bot()
@bot.event
async def on_ready():
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name="the best song ever"))
    print(f"{bot.user} is ready and online!")

@bot.slash_command(name = "hello", description = "Say hello to the bot")
async def hi(ctx):
    await ctx.send("Hey!")

@bot.slash_command(name = "version", description = "Check Bot Version")
async def ver(ctx):
    await ctx.send("Version 1.0.23 - Beta Branch - By .wuid")


@bot.command()
async def welcome_embed(ctx):
    embed = discord.Embed(
        title="Welcome!",
        description="Welcome to The Server! Here is a List of channels you should read up on!",
        color=discord.Colour.blurple(), # Pycord provides a class with default colors you can choose from
    )
    embed.add_field(name="Gen Chat!", value="**#General**")

    embed.add_field(name="Rules!", value="#Rules", inline=True)
    embed.add_field(name="Infomation!", value="#Info", inline=True)
    embed.add_field(name="Announced Something?", value="#Announcements", inline=True)
 
    embed.set_footer(text="by wuid") # footers can have icons too
    embed.set_author(name="by @.wuid", icon_url="https://pfps.gg/assets/pfps/1268-girl-pfp-1.png")
    embed.set_thumbnail(url="https://pfps.gg/assets/pfps/1268-girl-pfp-1.png")
    embed.set_image(url="https://pfps.gg/assets/banners/3332-90s-clouds.png")
 
    await ctx.respond("For Newbies!", embed=embed) # Send the embed with some text


@bot.command(description="Sends the bot's latency.") # this decorator makes a slash command
async def ping(ctx): # a slash command will be created with the name "ping"
    await ctx.respond(f"Pong! Latency is {bot.latency}")

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
        await interaction.response.send_message("<https://discord.com/api/oauth2/authorize?client_id=1122259720397394011&permissions=8&scope=bot>")
    
    @discord.ui.button(label="Support Server Link", row=1, style=discord.ButtonStyle.red)
    async def second_button_callback(self, button, interaction):
        await interaction.response.send_message("https://dsc.gg/mcarchive")

@bot.slash_command() # Create a slash command
async def bothelp(ctx):
    await ctx.respond("Click It!", view=MyView()) # Send a message with our View class that contains the button

@bot.command()
async def info(ctx):
    embed = discord.Embed(
        title="Info",
        description="Info About wuidBot",
        color=discord.Colour.red(), # Pycord provides a class with default colors you can choose from
    )
    embed.add_field(name="Fully Coded And Made By", value="**.wuid**")

    embed.add_field(name="Using ", value="Py-cord", inline=True)
    embed.add_field(name="and ", value="Wavelink", inline=True)
    embed.add_field(name="do /bothelp", value="For More!", inline=True)
 
    embed.set_footer(text="Info!") # footers can have icons too
    embed.set_author(name="Info Embed", icon_url="https://pfps.gg/assets/pfps/1268-girl-pfp-1.png")
    embed.set_thumbnail(url="https://pfps.gg/assets/pfps/1268-girl-pfp-1.png")
    embed.set_image(url="https://pfps.gg/assets/banners/3332-90s-clouds.png")
 
    await ctx.respond("Info!", embed=embed) # Send the embed with some text

@bot.slash_command()
async def serverinfo(ctx):
  server = ctx.guild
  if server.icon:
    server_icon_url = ctx.guild.icon.url
  else:
    server_icon_url = None

    embed = discord.Embed(
        title="Server Info",
        description=" Server Info!!",
        color=discord.Colour.red(), # Pycord provides a class with default colors you can choose from
    )
    embed.add_field(name="Name :", value= f"{ctx.guild.name}")

    embed.add_field(name="Created On :", value= ctx.guild.created_at.strftime("%b %d %Y"), inline = True)
    embed.add_field(name="Owner :", value=f"{ctx.guild.owner}", inline=True)
    embed.add_field(name="Bot Ping :", value=f'{bot.latency}', inline = True)
    embed.add_field(name="Member Count", value=f'{ctx.guild.member_count}', inline = True)
 
    embed.set_footer(text="ServerInfo") # footers can have icons too
    embed.set_author(name="By .wuid", icon_url="https://pfps.gg/assets/pfps/1268-girl-pfp-1.png")
    embed.set_thumbnail(url=server_icon_url)
 
    await ctx.respond("Info!", embed=embed)

@bot.slash_command()
async def avatar(ctx, member:discord.Member):
    await ctx.send(member.avatar)

@bot.slash_command(name = "say", description = "says whatever you want it to!")
async def say(ctx, message=None):
    await ctx.send(message)

class MyView(discord.ui.View): # Create a class called MyView that subclasses discord.ui.View
    async def on_timeout(self):
        self.disable_all_items()
        await self.message.edit(content="Button Timeout.",  view=self)
    @discord.ui.button(label="Github Link", style=discord.ButtonStyle.red) # Create a button with the label "😎 Click me!" with color Blurple
    async def button_callback(self, button, interaction):
        await interaction.response.send_message("https://github.com/Rlzt/Basic-discord-bot")
    

@bot.slash_command() # Create a slash command
async def github(ctx):
    await ctx.respond("Bot Source Code", view=MyView())




    
bot.run("TOKEN")
