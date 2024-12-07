from year2024.puzzles.day7 import Day, one_line


if __name__ == '__main__':
    day = Day()
    day.puzzles()
    one_line_str = one_line()
    if one_line_str is not None:
        print('\n--------------ONE LINER--------------')
        print(one_line_str)
