from abc import ABC, abstractmethod


class DayBase(ABC):
    @property
    @abstractmethod
    def num(self) -> int:
        pass

    @property
    @abstractmethod
    def year(self) -> int:
        pass

    def filepath(self, example = False):
        ex_str = ''
        if example:
            ex_str = 'ex'
            if example > 1:
                ex_str += str(example)
        return f'year{self.year}/data/day{self.num}{ex_str}data.txt'

    def puzzles(self):
        pass

    def get_raw_data(self, example=False):
        with open(self.filepath(example), 'r') as file:
            return file.read()

    def get_data(self, example=False):
        return self.get_raw_data(example).split('\n')


class DayBase2(DayBase, ABC):
    @abstractmethod
    def puzzle1(self):
        pass

    @abstractmethod
    def puzzle2(self):
        pass

    def puzzles(self):
        self.puzzle1()
        self.puzzle2()


class DayBase3(DayBase, ABC):
    @abstractmethod
    def puzzle(self, puzzle_num=1):
        pass

    def puzzles(self):
        self.puzzle(1)
        self.puzzle(2)
