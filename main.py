import telebot
import requests
import time
import config

bot = telebot.TeleBot(config.TOKEN)
hh_api_url = 'https://api.hh.ru/vacancies'
pages = []

query = {
    'text': None,
    'salary': None,
    'employment': None
}

# @bot.message_handler(commands=['start'])
# def start_message(message):
#     bot.send_message(message.chat.id, 'Привет, я hh bot! Могу помочь с поиском вакансии :)\n' +
#                      'Напиши ключевое слово: ')
#     bot.register_next_step_handler(message, get_key_word)
#
#
# def get_key_word(message):
#     query['text'] = message.text
#     bot.send_message(message.from_user.id, 'Напиши желаемый оклад: ')
#     bot.register_next_step_handler(message, get_salary)
#
#
# def get_salary(message):
#     query['salary'] = message.text
#     bot.send_message(message.from_user.id, 'Напиши тип занятости: ')
#     bot.register_next_step_handler(message, get_employment)
#
#
# def get_employment(message):
#     if message.text.find('Полная') != -1:
#         query['employment'] = 'full'
#     elif message.text.find('Частичная') != -1:
#         query['employment'] = 'part'
#     elif message.text.find('Проектная') != -1:
#         query['employment'] = 'project'
#     elif message.text.find('Волонтер') != -1:
#         query['employment'] = 'volunteer'
#     elif message.text.find('Стажировка') != -1:
#         query['employment'] = 'probation'
#
#     bot.send_message(message.from_user.id, 'Всё понял! Начинаю поиск')
#     search_vacancies(message)
#
#
# def search_vacancies(message):
#     while True:
#         for i in range(10):
#             r = requests.get(hh_api_url, params=query)
#             e = r.json()
#             pages.append(e)
#
#         for page in pages:
#             vacs = page['items']
#
#             for v in vacs:
#                 bot.send_message(message.from_user.id, v['alternate_url'])
#                 time.sleep(10)


@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id, 'Привет, я hh bot! Могу помочь с поиском вакансии :)\n' +
                     'Напиши ключевое слово: ')

@bot.message_handler(content_types=['text'])
def text_message(message):
    if query['text'] is None and query['salary'] is None and query['employment'] is None:
        query['text'] = message.text
        bot.send_message(message.chat.id, 'Напиши желаемый оклад')
    elif query['salary'] is None and query['employment'] is None:
        if message.text.isdigit():
            query['salary'] = message.text
            bot.send_message(message.chat.id, 'Напиши тип занятости')
        else:
            bot.send_message(message.chat.id, 'Неверно введенные данные')
    elif query['employment'] is None:
        if message.text.find('Полная') != -1:
            query['employment'] = 'full'
        elif message.text.find('Частичная') != -1:
            query['employment'] = 'part'
        elif message.text.find('Проектная') != -1:
            query['employment'] = 'project'
        elif message.text.find('Волонтер') != -1:
            query['employment'] = 'volunteer'
        elif message.text.find('Стажировка') != -1:
            query['employment'] = 'probation'
        if query['employment'] is None:
            bot.send_message(message.chat.id,
                             'Введите пожалуйста значения типа: (Полная,Частичная,Проектная,Волонтерство,Стажировка)')
        else:
            bot.send_message(message.chat.id, 'Всё понял! Начинаю поиск!')
            while True:
                for i in range(10):
                    r = requests.get(hh_api_url, params=query)
                    e = r.json()
                    pages.append(e)

                for page in pages:
                    vacs = page['items']

                    for v in vacs:
                        bot.send_message(message.from_user.id, v['alternate_url'])
                        time.sleep(10)


bot.polling(none_stop=True)