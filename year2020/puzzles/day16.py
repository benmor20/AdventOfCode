from year2020.day2020 import Day2020


class Day(Day2020):
    @property
    def num(self) -> int:
        return 16

    def get_data(self, example=False):
        lines = super().get_data(example)
        getting_rules = True
        rules = {}
        tickets = []  # List of all tickets, yours is first
        for line in lines:
            if getting_rules:
                if len(line) == 0:
                    getting_rules = False
                    continue
                field, ranges_str = tuple(line.split(': '))
                ranges_splt = ranges_str.split(' or ')
                ranges = []
                for range_str in ranges_splt:
                    range_splt = range_str.split('-')
                    r = range(int(range_splt[0]), int(range_splt[1]) + 1)
                    ranges.append(r)
                rules[field] = ranges
            elif not (':' in line or len(line) == 0):
                tickets.append(tuple(int(i) for i in line.split(',')))
        return rules, tickets[0], tickets[1:]

    def puzzles(self):
        rules, my_ticket, other_tickets = self.get_data()
        tickets_set = set(other_tickets)
        tickets_set.add(my_ticket)

        # Puzzle 1
        total = 0
        for ticket in other_tickets:
            for i, val in enumerate(ticket):
                in_a_range = False
                for rule in rules.values():
                    for r in rule:
                        if val in r:
                            in_a_range = True
                            break
                    if in_a_range:
                        break
                if not in_a_range:
                    tickets_set.remove(ticket)
                    total += val
        print(total)

        # Puzzle 2 (note that tickets_set has already been calculated)
        by_field = [set() for _ in range(len(my_ticket))]
        for ticket in tickets_set:
            for i, val in enumerate(ticket):
                by_field[i].add(val)
        possible_fields = {i: set() for i in range(len(by_field))}
        for i, field_vals in enumerate(by_field):
            for field, ranges in rules.items():
                can_be = True
                for val in field_vals:
                    if not any(val in r for r in ranges):
                        can_be = False
                        break
                if can_be:
                    possible_fields[i].add(field)

        print(possible_fields)
        field_key = {}
        while any(len(s) > 0 for s in possible_fields.values()):
            single_len = False
            for i, fields in possible_fields.items():
                if len(fields) == 1:
                    single_len = True
                    f = next(iter(fields))
                    field_key[f] = i
                    for n in possible_fields:
                        if f in possible_fields[n]:
                            possible_fields[n].remove(f)
            if not single_len:
                print('Ran into multiple solutions')
                print(possible_fields)
                return
        print(field_key)
        for i in range(len(by_field)):
            try:
                assert i in field_key.values()
            except AssertionError:
                print(f'{i} not in field_key')
        prod = 1
        for field in rules:
            if 'departure' in field:
                prod *= my_ticket[field_key[field]]
        print(prod)
