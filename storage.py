import shelve
import re
from typing import Optional, List

from dataclasses import dataclass
from abc import ABC, abstractmethod


class Storage(ABC):
    """
    Абстрактный класс для хранилища данных
    """

    @abstractmethod
    def create(self):
        pass

    @abstractmethod
    def edit(self):
        pass

    @abstractmethod
    def search(self):
        pass

    @abstractmethod
    def display(self):
        pass


@dataclass
class Record:
    """
    Класс, содержащий информацию о записи.
    """
    surname: str
    name: str
    patronymic: str
    organization: str
    office_number: str
    mobile_phone: str

    def search(self, other: "Record") -> Optional["Record"]:
        """
        Сравнивает два экземпляра Record

        :param other: экземпляр Record
        :return:
        """
        for field in self.__dict__:
            if other.__dict__[field] and re.search(rf'{other.__dict__[field]}', self.__dict__[field],
                                                   flags=re.IGNORECASE):
                return self

    def __repr__(self):
        return f'{self.surname}, {self.name}, {self.patronymic}, {self.organization}, ' \
               f'{self.office_number}, {self.mobile_phone}'


class FileStorage(Storage):
    """
    Класс, являющийся файловым хранилищем для записей.
    """

    def __init__(self, filename: str):
        self.file_storage = shelve.open(filename)

    def create(self, data: Record):
        """
        создает новую запись

        :param data: экземпляр Record
        :return:
        """
        id_ = str(len(self.file_storage) + 1)
        self.file_storage[id_] = data

    def edit(self, id_, new_data):
        """
        Вносит измененные данные

        :param id_: id записи
        :param new_data: экземпляр Record
        :return:
        """
        self.file_storage[id_] = new_data

    def search(self, other: "Record") -> Optional[List["Record"]]:
        """
        Выполняет поиск среди всех записей

        :param other:
        :return:
        """
        search_result = []
        for idx, record in enumerate(self.__iter__(), start=1):
            if record[1].search(other):
                search_result.append(idx)
                search_result.append(record[1])
        return search_result

    def display(self):
        """
        Возвращает экземпляр shelve

        :return:
        """
        if self.file_storage:
            return self.file_storage

    def __iter__(self):
        for row in range(1, len(self.file_storage) + 1):
            yield str(row), self.file_storage[str(row)]

    def __del__(self):
        self.file_storage.close()
