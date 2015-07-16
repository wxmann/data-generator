__author__ = 'tangz'

def repeatval(count, funcsetting, *ext_args, **ext_kwargs):
    while True:
        repeated_value = funcsetting.generatevalue(*ext_args, **ext_kwargs)
        for i in range(count):
            yield repeated_value


def repeatcluster(count, funcsetting):
    return _ClusterRepeatHandler(funcsetting, count)


class _ClusterRepeatHandler(object):

    def __init__(self, funcsetting, count, *ext_args, **ext_kwargs):
        self.funcsetting = funcsetting
        self.count = count
        self.cluster = []
        self.ext_args = ext_args
        self.ext_kwargs = ext_kwargs

    def series(self):
        for i in range(self.count):
            item = self.funcsetting.generatevalue(*self.ext_args, **self.ext_kwargs)
            self.cluster.append(item)
            yield item
        while True:
            for i in range(self.count):
                yield self.cluster[i]
