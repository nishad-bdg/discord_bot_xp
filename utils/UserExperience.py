from datetime import datetime
import config
import asyncio


user_cache = {}


class UserExperience:
    __slots__ = ['db', 'message', 'xp', 'bot']

    def __init__(self, db, message, xp, bot):
        self.db = db
        self.message = message
        self.xp = xp
        self.bot = bot

    @property
    def current_time(self):
        return datetime.utcnow()

    @property
    def channel_id(self):
        return self.bot.get_channel(config.CHANNEL_ID)

    async def user_obj(self):
        user_query = "SELECT * FROM user_xp WHERE user_id = %s"
        user_obj = await self.db.fetch(user_query, self.message.author.id)
        # if user obj is not found then create automatically
        if user_obj is None:
            await self.create_new_user()
        else:
            user_cache[self.message.author.id] = user_obj["created"]
        return user_obj
    
    async def create_new_user(self):
        try:
            level = 0
            user_insert = f"INSERT INTO user_xp (user_id,xp,level,created) VALUES (%s,%s,%s,%s)"
            await self.db.execute(user_insert, (self.message.author.id, self.xp, level, self.current_time))
            await self.message.author.send(
                f"{self.message.author.mention} Congratulations we have got {self.xp} xp"
            )
            #adding to dictionary
            user_cache[self.message.author.id] = self.current_time
            
        except Exception as e:
            print(e)

    async def update_user_xp_slot(self):
        queryset = f"UPDATE user_xp SET xp = %s, level= %s,created = %s WHERE id = %s"
        user_obj = await self.user_obj()
        new_xp = user_obj["xp"] + self.xp
        current_level = user_obj["level"]
        new_level = new_xp//600
        if new_level > current_level:
            await self.db.execute(queryset, (new_xp, new_level, self.current_time, user_obj["id"]))
            await self.message.author.send(
                f"{self.message.author.mention} You just advanced to level {new_level}!"
            )
        else:
            await self.db.execute(queryset, (new_xp, current_level, self.current_time, user_obj["id"]))
        #update user cache
        user_cache[self.message.author.id] = self.current_time
    
    async def add_user_xp(self):
        try:
            last_xp_time = user_cache[self.message.author.id]
            await self.time_diff(last_xp_time)
            print("dictionary block is working")
        except:
            print("Except working")
            user_obj = await self.user_obj()
            if user_obj is not None:
                await self.time_diff(user_obj["created"])
                # calculate the time difference
                
    #time difference function
    async def time_diff(self,user_last_xp_time):
        time_diff = (self.current_time - user_last_xp_time).total_seconds()
        print(time_diff)
        if time_diff >= 60:
            # await self.channel_id.send(f"Congratulations you have got {self.xp} xp")
            await self.message.author.send(f"{self.message.author.mention} Congratulations you have got {self.xp} xp")
            xp_update = await self.update_user_xp_slot()

    
    
    