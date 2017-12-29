import json,datetime
from django.conf.urls import url
from django.db.models import Q
from django.urls import reverse
from django.utils.safestring import mark_safe
from django.shortcuts import render,HttpResponse,redirect
from django.forms import ModelForm
from app01 import models
from stark.service import v1
from utils import message
from django.db import transaction


class SingleModelForm(ModelForm):
    class Meta:
        model = models.Customer
        exclude = ['consultant','status','recv_date','last_consult_date']



class CustomerConfig(v1.StarkConfig):
    order_by = ['-status']

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

    list_display = ['name','referral_from',display_gender,display_education,display_source,display_course,display_status,record]
    edit_link = ['name']

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
            url(r'^public/$', self.wrap(self.public_view), name="%s_%s_public" %app_model_name),
            url(r'^user/$', self.wrap(self.user_view), name="%s_%s_user" %app_model_name),
            url(r'^(\d+)/competition/$', self.wrap(self.competition_view),name = "%s_%s_competition" % app_model_name),
            url(r'^single/$', self.wrap(self.single_view), name="%s_%s_single" % app_model_name),
        ]
        return patterns

    def public_view(self,request):
        """
        公共客户资源, 未报名 & (15天未接单 or 三天未跟进)
        """

        current_user_id = 9

        # 当前日期
        current_date = datetime.datetime.now().date()
        # 最后接单时间
        no_deal = current_date - datetime.timedelta(days=15)
        # 最后跟进日期
        no_follow_date = current_date - datetime.timedelta(days=3)

        """公共客户"""
        # 方法一:
        # customer_list = models.Customer.objects.filter(Q(recv_date__lt=no_deal)|Q(last_consult_date__lt=no_follow),status=2)
        # customer_list = models.Customer.objects.filter(Q(recv_date__lt=no_deal)|Q(last_consult_date__lt=no_follow_date),status=2)
        # print('9999999999',customer_list)
        # 方法二:
        con = Q()
        q1 = Q(status=2)
        q2 = Q()
        q2.connector = 'OR'
        q2.children.append(('recv_date__lt', no_deal))
        q2.children.append(('last_consult_date__lt', no_follow_date))
        con.add(q1,'AND')
        con.add(q2,'AND')
        customer_list = models.Customer.objects.filter(con)

        return render(request,'public_view.html',{'customer_list':customer_list,"current_user_id":current_user_id})

    def competition_view(self,request,cid):
        """
        抢单表
        :param request:
        :param cid: customer_id 来自于公共资源里面的抢单选项,public_view
        :return:
        """
        current_user_id = 9 # 这个是从session中拿的
        """抢单之后,它会修改客户表里面的: recv_date & last_consult_date & 课程顾问
            可以抢单的前提条件是: 之前的顾问不是自己,状态必须是未报名,并且满足3/15的要求"""
        current_date = datetime.datetime.now().date()
        no_deal = current_date - datetime.timedelta(days=15) # 最后接单日期
        no_follow_date = current_date - datetime.timedelta(days=3) # 最后跟进日期
        # 更新数据
        row_count = models.Customer.objects.filter(Q(recv_date__lt=no_deal) | Q(last_consult_date__lt=no_follow_date),status=2,id=cid).exclude(consultant_id=current_user_id).update(recv_date=current_date,last_consult_date=current_date,consultant_id=current_user_id)
        if not row_count:
            return HttpResponse('配嘛...')
        # 如果存在的话,我们就把它添加到客户分配表CustomerDistribution里面
        models.CustomerDistribution.objects.create(ctime=current_date,customer_id=cid,user_id=current_user_id)
        return HttpResponse('嗯嗯,归你归你')

    def user_view(self,request):
        """当前登录用户的所有的客户(在我这成单的,以及我正在跟进的)"""
        current_user_id = 9
        customer_list = models.CustomerDistribution.objects.filter(user_id=current_user_id).order_by('status')
        return render(request,'user_view.html',{'customer_list':customer_list})

    def single_view(self,request):
        """单条录入客户信息"""
        from cccccccccccccc import AutoSale
        if request.method == 'GET':
            form = SingleModelForm()
            return render(request,'single_view.html',{'form':form})
        else:
            current_date = datetime.datetime.now().date()
            form = SingleModelForm(request.POST)
            if form.is_valid():
                print(form.cleaned_data)
                sale_id = AutoSale.get_sale_id()
                if not sale_id:
                    return HttpResponse('暂无课程顾问,请添加后再分配')
                try:
                    with transaction.atomic():
                        # 客户表保存
                        form.instance.consultant_id = sale_id
                        form.instance.recv_date = current_date
                        form.instance.last_consult_date = current_date

                        new_customer = form.save()  # 这就算创建完成了

                        # 将关系添加到客户分配表
                        models.CustomerDistribution.objects.create(customer=new_customer,ctime=current_date,user_id=sale_id)

                        # 发送邮件信息
                        # message.send_message('17701335022@163.com','saofei','fk','fk you')
                except Exception as e:
                    # 创建客户和分配销售异常
                    AutoSale.rollback(sale_id)
                    return HttpResponse('录入异常')

                return  HttpResponse('录入成功')
                
            else:
                return render(request,'single_view.html',{'form':form})

