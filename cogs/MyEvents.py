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
        xp = 300
        await ux.UserExperience(self.bot.db,message,xp,self.bot).add_user_xp()

def setup(bot):
    bot.add_cog(MyEvents(bot))