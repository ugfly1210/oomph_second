from stark.service import v1
from app01 import models




class DepartmentConfig(v1.StarkConfig):
    list_display = ['title','code']
    edit_link = ['title']

v1.site.register(models.Department,DepartmentConfig)


class UserInfoConfig(v1.StarkConfig):
    list_display = ['name','username','email','depart']
    # 组合搜索
    comb_filter = [
        v1.FilterOption('depart',text_func_name=lambda x:str(x),val_func_name=lambda x:x.code) # 字段  只在chioce,fk,m2m有用
    ]                          # 这俩函数就是为了防止你自定义的fk的值不是主键用的

v1.site.register(models.UserInfo,UserInfoConfig)
