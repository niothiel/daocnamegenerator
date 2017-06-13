import random
import re

HEADING_REGEX = re.compile('\[(.+)\]')
ORDERS = {'first': 0, 'second': 1, 'third': 2}


random.seed(0)


class NameGenerator:
    def __init__(self, path):
        self.names = self._load(path)

    @staticmethod
    def _load(path):
        names = {}
        race = None
        order = None

        with open(path, 'r') as fin:
            for line in fin.read().splitlines():
                match = HEADING_REGEX.match(line)
                if match:
                    race, order = match.group(1).split('-')
                    order = ORDERS[order]
                else:
                    if race not in names:
                        names[race] = [[] for _ in range(len(ORDERS))]
                    names[race][order].append(line)

        return names

    def generate(self, race=None):
        if race is None:
            race = random.choice(self.names.keys())

        return ''.join(random.choice(part) for part in self.names[race])


namegen = NameGenerator('names.dat')
names = namegen.names
from pprint import pprint

pprint(names)


min_n = 1e10
best_seed = 0

for seed in range(1000):
    n = 0
    name = None

    random.seed(seed)
    while name != 'Niothiel':
        name = namegen.generate('avalon')
        n += 1

    if n < min_n:
        min_n = n
        best_seed = seed

    print('seed', seed)
    print('min_n', min_n)

print('Found the name with min value of {} and seed of {}'.format(min_n, seed))
print('Generated name:', namegen.generate('avalon'))
