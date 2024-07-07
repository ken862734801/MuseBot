import os
from dotenv import load_dotenv
from statmuse_bot.bot import Bot

load_dotenv()

def main():
    token = os.getenv('token')

    bot = Bot(token=token)
    bot.run()

if __name__ == "__main__":
    main()
    