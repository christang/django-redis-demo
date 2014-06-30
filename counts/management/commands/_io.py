import collections
import csv


class StateCity(collections.namedtuple('StateCity', ('state', 'city'))):
    @staticmethod
    def of(state, city):
        return StateCity(state.strip(), city.strip())


def read_city_state_pop(stream):
    reader = csv.reader(stream, delimiter=',', quotechar='"')
    return { StateCity.of(state, city):to_int(pop) for city, state, pop in reader }   


def to_int(word):
    return int(word.replace(",", ""))

