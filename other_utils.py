import datetime


def get_age(birthday_raw):
    if birthday_raw == "Не указан":
        return "Неизвестен"
    else:
        birthday_cortage = [int(element) for element in reversed(birthday_raw.split("."))]
        date_now = \
            [int(datetime.datetime.now().year), int(datetime.datetime.now().month), int(datetime.datetime.now().day)]
        delta = date_now[0] - birthday_cortage[0]
        if date_now[1] < birthday_cortage[1]:
            delta -= 1
        elif date_now[1] == birthday_cortage[1]:
            if date_now[2] < birthday_cortage[2]:
                delta -= 1
    return str(delta)


def get_days_to_birthday(birthday_raw):
    if birthday_raw == "Не указан":
        return ""
    else:
        birthday_cortage = [int(element) for element in reversed(birthday_raw.split("."))][1:]
        date_now = datetime.date.today()
        date_birthday = \
            datetime.date(int(datetime.datetime.now().year), int(birthday_cortage[0]), int(birthday_cortage[1]))
        if str(date_birthday - date_now).split()[0] != '0:00:00':
            delta = int(str(date_birthday - date_now).split()[0])
            if delta < 0:
                date_birthday = \
                    datetime.\
                    date(int(datetime.datetime.now().year + 1), int(birthday_cortage[0]), int(birthday_cortage[1]))
                delta = int(str(date_birthday - date_now).split()[0])
        else:
            return "0"
    return str(delta)


def transform_phone(phone):
    if phone:
        if phone[0] == "+" and phone[1] == "7":
            phone = phone.replace("+7", "8", 1)[:]
    return phone
