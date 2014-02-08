import utils
import sys
#import mlp
import numpy as np
from collections import namedtuple

AlleleStats = namedtuple('AlleleStats', 'min max average median')


def get_average_x_y(coords):
    print 'c', coords
    if isinstance(coords[0], tuple):
        x, y = [_[0].x for _ in coords], [_[0].y for _ in coords]
    else:
        x, y = [_.x for _ in coords], [_.y for _ in coords]
    x_stats = AlleleStats(np.min(x), np.max(x), np.average(x), np.median(x))
    y_stats = AlleleStats(np.min(y), np.max(y), np.average(y), np.median(y))
    return x_stats, y_stats


def classify(train_data, test_data):
    train_map, test_map = utils.read_train_and_test(train_data, test_data)

    for set_id in train_map.set_ids():
        points = train_map.data_points(set_id)
        x, y = get_average_x_y(points)
        print '%03d %5.2f %5.2f %5.2f %5.2f %5.2f   %5.2f %5.2f %5.2f %5.2f %5.2f' % \
              (set_id,
               x.min, x.average, x.median, x.max, x.max-x.min,
               y.min, y.average, y.median, y.max, y.max-y.min)


if __name__ == '__main__':
    train_data = [_.strip() for _ in open(sys.argv[1])]
    test_data = [_.strip() for _ in open(sys.argv[2])]
    classify(train_data, test_data)