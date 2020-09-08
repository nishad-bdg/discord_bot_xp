import discord
from discord.ext import commands
from datetime import datetime
import random
import utils.UserExperience as ux
import config


class MyEvents(commands.Cog):
    __slots__ = ['bot']

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"We logegd in as : {self.bot.user}")
        print(f"version : {discord.__version__}")

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author == self.bot.user:
            return
        xp = 300
        users = self.bot.get_guild(config.SERVER_ID)

        await ux.UserExperience(self.bot.db, message, xp, self.bot).add_user_xp()


def setup(bot):
    bot.add_cog(MyEvents(bot))
