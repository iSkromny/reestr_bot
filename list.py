import html
import sqlite3
import pandas as pd
import numpy as np
import view
import time
from pprint import pprint

# tm = time.strftime("%a, %d %b %Y", time.localtime())

#pandas и попытка через него в таблицу
view.reestr_table()
arr = view.reestr_table()
# print(arr)
tbl = pd.DataFrame(arr, columns=["Начальник отдела", "Оборудование", "Количество", "Сотрудник", "Адрес установки", "Обоснование", "Комментарий"])
s = ["<!DOCTYPE HTML><HTML>"]
s.append("<HEAD><TITLE>Реестр </TITLE>"
         '<meta http-equiv="Content-Type" content="text/html" charset="windows-1251">'
         "<link  rel='stylesheet' type='text/css' href='style.css' /></HEAD>")
s.append("<BODY><HEADER><a href='' class='logo'>Выдано</a></HEADER>")
s.append(tbl.to_html())
s.append("</BODY></HTML>")
html_tab = ''.join(s)
html_file_tab = open('table.html', 'w')
html_file_tab.write(html_tab)
html_file_tab.close()




massive_setup = []
for i_item in view.reestr_tp_table():
     massive_setup.append([
          *i_item[:3],
          time.strftime("%a, %d %b %Y %H:%M", time.localtime(i_item[3])),
          time.strftime("%a, %d %b %Y %H:%M", time.localtime(i_item[4])),
          time.strftime("%a, %d %b %Y %H:%M", time.localtime(i_item[5])),
          i_item[6]
     ])
# pprint(massive_setup)
tbl2 = pd.DataFrame(massive_setup, columns=["Настроил", "Номер накладной", "ID оборудования", "Дата настройки", "Дата выдачи", "Дата установки", "Кто принял установку"])
q = ["<!DOCTYPE HTML><HTML>"]
q.append("<HEAD><TITLE>Реестр </TITLE>"
         '<meta http-equiv="Content-Type" content="text/html" charset="windows-1251">'
         "<link  rel='stylesheet' type='text/css' href='style.css' /></HEAD>")
q.append("<BODY><HEADER><a href='' class='logo'>Настроено</a></HEADER>")
q.append(tbl2.to_html())
q.append("</BODY></HTML>")
html_tab2 = ''.join(q)
html_file_tab2 = open('table2.html', 'w')
html_file_tab2.write(html_tab2)
html_file_tab2.close()


