import json

from django.conf.urls import url
from django.urls import reverse
from django.utils.safestring import mark_safe
from django.shortcuts import render,HttpResponse,redirect

from app01 import models
from stark.service import v1
from app01.stark import BasePermission
# 学生的学习记录
class StudyRecordConfig(BasePermission,v1.StarkConfig):
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
        return obj.get_record_display() # 获取到该记录选项
    list_display = ['student','course_record',display_record]

    comb_filter = [
        v1.FilterOption('course_record')
    ]

    def checked(self, request):
        pk_list = request.POST.getlist("pk")
        models.StudyRecord.objects.filter(id__in=pk_list).update(record="checked")
    checked.short_desc = "已签到"

    def vacate(self, request):
        pk_list = request.POST.getlist("pk")
        models.StudyRecord.objects.filter(id__in=pk_list).update(record="vacate")
    vacate.short_desc = "请假"

    def late(self, request):
        pk_list = request.POST.getlist("pk")
        models.StudyRecord.objects.filter(id__in=pk_list).update(record="late")
    late.short_desc = "迟到"

    def noshow(self, request):
        pk_list = request.POST.getlist("pk")
        models.StudyRecord.objects.filter(id__in=pk_list).update(record="noshow")
    noshow.short_desc = "缺勤"

    def leave_early(self, request):
        pk_list = request.POST.getlist("pk")
        models.StudyRecord.objects.filter(id__in=pk_list).update(record="leave_early")
    leave_early.short_desc = "早退"

    show_actions = True
    actions = [checked,vacate,late,noshow,leave_early]
    show_add_btn = False # 在上课记录里面，不允许创建


v1.site.register(models.StudyRecord,StudyRecordConfig)