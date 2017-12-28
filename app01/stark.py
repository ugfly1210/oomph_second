from django.shortcuts import redirect,HttpResponse
from stark.service import v1
from app01 import models
from django.conf.urls import url
from django.utils.safestring import mark_safe
from app01.configs.customer import CustomerConfig


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

    edit_link = ['name']

    # 显示搜索并支持模糊搜索
    show_search_form = True
    search_fields = ['name__contains']
v1.site.register(models.UserInfo,UserInfoConfig)


class CourseConfig(v1.StarkConfig):
    list_display = ['name']
    edit_link = ['name',]
v1.site.register(models.Course,CourseConfig)


class SchoolConfig(v1.StarkConfig):
    list_display = ['title']
    edit_link = ['title',]
v1.site.register(models.School,SchoolConfig)


class ClassListConfig(v1.StarkConfig):
    def course_semester(self,obj=None,is_header=None):
        if is_header:
            return '班级'
        return '%s(%s期)'%(obj.course.name,obj.semester)

    def num(self,obj=None,is_header=None):
        if is_header:
            return '人数'
        return obj.student_set.count()

    def teacher(self,obj=None,is_header=None):
        if is_header:
            return '教师'
        obj_list = obj.teachers.all()
        l = []
        [l.append(obj.name) for obj in obj_list]
        # for obj in obj_list:
        #     l.append(obj.name)
        return ','.join(l)

    #  组合搜索(根据校区,课程)
    comb_filter = [
        v1.FilterOption('school'),
        v1.FilterOption('course'),
        v1.FilterOption('teachers'),
    ]

    # ##############popup增加时，是否将新增的数据显示到页面中（获取条件） #############

    show_search_form = True
    list_display = ['school',course_semester,num,'start_date',teacher]
    edit_link = ['school']
v1.site.register(models.ClassList,ClassListConfig)


v1.site.register(models.Customer,CustomerConfig)


class ConsultRecordConfig(v1.StarkConfig):
    """
    客户跟进记录
    """
    show_comb_filter = False

    comb_filter = [
        v1.FilterOption('customer'),
    ]

    show_actions = True
    actions = []
    edit_link = ['customer']

    def changelist_view(self,request,*args,**kwargs):
        customer = request.GET.get('customer')
        current_login_user_id = 9

        ct = models.Customer.objects.filter(id=customer,consultant_id=current_login_user_id).first()
        if not ct :
            return HttpResponse('好好干你的活,拉你的人不行吗??? 嗯???💩💩💩💩💩💩💩💩💩💩')
        return super(ConsultRecordConfig, self).changelist_view(request,*args,**kwargs)

    list_display = ['customer','consultant','date']
v1.site.register(models.ConsultRecord,ConsultRecordConfig)



"""
1. 初始化学生学习记录

2. 考勤管理

3. 录成绩

4. 查看到学生所有成绩【highchart】
"""

class CourseRecordConfig(v1.StarkConfig):
    """上课记录表"""

    def display_score_list(self,obj=None,is_header=False):
        if is_header:
            return '成绩录入'


    def mutil_init(self,request):
        """自定义批量初始化方法"""
        # 上课记录id列表
        pk_list = request.POST.getlist('pk')
        # 上课记录对象列表
        record_list = models.CourseRecord.objects.filter(id__in=pk_list)

        for record in record_list:
            if models.StudyRecord.objects.filter(course_record=record).exists():
                continue
            student_list = models.Student.objects.filter(class_list=record.class_obj)
            # 为每一个学生创建dayn的学习记录
            bulk_list = []
            for student in student_list:
                bulk_list.append(models.StudyRecord(student=student,course_record=record))
            models.StudyRecord.objects.bulk_create(bulk_list)

    mutil_init.short_desc = "学生初始化"

    show_actions = True
    actions = [mutil_init,] # 因为这个是批量操作,咱们需要写点方法,里面是我们要实现的东西,所以函数

    list_display = ['class_obj','day_num','teacher',display_score_list]

v1.site.register(models.CourseRecord,CourseRecordConfig)

# v1.site.register(models.SaleRank,)
