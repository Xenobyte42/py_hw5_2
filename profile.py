from functools import wraps
from time import time
from inspect import isclass


def _sub_profile(cls=None):

    def decorator(func):

        @wraps(func)
        def wrapper(*args, **kwargs):
            if cls is not None:
                description = f"`{cls.__name__}.{func.__name__}`"
            else:
                description = f"`{func.__name__}`"

            print(f"{description} started")

            timer = time()
            answer = func(*args, **kwargs)

            print(f"{description} finished in {time() - timer:.6f}s")
            return answer

        return wrapper

    return decorator

def profile(obj):
    """
    If object is class - decorate all callable attributes of the class
    else decorate as function
    """

    if not isclass(obj):
        return _sub_profile()(obj)

    else:
        for attr_name in obj.__dict__:
            attr = getattr(obj, attr_name)
            if callable(attr):
                setattr(obj, attr_name, _sub_profile(obj)(attr))
        return obj

                

@profile
def hey(num):
    for i in range(10000000):
        pass

@profile
class TestClass:
    def __init__(self):
        print('init')

    @classmethod
    def bar(cls):
        print('class')

    @staticmethod
    def foo():
        print('static')

    def boo(self):
        print('method')


if __name__ == "__main__":
    hey(2)
    a = TestClass()
    TestClass.bar()
    TestClass.foo()
    a.boo()
    print('=' * 10)
    print(TestClass.bar.__name__)
    print(TestClass.boo.__name__)
    print(TestClass.foo.__name__)
    print(hey.__name__)

