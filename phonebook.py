import atexit
import json
import os
from typing import Dict, List


class PhoneBook(object):

    path_to_file = "phonebook.json"

    contacts = []

    def __init__(self):
        """
        Инициализация объекта
        Все контакты из файла считываются в список
        """
        if not os.path.exists(self.path_to_file):
            with open(self.path_to_file, 'x', encoding='utf8') as new_file:
                new_file.write('[]')

        with open(self.path_to_file, "r+", encoding='utf8') as contact_file:
            info = contact_file.read()
            if info != '':
                self.contacts = json.loads(info)

        atexit.register(self.write_to_file)

    def add(self, name: str, surname: str, patronymic: str,
            organisation: str, tel_1: str, tel_2: str) -> None:
        """
        Добавление контакта
        """
        self.contacts.append(
            {
                "id": str(len(self.contacts) + 1),
                "Имя": name,
                "Фамилия": surname,
                "Отчество": patronymic,
                "Организация": organisation,
                "Телефон рабочий": tel_1,
                "Телефон сотовый": tel_2,
            }
        )

    def find(self, args: Dict[str, str]) -> List[Dict[str, str]]:
        """
        Поиск контакта по параметрам
        """
        result = []
        for contact in self.contacts:
            for key, value in args.items():
                if contact[key] != value:
                    break
            else:
                result.append(contact)
        return result

    def edit(self, id: str, new_attr: Dict[str, str]) -> bool:
        """
        Изменение контакта
        """
        contact = self.find({'id': id})
        if len(contact) == 0:
            return False
        contact = contact[0]
        for key, value in new_attr.items():
            contact[key] = value
        return True

    def show_all(self, num_of_cont_in_one_page):
        """
        Все контакты, разделенные постранично
        """
        return [
            self.contacts[i: num_of_cont_in_one_page + i]
            for i in range(0, len(self.contacts), num_of_cont_in_one_page)
        ]

    def write_to_file(self):
        """
        Запись контактов в файл
        """
        with open(self.path_to_file, 'w', encoding='utf8') as f:
            f.write(json.dumps(self.contacts))


def print_contact(contact: Dict[str, str]):
    return f"{contact['id']}) {contact['Фамилия']} {contact['Имя']} {contact['Отчество']}\n " \
           f"Телефоны: {contact['Телефон рабочий']}, {contact['Телефон сотовый']}\n" \
           f"Организация: {contact['Организация']}\n" \
           f"---------------------------"


if __name__ == '__main__':
    p = PhoneBook()

    while True:
        command = input(
            'Выберите задание: \n'
            '1 - Показать все контакты\n'
            '2 - Добавить новый контакт\n'
            '3 - Редактировать контакт\n'
            '4 - Поиск номеров\n'
        )
        if command == '1':
            packages_of_contacts = p.show_all(10)
            for package in packages_of_contacts:
                for contact in package:
                    print(print_contact(contact))
                ans = input('Показать еще? (y/n) ')
                if ans != 'y':
                    break
        elif command == '2':
            name = input("Имя: ")
            surname = input("Фамилия: ")
            patronymic = input("Отчество: ")
            organisation = input("Организация: ")
            tel_1 = input("Телефон рабочий: ")
            tel_2 = input("Телефон сотовый: ")
            p.add(name, surname, patronymic, organisation, tel_1, tel_2)
            print('Контакт добавлен!')
        elif command == '3':
            id = input('Какой номер изменить?(id) ')
            ans = ''
            args = {}
            print('Введите поля, которые надо изменить(параметр:новое значение). После ввода наберите exit')
            while ans != 'exit':
                if ans != '':
                    param, value = ans.split(':')
                    if param != 'id':
                        args.update({param: value})
                ans = input()
            p.edit(id, args)
        elif command == '4':
            print('Введите поля, по которым надо искать(параметр:значение). После ввода наберите exit')
            ans = ''
            args = {}
            while ans != 'exit':
                if ans != '':
                    param, value = ans.split(':')
                    args.update({param: value})
                ans = input()
            contacts = p.find(args)
            for c in contacts:
                print(print_contact(c))
        else:
            break
