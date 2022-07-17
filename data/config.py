import telebot

TOKEN = ""

bot = telebot.TeleBot(token=TOKEN,threaded=False)

HELLO_REG = '''Добро пожаловать!\nДля продолжения работы Вам нужно зарегестрироваться.

Для регистрации введите команду: /reg

Списко доступных команд /help
'''
API_KEY = ''

HELP = '''Вам доступны следующие команды:
/info - общая информация о сервисе
/del - удалить данные регистрации из базы
/name - изменить имя
/surname - изменить фамилию
/age - изменить возраст
/city - изменить город
/gender - изменить пол
/infoempl - информация для компаний
/infopp - информация для людей
/newpp - размещение в PublicPlaces
/searchpp - поиск в PublicPlaces
/mypp - просмотр своих объявлений
/delpp - удалить PublicPlaces
/allpp - просмотр всех PublicPlaces в вашем городе
/getpp - получить контакты общественного места
/help - список доступных команд
/myinfo - информация о вашем аккаунте
/web - получить ссылку на веб-приложение
'''

HELP_NEW_USER = '''Вам доступны следующие команды:
/start - начало работы с ботом
/help - список доступных команд
/reg - регистрация
'''

INFO = '''Бот PublicPlaces предназначен для помощи в поиске общественных мест, в определенном радиусе, исходя из геопозиции.Так же по выбору определенной категории.

/help
'''

EMPLOYER = '''Если вы хотите разместить ващу компанию, то проделайте следующие шаги:
1. Введите команду /newpp.
2. Укажите данные, которые потребует бот.

В любой момент процесс размещения можно остановить, нажав на кнопку стоп.

Удалить компанию можно командой /delpp

/help
'''
SEEKER = '''Если вы желаете найти общественное место, то проделайте следующие шаги:
1. Просмотрите списко используя командку /allpp
2. Если хотите получить контакты общественное место, используйте команду /getpp, после чего потребуется ввести номер общественного места.

/help
'''

NEWPP = '''
Размещение в PublicPlaces!
'''
WEB = '''
Веб-приложение нашего бота: http://a0679737.xsph.ru
'''

SEARCHPP = '''
Поиск в PublicPlaces!
'''

MYPP = '''
Ваши объявления:
....
'''

ERROR = '''Извините, я вас не понимаю!\n
Воспользуйтесь командой /help.'''

LOCATION = '''Отправьте местоположение.
Формат координат: долгота, широта.

Так же ваше местоположение можно ввести словами, например: 
1. Новосибирск, Кировский район
2. улица Аникина
3. Большевистская
4. Москва

Либо кликаем по иконке скрепка, выбираем место на карте и прикрепляем геопозицию (Location)

Если хотите отправить свою геопозицю - Включаем GPS -> Транслировать мою геопозицию (Share My Live Location for...) - выбираем время (15 мин, 1 час, 8 часов) в течение которого в диалоге будет геопозиция, транслирующая Ваше местоположение онлайн.
'''

ERROR_LOCATION = '''
Извините, не могу определить адрес по этим координатам.

Повторите попытку:
'''

"""
info - общая информация о сервисе
del - удалить данные регистрации из базы
name - изменить имя
surname - изменить фамилию
age - изменить возраст
city - изменить город
gender - изменить пол
# infoempl - информация для работодателя
infopp - информация для людей
newpp - размещение в PublicPlaces
searchpp - поиск в PublicPlaces 
mypp - просмотр своих PublicPlaces!
delpp - удалить общественное место
allpp - просмотр всех PublicPlaces в вашем городе
getpp - получить контакты PublicPlaces
help - список доступных команд
myinfo - информация о вашем аккаунте
"""