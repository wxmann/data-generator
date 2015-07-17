from core import common

__author__ = 'tangz'

def repeatsingle(count, funcsetting, *ext_args, **ext_kwargs):
    return _SingleRepeatHandler(funcsetting, count, *ext_args, **ext_kwargs)


def repeatcluster(count, funcsetting, *ext_args, **ext_kwargs):
    return _ClusterRepeatHandler(funcsetting, count, *ext_args, **ext_kwargs)


class _SingleRepeatHandler(object):

    def __init__(self, func, count, *ext_args, **ext_kwargs):
        self.func = func
        self.count = count
        self.ext_args = ext_args
        self.ext_kwargs = ext_kwargs
        self._repeatedvalue = None
        self._index = 0

    def __iter__(self):
        return self

    def __next__(self):
        if self._index >= self.count:
            self._index = 0
        if self._index == 0:
            self._repeatedvalue = common.extractvalue(self.func, *self.ext_args, **self.ext_kwargs)
        self._index += 1
        return self._repeatedvalue


class _ClusterRepeatHandler(object):

    def __init__(self, func, count, *ext_args, **ext_kwargs):
        self.func = func
        self.count = count
        self._cluster = []
        self.ext_args = ext_args
        self.ext_kwargs = ext_kwargs
        self._firstgoaround = True
        self._index = 0

    def __iter__(self):
        return self

    def __next__(self):
        if self._index >= self.count:
            self._index = 0
            self._firstgoaround = False

        if self._firstgoaround:
            item = common.extractvalue(self.func, *self.ext_args, **self.ext_kwargs)
            self._cluster.append(item)
            self._index += 1
            return item
        else:
            oldindex = self._index
            self._index += 1
            return self._cluster[oldindex]
