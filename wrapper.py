import inspect

__author__ = 'tangz'


class FunctionWrapper(object):
    def __init__(self, func):
        self.func = func
        self._isgenerator = inspect.isgeneratorfunction(func)
        self.generator = None

    def get(self, *args, **kwargs):
        if self._isgenerator:
            if self.generator is None:
                self.generator = self.func(*args, **kwargs)
            return next(self.generator)
        else:
            return self.func(*args, **kwargs)


class SingleRepeater(object):
    def __init__(self, funcsetting, n):
        if n <= 0:
            raise ValueError("Must repeat at least one time; assert n > 0")
        self.funcsetting = funcsetting
        self._n = n
        self._i = 0
        self._repeateditem = None

    def get(self, *args, **kwargs):
        if self._i == 0:
            self._repeateditem = self.funcsetting.get(*args, **kwargs)

        self._i += 1
        if self._i >= self._n:
            self._i = 0

        return self._repeateditem


class ClusterRepeater(object):
    def __init__(self, funcsetting, n):
        if n <= 0:
            raise ValueError("Must repeat at least one time; assert n > 0")
        self.funcsetting = funcsetting
        self._n = n
        self._repeateditems = []
        self._i = 0
        self._useolditems = False

    def get(self, *args, **kwargs):
        if self._useolditems:
            item = self._repeateditems[self._i]
        else:
            item = self.funcsetting.get(*args, **kwargs)
            self._repeateditems.append(item)

        self._i += 1
        if self._i >= self._n:
            self._i = 0
            self._useolditems = True

        return item
