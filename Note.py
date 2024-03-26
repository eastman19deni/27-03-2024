import operator
import os
import random
from csv import DictReader, DictWriter


class LenNumberError(Exception):
    def __init__(self, txt):
        self.txt = txt


class SmallerThanMin(Exception):
    def __init__(self, txt):
        self.txt = txt


class BiggerThanMax(Exception):
    def __init__(self, txt):
        self.txt = txt


class FileNameLength(Exception):
    def __init__(self, txt):
        self.txt = txt


class WrongFileName(Exception):
    def __init__(self, txt):
        self.txt = txt


def get_new_contact(edit, modifying_contact):
    if edit:
        first_name_old = modifying_contact["Имя"]
        second_name_old = modifying_contact["Отчество"]
        last_name_old = modifying_contact["Фамилия"]
        print("Чтобы сохранить текущее значение, оставьте строку пустой.")
        print("Для определения пустого значения введите один пробел")
        first_name = input(f"Введите имя ({first_name_old}): ")
        second_name = input(f"Введите отчество ({second_name_old}): ")
        last_name = input(f"Введите фамилию ({last_name_old}): ")
        if first_name == " ":
            first_name = ""
        elif first_name == "":
            first_name = first_name_old
        if second_name == " ":
            second_name = ""
        elif second_name == "":
            second_name = second_name_old
        if last_name == " ":
            last_name = ""
        elif last_name == "":
            last_name = last_name_old
    else:
        first_name = input("Введите имя: ")
        second_name = input("Введите отчество: ")
        last_name = input("Введите фамилию: ")
    date = 0
    is_valid_date = False
    while not is_valid_date:
        try:
            if edit:
                date = modifying_contact["Дата"]
                date_string = input(f"Введите дату dd mm yyyy ({str(date)}): ")
                if date_string == "":
                    date_string = str(date)
                date = int(date_string)
            else:
                date = int(input("Введите дату: "))
            
        except ValueError:
            print("Дата должен состоять только из цифр.")
        except LenNumberError as error:
            print(error)
            continue
        is_valid_date = True
    return {"Имя": first_name, "Отчество": second_name, "Фамилия": last_name, "Дата": date}


def get_random_element(sequence):
    return sequence[random.randint(0, len(sequence) - 1)]


def create_file(file_name):
    # with - менеджер контекста
    with open(file_name, 'w', encoding="UTF-8") as data:
        f_writer = DictWriter(data, fieldnames=["Имя", "Отчество", "Фамилия", "Дата"])
        f_writer.writeheader()
        print(f"Файл сохранен под именем {file_name}")


def read_file(file_name):
    with open(file_name, 'r', encoding="UTF-8") as data:
        f_reader = DictReader(data)
        return list(f_reader)


def write_file(file_name, contacts_list):
    with open(file_name, 'w', encoding="UTF-8", newline='') as data:
        f_writer = DictWriter(data, fieldnames=["Имя", "Отчество", "Фамилия", "Дата"])
        f_writer.writeheader()
        f_writer.writerows(contacts_list)
        print(f"Файл {file_name} сохранен.")


def required_length_string(text, required_length):
    text = str(text)
    current_length = len(text)
    if current_length >= required_length:
        return text[0:required_length]
    else:
        return text + " " * (required_length - current_length)


def dictionaries_chars_count(dictionaries_list):
    result = {"Имя": 3, "Фамилия": 7, "Отчество": 8, "Дата": 11, "№": len(str(len(dictionaries_list)))}
    for current_dictionary in dictionaries_list:
        for current_key in current_dictionary.keys():
            current_value = len(str(current_dictionary.get(current_key)))
            saved_value = result.get(current_key)
            if saved_value is None:
                result[current_key] = current_value
            elif current_value > saved_value:
                result[current_key] = current_value
    return result


def dictionaries_list_to_text(dictionaries_list, numerated, numbers_list):
    if len(dictionaries_list) > 0:
        chars_count = dictionaries_chars_count(dictionaries_list)
        slim_end = '|'
        wide_end = " | "
        # Шапка таблицы
        result = f"| {required_length_string('№', chars_count['№'])}" + wide_end
        for key in dictionaries_list[0].keys():
            result += (required_length_string(key, chars_count[key])) + wide_end
        result += '\n'
        # Разделитель шапки
        result += f"|-{'-' * (chars_count['№'] + 1)}|"
        for key in dictionaries_list[0].keys():
            result += ("-" * (chars_count[key] + 2) + slim_end)
        result += '\n'
        # Строки таблицы
        for i in range(len(dictionaries_list)):
            contact = dictionaries_list[i]
            index = numbers_list[i] if numerated else i + 1
            result += (f"| {required_length_string(index, chars_count['№'])}" + wide_end)
            for key in contact.keys():
                result += (required_length_string(contact[key], chars_count[key]) + wide_end)
            i += 1
            result += '\n'
        return result
    else:
        return "Список пустой."


def select_element_from_list(my_list, to_print_list, message):
    if len(my_list) == 0:
        return -1
    else:
        if to_print_list:
            print(f"{message}:")
            for i in range(len(my_list)):
                print(i + 1, end="\t")
                print(my_list[i])
        while True:
            try:
                number = int(input("Введите дату для выбора строки: "))
                if 0 < number <= len(my_list):
                    return number - 1
                else:
                    print("В списке нет строки с такой датой.")
            except ValueError:
                print("Необходимо ввести целое число из списка.")


def look_up_for_tables():
    files_list = list()
    for entry in os.scandir(os.getcwd()):
        if entry.is_file():
            if os.path.splitext(entry.path)[1] == ".csv":
                files_list.append(entry.name)
    return files_list


def enter_file_name():
    while True:
        try:
            result = input("Введите имя, под которым файл будет сохранен: ").replace("\r\n", " ") + ".csv"
            directory_path = os.getcwd()
            full_path = directory_path + result
            if (len(full_path)) > 255:
                raise FileNameLength("Путь к файлу не может быть длиннее 255 символов. Сократите имя файла.")
            else:
                for ch in result:
                    if ch in {"<", ">", ":", "\"", "/", "\\", "|", "?", "*"}:
                        raise WrongFileName("Имя файла не может содержать символы < > : \" / \\ | ? *")
            return result
        except FileNameLength as error:
            print(error)
        except WrongFileName as error:
            print(error)


def enter_list_length():
    while True:
        try:
            result = int(input("Введите длину списка контактов: "))
            if result < 1:
                raise SmallerThanMin("Длина списка должна быть больше нуля.")
            elif result > 1000:
                raise BiggerThanMax("Программа не предназначена для работы с более чем 1000 контактов.")
            return result
        except ValueError:
            print("Длина списка контактов должна быть целым числом.")
            continue
        except SmallerThanMin as error:
            print(error)
        except BiggerThanMax as error:
            print(error)


def create_new_file():
    file_name = enter_file_name()
    create_file(file_name)
    contacts_list = list()
    work_with_file(file_name, contacts_list)


def open_existing_file():
    files_list = look_up_for_tables()
    if len(files_list) > 0:
        file_name = files_list[select_element_from_list(files_list, True, "Список файлов")]
        contacts_list = read_file(file_name)
        work_with_file(file_name, contacts_list)
    else:
        print("В текущей директории нет подходящих файлов.")


def remove_contact(contacts_list):
    if len(contacts_list) == 0:
        print("Список контактов пуст.")
    else:
        index = select_element_from_list(contacts_list, False, "")
        contacts_list.pop(index)
        print(f"Контакт №{index + 1} удален.")


def edit_contact(contacts_list):
    if len(contacts_list) == 0:
        print("Список контактов пуст.")
    else:
        index = select_element_from_list(contacts_list, False, "")
        contacts_list[index] = get_new_contact(True, contacts_list[index])
        print(f"Контакт №{index + 1} изменен.")


def move_contact(contacts_list):
    if len(contacts_list) == 0:
        print("Список контактов пуст.")
    else:
        index = select_element_from_list(contacts_list, False, "")
        while True:
            print("Перенести контакт: \"n\" – в новый список, \"o\" – в существующий.")
            command = input("Введите команду: ").lower()
            if command == "n":
                file_name = enter_file_name()
                write_file(file_name, [contacts_list[index]])
                break
            elif command == "o":
                files_list = look_up_for_tables()
                if len(files_list) > 0:
                    file_name = files_list[select_element_from_list(files_list, True, "Список файлов")]
                    another_contacts_list = read_file(file_name)
                    another_contacts_list.append(contacts_list[index])
                    write_file(file_name, another_contacts_list)
                    break
                else:
                    print("В текущей директории нет подходящих файлов.")


def find_contacts(contacts_list):
    if len(contacts_list) > 0:
        scores = list()
        matches = list()
        indexes = list()
        keywords = input("Введите поисковый запрос: ").lower().split(" ")
        for i in range(len(contacts_list)):
            contact = contacts_list[i]
            index = i + 1
            score = 0
            for keyword in keywords:
                if keyword in contact["Имя"].lower():
                    score -= 1
                if keyword in contact["Отчество"].lower():
                    score -= 1
                if keyword in contact["Фамилия"].lower():
                    score -= 1
                if keyword in str(contact["Дата"]).lower():
                    score -= 1
            if score < 0:
                scores.append(score)
                matches.append(contact)
                indexes.append(index)
        if len(matches) > 0:
            result = sorted(list(zip(scores, indexes, matches)), key=operator.itemgetter(0, 1))
            result_matches = list()
            result_indexes = list()
            for x in result:
                result_matches.append(x[2])
                result_indexes.append(x[1])
            print("Результаты поиска:")
            print(dictionaries_list_to_text(result_matches, True, result_indexes))
        else:
            print("Нет совпадений.")
    else:
        print("Список пустой.")


def work_with_file(file_name, contacts_list):
    print(f"Редактирование файла {file_name}:")
    while True:
        command = input("Введите команду или \"info\" для списка команд: ").lower()
        if command == "info":
            print("Список команд:")
            print("\"view\" – показать список заметок")
            print("\"add\" – добавить заметку")
            print("\"delete\" – удалить заметки")
            print("\"edit\" – редактировать заметки")
            print("\"find\" – найти заметку")
            print("\"move\" – перенести заметку в другой файл")
            print("\"save\" – сохранить файл")
            print("\"save diff\" – сохранить файл под другим именем")
            print("\"back\" – вернуться в главное меню")
        elif command == "view":
            print(dictionaries_list_to_text(contacts_list, False, None))
        elif command == "add":
            contacts_list.append(get_new_contact(False, None))
            print("Контакт добавлен.")
        elif command == "delete":
            remove_contact(contacts_list)
        elif command == "edit":
            edit_contact(contacts_list)
        elif command == "find":
            find_contacts(contacts_list)
        elif command == "move":
            move_contact(contacts_list)
        elif command == "save":
            write_file(file_name, contacts_list)
        elif command == "save diff":
            file_name = enter_file_name()
            write_file(file_name, contacts_list)
        elif command == "back":
            print("Возвращаемся в главное меню.")
            break
        else:
            print("Такой команды нет.")


def interface():
    print("Добро пожаловать в программу \"Список контактов\".")
    while True:
        command = input("Введите команду или \"cmds\" для вывода на экран списка команд: ").lower()
        if command == 'cmds':
            print("Список команд:")
            print("\t\"create\" – создать новый файл")
            print("\t\"open file\" – открыть существующий файл")
            print("\t\"quit\"– выйти из программы")
        elif command == 'quit':
            break
        elif command == 'open file':
            open_existing_file()
        elif command == 'create':
            create_new_file()
        else:
            print("Такой команды нет.")


interface()