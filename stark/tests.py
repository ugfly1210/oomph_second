from django.test import TestCase

# Create your tests here.



class Foo(object):
    pass

class Bar(Foo):
    pass

obj = Bar()

# isinstance 用于判断对象是否是指定类或者其派生类的实例
# print(isinstance(obj,Foo))
# print(isinstance(obj,Bar))

# 判定是否是哪个类型
# print((type(obj)))    # <class '__main__.Bar'>
# print(type(obj)==Bar) # True
# print(type(obj)==Foo) # False

from django.forms.models import ModelChoiceField

print(isinstance(obj,ModelChoiceField))

