import re

from storage import Record, FileStorage
from typing import Tuple
from settings import PAGINATION

storage = FileStorage('Notebook')


class CreateNote:
    """
    Класс CreateNote предназначен для создания записи
    """

    def execute(self, data: Record):
        """
        Делегирует создание записи экземпляру storage

        :param data: экземпляр Record
        :return: сообщение об успехе
        """
        storage.create(data)
        return 'Запись создана!'


class EditNote:
    """
    Класс EditNote предназначен для редактирования записи
    """

    def execute(self, id_data: Tuple[str, Record]):
        """
        Делегирует редактирование записи экземпляру storage

        :param id_data: кортеж из id записи и экземпляра Record
        :return: сообщение об успехе
        """
        id_, data = id_data
        storage.edit(id_, data)
        return 'Запись отредактирована!'


class ListNote:
    """
    Класс ListNote предназначен для вывода на экран записи или записей
    """

    def execute(self, id_: str = ''):
        """
        Если передан id_, то возвращается конкретная запись, иначе все записи с учетом пагинации

        :param id_: id записи
        :return: Если передан id_, то возвращается конкретная запись
        """
        if id_:
            return id_, storage.display()[id_]
        self._pagination()

    def _pagination(self):
        """
        Возвращает записи из хранилища с учетом пагинации

        :return:
        """
        view = []
        page = iter(storage)
        while page:
            for _ in range(PAGINATION):
                try:
                    view.append(next(page))
                except StopIteration:
                    page = None
                    break
            print('\n'.join([record[0] + ': ' + ' '.join(record[1].__dict__.values()) for record in
                             view]) if view else 'Записей больше нет')

            view.clear()
            if page:
                response = input(
                    'Введите "N[n]", чтобы отобразить следующую страницу, для выхода любую другую клавишу\n')
                if not re.search(r'[Nn]', response):
                    break


class SearchNote:
    """
    Класс SearchNote предназначен для поиска записей по параметрам
    """

    def execute(self, other: Record):
        """
        Делегирует поиск записей экземпляру storage и возвращает подходящие параметрам поиска записи

        :param other: экземпляр класса Record
        :return:
        """
        search_result = storage.search(other)

        return ('\n' + '{}: {}\n' * (len(search_result) // 2)).format(
            *search_result) if search_result else 'По Вашему запросу ничего найти не удалось'
