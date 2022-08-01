import discord
import json
import discord.ext

with open('setting.json', 'r', encoding='utf8') as jfile:
    jdata = json.load(jfile)


from discord.ext import commands
from core.classes import Cog_Extension
from discord import File
from easy_pil import Editor, load_image_async, Font, Text, Canvas   

class WelcomePage(Cog_Extension):
    @commands.Cog.listener()
    async def on_member_join(self, member):
        channel = self.bot.get_channel(int(jdata['Welcome_channel'])) # channel ID
        
        background = Editor("./images/welcome1.jpg")
        profile_image = await load_image_async(str(member.avatar_url))
        
        profile = Editor(profile_image).resize((400, 400)).circle_image()
        poppins = Font(path="naa.ttf", size=100)
        poppins_small = Font(path="naa.ttf", size=70)

        background.paste(profile, (760, 170))
        background.ellipse((760, 170), 400, 400, outline="white", stroke_width=10)
        background.text((960, 640), f"欢迎来到 {member.guild.name}", color="white", font=poppins, align="center")
        background.text((960, 780), f"{member} ", color="white", font=poppins_small, align="center")
        file = File(fp=background.image_bytes, filename="./images/paste.jpg")
        await channel.send(file=file)




def setup(bot):
    bot.add_cog(WelcomePage(bot))