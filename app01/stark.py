from django.shortcuts import redirect,HttpResponse
from stark.service import v1
from app01 import models
from django.conf.urls import url
from django.utils.safestring import mark_safe


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


class CustomerConfig(v1.StarkConfig):
    def display_gender(self,obj=None,is_header=None):
        if is_header:
            return '性别'
        return obj.get_gender_display()

    def display_education(self,obj=None,is_header=None):
        if is_header:
            return '学历'
        return obj.get_education_display()

    def display_source(self,obj=None,is_header=None):
        if is_header:
            return '客户来源'
        return obj.get_source_display()

    def display_course(self,obj=None,is_header=None):
        if is_header:
            return '咨询课程'
        html = []
        obj_list = obj.course.all()
        for obj1 in obj_list:
            temp = "<a style='display:inline-block;padding:3px 5px;border:2px solid red;margin:2px;' href='/stark/app01/customer/%s/%s/dc/'>%s <span class='glyphicon glyphicon-trash'></span></a>" %(obj.pk,obj1.pk,obj1.name)
            html.append(temp)
        return mark_safe(''.join(html))

    def display_status(self,obj=None,is_header=None):
        """
        客户状态是可以点击修改的
        :param obj:
        :param is_header:
        :return:
        """
        if is_header:
            return '客户状态'
        # print('obj......',obj)   姓名:骚伟,QQ:123456
        return obj.get_status_display()

    def record(self,obj=None,is_header=None):
        """客户跟进记录,
           http://127.0.0.1:8000/stark/app01/consultrecord/?customer=1
        """
        if is_header:
            return '客户跟进记录'
        return mark_safe("<a href='/stark/app01/consultrecord/?customer=%s'>查看跟进记录</a>"%(obj.pk))

    def delete_course(self,request,customer_id,course_id):
        """
        删除当前用户感兴趣的课程
        :param request:
        :param customer_id:
        :param course_id:
        :return:
        """
        # print('self.model_class=,=',self.model_class.objects.all())
        # < QuerySet[ < Customer: 姓名:骚伟, QQ: 123456 >] >
        customer_obj = self.model_class.objects.filter(pk=customer_id).first()
        # 在多对多字段中可以remove,
        customer_obj.course.remove(course_id)
        # ####################作业:  删除完成跳转回来的时候,带着走的时候的url
        # self.request.GET
        # self._query_param_key
        # 构造QueryDict
        # urlencode()
        return redirect(self.get_list_url())

    def extra_url(self):
        app_model_name = (self.model_class._meta.app_label,self.model_class._meta.model_name,)
        patterns = [
            url(r'^(\d+)/(\d+)/dc/$', self.wrap(self.delete_course), name="%s_%s_dc" %app_model_name),
        ]
        return patterns

    list_display = ['name','referral_from',display_gender,display_education,display_source,display_course,display_status,record]
    edit_link = ['name']
v1.site.register(models.Customer,CustomerConfig)


class ConsultRecordConfig(v1.StarkConfig):
    """
    客户跟进记录
    """
    show_comb_filter = False

    comb_filter = [
        v1.FilterOption('customer'),
    ]

    def changelist_view(self,request,*args,**kwargs):
        customer = request.GET.get('customer')
        current_login_user_id = 9
        ct = models.Customer.objects.filter(id=customer,consultant_id=current_login_user_id).first()
        if not ct :
            return HttpResponse('好好干你的活,拉你的人不行吗??? 嗯???💩💩💩💩💩💩💩💩💩💩')
        return super(ConsultRecordConfig, self).changelist_view(request,*args,**kwargs)

    list_display = ['customer','consultant','date']
v1.site.register(models.ConsultRecord,ConsultRecordConfig)