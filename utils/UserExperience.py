from datetime import datetime


class UserExperience:
    def __init__(self,db):
        self.db = db
    
    
    async def add_xp(self,user_id,xp):
        xp = int(xp)
        current_time = datetime.utcnow()
        # user query
        user_id = str(user_id)
        user_query = "SELECT * FROM user_xp WHERE user_id = %s"
        user = await self.db.fetch(user_query, user_id)
        #if user found
        if user is not None:
            print("User found")
            time_diff = current_time - user["created"]
            # if time difference is less than 60 seconds then user will get new xp
            if int(time_diff.total_seconds()) >= 60:
                print(f"User is going to get new xp {xp}")
                # now going set previous xp_slot to false and create a new xp_slot
                new_xp = int(user["xp"]) + xp
                prev_xp_false_query = "UPDATE user_xp SET xp = %s, created = %s WHERE id = %s"
                x = await self.db.execute(prev_xp_false_query, (new_xp,current_time,user["id"]))
                return True
            else:
                # user will not going to get any xp's
                print("User will not get any xps")
                return False
        else:
            level = 0
            insert_query = f"INSERT INTO user_xp (user_id,xp,level,created) VALUES (%s,%s,%s,%s)"
            print("New user xp added")
            await self.db.execute(insert_query, (user_id,xp,level,current_time))
            return True


    async def user_level(self,user_id,xp):
        user_query = "SELECT * FROM user_xp WHERE user_id = %s"
        user = await self.db.fetch(user_query,user_id)
        current_level = user["level"]
        print(f"current level : {current_level}")
        user_xp = user["xp"]
        new_level = user_xp//600
        print(f"new level {new_level}")

        if new_level > current_level:
            level_query = "UPDATE user_xp SET level = %s WHERE id = %s"
            await self.db.execute(level_query,(new_level,user["id"]))
            return True
        else:
            return False 

              

        
        
        





    

