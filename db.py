import asyncio
import aiomysql


class DB:
    def __init__(self, host, username, password, db, loop):
        self.host = host
        self.username = username
        self.password = password
        self.db = db
        self.loop = loop
        loop.run_until_complete(self.connect())

    async def connect(self):
        try:
            self.pool = await aiomysql.create_pool(host=self.host, port=3306, user=self.username, password=self.password,
                                                   db=self.db, loop=self.loop, charset='utf8mb4', use_unicode=True,
                                                   autocommit=True)
            print(f"Connected to database '{self.db}'")
        except Exception as e:
            print(f"Failed to connect with '{self.db}'")
            print(e)

    async def execute(self, query, args=None):
        async with self.pool.acquire() as conn:
            async with conn.cursor() as cur:
                r = await cur.execute(query, args=args)
                return r, cur.lastrowid

    async def fetch(self, query, args=None, *, fetchall=False):
        print("The fetch function triggered")
        async with self.pool.acquire() as conn:
            async with conn.cursor(aiomysql.DictCursor) as cur:
                await cur.execute(query, args=args)
                return await cur.fetchall() if fetchall else await cur.fetchone()
