""" This script is used to take a load of raw timestamps and turn them into a
.csv representing "counts" of timestamps.

:Author: Ralph Bean

"""

import collections


class CollisionDict(collections.MutableMapping):
    def __init__(self, keys):
        self._dict = collections.OrderedDict(zip(keys, [0] * len(keys)))

    def hash_key(self, key):
        """ "Hash" all keys in a timerange to the same value. """
        for i, destination_key in enumerate(self._dict):
            if key < destination_key:
                return destination_key

        return key

    def __setitem__(self, key, value):
        self._dict[self.hash_key(key)] = value

    def __getitem__(self, key):
        return self._dict[self.hash_key(key)]

    def __delitem__(self, key):
        del self._dict[self.hash_key(key)]

    def __len__(self):
        return len(self._dict)

    def __iter__(self):
        return iter(self._dict)


def load_data(fname, n):
    # TODO.. alternatively read from stdin.
    with open(fname, "r") as f:
        stamps = sorted(map(float, f.readlines()))

    span = stamps[-1] - stamps[0]
    size = span / n
    # TODO -- frange?
    keys = range(int(stamps[0]), int(stamps[-1]), int(size))

    return keys, stamps

if __name__ == '__main__':
    # The number of outputs you want.. try setting it to 5 or 10 first to see
    # how it works.
    n = 300

    keys, timestamps = load_data("timestamps.txt", n=n)

    # Smash all the timestamps together.
    bucket = CollisionDict(keys=keys)
    for i, stamp in enumerate(timestamps[:-1]):
        bucket[stamp] += 1

    # Then read them out.
    for key, value in bucket.items():
        print "%i, %i" % (key, value)
