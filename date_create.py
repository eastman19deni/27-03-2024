from logging import Logger

from Note import LenNumberError

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
        is_valid_phone = True
    return {"Имя": first_name, "Отчество": second_name, "Фамилия": last_name, "Дата": date}
    
