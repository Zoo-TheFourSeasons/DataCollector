from types import FunctionType
# from performance.thread import fn
from performance.decorator import func_timer


def decorate_meta(decorator):
    class MetaDecorate(type):
        def __new__(mcs, class_name, supers, class_dict):
            for attr, attr_val in class_dict.items():
                if type(attr_val) is FunctionType:
                    class_dict[attr] = decorator(attr_val)
            return type.__new__(mcs, class_name, supers, class_dict)
    return MetaDecorate


TimerMeta = decorate_meta(func_timer)
