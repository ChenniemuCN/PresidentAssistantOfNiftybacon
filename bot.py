import discord
import json
import os
import discord.ext
from discord.ext import commands, tasks
from itertools import cycle


with open('setting.json', 'r', encoding='utf8') as jfile:
    jdata = json.load(jfile)

intents = discord.Intents.default()
intents.members = True

bot = commands.Bot(command_prefix='>/', intents = intents)
status = cycle(['Blue Achieve', '蔚藍檔案'])

def power_account(ctx):
   return ctx.author.id == int(jdata['power_account_id'])

@bot.event
async def on_ready():
   change_status.start()
#   await bot.change_presence(status=discord.Status.idle, activity=discord.Game('BlueAchieve(蔚藍檔案)'))
   print("> Bot Is Online")

@tasks.loop(seconds=5)
async def change_status():
   await bot.change_presence(status=discord.Status.idle, activity=discord.Game(next(status)))

@bot.command()
@commands.check(power_account)
async def load(ctx, extension):
   bot.load_extension(f'cmds.{extension}')
   await ctx.send(f'成功加载 {extension} 模块啦！')

@bot.command()
@commands.check(power_account)
async def unload(ctx, extension):
   bot.unload_extension(f'cmds.{extension}')
   await ctx.send(f'成功卸载 {extension} 模块啦！')

@bot.command()
@commands.check(power_account)
async def reload(ctx, extension):
   bot.reload_extension(f'cmds.{extension}')
   await ctx.send(f'重新加载了 {extension} 模块！')





for filename in os.listdir('./cmds'):
   if filename.endswith('.py'):
      bot.load_extension(f'cmds.{filename[:-3]}')



if __name__ == "__main__":
   bot.run(jdata['TOKEN'])