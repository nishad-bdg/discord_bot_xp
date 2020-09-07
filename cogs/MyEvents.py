import discord
from discord.ext import commands
from datetime import datetime
import random
import utils.UserExperience as ux


class MyEvents(commands.Cog):
    __slots__ = ['bot']
    def __init__(self,bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self,message):
        if message.author == self.bot.user:
            return
        user_id = message.author.id
        xp = 300
        is_xp = await ux.UserExperience(self.bot.db,user_id,xp,self.bot).add_user_xp()
        return 
        # if is_xp:
        #     is_level_up = await ux.UserExperience(self.bot.db).user_level(user_id,xp)
        #     await message.channel.send(f"Congratulation {message.author} you got new xp : {xp}")
        #     if is_level_up:
        #         await message.channel.send(f"Congratualtions level up")
def setup(bot):
    bot.add_cog(MyEvents(bot))