from twitchio.ext import commands
from nba.client import get_career, get_record, get_game_score, get_boxscore

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
            career = get_career(name)
            await ctx.send(f'{career} @{ctx.author.name}')
        else:
            await ctx.send(f'Missing player name. @{ctx.author.name}')
    
    @commands.command(name='record')
    async def record(self, ctx: commands.Context):
        team = self.parse_command(ctx.message.content)
        if team:
            record = get_record(team);
            await ctx.send(f'{record} @{ctx.author.name}')
        else:
            await ctx.send(f'Missing team name. @{ctx.author.name}')

    @commands.command(name='score')
    async def score(self, ctx: commands.Context):
        team = self.parse_command(ctx.message.content)
        if team:
            score = get_game_score(team)
            await ctx.send(f'{score} @{ctx.author.name}')
        else:
            await ctx.send(f'Missing team name. @{ctx.author.name}')

    @commands.command(name='boxscore')
    async def boxscore(self, ctx: commands.Context):
        player = self.parse_command(ctx.message.content)
        if player:
            stat_line = get_boxscore(player)
            await ctx.send(f'{stat_line} @{ctx.author.name}')
        else:
            await ctx.send(f'Missing player name. @{ctx.author.name}')
