from stark.service import v1
from app01 import models




class DepartmentConfig(v1.StarkConfig):
    list_display = ['title','code']
    edit_link = ['title']

v1.site.register(models.Department,DepartmentConfig)


class UserInfoConfig(v1.StarkConfig):
    list_display = ['name','username','email','depart']

v1.site.register(models.UserInfo,UserInfoConfig)
