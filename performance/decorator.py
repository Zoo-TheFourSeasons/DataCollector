from functools import wraps
from time import time, perf_counter


def func_timer(func):
    """计时"""
    @wraps(func)
    def function_timer(*args, **kwargs):
        rel_start = time()
        cpu_start = perf_counter()
        result = func(*args, **kwargs)
        rel_cost = time() - rel_start
        cpu_cost = perf_counter() - cpu_start

        if '__code__' in dir(func):
            file_ = func.__getattribute__('__code__').co_filename
        else:
            file_ = 'builtin_function_or_method'

        s = ':'.join((file_ + '.' + func.__name__, str(rel_cost), str(cpu_cost)))
        print(s)
        return result

    return function_timer
