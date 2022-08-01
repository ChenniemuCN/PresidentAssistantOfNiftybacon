import discord
import json
import discord.ext


from discord.ext import commands
from core.classes import Cog_Extension
from discord import File
from typing import Optional
from easy_pil import Editor, load_image_async, Font, Text, Canvas



class Levelsys(Cog_Extension):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print("> Level & Xp system ready")

    @commands.Cog.listener()
    async def on_message(self, message):
        if not message.content.startswith(">/"):
             if not message.author.bot:
                with open('levels.json', 'r', encoding='utf-8') as file:
                    print(file)
                    data = json.load(file)
                if str(message.author.id) in data:
                    xp = data[str(message.author.id)]['xp']
                    lvl = data[str(message.author.id)]['level']
                    increased_xp = xp+25
                    new_level = int(increased_xp/100)

                    data[str(message.author.id)]['xp'] = increased_xp

                    with open("levels.json", "w",  encoding='utf-8') as file:
                        json.dump(data, file)
                    if new_level > lvl:
                        await message.channel.send(f"恭喜 {message.author.mention} 成功升级为 {new_level} 级!")
                        
                        data[str(message.author.id)]['level'] = new_level
                        data[str(message.author.id)]['xp'] = 0
                        
                        with open("levels.json", "w",  encoding='utf-8') as file:
                            json.dump(data, file)                        


                else :
                    data[str(message.author.id)] = {}
                    data[str(message.author.id)]['xp'] = 0
                    data[str(message.author.id)]['level'] = 1

                    with open("levels.json", "w", encoding='utf-8') as file:
                        json.dump(data, file)
    
    @commands.command(name="rank")
    async def rank(self, ctx: commands.Context, user: Optional[discord.Member]):
        userr = user or ctx.author

        with open("levels.json", "r", encoding='utf-8') as file:
            data = json.load(file)
        
        xp = data[str(userr.id)]["xp"]
        lvl = data[str(userr.id)]["level"]

        next_levelup_xp =(lvl+1)*100
        xp_need = next_levelup_xp
        xp_have = data[str(userr.id)]["xp"]

        percentage = int(((xp_have*100)/xp_need))

        background = Editor("./images/zCARD.png")
        profile = await load_image_async(str(userr.avatar_url))
        
        profile = Editor(profile).resize((170, 170)).circle_image()

        poppins = Font(path="naa.ttf", size=50)
        poppins_small = Font(path="naa.ttf", size=30)

        background.rectangle((20, 20), 894, 242, "#2a2e35")
        background.paste(profile, (60, 55))
        #background.ellipse((50, 50), width=185, height=185, outline="#43b581", stroke_width=10)
        background.rectangle((260, 180), width=630, height=40, fill="#484b4e", radius=20)
        background.bar(
            (260, 180),
            max_width=630,
            height=40,
            percentage=percentage,
            fill="#ffffff",
            radius=20,
        )
        background.text((270, 120), str(userr.name), font=poppins, color="#ffffff")
        background.text(
            (890, 50),
            f"LEVEL {lvl}  ",
            font=poppins_small,
            color="#ffffff",
            align="right",
        )
        
        if (lvl+1)*100 > 1000:
            xp_max = f"{((lvl+1)*100/1000)}k"

        else:
            xp_max = (lvl+1)*100

        if int(xp) > 1000:
            xp_new = f"{int(xp)/1000}k"
        
        else:
            xp_new = xp


        background.text(
            (870, 140),
            f"{xp_new} / {xp_max} xp",
            font=poppins_small,
            color="#ffffff",
            align="right",
        )

#        rank_level_texts = [
#            Text("Rank ", color="#00fa81", font=poppins),
#            Text(f"N/A", color="#1EAAFF", font=poppins),
#            Text("   Level ", color="#00fa81", font=poppins),
#            Text(f"{lvl}", color="#1EAAFF", font=poppins),
#        ]
#
#        background.multicolor_text((850, 30), texts=rank_level_texts, align="right") 
        card = File(fp=background.image_bytes, filename="./images/zCARD.png")
        await ctx.send(file=card)






def setup(bot):
    bot.add_cog(Levelsys(bot))