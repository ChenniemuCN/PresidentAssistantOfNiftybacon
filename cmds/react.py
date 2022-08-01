import discord
import discord.ext
from typing import Optional
import json

from discord.ext import commands
from core.classes import Cog_Extension

with open('setting.json', 'r', encoding='utf8') as jfile:
    jdata = json.load(jfile)

intents = discord.Intents.default()
intents.members = True

class React(Cog_Extension):
    def power_account(ctx):
        return ctx.author.id == int(jdata['power_account_id'])
    
    @commands.command()
    async def avatar(self, ctx, member: discord.Member):
        await ctx.send(discord.Member.avatar_url)

    @commands.command()
    @commands.check(power_account)
    async def kick(self, ctx:commands.Context, member : commands.MemberConverter, *, reason=None):
        await member.kick(reason=reason)
        await ctx.send(f'{member} 已经被踢出了服务器，理由是：{reason}')

    @commands.command()
    @commands.check(power_account)
    async def ban(self, ctx:commands.Context, member : commands.MemberConverter, *, reason=None):
        await member.ban(reason=reason)
        await ctx.send(f'{member} 已经被服务器封锁，理由是：{reason}')
    
    @commands.command()
    @commands.check(power_account)
    async def unban(self, ctx, *, member):
        banned_users = await ctx.guild.bans()
        member_name, member_discriminator = member.split('#')
        
        for ban_entry in banned_users:
            user = ban_entry.user
            
            if(user.name, user.discriminator) == (member_name, member_discriminator):
                await ctx.guild.unban(user)
                await ctx.send(f'服务器已经解除对 {user.mention} 的封锁')
                return
    

def setup(bot):
    bot.add_cog(React(bot))