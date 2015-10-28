import inspect

__author__ = 'tangz'


class FunctionWrapper(object):
    def __init__(self, func):
        self.func = func
        # this will allow it to handle both generators and iterators
        self._isgenerator = inspect.isgeneratorfunction(func)
        self._iterable = hasattr(func, '__iter__')
        self._iterator = None

    def eval(self, *args, **kwargs):
        if self._isgenerator:
            if self._iterator is None:
                self._iterator = self.func(*args, **kwargs)
        elif self._iterable:
            if self._iterator is None:
                self._iterator = iter(self.func(*args, **kwargs))
        else:
            return self.func(*args, **kwargs)
        # this only gets called if it's an iterable
        return next(self._iterator)


class FormatWrapper(object):
    def __init__(self, funcwrapper, formatter):
        self.funcwrapper = funcwrapper
        self.formatter = formatter

    def eval(self, *args, **kwargs):
        value = self.funcwrapper.eval(*args, **kwargs)
        return self.formatter(value)


class SingleRepeater(object):
    def __init__(self, funcwrapper, n):
        if n <= 0:
            raise ValueError("Must repeat at least one time; assert n > 0")
        self.funcwrapper = funcwrapper
        self._n = n
        self._i = 0
        self._repeateditem = None

    def eval(self, *args, **kwargs):
        if self._i == 0:
            self._repeateditem = self.funcwrapper.eval(*args, **kwargs)

        self._i += 1
        if self._i >= self._n:
            self._i = 0

        return self._repeateditem


class ClusterRepeater(object):
    def __init__(self, funcwrapper, n):
        if n <= 0:
            raise ValueError("Must repeat at least one time; assert n > 0")
        self.funcwrapper = funcwrapper
        self._n = n
        self._repeateditems = []
        self._i = 0
        self._useolditems = False

    def eval(self, *args, **kwargs):
        if self._useolditems:
            item = self._repeateditems[self._i]
        else:
            item = self.funcwrapper.eval(*args, **kwargs)
            self._repeateditems.append(item)

        self._i += 1
        if self._i >= self._n:
            self._i = 0
            self._useolditems = True

        return item
