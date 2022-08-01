import discord
import discord.ext
from discord.ext import commands
from core.classes import Cog_Extension
import json

with open('setting.json', 'r', encoding='utf8') as jfile:
    jdata = json.load(jfile)


class Main(Cog_Extension):
    def power_account(ctx):
        return ctx.author.id == int(jdata['power_account_id'])

    @commands.command()
    @commands.check(power_account)
    async def ping(self, ctx):
        await ctx.send(f'{round(self.bot.latency*1000)} (ms)')

    @commands.command()
    @commands.check(power_account)
    async def sayd(self, ctx, *,msg):
        await ctx.message.delete()
        await ctx.send(msg)

    @commands.command()
    @commands.check(power_account)
    async def clean(self, ctx, num:int):
        await ctx.channel.purge(limit=num+1)



def setup(bot):
    bot.add_cog(Main(bot))