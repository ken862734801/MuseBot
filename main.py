import sys
from statmuse_bot.bot import Bot

def main():
    if len(sys.argv) !=2:
        sys.exit(1)
    
    token = sys.argv[1]
    
    bot = Bot(token=token)
    bot.run()

if __name__ == "__main__":
    main()