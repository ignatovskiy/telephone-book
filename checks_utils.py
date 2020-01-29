def analysis_of_data(name, surname, birthday, phone):
    result_name_surname_test = _names_test(name, surname)
    result_birthday_test = _birthday_test(birthday)
    result_phone_test = _phone_test(phone)
    return result_name_surname_test, result_birthday_test, result_phone_test


def analysis_of_search(searching_data):
    error_list = []
    if searching_data[0]:
        if not searching_data[0].isalpha():
            error_list.append("Ошибка. Недопустимые символы в имени.")
        else:
            error_list.append("OK")
    if searching_data[1]:
        if not searching_data[1].isalpha():
            error_list.append("Ошибка. Недопустимые символы в фамилии.")
        else:
            error_list.append("OK")
    if searching_data[2]:
        error_list.append(_birthday_test(searching_data[2]))
    if searching_data[3]:
        error_list.append(_phone_test(searching_data[3]))
    return error_list


def _names_test(name, surname):
    if not name.isalpha() and not surname.isalpha():
        return "Ошибка! Недопустимые символы в имени и фамилии!"
    elif not name.isalpha():
        return "Ошибка! Имя содержит недопустимые символы!"
    elif not surname.isalpha():
        return "Ошибка! Фамилия содержит недопустимые символы!"
    return "OK"


def _birthday_test(birthday):
    if birthday != ('', '', ''):
        if '' in birthday:
            return "Ошибка! Заполните дату полностью!"
        elif int(birthday[1]) in (4, 6, 9, 11) and int(birthday[0]) == 31:
            return "Ошибка! В этом месяце 30 дней!"
        elif int(birthday[0]) > 29 and int(birthday[1]) == 2\
                or int(birthday[0]) == 29 \
                and int(birthday[1]) == 2 \
                and (int(birthday[2]) % 4 != 0 or (int(birthday[2]) % 100 == 0 and int(birthday[2]) % 400 != 0)):
            return "Ошибка! В этом году в феврале 28 дней!"
        return "OK"
    return "OK"


def _phone_test(phone):
    if not phone.isdigit():
        return "Ошибка! Недопустимые символы в номере телефона!"
    elif len(phone) != 11:
        return "Ошибка! Неверная длина номера телефона!"
    elif phone[0] != "8":
        return "Ошибка! Номер должен начинаться с 8 или +7"
    return "OK"
