try:
    from year2022.puzzles.day4 import Day, one_line
except ImportError:
    pass


if __name__ == '__main__':
    day = Day()
    day.puzzles()
    print('\n--------------ONE LINER--------------')
    try:
        one_line()
    except NameError as e:
        print('Not implemented')
