from functools import wraps
from time import time
from inspect import isclass


def profile_class(obj):

    def decorator(cls_func):

        @wraps(cls_func)
        def wrapper(*args, **kwargs):
            print(f"`{obj.__name__}.{cls_func.__name__}` started")
            timer = time()
            answer = cls_func(*args, **kwargs)
            print(f"`{obj.__name__}.{cls_func.__name__}` finished in {(time() - timer):.6f}s\n")
            return answer
            
        return wrapper

    return decorator

def profile(obj):
    """
    If object is class - decorate all callable attributes of the class
    else decorate as function
    """

    if not isclass(obj):
        @wraps(obj)
        def wrapper(*args, **kwargs):
            print(f"`{obj.__name__}` started")
            timer = time()
            answer = obj(*args, **kwargs)
            print(f"`{obj.__name__}` finished in {(time() - timer):.6f}s\n")
            return answer
            
        return wrapper

    else:
        for attr_name in obj.__dict__:
            attr = getattr(obj, attr_name)
            if callable(attr):
                setattr(obj, attr_name, profile_class(obj)(attr))
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

