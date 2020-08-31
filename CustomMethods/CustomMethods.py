from datetime import datetime
import discord
from discord.ext import commands

GETXP = False

class CustomMethods(commands.Cog):
    def __init__(self,bot):
        self.bot = bot
    
     # add xp function
    async def add_xp(self,user_id,message,xp):
        global GETXP
        current_time = datetime.utcnow()
        #user query
        user_id = str(user_id)
        user_query = "SELECT * FROM xp_table WHERE user_id = %s"
        r = await self.bot.db.fetch(user_query,user_id)
        if r is not None:
            print("User found")
            #if user found
            # we will go for the last xp slot for this particular user
            user_xp_query = "SELECT * FROM xp_table WHERE user_id = %s and xp_slot = 1"
            r_xp = await self.bot.db.fetch(user_xp_query,user_id)
            # once xp_slot found
            if r_xp is not None:
                time_diff = current_time - r_xp["created"]
                # if time difference is less than 60 seconds then user will get new xp
                print(time_diff.total_seconds())
                print(type(time_diff.total_seconds()))

                if int(time_diff.total_seconds()) >= 60:
                    print(f"User is going to get new xp {r_xp['id']}")
                    #now going set previous xp_slot to false and create a new xp_slot
                    prev_xp_false_query = "UPDATE xp_table SET xp_slot = 0 WHERE id = %s"
                    x = await self.bot.db.execute(prev_xp_false_query,int(r_xp["id"]))
                    #then creating another record with a xp_slot
                    new_xp_query = f"INSERT INTO xp_table (user_id,message,xp_slot,xp_value,created) VALUES (%s,%s,%s,%s,%s)"
                    GETXP = True
                    await self.bot.db.execute(new_xp_query,(user_id,message,True,xp,current_time))
                    
                else:
                    # creating a new record without xp
                    noxp_query = f"INSERT INTO xp_table (user_id,message,xp_slot,xp_value,created) VALUES (%s,%s,%s,%s,%s)"
                    await self.bot.db.execute(noxp_query,(user_id,message,False,0,current_time))
                    print("user is not going to get xp")
                    GETXP = False
        else:
            insert_query = f"INSERT INTO xp_table (user_id,message,xp_slot,xp_value,created) VALUES (%s,%s,%s,%s,%s)"
            print("New user xp added")
            GETXP = True
            await self.bot.db.execute(insert_query,(user_id,message,True,xp,current_time))

        

            