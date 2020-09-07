from datetime import datetime
import config
import asyncio


class UserExperience:
    __slots__ = ['db', 'user_id', 'xp', 'bot']

    def __init__(self, db, user_id, xp, bot):
        self.db = db
        self.user_id = user_id
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
        user_obj = await self.db.fetch(user_query, self.user_id)
        # if user obj is not found then create automatically
        if user_obj is None:
            level = 0
            user_insert = f"INSERT INTO user_xp (user_id,xp,level,created) VALUES (%s,%s,%s,%s)"
            user_obj = await self.db.execute(user_insert, (self.user_id, self.xp, level, self.current_time))
            await self.channel_id.send(f"Congratulations you have got {self.xp} xp")
            user_obj = None
        return user_obj

    async def update_user_xp_slot(self):
        queryset = f"UPDATE user_xp SET xp = %s, level= %s,created = %s WHERE id = %s"
        user_obj = await self.user_obj()
        new_xp = user_obj["xp"] + self.xp
        current_level = user_obj["level"]
        new_level = new_xp//600
        if new_level > current_level:
            await self.db.execute(queryset, (new_xp, new_level, self.current_time, user_obj["id"]))
            await self.channel_id.send(f"You have reached to level: {new_level}")
        else:
            await self.db.execute(queryset, (new_xp, current_level, self.current_time, user_obj["id"]))

    async def add_user_xp(self):
        user_obj = await self.user_obj()
        if user_obj is not None:
            # calculate the time difference
            time_diff = (self.current_time -
                         user_obj["created"]).total_seconds()

            print(time_diff)
            if time_diff >= 60:
                await self.channel_id.send(f"Congratulations you have got {self.xp} xp")
                xp_update = await self.update_user_xp_slot()

    