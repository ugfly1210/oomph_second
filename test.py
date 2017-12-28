#!/usr/bin/env python
# import os
# import sys
#
# if __name__ == "__main__":
#     os.environ.setdefault("DJANGO_SETTINGS_MODULE", "oomph_2.settings")
#     try:
#         from django.core.management import execute_from_command_line
#     except ImportError as exc:
#         raise ImportError(
#             "Couldn't import Django. Are you sure it's installed and "
#             "available on your PYTHONPATH environment variable? Did you "
#             "forget to activate a virtual environment?"
#         ) from exc
#     execute_from_command_line(sys.argv)


# class Singleton(object):
#     _instance = None
#
#     def __new__(cls, *args, **kwargs):
#         if not cls._instance:
#             cls._instance = super(Singleton, cls).__new__(cls, *args, **kwargs)
#         return cls._instance
#
#
# class MyClass(Singleton):
#     a = 1
#
#
# one = MyClass()


"""


related_obj.model

[25/Dec/2017 12:46:45] "POST /stark/app01/userinfo/add/?_popbackid=id_consultant&model_name=customer&related_name=consultant HTTP/1.1" 200 342
app01.ClassList.teachers
app01.Customer.consultant
app01.ConsultRecord.consultant
app01.PaymentRecord.consultant
app01.CourseRecord.teacher
"""


"""
related_obj.model._meta

[25/Dec/2017 12:47:14] "POST /stark/app01/userinfo/add/?_popbackid=id_consultant&model_name=customer&related_name=consultant HTTP/1.1" 200 342
<class 'app01.models.UserInfo'>
<class 'app01.models.UserInfo'>
<class 'app01.models.UserInfo'>
<class 'app01.models.UserInfo'>
<class 'app01.models.UserInfo'>
<class 'app01.models.UserInfo'>
"""

"""
related_obj.model._meta.model_class

userinfo
userinfo
userinfo
userinfo
userinfo
userinfo
"""





# 对象之间的加减乘除
#
# class Foo(object):
#     def __init__(self,age):
#         self.age = age
#     def __add__(self, other):
#         return Foo(self.age + other.age)
#
# obj1 = Foo(1)
# obj2 = Foo(2)
#
# obj3 = obj1+obj2
# print(obj3)
# import datetime,time
#
# current_data = datetime.datetime.now()
# time.sleep(1)
# current_data1 = datetime.datetime.now()
#
# print(current_data1-current_data,type(current_data))


# class People:
#     country = "china"
#     def __init__(self,name):
#         self.name = name
#
#     def walk(self):
#         print("%s is working" % self.name)
#
# p = People("egon")
#
# print(dir(People))
# print(People.__dict__)

# from collections import OrderedDict
# d = OrderedDict({'a':1,'b':2,'c':3})
# l = []
# flag = True
# # 代码 一
# # while flag:
# #     for k,v in d.items():
# #         print(v,type(v))
# #         if v != 0:
# #             l.append(k)
# #             v -= 1
# #
# #     for v in d.values() :
# #         if v != 0:
# #             break
# #     else:
# #         flag = False
#
# # 代码 二
# while flag:
#     for k in d:
#         if d[k] != 0:
#             l.append(k)
#             d[k] -= 1
#
#     for vv in d.values() :
#         if vv != 0:
#             break
#     else:
#         flag = False
#
# print(l)
#
#
# import os
# import sys
# import django
# sys.path.append(r'/Users/macbookpro/PycharmProjects/oomph_2')
# os.chdir(r'/Users/macbookpro/PycharmProjects/oomph_2')
# os.environ.setdefault("DJANGO_SETTINGS_MODULE", "oomph_2.settings")
# django.setup()
#
# from app01 import models
#
# obj = models.UserInfo.objects.all() # 这是拿到权重表里面的对象
# # print(obj,type(obj))
# dict = OrderedDict()
# for i in obj :
#     dict[i.user_id] = i.num


# d = (('a',1),('b',2),('c',3))
while 1:
    for i in [1,2,3]:
        print(i)
    print(666)




