import sqlite3 as sql


class DataBase:
    def __init__(self):
        self.db_connect = sql.connect("phone_book.db")
        self.cursor = self.db_connect.cursor()
        self.cursor\
            .execute('''CREATE TABLE IF NOT EXISTS phone_book (name text, surname text, birthday text, phone integer)''')
        self.db_connect.commit()

    def add_record(self, name, surname, birthday, phone):
        self.cursor.execute('''INSERT INTO phone_book(name, surname, birthday, phone) VALUES (?, ?, ?, ?)''',
                            (name, surname, birthday, phone))
        self.db_connect.commit()

    def edit_record(self, name, surname, birthday, phone, choice):
        self.cursor \
            .execute('''UPDATE phone_book SET name=?, surname=?, birthday=?, phone=? WHERE name=? AND surname=?''',
                     (name, surname, birthday, phone,
                      choice[0], choice[1]))
        self.db_connect.commit()

    def delete_record(self, name, surname):
        self.cursor.execute('''DELETE FROM phone_book WHERE name=? AND surname=?''',
                            (name, surname))
        self.db_connect.commit()
