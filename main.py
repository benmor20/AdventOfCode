try:
    from year2022.puzzles.day7 import Day, one_line
except ImportError:
    pass


if __name__ == '__main__':
    day = Day()
    day.puzzles()
    try:
        f = one_line
        print('\n--------------ONE LINER--------------')
        one_line()
    except NameError as e:
        pass
