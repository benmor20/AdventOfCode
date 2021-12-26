from year2021.day2021 import Day2021

open = '([{<'
pairs = {'(': ')',
         '[': ']',
         '{': '}',
         '<': '>',
         ')': '(',
         ']': '[',
         '}': '{',
         '>': '<'}
scores = {'(': 3,
          '[': 57,
          '{': 1197,
          '<': 25137}
auto_scores = {'(': 1,
              '[': 2,
              '{': 3,
              '<': 4}


class Day(Day2021):
    @property
    def num(self) -> int:
        return 10

    def puzzle1(self):
        score = 0
        for line in self.get_data():
            stack = []
            for c in line:
                if c in open:
                    stack.append(c)
                else:
                    o = stack.pop()
                    if pairs[o] != c:
                        score += scores[pairs[c]]
                        break
        print(score)

    def puzzle2(self):
        scores2 = []
        for line in self.get_data():
            stack = []
            found = False
            for c in line:
                if c in open:
                    stack.append(c)
                else:
                    o = stack.pop()
                    if pairs[o] != c:
                        found = True
                        break
            if not found and len(stack) > 0:
                score = 0
                for o in stack[::-1]:
                    score *= 5
                    score += auto_scores[o]
                scores2.append(score)
        print(sorted(scores2)[len(scores2) // 2])
