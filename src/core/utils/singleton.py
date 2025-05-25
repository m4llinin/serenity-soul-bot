class _SingletonWrapper:
    def __init__(self, cls):
        self.__wrapped__ = cls
        self.__instance = None

    def __call__(self, *args, **kwargs):
        if self.__instance is None:
            self.__instance = self.__wrapped__(*args, **kwargs)
        return self.__instance


def singleton(cls):
    return _SingletonWrapper(cls)
