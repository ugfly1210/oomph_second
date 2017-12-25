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


class Singleton(object):
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(Singleton, cls).__new__(cls, *args, **kwargs)
        return cls._instance


class MyClass(Singleton):
    a = 1


one = MyClass()



















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