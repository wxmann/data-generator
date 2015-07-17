__author__ = 'tangz'

def repeatsingle(count, funcsetting, *ext_args, **ext_kwargs):
    return _SingleRepeatHandler(funcsetting, count, *ext_args, **ext_kwargs)


def repeatcluster(count, funcsetting, *ext_args, **ext_kwargs):
    return _ClusterRepeatHandler(funcsetting, count, *ext_args, **ext_kwargs)


class _SingleRepeatHandler(object):

    def __init__(self, funcsetting, count, *ext_args, **ext_kwargs):
        self.funcsetting = funcsetting
        self.count = count
        self.ext_args = ext_args
        self.ext_kwargs = ext_kwargs
        self.repeated_value = None
        self.index = 0

    def __iter__(self):
        return self

    def __next__(self):
        if self.index >= self.count:
            self.index = 0
        if self.index == 0:
            self.repeated_value = self.funcsetting.generatevalue(*self.ext_args, **self.ext_kwargs)
        self.index += 1
        return self.repeated_value


class _ClusterRepeatHandler(object):

    def __init__(self, funcsetting, count, *ext_args, **ext_kwargs):
        self.funcsetting = funcsetting
        self.count = count
        self.cluster = []
        self.ext_args = ext_args
        self.ext_kwargs = ext_kwargs
        self.firstgoaround = True
        self.index = 0

    def __iter__(self):
        return self

    def __next__(self):
        if self.index >= self.count:
            self.index = 0
            self.firstgoaround = False

        if self.firstgoaround:
            item = self.funcsetting.generatevalue(*self.ext_args, **self.ext_kwargs)
            self.cluster.append(item)
            self.index += 1
            return item
        else:
            oldindex = self.index
            self.index += 1
            return self.cluster[oldindex]
