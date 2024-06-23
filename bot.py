import os
from dotenv import load_dotenv
from twitchio.ext import commands

load_dotenv()

ACCESS_TOKEN = os.getenv('ACCESS_TOKEN')
INITIAL_CHANNELS = ['']

class Bot(commands.Bot):

    def __init__(self):
        super().__init__(token=ACCESS_TOKEN, prefix='!', initial_channels=INITIAL_CHANNELS)

    async def event_ready(self):
        print(f'Logged in as | {self.nick}')
        print(f'User id is | {self.user_id}')

    @commands.command(name='hello')
    async def hello(self, ctx: commands.Context):
        await ctx.send('Hello, World!')

if __name__ == '__main__':
    bot = Bot()
    bot.run()