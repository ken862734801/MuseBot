import sys
from twitchio.ext import commands

class TwitchBot(commands.Bot):

    def __init__(self, token):
        super().__init__(token=token, prefix="!", initial_channels=[''])

    async def event_ready(self):
        print(f'Logged in as | {self.nick}')
        print(f'User id is | {self.user_id}')

def main():
    if len(sys.argv) != 2:
        print('Missing arguments...')
        sys.exit(1)
    
    token = sys.argv[1]

    statmusebot = TwitchBot(token=token)
    statmusebot.run()

if __name__ == "__main__":
    main()