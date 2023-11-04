import os.path


SECURE_FILE_NAME: str = '.secure'

TELEGRAM_TOKEN: str = ''

EXCHANGE_TOKEN: str = ''

if not os.path.isfile(SECURE_FILE_NAME):
    raise f'Создайте файл с именем {SECURE_FILE_NAME} содержащий две строки. На первой токен для бота,' \
          f' на второй токен для курса валют.'


secure_file = open(".secure", "r")
try:
    TELEGRAM_TOKEN = secure_file.readline()
    TELEGRAM_TOKEN = TELEGRAM_TOKEN.strip()

    EXCHANGE_TOKEN = secure_file.readline()
    EXCHANGE_TOKEN = EXCHANGE_TOKEN.strip()
finally:
    secure_file.close()

print(TELEGRAM_TOKEN)
print(EXCHANGE_TOKEN)
