from twitchio.ext import commands

class Bot(commands.Bot):
    
    def __init__(self, token):
        super().__init__(token=token, prefix="!", initial_channels=[''])

    async def event_ready(self):
        print(f'Logged in as: {self.nick}')

