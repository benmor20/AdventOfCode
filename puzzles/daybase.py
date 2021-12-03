from abc import ABC, abstractmethod


class DayBase(ABC):
    @property
    @abstractmethod
    def num(self) -> int:
        pass

    @abstractmethod
    def puzzle1(self):
        pass

    @abstractmethod
    def puzzle2(self):
        pass

    def get_data(self):
        with open(f'data/day{self.num}data.txt', 'r') as file:
            return file.readlines()
