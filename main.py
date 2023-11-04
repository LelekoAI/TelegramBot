import ExchangeApi
from Config import TELEGRAM_TOKEN, EXCHANGE_TOKEN
import Telegram


bot: Telegram.Telegram = Telegram.Telegram(TELEGRAM_TOKEN, ExchangeApi.Exchange(EXCHANGE_TOKEN))
bot.run()

