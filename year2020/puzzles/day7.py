from year2020.day2020 import Day2020_3
import networkx as nx


class Day(Day2020_3):
    @property
    def num(self) -> int:
        return 7

    def get_data(self, example: bool = False):
        rules = super().get_data(example)
        g = nx.DiGraph()
        g.add_nodes_from([r.split(' bags contain ')[0] for r in rules])
        for rule in rules:
            splt = rule[:-1].split(' bags contain ')
            key = splt[0]
            if splt[1] == 'no other bags':
                continue
            vals = {}
            vals_str = splt[1].split(', ')
            for val_str in vals_str:
                words = val_str.split(' ')
                g.add_edge(key, ' '.join(words[1:3]), num=int(words[0]))
        return g

    def get_nodes_from(self, g, start):
        seen = set()
        stack = [start]
        while len(stack) > 0:
            node = stack.pop()
            for n in g[node]:
                if n not in seen:
                    seen.add(n)
                    stack.append(n)
        return seen

    def get_total_bags(self, g, start):
        total = 0
        for node, info in g[start].items():
            total += info['num'] * (self.get_total_bags(g, node) + 1)
        return total

    def puzzle(self, num=1):
        g = self.get_data()
        if num == 1:
            g = g.reverse()
            print(len(self.get_nodes_from(g, 'shiny gold')))
        elif num == 2:
            print(self.get_total_bags(g, 'shiny gold'))
