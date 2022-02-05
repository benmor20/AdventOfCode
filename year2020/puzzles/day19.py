import itertools
import numpy as np

from year2020.day2020 import Day2020


def compose(langs):
    for p in itertools.product(*langs):
        yield ''.join(p)


def set_ele(s):
    for e in s:
        return e


# Language 0 is 8 followed by 11
# L8 is L42* - {""}
# L11 is L42^mL31^m where m > 0
# Therefore, L0 is L42^nL31^m where 0 < m < n
# L42 intersect L31 = {}
# All strings in both languages have length 8 (or 5 in example)
def match0(msg, lang42, lang31):
    length = len(set_ele(lang42))
    assert len(lang42 & lang31) == 0
    assert all(len(s) == length for s in lang42)
    assert all(len(s) == length for s in lang31)
    if len(msg) % length != 0:
        return False
    split = [''.join(r) for r in np.array([c for c in msg]).reshape((-1, length))]
    i = 0
    for i in itertools.count():
        if i == len(split):
            return False  # if all 42, false (m = 0)
        if split[i] not in lang42:
            break
    n = i
    for i in itertools.count(n):
        if i == len(split):
            m = i - n
            return m < n
        if split[i] not in lang31:
            return False


class Day(Day2020):
    @property
    def num(self) -> int:
        return 19

    def get_data(self, example=False):
        lines = super().get_data(example)
        rules = {}
        i = 0
        for i in itertools.count():
            line = lines[i]
            if len(line) == 0:
                break
            split = line.split(': ')
            num = int(split[0])
            rule_str = split[1]
            if rule_str[0] == '"':
                rules[num] = rule_str[1:-1]
            else:
                options_str = rule_str.split(' | ')
                options = [tuple(int(i) for i in o.split(' ')) for o in options_str]
                rules[num] = options
        return rules, lines[i+1:]

    def puzzles(self):
        rules, msgs = self.get_data()
        langs = {}
        to_do = set(rules)
        to_do.remove(8)
        to_do.remove(11)
        to_do.remove(0)

        # Get all non-looping languages
        while len(to_do) > 0:
            print(f'Top of loop: to_do is {to_do}')
            for l in list(to_do):
                print(f'Analyzing rule {l}')
                if isinstance(rules[l], str):
                    print(f'Rule {l} is a base case')
                    langs[l] = {rules[l]}
                    to_do.remove(l)
                    continue
                has_all = True
                for option in rules[l]:
                    if any(v in to_do for v in option):
                        has_all = False
                        break
                if not has_all:
                    print(f'Rule {l} does not have all sub-rules calculated. Moving on...')
                    continue
                print(f'Rule {l} has all sub-rules calculated.')
                lang = set()
                for option in rules[l]:
                    olangs = [langs[o] for o in option]
                    print(f'Updating lang with {option}, which maps to {olangs}')
                    lang.update(compose(olangs))
                print(f'Rule {l} is {lang}')
                langs[l] = lang
                to_do.remove(l)

        nmatch0 = len([1 for m in msgs if match0(m, langs[42], langs[31])])
        print(nmatch0)
