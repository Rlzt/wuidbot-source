import json
import discord
from discord.ext import commands

bot = discord.Bot()



intents = discord.Intents.default()
intents.typing = False
intents.presences = False



  
@bot.slash_command(name = "hello", description = "Say hello to the bot")
async def hello(ctx):
    await ctx.respond("Hey!")


class MyV1ew(discord.ui.View): # Create a class called MyView that subclasses discord.ui.View
    async def on_timeout(self):
        self.disable_all_items()
        await self.message.edit(content="You Took Too long!!",  view=self)
    @discord.ui.button(label="Invite wuidBot!", style=discord.ButtonStyle.red) # Create a button with the label "😎 Click me!" with color Blurple
    async def button_callback(self, button, interaction):
        await interaction.response.send_message("https://discord.com/api/oauth2/authorize?client_id=1122259720397394011&permissions=8&scope=bot")
    

@bot.slash_command() # Create a slash command
async def github(ctx):
    await ctx.respond("Invite Link For wuidBot", view=MyV1ew())

click_count = 0

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name} ({bot.user.id})')

@bot.slash_command()
async def click(ctx):
    global click_count
    click_count += 1
    await ctx.respond(f'Clicked! Total clicks: {click_count}')

bot.run('')
