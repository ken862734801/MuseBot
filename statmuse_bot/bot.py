from twitchio.ext import commands
from nba.client import get_record

class Bot(commands.Bot):
    
    def __init__(self, token):
        super().__init__(token=token, prefix="!", initial_channels=[''])

    def parse_command(self, message):
        words = message.split()
        if len(words) > 1:
            name = ' '.join(words[1:])
            return name
        else:
            return None

    async def event_ready(self):
        print(f'Logged in as: {self.nick}')
        print(f'User id is: {self.user_id}')

    @commands.command(name='career')
    async def career(self, ctx: commands.Context):
        name = self.parse_command(ctx.message.content)
        if name:
            await ctx.send(f'{name}')
        else:
            await ctx.send('Incorrect usage!')
    
    @commands.command(name='record')
    async def record(self, ctx: commands.Context):
        team = self.parse_command(ctx.message.content)
        record = get_record(team);
        if team:
            await ctx.send(f'{record}')
        else:
            await ctx.send(f'Incorrect usage!')

    @commands.command(name='score')
    async def score(self, ctx: commands.Context):
        team = self.parse_command(ctx.message.content)
        if team:
            await ctx.send(f'{team}')
        else:
            await ctx.send(f'Incorrect usage!')
