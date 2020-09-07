import discord
from discord.ext import commands
import config
import db

class MyXp(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix = config.PREFIX)
        self.load_extensions()
        self.db = db.DB(config.HOST, config.USER, config.PASSWORD, config.DB,self.loop)

    def load_extensions(self):
        for cog in config.EXTENSIONS:
            self.load_extension(cog)
   
    
    # @property
    # def get_guild(self):
    #     return self.get_guild(config.SERVER_ID)

    def run(self):
        super().run(config.TOKEN)
    

if __name__ == "__main__":
    my_xp = MyXp()
    my_xp.run()
