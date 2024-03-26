import operator
from Note import dictionaries_list_to_text


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