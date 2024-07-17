# StatMuse Bot

The script used to start the StatMuse Bot. 

## Getting Started

### Prerequisites

Before you can run the script, ensure you have python installed:

-  Python 3.x - https://www.python.org/downloads/

### Installation

Clone the repository:

    git clone git@github.com:ken862734801/statmuse-bot.git

Create a virtual environment:

    python3 -m venv venv

    source venv/bin/activate

Install required packages:

    pip install -r requirements.txt

### Setup

1. Get your Twitch Credentials
    - Visit - https://dev.twitch.tv/console
    - Register your application to get a Client ID and Client Secret.
2. Generate an Access Token
    - Visit - https://twitchtokengenerator.com/
    - Follow the instructions to generate an access token.
3. Create an `.env` file in the root directory of the project and add your token:

        token=your_twitch_auth_token
4. Specify the Channel
    - Open the `bot.py` file, and add your channel name to the initial_channels array.

### Execution

To start the script, run:

    python3 main.py