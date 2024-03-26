from logger import *
from Note import create_new_file, create_random_file, open_existing_file

def interface():
    print("Добро пожаловать в программу \"Список контактов\".")
    while True:
        command = input("Введите команду или \"h\" для списка команд: ").lower()
        if command == 'h':
            print("Список команд:")
            print("\t\"n\" – создать новый файл")
            print("\t\"r\" – сгенерировать случайный список")
            print("\t\"o\" – открыть существующий файл")
            print("\t\"q\"– выйти из программы")
        elif command == 'q':
            break
        elif command == 'o':
            open_existing_file()
        elif command == 'r':
            create_random_file()
        elif command == 'n':
            create_new_file()
        else:
            print("Такой команды нет.")


interface()