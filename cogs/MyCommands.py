import discord
from discord.ext import commands

class MyCommands(commands.Cog):
    __slots__ = ['bot']
    def __init__(self,bot):
        self.bot = bot

    @commands.command()
    @commands.cooldown(1,30,commands.BucketType.user)
    async def hello(self,ctx):
        await ctx.channel.send("Hi")
        
def setup(bot):
    bot.add_cog(MyCommands(bot))
