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


class CourseRecordConfig(v1.StarkConfig):
    """上课记录表"""

    def display_score_list(self,obj=None,is_header=False):
        if is_header:
            return '成绩录入'

    def kaoqin(self,obj=None,is_header=False):
        if is_header:
            return '考勤'
        # 这里点击考勤后，会跳转到学习记录表展示页
        return mark_safe("<a href='/stark/app01/studyrecord/?course_record=%s'>考勤管理</a>" %obj.pk)

    list_display = ['class_obj', 'day_num', 'teacher', kaoqin, display_score_list]
                                                # 点击考勤后，应该是产生学习记录的数据
    def mutil_init(self,request):
        """自定义批量初始化方法"""
        # 上课记录id列表
        pk_list = request.POST.getlist('pk')
        # 上课记录对象列表
        record_list = models.CourseRecord.objects.filter(id__in=pk_list)
        # print(record_list)
        # # 这种是，遍历每一个学生，查看是否存在记录。
        # for record in record_list:
        #     student_list = models.Student.objects.filter(class_list=record.class_obj)
        #     bulk_list = []
        #     for student in student_list:
        #         exists = models.StudyRecord.objects.filter(student=student,course_record=record).exists()
        #         if exists:
        #             continue
        #         bulk_list.append(models.StudyRecord(student=student,course_record=record))
        #     models.StudyRecord.objects.bulk_create(bulk_list)

        # 下面这种是，只要有当天的学习记录，后面不管还有没有学生来，都不能添加
        for record in record_list:
            if models.StudyRecord.objects.filter(course_record=record).exists():
                continue
            student_list = models.Student.objects.filter(class_list=record.class_obj)
            # 为每一个学生创建dayn的学习记录
            bulk_list = []
            for student in student_list:
                bulk_list.append(models.StudyRecord(student=student,course_record=record))
            models.StudyRecord.objects.bulk_create(bulk_list)
        # return redirect('/stark/app01/courserecord/')
        return HttpResponse('初始化成功！')

    show_actions = True
    mutil_init.short_desc = "学生初始化"
    actions = [mutil_init,] # 因为这个是批量操作,咱们需要写点方法,里面是我们要实现的东西,所以函数
v1.site.register(models.CourseRecord,CourseRecordConfig)


# 学生的学习记录
class StudyRecordConfig(v1.StarkConfig):
    """
    1. 初始化学生学习记录

    2. 考勤管理

    3. 录成绩

    4. 查看到学生所有成绩【highchart】
    """
    # 出勤信息(choices选项)
    def display_record(self,obj=None,is_header=False):
        if is_header:
            return '出勤'
        return obj.get_record_display()
    list_display = ['student','course_record',display_record]

    comb_filter = [
        v1.FilterOption('course_record')
    ]

    def action_checked(self,request):
        pass
    action_checked.short_desc = '签到'

    def action_vacate(self, request):
        pass
    action_vacate.short_desc = "请假"

    def action_late(self, request):
        pass
    action_late.short_desc = "迟到"

    def action_noshow(self, request):
        pk_list = request.POST.getlist('pk')
        models.StudyRecord.objects.filter(id__in=pk_list).update(record='noshow')
    action_noshow.short_desc = "缺勤"

    def action_leave_early(self, request):
        pass
    action_leave_early.short_desc = "早退"

    actions = [action_checked, action_vacate, action_late, action_noshow, action_leave_early]
    show_actions = True

    show_add_btn = False # 在上课记录里面，不允许创建
v1.site.register(models.StudyRecord,StudyRecordConfig)


class StudentConfig(v1.StarkConfig):
    list_display = ['username','emergency_contract']
v1.site.register(models.Student,StudentConfig)