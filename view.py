import sqlite3

from prettytable import PrettyTable
from prettytable import from_db_cursor


def pretty():
    with sqlite3.connect('database.db') as db:
        cursor = db.cursor()
        cursor.execute(""" SELECT * from reestr_tp """)
        mytable = from_db_cursor(cursor)
        db.commit()
        return (mytable)


def creat_table_users_name():
    with sqlite3.connect('database.db') as db:
        cursor = db.cursor()
        query = """ CREATE TABLE IF NOT EXISTS equipment (id INTEGER PRIMARY KEY UNIQUE NOT NULL, equipment TEXT NOT NULL) """
        cursor.execute(query)
        db.commit()


def add_c_equ():
    with sqlite3.connect('database.db') as db:
        cursor = db.cursor()
        query2 = """ INSERT INTO equipment (equipment) VALUES(Mikrotik_rb750gr3) """
        cursor.execute(query2)
        db.commit()


def add_columns_users_name():
    with sqlite3.connect('database.db') as db:
        cursor = db.cursor()
        query1 = """ INSERT INTO users_name (tlgrm_user_id, names) VALUES(35409597, 'Шуруба') """
        query2 = """ INSERT INTO users_name (tlgrm_user_id, names) VALUES(678077096, 'Метешкин') """
        query3 = """ INSERT INTO users_name (tlgrm_user_id, names) VALUES(724749503, 'Губин') """
        query4 = """ INSERT INTO users_name (tlgrm_user_id, names) VALUES(1908124857, 'Корниенко') """
        cursor.execute(query1)
        cursor.execute(query2)
        cursor.execute(query3)
        cursor.execute(query4)
        db.commit()


# добавление в таблицу заявки на выдачу
def add_columns_reestr(user_id, equipment, kolvo, sotrudnik, address, reason, comment_):
    with sqlite3.connect('database.db') as db:
        cursor = db.cursor()
        cursor.execute(
            """ INSERT INTO reestr (user_id, equipment, kolvo, sotrudnik, address, reason, comment_) 
            VALUES (?, ?, ?, ?, ?, ?, ?) """,
            (user_id, equipment, kolvo, sotrudnik, address, reason, comment_))
        db.commit()

def add_reestr_tp(
    tp_setup_id, n_n, id_equip, data_setup, data_vid, data_install, tp_install_id
):
    with sqlite3.connect('database.db') as db:
        cursor = db.cursor()
        cursor.execute(
            """ INSERT INTO reestr_tp (tp_setup_id, n_n, id_equip, data_setup, data_vid, data_install, 
            tp_install_id) 
            VALUES (?, ?, ?, ?, ?, ?, ?) """,
            (
                tp_setup_id,
                n_n,
                id_equip,
                data_setup,
                data_vid,
                data_install,
                tp_install_id
            )
        )
        db.commit()


def add_reestr_all(user_id, equipment, number, sotrudnik, address, reason, comment_, tp_setup_id, n_n, id_equip,
                   data_setup, data_vid, data_install, tp_install_id):
    with sqlite3.connect('database.db') as db:
        cursor = db.cursor()
        cursor.execute(
            """ INSERT INTO reestr_all (user_id, equipment, number, sotrudnik, address, reason, comment_, tp_setup_id, n_n, id_equip, data_setup, data_vid, data_install, tp_install_id) 
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?) """,
            (user_id, equipment, number, sotrudnik, address, reason, comment_, tp_setup_id, n_n, id_equip, data_setup,
             data_vid, data_install, tp_install_id))
        db.commit()


def add_columns_replace(user_id, equipment, kolvo, sotrudnik, address, comment_):
    with sqlite3.connect('database.db') as db:
        cursor = db.cursor()
        cursor.execute(
            """ INSERT INTO replace_equip (user_id, equipment, kolvo, sotrudnik, address, comment_) 
            VALUES (?, ?, ?, ?, ?, ?) """,
            (user_id, equipment, kolvo, sotrudnik, address, comment_))
        db.commit()


# возврат на склад
def add_return_equipment(equipment_id):
    with sqlite3.connect('database.db') as db:
        cursor = db.cursor()
        cursor.execute(""" INSERT INTO return_equipment (equipment_id)
        VALUES (?) """,
                       (equipment_id,))
        db.commit()

# добавление в таблицу данных о настройке
def reestr_all_update(
    tp_setup_id, n_n, id_equip, data_setup, data_vid, data_install, tp_install_id
):
    with sqlite3.connect('database.db') as db:
        cursor = db.cursor()
        cursor.execute(
            """UPDATE reestr_all SET tp_setup_id=?, n_n=?, id_equip=?, data_setup=?, data_vid=?, data_install=?, 
            tp_install_id=? """,
            (
                tp_setup_id,
                n_n,
                id_equip,
                data_setup,
                data_vid,
                data_install,
                tp_install_id
            )
        )
        db.commit()


# обновление таблицы reestr_tp
def add_data_vid_tp_update(data_vid, id_equip):
    with sqlite3.connect('database.db') as db:
        cursor = db.cursor()
        cursor.execute("""
               UPDATE reestr_tp
               SET data_vid=?
               WHERE id_equip=?
            """, (data_vid, id_equip))
        db.commit()


# обновление таблицы reestr_tp
def add_data_install_tp_update(data_install, tp_install_id, id_equi):
    with sqlite3.connect('database.db') as db:
        cursor = db.cursor()
        cursor.execute("""
                       UPDATE reestr_tp
                       SET data_install=?, tp_install_id=?
                       WHERE id_equip=?
                    """, (data_install, tp_install_id, id_equi))
        db.commit()


def check_id_equipment():
    with sqlite3.connect('database.db') as db:
        cursor = db.cursor()
        cursor.execute("""
               SELECT id_equip FROM reestr_tp """)
        abc = cursor.fetchall()
        db.commit()
        return (abc)


# номер накладной для проверки перед обновлением таблицы
def check_NN():
    with sqlite3.connect('database.db') as db:
        cursor = db.cursor()
        cursor.execute("""
               SELECT n_n FROM reestr_tp """)
        abc = cursor.fetchall()
        db.commit()
        return (abc)

# список всего оборудования для команды /give
def select_equip():
    with sqlite3.connect('database.db') as db:
        cursor = db.cursor()
        cursor.execute(""" SELECT equipment, info FROM equipment """)
        abc = cursor.fetchall()
        db.commit()
        return (abc)


# id оборудования и дата выдачи для проверки перед обновлением таблицы
def data_vid():
    with sqlite3.connect('database.db') as db:
        cursor = db.cursor()
        cursor.execute(""" SELECT id_equip, data_vid from reestr_tp """)
        abc = cursor.fetchall()
        db.commit()
        return (abc)

# id оборудования для проверки наличия id в базе// дубль. можно использовать check_id_equipment
# def data_vidachi():
#     with sqlite3.connect('database.db') as db:
#         cursor = db.cursor()
#         cursor.execute(""" SELECT id_equip from reestr_tp """)
#         abc = cursor.fetchall()
#         db.commit()
#         return (abc)

# id оборудования и дата установки для проверки перед обновлением таблицы
def data_install():
    with sqlite3.connect('database.db') as db:
        cursor = db.cursor()
        cursor.execute(""" SELECT id_equip, data_install from reestr_tp """)
        abc = cursor.fetchall()
        db.commit()
        return (abc)

# список фамилий и id телеги нач. отделов для сопоставления
def otdely_tlgrm_user_id():
    with sqlite3.connect('database.db') as db:
        cursor = db.cursor()
        cursor.execute(""" SELECT telegram_user_id, names from users_name """)
        spisok = cursor.fetchall()
        db.commit()
        return (spisok)

#список фамилий и id телеги ТП для сопоставления
def tp_name_user_id():
    with sqlite3.connect('database.db') as db:
        cursor = db.cursor()
        cursor.execute(""" SELECT telegram_id, names from tp_users """)
        spisok = cursor.fetchall()
        db.commit()
        return (spisok)

#список id телеги нач.отделов
def nachalniki_otdelov_id():
    with sqlite3.connect('database.db') as db:
        cursor = db.cursor()
        cursor.execute(""" SELECT telegram_user_id from users_name """)
        spisok = cursor.fetchall()
        db.commit()
        return (spisok)

#список id телеги ТП
def tehpod_user_id():
    with sqlite3.connect('database.db') as db:
        cursor = db.cursor()
        cursor.execute(""" SELECT telegram_id from tp_users """)
        spisok = cursor.fetchall()
        db.commit()
        return (spisok)

# запрос всех данных таблицы реестр, где хранятся данные о выдаче железа
def reestr_table():
    with sqlite3.connect('database.db') as db:
        cursor = db.cursor()
        cursor.execute(""" SELECT user_id, equipment, kolvo, sotrudnik, 
        address, reason, comment_ from reestr """)
        spisok = cursor.fetchall()
        db.commit()
        return spisok

# запрос всех данных таблицы реестр_тп, где хранятся данные о настройке железа
def reestr_tp_table():
    with sqlite3.connect('database.db') as db:
        cursor = db.cursor()
        cursor.execute(""" SELECT tp_setup_id, n_n, id_equip, data_setup, 
        data_vid, data_install, tp_install_id from reestr_tp """)
        spisok = cursor.fetchall()
        db.commit()
        return spisok

# тест для общей таблицы. неиспользую
# def testtest():
#     with sqlite3.connect('database.db') as db:
#         cursor = db.cursor()
#         cursor.execute(""" SELECT user_id, equipment, kolvo, sotrudnik,
#         address, reason, comment_
#         FROM reestr
#         INNER JOIN users_name ON reestr.user_id = users_name.telegram_user_id
#         """)
#         spisok = cursor.fetchall()
#         db.commit()
#         return spisok