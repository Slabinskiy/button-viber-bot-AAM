
import json
import logging
import webbrowser

import requests
from flask import Flask, request, Response
from viberbot import Api
from viberbot.api.bot_configuration import BotConfiguration
from viberbot.api.messages.text_message import TextMessage
from viberbot.api.messages.url_message import URLMessage
from viberbot.api.viber_requests import ViberFailedRequest, ViberConversationStartedRequest
from viberbot.api.viber_requests import ViberMessageRequest
from viberbot.api.viber_requests import ViberSubscribedRequest



app = Flask(__name__)
viber = Api(BotConfiguration(
    name='', # название бота
    avatar='',
    auth_token='' # viber токен
))

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

LINKS = (
    ('sait', 'Сайт ААМ'),
    ('chlenstvo', 'Вступ в Асоціацію'),
    ('rozklad-zahodiv', 'Розклад заходів'),
    ('arhiv-zahodiv', 'Архів заходів'),
    ('dodatok', 'Додаток "МедАкаунт"'),
    ('soc', 'Соціальна мережа "МедАккаунт"'),
    ('pobota', 'Сайт пошуку роботи СОЗ'),
)

FAQ = (
    ('sert', 'Як отримати сертифікат'),
    ('zahid', 'Як зареєструватись на вебінар'),
)

def get_buttons(action_type, items):
    return [{
        "Columns": 3,
        "Rows": 1,
        "BgColor": "#e6f5ff",
        "BgLoop": True,
        "ActionType": 'reply',
        "ActionBody": "{action_type}|{value}".format(action_type=action_type, value=item[0]),
        "ReplyType": "message",
        "Text": item[1]
    } for item in items]


bot_actions_actions = ('select_links', 'faq', 'faq_answers_sait')


@app.route('/', methods=['POST'])
def incoming():


    # print("received request. post data: {0}".format(request.get_data()))
    # every viber message is signed, you can verify the signature using this method
    if not viber.verify_signature(request.get_data(), request.headers.get('X-Viber-Content-Signature')):
        return Response(status=403)

    # this library supplies a simple way to receive a request object
    viber_request = viber.parse_request(request.get_data())

    if isinstance(viber_request, ViberMessageRequest):

        message = viber_request.message
        text = message.text
        text = text.split('|')
        text_type = text[0]
        text_message = ''

        tracking_data = message.tracking_data
        if tracking_data is None:
            tracking_data = {}
        else:
            tracking_data = json.loads(tracking_data)

        keyboard = {
            "DefaultHeight": True,
            "BgColor": "#FFFFFF",
            "Type": "keyboard",
            "Buttons": [
                {
                    "Columns": 6,
                    "Rows": 1,
                    "BgColor": "#e6f5ff",
                    "BgLoop": True,
                    "ActionType": "reply",
                    "ActionBody": "useful_links",
                    "ReplyType": "message",
                    "Text": "Корисні посилання"
                },
                {
                    "Columns": 6,
                    "Rows": 1,
                    "BgColor": "#e6f5ff",
                    "BgLoop": True,
                    "ActionType": "reply",
                    "ActionBody": "faq",
                    "ReplyType": "message",
                    "Text": "Найчастіші питання"
                }
            ]

        }
        keyboard_menu_posilannya = {
            "DefaultHeight": True,
            "BgColor": "#FFFFFF",
            "Type": "keyboard",
            "Buttons": [
                {
                    "Columns": 3,
                    "Rows": 1,
                    "BgColor": "#e6f5ff",
                    "BgLoop": True,
                    "ActionType": "reply",
                    "ActionBody": "aam",
                    "ReplyType": "message",
                    "Text": "Сайт ААМ"
                },
                {
                    "Columns": 3,
                    "Rows": 1,
                    "BgColor": "#e6f5ff",
                    "BgLoop": True,
                    "ActionType": "reply",
                    "ActionBody": "vstup",
                    "ReplyType": "message",
                    "Text": "Вступ в Асоціацію"
                },
                {
                    "Columns": 3,
                    "Rows": 1,
                    "BgColor": "#e6f5ff",
                    "BgLoop": True,
                    "ActionType": "reply",
                    "ActionBody": "rozklad",
                    "ReplyType": "message",
                    "Text": "Розклад заходів"
                },
                {
                    "Columns": 3,
                    "Rows": 1,
                    "BgColor": "#e6f5ff",
                    "BgLoop": True,
                    "ActionType": "reply",
                    "ActionBody": "arhiv-zahodiv",
                    "ReplyType": "message",
                    "Text": "Архів заходів"
                },
                {
                    "Columns": 3,
                    "Rows": 1,
                    "BgColor": "#e6f5ff",
                    "BgLoop": True,
                    "ActionType": "reply",
                    "ActionBody": "dodatok",
                    "ReplyType": "message",
                    "Text": "Додаток МедАкаунт \n (Android)"
                },
                {
                    "Columns": 3,
                    "Rows": 1,
                    "BgColor": "#e6f5ff",
                    "BgLoop": True,
                    "ActionType": "reply",
                    "ActionBody": "dodatok-ios",
                    "ReplyType": "message",
                    "Text": "Додаток МедАкаунт \n (IOS)"
                },
                {
                    "Columns": 3,
                    "Rows": 1,
                    "BgColor": "#e6f5ff",
                    "BgLoop": True,
                    "ActionType": "reply",
                    "ActionBody": "soc",
                    "ReplyType": "message",
                    "Text": "Соціальна мережа МедАккаунт"
                },
                {
                    "Columns": 3,
                    "Rows": 1,
                    "BgColor": "#e6f5ff",
                    "BgLoop": True,
                    "ActionType": "reply",
                    "ActionBody": "robota",
                    "ReplyType": "message",
                    "Text": "Сайт пошуку роботи СОЗ"
                },
                {
                    "Columns": 6,
                    "Rows": 1,
                    "BgColor": "#e6f5ff",
                    "BgLoop": True,
                    "ActionType": "reply",
                    "ActionBody": "back",
                    "ReplyType": "message",
                    "Text": "На початок"
                },
            ]

        }
        keyboard_menu_faq = {
            "DefaultHeight": True,
            "BgColor": "#FFFFFF",
            "Type": "keyboard",
            "Buttons": [
                {
                    "Columns": 3,
                    "Rows": 1,
                    "BgColor": "#e6f5ff",
                    "BgLoop": True,
                    "ActionType": "reply",
                    "ActionBody": "bad",
                    "ReplyType": "message",
                    "Text": "Помилка Bad request"
                },
                {
                    "Columns": 3,
                    "Rows": 1,
                    "BgColor": "#e6f5ff",
                    "BgLoop": True,
                    "ActionType": "reply",
                    "ActionBody": "translation",
                    "ReplyType": "message",
                    "Text": "Мене викидає з трансляції"
                },
                {
                    "Columns": 3,
                    "Rows": 1,
                    "BgColor": "#e6f5ff",
                    "BgLoop": True,
                    "ActionType": "reply",
                    "ActionBody": "when",
                    "ReplyType": "message",
                    "Text": "Коли я отримаю сертифікат?"
                },
                {
                    "Columns": 3,
                    "Rows": 1,
                    "BgColor": "#e6f5ff",
                    "BgLoop": True,
                    "ActionType": "reply",
                    "ActionBody": "zapis",
                    "ReplyType": "message",
                    "Text": "Чи можу я передивитися захід у записі?"
                },
                {
                    "Columns": 3,
                    "Rows": 1,
                    "BgColor": "#e6f5ff",
                    "BgLoop": True,
                    "ActionType": "reply",
                    "ActionBody": "net-sert",
                    "ReplyType": "message",
                    "Text": "Я не отримав(ла) сертифікат"
                },
                {
                    "Columns": 3,
                    "Rows": 1,
                    "BgColor": "#e6f5ff",
                    "BgLoop": True,
                    "ActionType": "reply",
                    "ActionBody": "error-data",
                    "ReplyType": "message",
                    "Text": "Некоректні дані в сертифікаті"
                },
                {
                    "Columns": 3,
                    "Rows": 1,
                    "BgColor": "#e6f5ff",
                    "BgLoop": True,
                    "ActionType": "reply",
                    "ActionBody": "xaomi",
                    "ReplyType": "message",
                    "Text": "Проблеми з трансляцією на пристрої Xaiomi"
                },
                {
                    "Columns": 3,
                    "Rows": 1,
                    "BgColor": "#e6f5ff",
                    "BgLoop": True,
                    "ActionType": "reply",
                    "ActionBody": "problems-translayions",
                    "ReplyType": "message",
                    "Text": "Проблеми з трансляцією"
                },
                {
                    "Columns": 3,
                    "Rows": 1,
                    "BgColor": "#e6f5ff",
                    "BgLoop": True,
                    "ActionType": "reply",
                    "ActionBody": "zareestrovaniy",
                    "ReplyType": "message",
                    "Text": "Чи я вже зареєстрований на вебінар?"
                },
                {
                    "Columns": 3,
                    "Rows": 1,
                    "BgColor": "#e6f5ff",
                    "BgLoop": True,
                    "ActionType": "reply",
                    "ActionBody": "rosklad-korisni",
                    "ReplyType": "message",
                    "Text": "Розклад заходів"
                },
                {
                    "Columns": 6,
                    "Rows": 1,
                    "BgColor": "#e6f5ff",
                    "BgLoop": True,
                    "ActionType": "reply",
                    "ActionBody": "back",
                    "ReplyType": "message",
                    "Text": "На початок"
                },
            ]

        }



        is_finished = False
        buttons = {}


        if text_type == 'useful_links':
            tracking_data = {}
            links = [link[1] for link in LINKS]
            text_message = 'Доступні наступні посилання:\n {links}. \n Будь-ласка, на ресурс, що Вас цікавить.' \
                .format(links=', \n '.join(links))
            keyboard = keyboard_menu_posilannya
        elif text_type == 'aam':
            text_message = 'https://aam.com.ua/'
            keyboard = keyboard_menu_posilannya
        elif text_type == 'vstup':
            text_message = 'https://aam.com.ua/chlenstvo/'
            keyboard = keyboard_menu_posilannya
        elif text_type == 'rozklad':
            text_message = 'https://aam.com.ua/rozklad-zahodiv/'
            keyboard = keyboard_menu_posilannya
        elif text_type == 'arhiv-zahodiv':
            text_message = 'https://aam.com.ua/arhiv-zahodiv/'
            keyboard = keyboard_menu_posilannya
        elif text_type == 'dodatok':
            text_message = 'https://play.google.com/store/apps/details?id=com.olegkamchatniy.rnwebviewonesignal'
            keyboard = keyboard_menu_posilannya
        elif text_type == 'dodatok-ios':
            text_message = 'https://apps.apple.com/ua/app/medaccountpro/id1595139245?l=ru'
            keyboard = keyboard_menu_posilannya
        elif text_type == 'soc':
            text_message = 'https://www.med.aam.com.ua/'
            keyboard = keyboard_menu_posilannya
        elif text_type == 'robota':
            text_message = 'http://job.aam.com.ua/'
            keyboard = keyboard_menu_posilannya
        elif text_type == 'back':
            text_message = "Оберіть питання"
            keyboard = keyboard
        elif text_type == 'faq':
            tracking_data = {}
            text_message = ' '
            keyboard = keyboard_menu_faq
        elif text_type == 'bad':
            tracking_data = {}
            text_message = 'Якщо ви бачите білий екран з написом «Bad request», або «поганий запит», або «занадто довгий запит», необхідно видалити Cookie файли з Вашого браузера. Для цього перейдіть в налаштування браузера -> Історія -> очистити історію. В часовому діапазоні оберіть «весь час». Поставте V (галочку) Файли cookie. Інші поля мають бути порожні. Натисніть «Видалити дані». Після цього перейдіть на сторінку вебінара та оновіть її.'
            keyboard = keyboard_menu_faq
        elif text_type == 'translation':
            tracking_data = {}
            text_message = 'З одного аккаунта неможливо переглядати вебінар на кількох пристроях одночасно (наприклад, на смартфоні і комп’ютері) Також, на одному пристрої неможна використовувати більше одного аккаунта. Беріть участь тільки з одного пристрою'
            keyboard = keyboard_menu_faq
        elif text_type == 'when':
            tracking_data = {}
            text_message = 'Сертифікат буде відправлений Вам на вказану при реєстрації електронну пошту протягом місяця після закінчення заходу'
            keyboard = keyboard_menu_faq
        elif text_type == 'zapis':
            tracking_data = {}
            text_message = 'Через 3 робочі дні захід можна передивитися у записі з можливістю отримання сертифікату на нашому сайті у розділі "Архів заходів"'
            keyboard = keyboard_menu_faq
        elif text_type == 'net-sert':
            tracking_data = {}
            text_message = 'Переконайтесь, що було коректно заповнено реєстраційну форму. На електронну пошту Вам мало надійти підтвердження реєстрації. Якщо не надійшло – перевірте скриньки «Спам» і «Промоакції» \nТакож переконайтесь що відповідали на тестові запитання підчас заходу (відповідно до програми заходу)'
            keyboard = keyboard_menu_faq
        elif text_type == 'error-data':
            tracking_data = {}
            text_message = 'Дані які Ви вводите при реєстрації (а саме: «E-mail», «Прізвище», «Ім’я», «По-батькові») автоматично використовуються для формування та відправки сертифікату. Ми не несемо відповідальності за коректність даних і надалі не зможемо відредагувати сертифікат'
            keyboard = keyboard_menu_faq
        elif text_type == 'xaomi':
            tracking_data = {}
            text_message = 'Стандартний браузер Xaiomi вже не підтримується виробником. Використовуйте браузер Google Chrome, Opera, Firefox. Якщо посилання відкрилось у стандартному браузері скопіюйте його і вставте в адресний рядок іншого браузера'
            keyboard = keyboard_menu_faq
        elif text_type == 'problems-translayions':
            tracking_data = {}
            text_message = 'Переконайтесь в надійності Вашого інтернет з’єднання. Стабільність трансляції з нашого боку постійно контролюється модераторами'
            keyboard = keyboard_menu_faq
        elif text_type == 'zareestrovaniy':
            tracking_data = {}
            text_message = 'Якшо Ви вже заповнили форму реєстрації, але сайт просить Вас повторити реєстрацію знайдіть під формою кнопку «Вже зареєстрований», введіть Ваш e-mail та авторизуйтесь.'
            keyboard = keyboard_menu_faq
        elif text_type == 'rosklad-korisni':
            tracking_data = {}
            text_message = 'https://aam.com.ua/rozklad-zahodiv/'
            keyboard = keyboard_menu_faq
        elif text_type == 'back':
            text_message = "Оберіть питання"
            keyboard = keyboard
        else:
             text_message = "Оберіть питання"


        messages = []
        if is_finished:
            response = requests.get(VACANCIES_URL, params=tracking_data)
            json_response = response.json()
            items = json_response.get('results', [])
            for item in items:
                messages.append(URLMessage(media=item.get('url'),
                                           keyboard=keyboard,
                                           tracking_data={}))

            if not messages:
                messages.append(TextMessage(text='Извините, по выбранным критериям, вакансий не найдено.',
                                            keyboard=keyboard,
                                            tracking_data={}))
        else:
            keyboard_buttons = keyboard.get('Buttons', [])
            keyboard_buttons.extend(buttons)
            keyboard['Buttons'] = keyboard_buttons
            keyboard = keyboard if keyboard.get('Buttons') else None
            tracking_data = json.dumps(tracking_data)
            messages.append(TextMessage(text=text_message,
                                        keyboard=keyboard,
                                        tracking_data=tracking_data))

        viber.send_messages(viber_request.sender.id, messages)

    elif isinstance(viber_request, ViberSubscribedRequest):
        viber.send_messages(viber_request.user.id, [
            TextMessage(text="Дякуємо що приєднались!")
        ])
    elif isinstance(viber_request, ViberFailedRequest):
        logger.warn("client failed receiving message. failure: {0}".format(viber_request))
    elif isinstance(viber_request, ViberConversationStartedRequest):
        keyboard = {
            "DefaultHeight": True,
            "BgColor": "#FFFFFF",
            "Type": "keyboard",
            "Buttons": [
                {
                    "Columns": 6,
                    "Rows": 1,
                    "BgColor": "#e6f5ff",
                    "BgLoop": True,
                    "ActionType": "reply",
                    "ActionBody": "search_vacancies",
                    "ReplyType": "message",
                    "Text": "Почати!"
                }
            ]
        }
        viber.send_messages(viber_request.user.id, [
            TextMessage(text="Вітаємо!\nНатисніть \'Почати!\'", keyboard=keyboard)
        ])

    return Response(status=200)


if __name__ == "__main__":
    #context = ('server.crt', 'server.key')
    #app.run(port="8087")

