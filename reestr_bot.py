import time

import telebot

import view

import logging

bot = telebot.TeleBot('your_token', skip_pending=True)

logger = telebot.logger

logging.basicConfig(filename='log.log', filemode='a', format='%(asctime)s, - %(name)s - %(levelname)s - %(message)s')
# telebot.logger.setLevel(logging.ERROR)
# telebot.logger.setLevel(logging.DEBUG)


username = view.user_id()
us = []  # список нач отедлов из БД
for i in username:
    us += i
print(us)

username = view.tp_user_id()
tp_us = []  # список сотрудников ТП из БД
for i in username:
    tp_us += i
print(tp_us)

id_equipment = view.check_id()
id_eq = []  # список id оборудования из БД
for i in id_equipment:
    id_eq += i
print(id_eq)

NN = view.check_NN()
nn = []  # список накладных из БД
for i in NN:
    nn += i
print(nn)


give_msg = {}  # заявка на выдачу
return_eq = {}  # возврат
tp_setting = {}  # настроенное
tp_replace = {}  # заявка на замену

time_m = lambda x: time.strftime("%d.%m.%Y", time.localtime(x))  # функция возвращает дату и время отправки сообщения


@bot.message_handler(commands=['start'])
def send_welcome(message):
    try:
        bot.send_message(message.chat.id, """Привет. Ознакомься с возможными командами: \n
/give - заявка на выдачу оборудования со склада. Доступна только для начальников отдела.
/return_e - заявка на возврат оборудования. Доступна только для начальников отдела.
/replace - заявка на замену оборудования. Доступна только для начальников отдела.
/setting - настройка оборудования ТП для монтажного отдела. Доступна только для отдела техподдержки.
/give_away - выдача настроенного оборудования монтажному отделу. Доступна только для отдела техподдержки.
/install - приём установленного оборудования. Доступна только для отдела техподдержки.""")


    except Exception as e:
        bot.reply_to(message, 'В функции send_welcome ошибка: ' + f'{e}')
        print(e)


@bot.message_handler(commands=['give'])
def user_choice(message):
    global ttt, e, equipment_sklad
    try:
        ttt = view.tlgrm_user_id()
        for y in ttt:
            if message.from_user.id == y[0]:
                give_msg['Нач.Отдела'] = y[1]
                break
        equipment_sklad = str(view.select_equip())
        e = ""
        for i in view.select_equip():
            e += '\n' + "/" + i[0] + ' - ' + i[1] + '\n'
        if message.from_user.id in us:
            bot.send_message(message.chat.id, 'Выбери оборудование \n' + e)
            bot.register_next_step_handler(message, more)
    except Exception as e:
        bot.reply_to(message, 'В функции user_choice ошибка: ' + f'{e}')
        print(e)


def more(message):
    try:
        give_msg['Оборудование'] = message.text[1:]
        bot.send_message(message.chat.id, "Укажи количество:")
        bot.register_next_step_handler(message, otdel)
    except Exception as e:
        bot.reply_to(message, 'В функции more ошибка:' + f'{e}')
        print(e)


def otdel(message):
    try:
        give_msg["Количество"] = message.text
        bot.send_message(message.chat.id, 'Введи фамилию сотрудника')
        bot.register_next_step_handler(message, add_address)
    except Exception as e:
        bot.reply_to(message, 'В функции otdel ошибка: ' + f'{e}')
        print(e)


def add_address(message):
    try:
        give_msg['Сотрудник'] = message.text
        bot.send_message(message.chat.id, 'Введи адрес установки узла:')
        bot.register_next_step_handler(message, reason)
    except Exception as e:
        bot.reply_to(message, 'В функции add_address ошибка: ' + f'{e}')
        print(e)


def reason(message):
    try:
        give_msg['Адрес узла'] = message.text
        bot.send_message(message.chat.id, 'Введи обоснование выдачи:')
        bot.register_next_step_handler(message, comment)
    except Exception as e:
        bot.reply_to(message, 'В функции reason ошибка: ' + f'{e}')
        print(e)


def comment(message):
    try:
        give_msg['Обоснование'] = message.text
        bot.send_message(message.chat.id, 'Введи комментарий:')
        bot.register_next_step_handler(message, send_to_sklad)
    except Exception as e:
        bot.reply_to(message, 'В функции comment ошибка: ' + f'{e}')
        print(e)


def send_to_sklad(message):
    try:
        give_msg['Кoмментарий'] = message.text
        print(give_msg)
        a = f"Выдать \n"
        for k, v in give_msg.items():
            a += f"\n {k} {' ' * 8} {v}"
        bot.send_message(message.chat.id, a)
    except Exception as e:
        bot.reply_to(message, 'В функции send_to_sklad ошибка: ' + f'{e}')
        print(e)
    view.add_columns_reestr(user_id=give_msg['Нач.Отдела'], kolvo=give_msg["Количество"],
                            equipment=give_msg['Оборудование'],
                            sotrudnik=give_msg['Сотрудник'], address=give_msg['Адрес узла'],
                            reason=give_msg['Обоснование'],
                            comment_=give_msg['Кoмментарий'])


@bot.message_handler(commands=['return_e'])
def return_button(message):
    try:
        bot.send_message(message.chat.id, 'Введи id оборудования для возврата на склад')
        bot.register_next_step_handler(message, return_equipment)
    except Exception as e:
        bot.reply_to(message, 'В return_button ошибка: ' + f'{e}')
        print(e)


def return_equipment(message):
    try:
        return_eq = message.text
        if return_eq.isdigit():
            if len(return_eq) < 3 or len(return_eq) > 5:
                bot.send_message(message.chat.id, 'Неверное количество символов. Введи id оборудования:')
                bot.register_next_step_handler(message, return_equipment)
            else:
                b = f'Возврат на склад id{return_eq}'
                bot.send_message(message.chat.id, b)
                view.add_return_equipment(equipment_id=return_eq)
        else:
            bot.send_message(message.chat.id, 'Неверный формат. Введи id оборудования (только цифры):')
            bot.register_next_step_handler(message, return_equipment)
    except Exception as e:
        bot.reply_to(message, 'В функции return_equipment ошибка:' + f'{e}')
        print(e)


@bot.message_handler(commands=['replace'])
def replace_button(message):
    global ttt, e, equipment_sklad
    try:
        ttt = view.tlgrm_user_id()
        for y in ttt:
            if message.from_user.id == y[0]:
                tp_replace['Нач.Отдела'] = y[1]
                break
        equipment_sklad = str(view.select_equip())
        e = ""
        for i in view.select_equip():
            e += '\n' + "/" + i[0] + ' - ' + i[1] + '\n'
        if message.from_user.id in us:
            bot.send_message(message.chat.id, 'Выбери оборудование \n' + e)
            bot.register_next_step_handler(message, rep_more)
    except Exception as e:
        bot.reply_to(message, 'В replace_button ошибка: ' + f'{e}')
        print(e)


def rep_more(message):
    try:
        tp_replace["Оборудование"] = message.text[1:]
        bot.send_message(message.chat.id, "Укажи количество:")
        bot.register_next_step_handler(message, rep_otdel)
    except Exception as e:
        bot.reply_to(message, 'В функции rep_more ошибка: ' + f'{e}')
        print(e)


def rep_otdel(message):
    try:
        tp_replace["Количество"] = message.text
        bot.send_message(message.chat.id, 'Введи фамилию сотрудника')
        bot.register_next_step_handler(message, rep_add_address)
    except Exception as e:
        bot.reply_to(message, 'В функции rep_otdel ошибка: ' + f'{e}')
        print(e)


def rep_add_address(message):
    try:
        tp_replace['Сотрудник'] = message.text
        bot.send_message(message.chat.id, 'Введи адрес установки узла:')
        bot.register_next_step_handler(message, rep_comment)
    except Exception as e:
        bot.reply_to(message, 'В функции rep_add_address ошибка: ' + f'{e}')
        print(e)


def rep_comment(message):
    try:
        tp_replace['Адрес узла'] = message.text
        bot.send_message(message.chat.id, 'Введи комментарий:')
        bot.register_next_step_handler(message, rep_send_to_sklad)
    except Exception as e:
        bot.reply_to(message, 'В функции rep_comment ошибка: ' + f'{e}')
        print(e)


def rep_send_to_sklad(message):
    try:
        tp_replace['Кoмментарий'] = message.text
        print(tp_replace)
        a = f"ЗАМЕНИТЬ \n"
        for k, v in tp_replace.items():
            a += f"\n {k} {' ' * 8} {v}"
        bot.send_message(message.chat.id, a)

    except Exception as e:
        bot.reply_to(message, 'В функции rep_send_to_sklad ошибка: ' + f'{e}')
        print(e)
    view.add_columns_replace(user_id=tp_replace['Нач.Отдела'], kolvo=tp_replace["Количество"],
                             equipment=tp_replace['Оборудование'],
                             sotrudnik=tp_replace['Сотрудник'], address=tp_replace['Адрес узла'],
                             comment_=tp_replace['Кoмментарий'])


@bot.message_handler(commands=["setting"])
def setting(message):
    try:
        tp_setting['Фам'] = message.from_user.id
        if message.from_user.id in tp_us:
            bot.send_message(message.chat.id, 'Введи номер накладной')
            bot.register_next_step_handler(message, nomer_nakladnoy)
    except Exception as e:
        bot.reply_to(message, 'В commands=[setting] ошибка: ' + f'{e}')
        print(e)


def setup_tp(message):
    try:
        tp_setting["NN"] = message.text
        if tp_setting["NN"].isdigit():
            if len(tp_setting["NN"]) < 4 or len(tp_setting['NN']) > 5:
                bot.send_message(message.chat.id, "Неверное количество символов. Введи номер накладной:")
                bot.register_next_step_handler(message, nomer_nakladnoy)
            elif int(message.text) in nn:
                bot.send_message(message.chat.id, "Такая накладная уже есть в базе. Введи правильный номер накладной:")
                bot.register_next_step_handler(message, nomer_nakladnoy)
            else:
                bot.send_message(message.chat.id, "Введи id оборудования:")
                bot.register_next_step_handler(message, id_oborudovaniya)
        else:
            bot.send_message(message.chat.id, 'Неверный формат. Введи номер накладной (только цифры):')
            bot.register_next_step_handler(message, nomer_nakladnoy)
    except Exception as e:
        bot.reply_to(message, 'В setup_tp ошибка: ' + f'{e}')
        print(e)


def nomer_nakladnoy(message):
    try:
        setup_tp(message)
    except Exception as e:
        bot.reply_to(message, 'В nomer_nakladnoy ошибка: ' + f'{e}')
        print(e)


def id_oborudovaniya(message):
    try:
        id_equip(message)
    except Exception as e:
        bot.reply_to(message, 'В id_oborudovaniya ошибка: ' + f'{e}')
        print(e)


def id_equip(message):
    global time_m
    try:
        tp_setting["id оборудования"] = message.text
        if tp_setting["id оборудования"].isdigit():
            if len(tp_setting["id оборудования"]) < 3 or len(tp_setting["id оборудования"]) > 5:
                bot.send_message(message.chat.id, "Неверное количество символов. Введи id оборудования:")
                bot.register_next_step_handler(message, id_oborudovaniya)
            elif int(message.text) in id_eq:
                bot.send_message(message.chat.id, "Так id уже есть в базе. Введи правильный id:")
                bot.register_next_step_handler(message, id_oborudovaniya)
            else:
                tp_setting['Дата настройки'] = time_m(message.date)
                tp_setting['Data_sett'] = message.date
                bot.send_message(message.chat.id, "Дата настройки: " f"{tp_setting['Дата настройки']} \nВыдал сегодня?")
                bot.register_next_step_handler(message, date_give)
        else:
            bot.send_message(message.chat.id, 'Неверный формат. Введи id оборудования (только цифры):')
            bot.register_next_step_handler(message, id_oborudovaniya)
    except Exception as e:
        bot.reply_to(message, 'В id_equip ошибка: ' + f'{e}')
        print(e)


def date_give(message):
    try:
        if 'да' in message.text.lower():
            if message.from_user.id in tp_us:
                tp_setting['Дата выдачи'] = time_m(message.date)
                tp_setting['Data_v'] = message.date
                bot.send_message(message.chat.id, "Дата выдачи: " + f"{tp_setting['Дата выдачи']}")
                view.add_columns_reestr_tp(tp_setup_id=tp_setting['Фам'], n_n=tp_setting["NN"],
                                           id_equip=tp_setting['id оборудования'],
                                           data_setup=tp_setting['Data_sett'],
                                           data_vid=tp_setting['Data_v'], data_install=0, tp_install_id=0)

        else:
            bot.send_message(message.chat.id, 'Введи команду /give_away когда будешь выдавать оборудование на руки')
            # bot.register_next_step_handler(message, date_give)
            view.add_columns_reestr_tp(tp_setup_id=tp_setting['Фам'], n_n=tp_setting["NN"],
                                       id_equip=tp_setting['id оборудования'],
                                       data_setup=tp_setting['Data_sett'],
                                       data_vid=0, data_install=0, tp_install_id=0)
    except Exception as e:
        bot.reply_to(message, 'В date_give ошибка: ' + f'{e}')
        print(e)
    print(tp_setting)


@bot.message_handler(commands=['give_away'])
def give_away(message):
    try:
        if message.from_user.id in us:
            bot.send_message(message.chat.id, 'Введи id выданного оборудования')
            bot.register_next_step_handler(message, check_id_vidacha)
    except Exception as e:
        bot.reply_to(message, 'В commands=[give_away] ошибка: ' + f'{e}')
        print(e)


def check_id_vidacha(message):
    try:
        give_m2(message)
    except Exception as e:
        bot.reply_to(message, 'В check_id_vidacha ошибка: ' + f'{e}')
        print(e)


def give_m2(message):
    global data_vid
    try:
        data_vid = view.data_vid()
        tp_setting['id_v'] = message.text
        if tp_setting['id_v'].isdigit():
            if len(tp_setting['id_v']) < 3 or len(tp_setting['id_v']) > 5:
                bot.send_message(message.chat.id, 'Неверное количество символов. Введи id выданного оборудования:')
                bot.register_next_step_handler(message, check_id_vidacha)
                for i in data_vid:
                    if int(message.text) == i[0]:
                        if i[1] != 0:
                            bot.send_message(message.chat.id,
                                                 "Это оборудование уже выдали. Введи id выданного оборудования:")
                            bot.register_next_step_handler(message, check_id_vidacha)
                else:
                    tp_setting['Дата выдачи'] = time_m(message.date)
                    tp_setting['Data_v'] = message.date
                    bot.send_message(message.chat.id, "Дата выдачи: " + f"{tp_setting['Дата выдачи']}")
                    view.add_data_vid_tp_update(tp_setting['Data_v'], tp_setting['id_v'])
        else:
            bot.send_message(message.chat.id, 'Неверный формат. Введи id оборудования (только цифры):')
            bot.register_next_step_handler(message, check_id_vidacha)
    except Exception as e:
        bot.reply_to(message, 'В give_m2 ошибка: ' + f'{e}')
        print(e)




@bot.message_handler(commands=['install'])
def install(message):
    try:
        if message.from_user.id in us:
            tp_setting['Принял установку'] = message.from_user.id
            bot.send_message(message.chat.id, 'Введи id установленного оборудования')
            bot.register_next_step_handler(message, install2)
    except Exception as e:
        bot.reply_to(message, 'В install ошибка: ' + f'{e}')
        print(e)


def install2(message):
    try:
        tp_setting['Проверка id'] = message.text
        tp_setting['Дата установки'] = time_m(message.date)
        tp_setting['Data_install'] = message.date
        bot.send_message(message.chat.id, "Дата установки: " + f"{tp_setting['Дата установки']}")

        view.add_data_install_tp_update(data_install=tp_setting['Data_install'],
                                        tp_install_id=tp_setting['Принял установку'],
                                        id_equi=tp_setting['Проверка id'])
    except Exception as e:
        bot.reply_to(message, 'В setup2 ошибка: ' + f'{e}')
        print(e)


# запуск бота
bot.enable_save_next_step_handlers(delay=2)
bot.load_next_step_handlers()
while True:
    try:
        if __name__ == '__main__':
            bot.infinity_polling(skip_pending=True)
    except Exception as e:
        logger.error(e)
        print(e)  # или просто print(e)
        time.sleep(15)
