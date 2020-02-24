import telebot
import requests
import time
import config
import databases

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

bot = telebot.TeleBot(config.TOKEN)

hh_api_url = 'https://api.hh.ru/vacancies'
pages = []

engine = create_engine(config.DB_URI)
databases.Base.metadata.create_all(bind=engine)

Session = sessionmaker()
Session.configure(bind=engine)
session = Session()

query = {
    'text': None,
    'salary': None,
    'employment': None
}

@bot.message_handler(commands=['start'])
def start_message(message):
    row = session.query(databases.Chat_Table).filter(databases.Chat_Table.chat_id == message.chat.id).first()
    if not row:
        new_row = databases.Chat_Table(chat_id=message.chat.id)
        session.add(new_row)
        session.commit()
    bot.send_message(message.chat.id, 'Привет, я hh bot! Могу помочь с поиском вакансии :)\n' +
                     'Напиши ключевое слово: ')


@bot.message_handler(content_types=['text'])
def text_message(message):
    row = session.query(databases.Chat_Table).filter(databases.Chat_Table.chat_id == message.chat.id).first()
    if row.text is None and row.salary is None and row.employment is None:
        row.text = message.text
        session.commit()
        bot.send_message(message.chat.id, 'Напиши желаемый оклад')
    elif row.salary is None and row.employment is None:
        if message.text.isdigit():
            row.salary = message.text
            session.commit()
            bot.send_message(message.chat.id, 'Напиши тип занятости')
        else:
            bot.send_message(message.chat.id, 'Неверно введенные данные')
    elif query['employment'] is None:
        if message.text.find('Полная') != -1:
            row.employment = 'full'
        elif message.text.find('Частичная') != -1:
            row.employment = 'part'
        elif message.text.find('Проектная') != -1:
            row.employment = 'project'
        elif message.text.find('Волонтер') != -1:
            row.employment = 'volunteer'
        elif message.text.find('Стажировка') != -1:
            row.employment = 'probation'
        if row.employment is None:
            bot.send_message(message.chat.id,
                             'Введите пожалуйста значения типа: (Полная,Частичная,Проектная,Волонтерство,Стажировка)')
        else:
            session.commit()
            bot.send_message(message.chat.id, 'Всё понял! Начинаю поиск!')
            # while True:
            #     for i in range(10):
            #         r = requests.get(hh_api_url, params={'text': row.text,
            #                                              'salary': str(round(row.salary)),
            #                                              'employment': row.employment})
            #         e = r.json()
            #         pages.append(e)
            #
            #     for page in pages:
            #         vacs = page['items']
            #
            #         for v in vacs:
            #             bot.send_message(message.chat.id, v['alternate_url'])
            #             time.sleep(10)

bot.polling(none_stop=True, interval=0, timeout=20)