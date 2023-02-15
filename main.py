import os
import warnings

from dotenv import load_dotenv

from functions import telegram as t

warnings.filterwarnings('ignore')
load_dotenv()

if __name__ == '__main__':
    token = os.environ.get("BOT_TOKEN")
    t.telegram_bot(token)