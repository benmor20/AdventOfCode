from typing import *

from year2020.day2020 import Day2020
from utils.utils import *


class Day(Day2020):
    @property
    def num(self) -> int:
        return 21

    def get_data(self, example=False) -> List[Tuple[Set[str], Set[str]]]:
        lines = super().get_data(example)
        foods = []
        for line in lines:
            ing_all_split = line.split(' (')
            if len(ing_all_split) == 1:  # No allergens
                foods.append((set(line.split(' ')), set()))
            elif len(ing_all_split) == 2:  # Allergens
                ingredients = ing_all_split[0].split(' ')
                allergens = ing_all_split[1][9:-1].split(', ')
                foods.append((set(ingredients), set(allergens)))
            else:
                assert False  # Should only be len 1 or 2
        return foods

    def puzzles(self):
        foods = self.get_data()
        ingredients = set().union(*(f[0] for f in foods))

        allergen_indexes = {}
        for aller in set().union(*(f[1] for f in foods)):
            allergen_indexes[aller] = []
            for i, (_, allers) in enumerate(foods):
                if aller in allers:
                    allergen_indexes[aller].append(i)

        # All possibilities (no logic, just intersection of where they appear)
        aller_to_poss_ing = {}
        for aller, indexes in allergen_indexes.items():
            if len(indexes) == 1:
                aller_to_poss_ing[aller] = foods[indexes[0]][0]
            else:
                aller_to_poss_ing[aller] = foods[indexes[0]][0].intersection(*(foods[i][0] for i in indexes[1:]))

        # Based on logic
        ing_to_aller = {}
        made_change = True
        while made_change:
            made_change = False
            for aller in allergen_indexes:
                if aller not in aller_to_poss_ing:
                    continue
                num_ing = len(aller_to_poss_ing[aller])
                assert num_ing > 0
                if num_ing == 1:
                    ing = first_ele(aller_to_poss_ing[aller])
                    ing_to_aller[ing] = aller
                    del aller_to_poss_ing[aller]
                    made_change = True
                    for ings in aller_to_poss_ing.values():
                        if ing in ings:
                            ings.remove(ing)

        ings_with_allers = set(ing_to_aller)
        ings_with_poss_allers = set().union(*aller_to_poss_ing.values())
        ings_without_allers = ingredients - ings_with_allers - ings_with_poss_allers

        puzz1ans = 0
        for ings, _ in foods:
            puzz1ans += len([1 for i in ings if i in ings_without_allers])
        print(f'Ingredients with definitely no allergens appear {puzz1ans} times')

        print(','.join(sorted(ings_with_allers, key=lambda i: ing_to_aller[i])))
