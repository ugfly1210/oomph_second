import json

from django.conf.urls import url
from django.urls import reverse
from django.utils.safestring import mark_safe
from django.shortcuts import render,HttpResponse,redirect

from app01 import models
from stark.service import v1


class StudentConfig(v1.StarkConfig):

    def extra_url(self):
        app_model_name = (self.model_class._meta.app_label, self.model_class._meta.model_name,)
        # print("app_model_name",app_model_name)
        url_list = [
            url(r'^(\d+)/sv/$', self.wrap(self.scores_view), name="%s_%s_sv" % app_model_name),
            url(r'^chart$',self.wrap(self.scores_chart),name='%s_%s_chart'%app_model_name),
        ]
        return url_list

    def scores_view(self,request,sid):
        obj = models.Student.objects.filter(id=sid).first()
        if not obj :
            return HttpResponse('兄弟，没有这个银儿呢。。。')

        # 学生和班级是多对多，所以拿到的是classlist，可以查看当前学生在不同班级的所有成绩
        class_list = obj.class_list.all()
        return render(request,'scores_view.html',{'class_list':class_list,'sid':sid})

    def scores_chart(self,request):
        ret = {'status': False, 'data': None, 'msg': None}
        try:
            cid = request.GET.get('cid')
            sid = request.GET.get('sid')
            # 查看当前学生的学习记录，去学习记录表查
            record_list = models.StudyRecord.objects.filter(student_id=sid,course_record__class_obj_id=cid).order_by('course_record_id')
            data = []
            for row in record_list:
                day = 'day%s'%row.course_record.day_num
                data.append([day,row.score])
            ret['data'] = data
            print(record_list)
            ret['status'] = True
        except Exception as e :
            ret['msg'] = '获取失败'
        return HttpResponse(json.dumps(ret))

    def display_score(self,obj=None,is_header=False):
        if is_header:
            return '成绩'
        surl = reverse('stark:app01_student_sv',args=(obj.pk))
        return mark_safe('<a href="%s">查看成绩</a>'%surl)

    list_display = ['username', 'emergency_contract',display_score]