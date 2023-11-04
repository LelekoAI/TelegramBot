import telebot
from telebot import types
import CacheCurrency
import AdressBook
import ExchangeApi
import FreakingCurrency
import VirRusCalculator


class CommandList:
    against: str = 'against'
    to: str = 'to'
    amount: str = 'amount'
    back: str = 'back'
    another: str = 'Another'
    group: str = 'G:'

    @staticmethod
    def make_command(command_name: str, payload: str = None) -> str:
        if payload is None:
            return command_name
        return f'{command_name} {payload}'

    @staticmethod
    def parse_command(command_payload: str) -> tuple[str, str]:
        values: list[str] = command_payload.split(' ', 1)
        if len(values) == 1:
            return (values[0], '')
        return (values[0], values[1])


class Telegram:
    cash: CacheCurrency.CacheCurrency
    against: str
    to: str

    def __init__(self, token: str, api: ExchangeApi.Exchange):
        self.bot: telebot.TeleBot = telebot.TeleBot(token, parse_mode=None)
        self.cash = CacheCurrency.CacheCurrency(api)
        self.cash.get_currencies()

        # @self.bot.message_handler(commands=['start', 'help', ])
        # def reply_start_help(message):
        #     self.bot.reply_to(message, "Howdy, how are you doing?")

        @self.bot.message_handler(commands=['start'])
        def first_ask(message):
            self.against = None
            self.to = None
            markup = self.get_start_currency(CommandList.against)
            self.bot.send_message(message.chat.id, 'Выберите валюту для обмена: ', reply_markup=markup)

        @self.bot.message_handler(commands=['another_currency'])
        def question(message):
            markup = self.get_groups_buttons()
            self.bot.send_message(message.chat.id, 'Выберите первую букву валюты: ', reply_markup=markup)

        @self.bot.callback_query_handler(func=lambda call: True)
        def answer(callback):
            if not callback.message:
                return
            command_payload: tuple[str, str] = CommandList.parse_command(callback.data)
            command_name: str = command_payload[0]
            payload: str = command_payload[1]
            if command_name == CommandList.against:
                if payload == CommandList.another:
                    self.bot.edit_message_text(
                        chat_id=callback.message.chat.id,
                        message_id=callback.message.message_id,
                        text="Выберите первую букву валюты из которой конвертируем.",
                        parse_mode="markdown",
                        reply_markup=self.get_groups_buttons(CommandList.against))
                    return
                if payload.startswith(CommandList.group):
                    group: list[str] = payload[len(CommandList.group):].split(', ')
                    self.bot.edit_message_text(
                        chat_id=callback.message.chat.id,
                        message_id=callback.message.message_id,
                        text="Выберите валюту из которой конвертируем.",
                        parse_mode="markdown",
                        reply_markup=self.get_group_currency(CommandList.against, group))
                    return
                else:
                    self.against = payload
                    self.bot.edit_message_text(
                        chat_id=callback.message.chat.id,
                        message_id=callback.message.message_id,
                        text="Выберите валюту в которую конвертируем.",
                        parse_mode="markdown",
                        reply_markup=self.get_start_currency(CommandList.to))
                    return
            if command_name == CommandList.to:
                if payload == CommandList.another:
                    self.bot.edit_message_text(
                        chat_id=callback.message.chat.id,
                        message_id=callback.message.message_id,
                        text="Выберите первую букву валюты в которую конвертируем.",
                        parse_mode="markdown",
                        reply_markup=self.get_groups_buttons(CommandList.to))
                    return
                if payload.startswith(CommandList.group):
                    group: list[str] = payload[len(CommandList.group):].split(', ')
                    self.bot.edit_message_text(
                        chat_id=callback.message.chat.id,
                        message_id=callback.message.message_id,
                        text="Выберите валюту в которую конвертируем.",
                        parse_mode="markdown",
                        reply_markup=self.get_group_currency(CommandList.to, group))
                    return
                else:
                    self.to = payload
                    self.bot.send_message(callback.message. chat.id, f'Введите количество конвертируемой валюты {self.against}.')
                    self.bot.register_next_step_handler(callback.message, self.calculate)
                    return
            # if callback.data == 'answer_same':
            #     self.bot.send_message(callback.message. chat.id, 'Congratulations! You are the winner!')
            # else:
            #     self.bot. send_message(callback.message. chat.id, 'Think again...')

    def get_start_currency(self, command_name: str):
        markup = types.InlineKeyboardMarkup(row_width=3)
        rub = types.InlineKeyboardButton('RUB', callback_data=CommandList.make_command(command_name, 'RUB'))
        eur = types.InlineKeyboardButton('EUR', callback_data=CommandList.make_command(command_name, 'EUR'))
        usd = types.InlineKeyboardButton('USD', callback_data=CommandList.make_command(command_name, 'USD'))
        markup.add(rub, eur, usd)
        another = types.InlineKeyboardButton('Another...', callback_data=CommandList.make_command(command_name, CommandList.another))
        markup.add(another)
        return markup

    def get_groups_buttons(self, command_name: str):
        markup = types.InlineKeyboardMarkup(row_width=3)
        group_coins: list[list[str]] = AdressBook.AdressBook.create_group_coins(self.cash)
        buttons: list = []
        for group in group_coins:
            group_name: str = ', '.join(group)
            button = types.InlineKeyboardButton(group_name, callback_data=CommandList.make_command(command_name, f'{CommandList.group}{group_name}'))
            buttons.append(button)
        markup.add(*buttons)
        return markup

    def get_group_currency(self, command_name: str, group: list[str]):
        markup = types.InlineKeyboardMarkup(row_width=3)
        currencies: dict[str, FreakingCurrency.FreakingCurrency] = AdressBook.AdressBook.get_currency_by_group(group, self.cash)
        buttons: list = []
        for key in currencies.keys():
            button = types.InlineKeyboardButton(key, callback_data=CommandList.make_command(command_name, key))
            buttons.append(button)
        markup.add(*buttons)
        return markup

    def calculate(self, message: telebot.types.Message):
        value: int = int(message.text)
        currencies: dict[str, FreakingCurrency] = self.cash.get_currencies()
        self.bot.send_message(message.chat.id, f'Количество получаемой валюты {self.to}: {VirRusCalculator.Claculator.calculate(value, currencies[self.against], currencies[self.to])}')


    def run(self):
        self.bot.infinity_polling()

    # # Например, при помощи reply_markup в  edit_message_text
    #
    # def inline_key(num):
    #     """Функция для вывода кнопок
    #     """
    #     i = 1
    #     btns = []
    #     while i <= num:
    #         btns.append(types.InlineKeyboardButton(text='Кнопка ' + str(i + 10), callback_data='butt' + str(i + 10)))
    #         i = i + 1
    #     btns.append(types.InlineKeyboardButton(text='назад', callback_data='nazad'))
    #     keyboard = types.InlineKeyboardMarkup()
    #     keyboard.add(*btns)
    #     return keyboard
    #
    # @bot.message_handler(commands=["start"])
    # # главное меню
    # def start(m):
    #     key = types.InlineKeyboardMarkup()
    #     key.add(types.InlineKeyboardButton(text='кнопка1', callback_data="butt1"))
    #     key.add(types.InlineKeyboardButton(text='кнопка2', callback_data="butt2"))
    #     msg = bot.send_message(m.chat.id, 'Нажми кнопку', reply_markup=inline_main())
    #     logging.info(m.chat.id)
    #
    # @bot.callback_query_handler(func=lambda call: True)
    # def inline(c):
    #
    #     if c.data == 'butt1':
    #         bot.edit_message_text(
    #             chat_id=c.message.chat.id,
    #             message_id=c.message.message_id,
    #             text="нажата *кнопка 1*",
    #             parse_mode="markdown")
    #     elif c.data == 'butt2':
    #         bot.edit_message_text(
    #             chat_id=c.message.chat.id,
    #             message_id=c.message.message_id,
    #             text="нажата *кнопка 2*",
    #             parse_mode="markdown",
    #             reply_markup=inline_key(5))
    #     elif c.data == 'nazad':
    #         bot.edit_message_text(
    #             chat_id=c.message.chat.id,
    #             message_id=c.message.message_id,
    #             text="нажата *кнопка 2*",
    #             parse_mode="markdown",
    #             reply_markup=inline_key(2))