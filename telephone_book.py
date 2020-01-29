import tkinter as tk
from tkinter import ttk
from database_utils import DataBase as DB
from checks_utils import analysis_of_data, analysis_of_search
from other_utils import get_age, transform_phone, get_days_to_birthday


class MainWindow(tk.Frame):

    def __init__(self):
        super().__init__(main_window)
        self.add_img = tk.PhotoImage(file="add_record.png")
        self.del_img = tk.PhotoImage(file="delete_record.png")
        self.edit_img = tk.PhotoImage(file="edit_record.png")
        self.search_img = tk.PhotoImage(file="search_record.png")
        self.show_img = tk.PhotoImage(file="show_record.png")
        self.show_all_img = tk.PhotoImage(file="show_all.png")
        self.records_list = ttk.Treeview(self,
                                         columns=('name', 'surname', 'birthday', 'phone'),
                                         height=20,
                                         show="headings")
        self.records_list.bind('<Button>', self.handle_click)
        self.db = db
        self.init_main_window_entities()
        self.view_records_list()

    def handle_click(self, event):
        if self.records_list.identify_region(event.x, event.y) == "separator":
            return "break"

    def init_main_window_entities(self):
        buttons_bar = tk.Frame(bg='#FFFFFF', bd=2)
        buttons_bar.pack(side=tk.TOP, fill=tk.X)

        btn_add_record = tk.Button(buttons_bar,
                                   text='Добавить запись',
                                   command=self.open_add_record_dialog,
                                   bg='#FFFFFF',
                                   compound=tk.TOP,
                                   image=self.add_img)
        btn_del_record = tk.Button(buttons_bar,
                                   text='Удалить запись',
                                   command=self.delete_records_from_db,
                                   bg='#FFFFFF',
                                   compound=tk.TOP,
                                   image=self.del_img)
        btn_edit_record = tk.Button(buttons_bar,
                                    text='Редактировать запись',
                                    command=self.open_edit_record_dialog,
                                    bg='#FFFFFF',
                                    compound=tk.TOP,
                                    image=self.edit_img)
        btn_search_record = tk.Button(buttons_bar,
                                      text='Найти запись',
                                      command=self.open_search_record_dialog,
                                      bg='#FFFFFF',
                                      compound=tk.TOP,
                                      image=self.search_img)
        btn_show_record = tk.Button(buttons_bar,
                                    text='Подробнее о записи',
                                    command=self.open_show_record_dialog,
                                    bg='#FFFFFF',
                                    compound=tk.TOP,
                                    image=self.show_img)
        btn_show_all = tk.Button(buttons_bar,
                                 text='Все записи',
                                 command=self.view_records_list,
                                 bg='#FFFFFF',
                                 compound=tk.TOP,
                                 image=self.show_all_img)

        btn_add_record.pack(side=tk.LEFT)
        btn_del_record.pack(side=tk.LEFT)
        btn_edit_record.pack(side=tk.LEFT)
        btn_search_record.pack(side=tk.LEFT)
        btn_show_record.pack(side=tk.LEFT)
        btn_show_all.pack(side=tk.LEFT)

        self.records_list.column("name", width=200, anchor=tk.CENTER)
        self.records_list.column("surname", width=200, anchor=tk.CENTER)
        self.records_list.column("birthday", width=126, anchor=tk.CENTER)
        self.records_list.column("phone", width=146, anchor=tk.CENTER)

        self.records_list.heading("name", text="Имя")
        self.records_list.heading("surname", text="Фамилия")
        self.records_list.heading("birthday", text="Дата рождения")
        self.records_list.heading("phone", text="Телефон")
        self.records_list.pack()

    def add_record_to_db(self, name, surname, birthday, phone):
        self.db.add_record(name,
                           surname,
                           birthday,
                           phone)
        self.view_records_list()

    def edit_record_in_db(self, name, surname, birthday, phone):
        if self.records_list.selection():
            self.db.edit_record(name,
                                surname,
                                birthday,
                                phone,
                                ((self.records_list.set(self.records_list.selection()[0])).get('name'),
                                (self.records_list.set(self.records_list.selection()[0])).get('surname'))
                                )
            self.view_records_list()

    def delete_records_from_db(self):
        selected_records = self.records_list.selection()
        for record in selected_records:
            self.db.delete_record((self.records_list.set(record))['name'],
                                  (self.records_list.set(record))['surname'])
        self.view_records_list()

    def view_records_list(self):
        self.db.cursor.execute('''SELECT * FROM phone_book ORDER BY name, surname''')
        [self.records_list.delete(record) for record in self.records_list.get_children()]
        [self.records_list.insert('', 'end', values=record) for record in self.db.cursor.fetchall()]

    def open_add_record_dialog(self):
        AddRecordWindow()

    def open_edit_record_dialog(self):
        if self.records_list.selection():
            EditRecordWindow(self.records_list.set(self.records_list.selection()[0]))

    def open_show_record_dialog(self):
        if self.records_list.selection():
            ShowRecord()

    def open_search_record_dialog(self):
        SearchWindow()


class AddRecordWindow(tk.Toplevel):
    def __init__(self):
        super().__init__(main_window)

        self.entry_name = ttk.Entry(self)
        self.entry_surname = ttk.Entry(self)
        self.entry_birth_day = ttk.Combobox(self, state='readonly', width=2)
        self.entry_birth_month = ttk.Combobox(self, state='readonly', width=2)
        self.entry_birth_year = ttk.Combobox(self, state='readonly', width=4)
        self.entry_birthday = ttk.Entry(self)
        self.entry_phone = ttk.Entry(self)

        self.status = tk.StringVar()
        self.label_status = tk.Message(self, textvariable=self.status, width=350)

        self.button_add = ttk.Button(self, text="Добавить")
        self.button_cancel = ttk.Button(self, text="Закрыть", command=self.destroy)

        self.in_main_window = application
        self.init_window_entities()

    def init_window_entities(self):
        self.title("Добавление записи в базу")
        self.geometry('360x280+400+300')
        self.resizable(False, False)

        label_name = tk.Label(self, text="Имя")
        label_name.place(x=0, y=20)
        label_surname = tk.Label(self, text="Фамилия")
        label_surname.place(x=0, y=50)
        label_birthday = tk.Label(self, text="День рождения")
        label_birthday.place(x=0, y=80)
        label_phone = tk.Label(self, text="Телефон")
        label_phone.place(x=0, y=110)

        self.entry_birth_day['values'] = list(range(1, 32))
        self.entry_birth_month['values'] = list(range(1, 13))
        self.entry_birth_year['values'] = list(reversed(range(1900, 2020)))

        self.entry_name.place(x=150, y=20)
        self.entry_surname.place(x=150, y=50)
        self.entry_birth_day.place(x=150, y=80)
        self.entry_birth_month.place(x=190, y=80)
        self.entry_birth_year.place(x=230, y=80)
        self.entry_phone.place(x=150, y=110)

        self.button_add.place(x=65, y=170)
        self.button_add.bind('<Button-1>',
                             lambda event: self.adding_record(self.entry_name.get().title(),
                                                              self.entry_surname.get().title(),
                                                              (self.entry_birth_day.get(),
                                                              self.entry_birth_month.get(),
                                                              self.entry_birth_year.get()),
                                                              self.entry_phone.get()))

        self.button_cancel.place(x=200, y=170)

        self.label_status.place(x=0, y=200)

    def adding_record(self, name, surname, birthday, phone):
        phone = transform_phone(phone)

        errors_result = \
            [error for error in analysis_of_data(str(name), str(surname), birthday, str(phone)) if error != "OK"]

        if errors_result:
            self.status.set("\n".join(errors_result))

        elif list(self.in_main_window.db.cursor.execute('SELECT * FROM phone_book WHERE name=? AND surname=?',
                                                        (name, surname))):

            self.status.set("")
            CollisionDialog([name, surname, birthday, phone])

        else:

            if birthday == ('', '', ''):
                birthday = ["Не указан"]

            self.in_main_window.add_record_to_db(name, surname, ".".join(birthday), phone)
            self.destroy()


class EditRecordWindow(AddRecordWindow):
    def __init__(self, selection):
        super().__init__()
        self.button_add.destroy()
        self.button_edit = ttk.Button(self, text="Редактировать")
        self.in_main_window = application
        self.selection = selection
        self.entry_name.insert(0, self.selection['name'])
        self.entry_surname.insert(0, self.selection['surname'])
        self.entry_phone.insert(0, self.selection['phone'])
        self.init_edit_window_entities()

    def init_edit_window_entities(self):
        self.title("Редактирование записи")
        self.button_edit.place(x=65, y=170)

        if self.selection['birthday'] != "Не указан":
            birthday_list = self.selection['birthday'].split(".")
            self.entry_birth_day.set(int(birthday_list[0]))
            self.entry_birth_month.set(int(birthday_list[1]))
            self.entry_birth_year.set(int(birthday_list[2]))

        self.button_edit.bind('<Button-1>',
                              lambda event: self.editing_record(self.entry_name.get().title(),
                                                                self.entry_surname.get().title(),
                                                                (self.entry_birth_day.get(),
                                                                self.entry_birth_month.get(),
                                                                self.entry_birth_year.get()),
                                                                self.entry_phone.get()))

    def editing_record(self, name, surname, birthday, phone):
        phone = transform_phone(phone)

        errors_result = \
            [error for error in analysis_of_data(str(name), str(surname), birthday, str(phone)) if error != "OK"]
        if errors_result:
            self.status.set("\n".join(errors_result))
        elif name != self.selection['name'] and surname != self.selection['surname'] and\
                list(self.in_main_window.db.cursor.execute('SELECT * FROM phone_book WHERE name=? AND surname=?',
                                                           (name, surname))):

            self.status.set("")
            CollisionDialog([name, surname, birthday, phone])
        else:
            if birthday == ('', '', ''):
                birthday = ["Не указан"]
            self.in_main_window.edit_record_in_db(name, surname, ".".join(birthday), phone)
            self.destroy()


class ShowRecord(tk.Toplevel):
    def __init__(self):
        super().__init__(main_window)

        self.in_main_window = application

        self.needed_record = self.in_main_window.records_list.set(self.in_main_window.records_list.selection()[0])
        self.to_birthday = get_days_to_birthday(self.needed_record['birthday'])
        self.init_show_window_entities()

    def init_show_window_entities(self):
        self.title("Информация о человеке")
        self.geometry('360x200+400+300')
        self.resizable(False, False)

        if self.to_birthday == "0":
            text_birthday = self.needed_record['birthday'] + " (Сегодня ДР!)"
        elif self.needed_record['birthday'] != "Не указан":
            text_birthday = self.needed_record['birthday'] + " (ДР через {} д.)".format(self.to_birthday)
        else:
            text_birthday = self.needed_record['birthday']

        label_name = tk.Label(self, text="Имя")
        label_name.place(x=0, y=20)
        label_surname = tk.Label(self, text="Фамилия")
        label_surname.place(x=0, y=50)
        label_birthday = tk.Label(self, text="Дата рождения")
        label_birthday.place(x=0, y=80)
        label_age = tk.Label(self, text="Возраст")
        label_age.place(x=0, y=110)
        label_phone = tk.Label(self, text="Телефон")
        label_phone.place(x=0, y=140)

        label_name = tk.Label(self, text=self.needed_record['name'])
        label_name.place(x=150, y=20)
        label_surname = tk.Label(self, text=self.needed_record['surname'])
        label_surname.place(x=150, y=50)
        label_birthday = tk.Label(self, text=text_birthday)
        label_birthday.place(x=150, y=80)
        label_age = tk.Label(self, text=get_age(self.needed_record['birthday']))
        label_age.place(x=150, y=110)
        label_phone = tk.Label(self, text=self.needed_record['phone'])
        label_phone.place(x=150, y=140)

        button_close = ttk.Button(self, text="Закрыть", command=self.destroy)
        button_close.place(x=150, y=170)


class CollisionDialog(tk.Toplevel):
    def __init__(self, collision_record):
        super().__init__(main_window)
        self.cr = collision_record

        self.in_main_window = application
        self.init_collision_window_entities()

    def init_collision_window_entities(self):
        self.title("Запись с такими инициалами уже существует")
        self.geometry('450x100+400+300')
        self.resizable(False, False)

        label_name = tk.Label(self, text="Перезаписать существующую запись или изменить данные новой?")
        label_name.place(x=0, y=20)

        button_collision = ttk.Button(self, text="Перезаписать", command=self.turn_into_editing)
        button_collision.place(x=30, y=50)

        button_close = ttk.Button(self, text="Изменить текущие данные", command=self.destroy)
        button_close.place(x=220, y=50)

    def turn_into_editing(self):
        self.destroy()
        if self.cr[2] == ('', '', ''):
            self.cr[2] = "Не указан"
        else:
            self.cr[2] = ".".join(self.cr[2])
        self.in_main_window.db.edit_record(self.cr[0],
                                           self.cr[1],
                                           self.cr[2],
                                           self.cr[3],
                                           (self.cr[0],
                                           self.cr[1]))
        self.in_main_window.view_records_list()


class SearchWindow(tk.Toplevel):
    def __init__(self):
        super().__init__(main_window)
        self.sql_request = []

        self.entry_name = ttk.Entry(self, width=15)
        self.entry_surname = ttk.Entry(self, width=15)
        self.entry_birth_day = ttk.Combobox(self, state='readonly', width=2)
        self.entry_birth_month = ttk.Combobox(self, state='readonly', width=2)
        self.entry_birth_year = ttk.Combobox(self, state='readonly', width=4)
        self.entry_phone = ttk.Entry(self, width=15)

        self.status = tk.StringVar()
        self.label_status = tk.Message(self, textvariable=self.status, width=350)

        self.button_close = ttk.Button(self, text="Закрыть", command=self.destroy)
        self.button_search = ttk.Button(self, text="Поиск")
        self.button_birthdays = ttk.Button(self, text="Ближайшие ДР", command=self.show_nearest_birthdays)
        self.in_main_window = application
        self.init_search_window_entities()

    def init_search_window_entities(self):
        self.title("Поиск/Фильтры")
        self.geometry('600x200+400+300')
        self.resizable(False, False)

        label_name = tk.Label(self, text="Имя")
        label_name.place(x=0, y=25)
        label_surname = tk.Label(self, text="Фамилия")
        label_surname.place(x=150, y=25)
        label_birthday = tk.Label(self, text="День рождения")
        label_birthday.place(x=300, y=25)
        label_phone = tk.Label(self, text="Телефон")
        label_phone.place(x=450, y=25)

        self.entry_birth_day['values'] = list(range(1, 32))
        self.entry_birth_month['values'] = list(range(1, 13))
        self.entry_birth_year['values'] = list(reversed(range(1900, 2020)))

        self.entry_name.place(x=0, y=50)
        self.entry_surname.place(x=150, y=50)
        self.entry_birth_day.place(x=300, y=50)
        self.entry_birth_month.place(x=340, y=50)
        self.entry_birth_year.place(x=380, y=50)
        self.entry_phone.place(x=450, y=50)

        self.button_close.place(x=380, y=90)
        self.button_birthdays.place(x=150, y=90)

        self.button_search.bind('<Button-1>',
                                lambda event: self.searching(self.entry_name.get().title(),
                                                             self.entry_surname.get().title(),
                                                             (self.entry_birth_day.get(),
                                                             self.entry_birth_month.get(),
                                                             self.entry_birth_year.get()),
                                                             self.entry_phone.get()))
        self.button_search.place(x=285, y=90)
        self.label_status.place(x=0, y=120)

    def show_nearest_birthdays(self):
        self.in_main_window.db.cursor.execute('''SELECT * FROM phone_book ORDER BY birthday''')
        [self.in_main_window.records_list.delete(record) for record in self.in_main_window.records_list.get_children()]
        [self.in_main_window.records_list
             .insert('', 'end', values=record)
         for record in self.in_main_window.db.cursor.fetchall()
         if record[2] != "Не указан" and int(get_days_to_birthday(record[2])) < 31]
        self.destroy()

    def searching(self, name, surname, birthday, phone):
        phone = transform_phone(phone)

        errors_result = \
            [error for error in analysis_of_search((str(name), str(surname), birthday, str(phone))) if error != "OK"]

        if errors_result:
            self.status.set("\n".join(errors_result))

        elif not name and not surname and not phone and birthday == ('', '', ''):
            self.status.set("Вы не заполнили ни одного поля поиска!")

        else:
            self.status.set("")

            if birthday != ('', '', ''):
                birthday = ".".join(birthday)
            else:
                birthday = "birthday"

            search_dict = {"name": name, "surname": surname, "birthday": birthday, "phone": phone}
            pre_search_dict = {"name": "name", "surname": "surname", "birthday": "birthday", "phone": "phone"}

            for element in search_dict:
                if search_dict[element] not in ('', ('', '', '')):
                    pre_search_dict[element] = search_dict[element]

            self.sql_request = " AND "\
                .join(element + "=?" for element in pre_search_dict if element != pre_search_dict[element])

            self.in_main_window.db.cursor\
                .execute('SELECT * FROM phone_book WHERE ' + self.sql_request,
                         list(pre_search_dict[element]
                              for element in pre_search_dict if element != pre_search_dict[element]))

            [self.in_main_window.records_list.delete(record)
             for record in self.in_main_window.records_list.get_children()]
            [self.in_main_window.records_list.insert('', 'end', values=record)
             for record in self.in_main_window.db.cursor.fetchall()]
            self.destroy()


if __name__ == "__main__":
    db = DB()
    main_window = tk.Tk()
    application = MainWindow()
    application.pack()
    main_window.title("Телефонный справочник")
    main_window.geometry("666x400+300+200")
    main_window.resizable(False, False)
    main_window.mainloop()

