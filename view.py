import os
from commands import (CreateNote, EditNote, ListNote, SearchNote)
from storage import Record
from typing import Callable, Tuple


class Option:
    """
    Класс, связывающий текст, выводимый на экран пользователя, с командой, которую он запускает
    """

    def __init__(self, name: str, command, prep_call: Callable = None):
        """

        :param name: название команды
        :param command: экземпляр класса команды
        :param prep_call: функция, возвращающая данные подготовительного шага
        """
        self.name = name
        self.command = command
        self.prep_call = prep_call

    def choose(self):
        """
        Выполняет соответсвующую команду и возвращает ее результат

        :return:
        """
        data = self.prep_call() if self.prep_call else None
        message = self.command.execute(data) if data else self.command.execute()
        if message:
            print(message)

    def __str__(self):
        return self.name


def print_all_options(options: dict):
    """
    Печатает варианты команд

    :param options: словарь вариантов команд
    :return:
    """
    for shortcut, option in options.items():
        print(f'({shortcut}) {option}')
    print()


def get_opt_choice(options: dict) -> Option:
    """
    Предлагает пользователю выбрать одну из команд

    :param options: словарь вариантов команд
    :return:
    """
    choice = input('Выберите один из вариантов:\n')
    while choice not in options:
        print('Такого варианта нет')
        choice = input('Выберите один из вариантов:\n')
    return options[choice]


def get_user_input(label: str) -> str:
    """
    Запрашивает у пользователя данные

    :param label: поле данных
    :return:
    """
    value = input(f'{label}\n')
    return value


def get_new_note_data() -> Record:
    """
    Создает новый экземпляр Record

    :return: экземпляр Record
    """
    record = Record(surname=get_user_input('Фамилия:'), name=get_user_input('Имя:'),
                    patronymic=get_user_input('Отчество:'), organization=get_user_input('Название организаци:'),
                    office_number=get_user_input('Рабочий телефон:'), mobile_phone=get_user_input('Личный телефон:'))
    return record


def clear_screen():
    """
    Очищает экран пользователя

    :return:
    """
    clear = 'cls' if os.name == 'nt' else 'clear'
    os.system(clear)


def get_edit_id() -> Tuple[str, Record]:
    """
    Создает экземпляр Record для будущего редактирования

    :return:
    """
    id_ = input('Введите порядковый номер записи, которую хотите изменить:\n')
    old_data = ListNote().execute(id_)[1]
    print(' '.join(old_data.__dict__.values()))
    print('\nВпишите измененные данные в нужные поля, остальные пропускайте, нажимая "Enter"\n')
    edit_data = get_new_note_data()
    new_data = Record(surname=edit_data.surname or old_data.surname,
                      name=edit_data.name or old_data.name,
                      patronymic=edit_data.patronymic or old_data.patronymic,
                      organization=edit_data.organization or old_data.organization,
                      office_number=edit_data.office_number or old_data.office_number,
                      mobile_phone=edit_data.mobile_phone or old_data.mobile_phone)
    return id_, new_data


def main():
    options = {
        '1': Option('Добавить запись', CreateNote(), prep_call=get_new_note_data),
        '2': Option('Показать все записи', ListNote()),
        '3': Option('Редактировать запись', EditNote(), prep_call=get_edit_id),
        '4': Option('Поиск по записям', SearchNote(), prep_call=get_new_note_data),
    }
    clear_screen()
    print_all_options(options)
    user_option = get_opt_choice(options)
    clear_screen()
    user_option.choose()
    _ = input('Нажмите Enter для перехода в главное меню')


if __name__ == '__main__':
    print('Добро пожаловать в записную книжку!')
    while True:
        main()
