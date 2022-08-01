import discord
import json
from core.classes import Cog_Extension
import os

with open('setting.json', 'r', encoding='utf8') as jfile:
    jdata = json.load(jfile)

from discord.ext import commands




class Event(Cog_Extension):
    
    @commands.Cog.listener()
    async def on_message(self, msg):
        if msg.content == '你好' and msg.author != self.bot.user:
            await msg.channel.send('你好呀！')

    @commands.Cog.listener()
    async def on_member_join(self, member):
        channel = self.bot.get_channel(int(jdata['Welcome_channel'])) # channel ID
        await channel.send(f'{member} 加入了服务器!')

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        channel = self.bot.get_channel(int(jdata['Leave_channel'])) # channel ID
        await channel.send(f'{member} 离开了服务器!' )

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, reaction_role):
        if reaction_role.message_id == 1001774192729010207:
         if str(reaction_role.emoji) == '🍎':
            guild = self.bot.get_guild(reaction_role.guild_id)
            role1 = guild.get_role(1000597696408719480)
            await reaction_role.member.add_roles(role1)
            await reaction_role.member.send(f"碧蓝档案 >> 服务器消息 >> 你获得了 <{role1}> 身份组！")
         elif str(reaction_role.emoji) == '🍇':
            guild = self.bot.get_guild(reaction_role.guild_id)
            role2 = guild.get_role(1000597859663618128)
            await reaction_role.member.add_roles(role2)
            await reaction_role.member.send(f"碧蓝档案 >> 服务器消息 >> 你获得了 <{role2}> 身份组！")
        #print(reaction_role.emoji)
    
    @commands.Cog.listener()
    async def on_raw_reaction_remove(self, reaction_role):
        if reaction_role.message_id == 1001774192729010207:
         if str(reaction_role.emoji) == '🍎':
            guild = self.bot.get_guild(reaction_role.guild_id)
            user = guild.get_member(reaction_role.user_id)
            role1 = guild.get_role(1000597696408719480)
            await user.remove_roles(role1)
            await user.send(f"碧蓝档案 >> 服务器消息 >> 你移除了 <{role1}> 身份组！")
         elif str(reaction_role.emoji) == '🍇':
            guild = self.bot.get_guild(reaction_role.guild_id)
            user = guild.get_member(reaction_role.user_id)
            role2 = guild.get_role(1000597859663618128)
            await user.remove_roles(role2)
            await user.send(f"碧蓝档案 >> 服务器消息 >> 你移除了 <{role2}> 身份组！")
        
    
    

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.errors.MissingRequiredArgument):
            embed=discord.Embed(color=0xff0000)
            embed=discord.Embed(title="**错误 : 缺少必须添加的参数**", color=0xff0000)
            await ctx.send(embed=embed)
        elif isinstance(error, commands.errors.CommandNotFound):
            embed=discord.Embed(title="**错误 : 找不到这个指令**", color=0xff0000)
            await ctx.send(embed=embed)
        elif isinstance(error, commands.errors.BadArgument):
            embed=discord.Embed(title="**错误 : 请填写正确的参数**", color=0xff0000)
            await ctx.send(embed=embed)
        elif isinstance(error, commands.errors.TooManyArguments):
            embed=discord.Embed(title="**错误 : 太多参数啦~**", color=0xff0000)
            await ctx.send(embed=embed)
        else:
            embed=discord.Embed(title="**呐，发生错误~**", color=0xff0000)
            await ctx.send(embed=embed)


#    @commands.Cog.listener()
#    async def on_message_delete(self, msg):
#        async for audilog in msg.guild.audit_logs(limit=1, action=discord.AuditLogAction.message_delete):
#            await msg.channel.send(msg.member)



def setup(bot):
    bot.add_cog(Event(bot))