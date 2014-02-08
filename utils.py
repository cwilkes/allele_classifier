import sys
from collections import namedtuple
import numpy as np


class Category(object):
    ZERO = 0
    ZERO_OR_ONE = 1
    ONE = 2
    ONE_OR_TWO = 3
    TWO = 4
    TWO_OR_MORE = 5


_categories_ary = ['0', '0 or 1', '1', '1 or 2', '2', '>2']
_categories = {'0': Category.ZERO, '0 or 1': Category.ZERO_OR_ONE, '1': Category.ONE,
               '1 or 2': Category.ONE_OR_TWO, '2': Category.TWO, '>2': Category.TWO_OR_MORE}


def get_label(category):
    return _categories_ary[category]


class AlleleMap(object):
    def __init__(self):
        self.my_dict = dict()
        self.my_ary = dict()

    def _add_record(self, line):
        parts = line.split(',')
        set_id, data_point_id = int(parts[0]), int(parts[1])
        if not set_id in self.my_dict:
            self.my_dict[set_id] = dict()
        coord_x, coord_y = float(parts[2]), float(parts[3])
        if len(parts) == 5:
            self.my_dict[set_id][data_point_id] = [coord_x, coord_y, _categories[parts[4]]]
        else:
            self.my_dict[set_id][data_point_id] = [coord_x, coord_y]

    def finalize(self):
        for set_id in self.my_dict.keys():
            self.my_ary[set_id] = np.array(self.my_dict[set_id].values())

    def set_ids(self):
        return sorted(self.my_ary.keys())

    def data_points(self, set_id):
        return self.my_ary[set_id]

    def __repr__(self):
        output = list()
        for set_id in self.set_ids():
            vals = ','.join(str(_) for _ in self.data_points(set_id))
            output.append('%d => %s' % (set_id, vals))
        return '\n'.join(output)


def read_train_and_test(train_data, test_data):
    return read_allele_map(train_data), read_allele_map(test_data)


def read_allele_map(reader):
    ret = AlleleMap()
    for line in reader:
        ret._add_record(line.strip())
    ret.finalize()
    return ret


if __name__ == '__main__':
    allele_map = read_allele_map(sys.stdin)
    print allele_map