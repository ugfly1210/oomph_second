from django.shortcuts import redirect,HttpResponse,render
from stark.service import v1
from app01 import models
from django.conf.urls import url
from django.utils.safestring import mark_safe
# from app01.configs.customer import CustomerConfig
# from app01.configs.student import StudentConfig

class BasePermission(object):

    def get_show_add_btn(self):
        code_list = self.request.permission_code_list
        if 'add' in  code_list:
            return True

    def get_edit_link(self):
        code_list = self.request.permission_code_list
        if "edit" in code_list:
            return super(BasePermission, self).get_edit_link()
        else:
            return []

    def get_list_display(self):
        code_list = self.request.permission_code_list
        data = []
        if self.list_display:
            data.extend(self.list_display)
            if 'del' in code_list:
                data.append(v1.StarkConfig.delete)
            data.insert(0, v1.StarkConfig.checkbox)
        return data


class DepartmentConfig(BasePermission,v1.StarkConfig):
    list_display = ['title','code']
    edit_link = ['title']
v1.site.register(models.Department,DepartmentConfig)


class UserInfoConfig(BasePermission,v1.StarkConfig):
    list_display = ['name','username','email','depart']
    # 组合搜索
    comb_filter = [
        v1.FilterOption('depart',text_func_name=lambda x:str(x),val_func_name=lambda x:x.code) # 字段  只在choice,fk,m2m有用
    ]                          # 这俩函数就是为了防止你自定义的fk的值不是主键用的

    edit_link = ['name']

    # 显示搜索并支持模糊搜索
    show_search_form = True
    search_fields = ['name__contains']
v1.site.register(models.UserInfo,UserInfoConfig)


class CourseConfig(BasePermission,v1.StarkConfig):
    list_display = ['name']
    edit_link = ['name',]
v1.site.register(models.Course,CourseConfig)


class SchoolConfig(BasePermission,v1.StarkConfig):
    list_display = ['title']
    edit_link = ['title',]
v1.site.register(models.School,SchoolConfig)


class ClassListConfig(BasePermission,v1.StarkConfig):
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


# v1.site.register(models.Customer,CustomerConfig)


class ConsultRecordConfig(BasePermission,v1.StarkConfig):
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
            return HttpResponse('好好干你的活,拉你的人不行吗??? ')
        return super(ConsultRecordConfig, self).changelist_view(request,*args,**kwargs)

    list_display = ['customer','consultant','date']
v1.site.register(models.ConsultRecord,ConsultRecordConfig)


class CourseRecordConfig(BasePermission,v1.StarkConfig):
    """上课记录表"""
    def extra_url(self):
        app_model_name = (self.model_class._meta.app_label, self.model_class._meta.model_name,)
        url_list = [
            url(r'^(\d+)/score_list/$', self.wrap(self.score_list), name="%s_%s_score_list" % app_model_name),
        ]
        return url_list

    def score_list(self,request,record_id):
        """
        录入成绩页面
        :param request:
        :param record_id: 老师上课记录ID
        :return:
        """
        if request.method == 'GET':
            from django.forms import Form
            from django.forms import fields
            from django.forms import widgets
            ##方式一
            # study_record_list = models.StudyRecord.objects.filter(course_record_id=record_id)  #这一天上课的所有的学生的学习记录
            # score_choices = models.StudyRecord.score_choices
            # return render(request,"score_list.html",{"study_record_list":study_record_list,"score_choices":score_choices})

            # 改款
            # class TestForm(Form):
            #     score = fields.ChoiceField(choices=models.StudyRecord.record_choices)
            #     homeword_note = fields.CharField(widget=widgets.Textarea())

            # 因为前端要拿到id和对象，所以使用type来创建，来自定义字段
            study_record_list = models.StudyRecord.objects.filter(course_record_id=record_id)
            data = []
            for obj in study_record_list:
                TestForm = type('TempForm',(Form,),{
                    'score_%s'%obj.pk : fields.ChoiceField(choices=models.StudyRecord.score_choices),
                    'homework_note_%s'%obj.pk : fields.CharField(widget=widgets.Textarea())
                })
                data.append({'obj':obj,'form':TestForm(initial={'score_%s' %obj.pk:obj.score,'homework_note_%s' %obj.pk:obj.homework_note})})
            return render(request,'score_list.html',{'data':data})
        else:
            data_dict = {}
            """
            构造这样的字典，目的是保存更新数据库里面的数据，字典的结构的
            {
                3:{"score":2,"homework_note":2}
                4:{"score":4,"homework_note":4}
            }
            """
            for key, value in request.POST.items():
                if key == "csrfmiddlewaretoken":
                    continue
                name, nid = key.rsplit('_', 1)
                if nid in data_dict:
                    data_dict[nid][name] = value
                else:
                    data_dict[nid] = {name: value}

            for nid, update_dict in data_dict.items():
                print(data_dict.items())
                models.StudyRecord.objects.filter(id=nid).update(**update_dict)

            return redirect(request.path_info)

    def display_score_list(self,obj=None,is_header=False):
        if is_header:
            return '成绩录入'
        from django.urls import reverse
        # 点击后跳转到成绩录入页面
        rurl = reverse('stark:app01_courserecord_score_list',args=(obj.pk,))
        print('<a href="%s">成绩录入</a>'%rurl)
        return mark_safe('<a href="%s">成绩录入</a>'%rurl)

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

        print(pk_list)
        # 上课记录对象列表
        record_list = models.CourseRecord.objects.filter(id__in=pk_list)
        print(record_list)
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





# v1.site.register(models.Student,StudentConfig)