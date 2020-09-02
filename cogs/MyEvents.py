import discord
from discord.ext import commands
from datetime import datetime
import random
import CustomMethods.CustomMethods as cm
import utils.UserExperience as ux


class MyEvents(commands.Cog):
    def __init__(self,bot):
        self.bot = bot
    

    @commands.Cog.listener()
    async def on_message(self,message):
        if message.author == self.bot.user:
            return
        xp = random.randint(15,25)

        is_xp = await ux.UserExperience(self.bot.db).add_xp(message.author.id,message.content,xp)
        if is_xp:
            await message.channel.send(f"Congratulation {message.author} you got new xp : {xp}")


       
def setup(bot):
    bot.add_cog(MyEvents(bot))