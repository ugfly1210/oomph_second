# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-12-24 07:28
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ClassList',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('semester', models.IntegerField(verbose_name='班级(期)')),
                ('price', models.IntegerField(verbose_name='学费')),
                ('start_date', models.DateField(verbose_name='开班日期')),
                ('graduate_date', models.DateField(blank=True, null=True, verbose_name='结业日期')),
                ('memo', models.CharField(blank=True, max_length=256, null=True, verbose_name='说明')),
            ],
        ),
        migrations.CreateModel(
            name='ConsultRecord',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(auto_now_add=True, verbose_name='跟进日期')),
                ('note', models.TextField(verbose_name='跟进内容...')),
            ],
        ),
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=32, verbose_name='课程名称')),
            ],
        ),
        migrations.CreateModel(
            name='CourseRecord',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('day_num', models.IntegerField(help_text='此处填写第几节课或第几天课程...,必须为数字', verbose_name='节次')),
                ('date', models.DateField(auto_now_add=True, verbose_name='上课日期')),
                ('course_title', models.CharField(blank=True, max_length=64, null=True, verbose_name='本节课程标题')),
                ('course_memo', models.TextField(blank=True, null=True, verbose_name='本节课程内容概要')),
                ('has_homework', models.BooleanField(default=True, verbose_name='本节有作业')),
                ('homework_title', models.CharField(blank=True, max_length=64, null=True, verbose_name='本节作业标题')),
                ('homework_memo', models.TextField(blank=True, max_length=500, null=True, verbose_name='作业描述')),
                ('exam', models.TextField(blank=True, max_length=300, null=True, verbose_name='踩分点')),
                ('class_obj', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app01.ClassList', verbose_name='班级')),
            ],
        ),
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('qq', models.CharField(help_text='QQ号必须唯一', max_length=64, unique=True, verbose_name='qq')),
                ('name', models.CharField(max_length=16, verbose_name='学生姓名')),
                ('gender', models.SmallIntegerField(choices=[(1, '男'), (2, '女')], verbose_name='性别')),
                ('education', models.IntegerField(blank=True, choices=[(1, '重点大学'), (2, '普通本科'), (3, '独立院校'), (4, '民办本科'), (5, '大专'), (6, '民办专科'), (7, '高中'), (8, '其他')], null=True, verbose_name='学历')),
                ('graduation_school', models.CharField(blank=True, max_length=64, null=True, verbose_name='毕业学校')),
                ('major', models.CharField(blank=True, max_length=64, null=True, verbose_name='所学专业')),
                ('experience', models.IntegerField(blank=True, choices=[(1, '在校生'), (2, '应届毕业'), (3, '半年以内'), (4, '半年至一年'), (5, '一年至三年'), (6, '三年至五年'), (7, '五年以上')], null=True, verbose_name='工作经验')),
                ('work_status', models.IntegerField(blank=True, choices=[(1, '在职'), (2, '无业')], default=1, null=True, verbose_name='职业状态')),
                ('company', models.CharField(blank=True, max_length=64, null=True, verbose_name='目前就职公司')),
                ('salary', models.CharField(blank=True, max_length=64, null=True, verbose_name='当前薪资')),
                ('source', models.SmallIntegerField(choices=[(1, 'qq群'), (2, '内部转介绍'), (3, '官方网站'), (4, '百度推广'), (5, '360推广'), (6, '搜狗推广'), (7, '腾讯课堂'), (8, '广点通'), (9, '高校宣讲'), (10, '渠道代理'), (11, '51cto'), (12, '智汇推'), (13, '网盟'), (14, 'DSP'), (15, 'SEO'), (16, '其它')], default=1, verbose_name='客户来源')),
                ('status', models.IntegerField(choices=[(1, '已报名'), (2, '未报名')], default=2, help_text='选择客户此时的状态', verbose_name='状态')),
                ('date', models.DateField(auto_now_add=True, verbose_name='咨询日期')),
                ('last_consult_date', models.DateField(auto_now_add=True, verbose_name='最后跟进日期')),
            ],
        ),
        migrations.CreateModel(
            name='Department',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=16, verbose_name='部门名称')),
                ('code', models.IntegerField(unique=True, verbose_name='部门编号')),
            ],
        ),
        migrations.CreateModel(
            name='PaymentRecord',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pay_type', models.IntegerField(choices=[(1, '订金/报名费'), (2, '学费'), (3, '转班'), (4, '退学'), (5, '退款')], default=1, verbose_name='费用类型')),
                ('paid_fee', models.IntegerField(default=0, verbose_name='费用数额')),
                ('turnover', models.IntegerField(blank=True, null=True, verbose_name='成交金额')),
                ('quote', models.IntegerField(blank=True, null=True, verbose_name='报价金额')),
                ('note', models.TextField(blank=True, null=True, verbose_name='备注')),
                ('date', models.DateTimeField(auto_now_add=True, verbose_name='交款日期')),
                ('class_list', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='app01.ClassList', verbose_name='班级')),
            ],
        ),
        migrations.CreateModel(
            name='School',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=32, verbose_name='校区名称')),
            ],
        ),
        migrations.CreateModel(
            name='Student',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=32, verbose_name='用户名')),
                ('password', models.CharField(max_length=64, verbose_name='密码')),
                ('emergency_contract', models.CharField(blank=True, max_length=32, null=True, verbose_name='紧急联系人')),
                ('company', models.CharField(blank=True, max_length=128, null=True, verbose_name='公司')),
                ('location', models.CharField(blank=True, max_length=64, null=True, verbose_name='所在区域')),
                ('position', models.CharField(blank=True, max_length=64, null=True, verbose_name='岗位')),
                ('salary', models.IntegerField(blank=True, null=True, verbose_name='薪资')),
                ('welfare', models.CharField(blank=True, max_length=256, null=True, verbose_name='福利')),
                ('date', models.DateField(blank=True, help_text='格式yyyy-mm-dd', null=True, verbose_name='入职时间')),
                ('memo', models.CharField(blank=True, max_length=256, null=True, verbose_name='备注')),
                ('class_list', models.ManyToManyField(blank=True, to='app01.ClassList', verbose_name='已报班级')),
                ('customer', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='app01.Customer', verbose_name='客户信息')),
            ],
        ),
        migrations.CreateModel(
            name='StudyRecord',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('record', models.CharField(choices=[('checked', '已签到'), ('vacate', '请假'), ('late', '迟到'), ('noshow', '缺勤'), ('leave_early', '早退')], default='checked', max_length=64, verbose_name='上课纪录')),
                ('score', models.IntegerField(choices=[(100, 'A+'), (90, 'A'), (85, 'B+'), (80, 'B'), (70, 'B-'), (60, 'C+'), (50, 'C'), (40, 'C-'), (0, ' D'), (-1, 'N/A'), (-100, 'COPY'), (-1000, 'FAIL')], default=-1, verbose_name='本节成绩')),
                ('homework_note', models.CharField(blank=True, max_length=255, null=True, verbose_name='作业评语')),
                ('note', models.CharField(blank=True, max_length=255, null=True, verbose_name='备注')),
                ('homework', models.FileField(blank=True, default=None, null=True, upload_to='', verbose_name='作业文件')),
                ('stu_memo', models.TextField(blank=True, null=True, verbose_name='学员备注')),
                ('date', models.DateTimeField(auto_now_add=True, verbose_name='提交作业日期')),
                ('course_record', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app01.CourseRecord', verbose_name='第几天课程')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app01.Student', verbose_name='学员')),
            ],
        ),
        migrations.CreateModel(
            name='UserInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=16, verbose_name='员工姓名')),
                ('username', models.CharField(max_length=32, verbose_name='用户名')),
                ('password', models.CharField(max_length=64, verbose_name='密码')),
                ('email', models.EmailField(max_length=64, verbose_name='邮箱')),
                ('depart', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app01.Department', to_field='code', verbose_name='部门')),
            ],
        ),
        migrations.AddField(
            model_name='paymentrecord',
            name='consultant',
            field=models.ForeignKey(help_text='谁签的单就选谁', on_delete=django.db.models.deletion.CASCADE, to='app01.UserInfo', verbose_name='负责老师'),
        ),
        migrations.AddField(
            model_name='paymentrecord',
            name='customer',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app01.Customer', verbose_name='客户'),
        ),
        migrations.AddField(
            model_name='customer',
            name='consultant',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='consultant', to='app01.UserInfo', verbose_name='课程顾问'),
        ),
        migrations.AddField(
            model_name='customer',
            name='course',
            field=models.ManyToManyField(to='app01.Course', verbose_name='咨询课程'),
        ),
        migrations.AddField(
            model_name='customer',
            name='referral_from',
            field=models.ForeignKey(blank=True, help_text='若此客户是转介绍自内部学员,请在此处选择内部学员姓名', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='internal_referral', to='app01.Customer', verbose_name='转介绍自学员'),
        ),
        migrations.AddField(
            model_name='courserecord',
            name='teacher',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app01.UserInfo', verbose_name='讲师'),
        ),
        migrations.AddField(
            model_name='consultrecord',
            name='consultant',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app01.UserInfo', verbose_name='跟踪人'),
        ),
        migrations.AddField(
            model_name='consultrecord',
            name='customer',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app01.Customer', verbose_name='所咨询客户'),
        ),
        migrations.AddField(
            model_name='classlist',
            name='course',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app01.Course', verbose_name='课程名称'),
        ),
        migrations.AddField(
            model_name='classlist',
            name='school',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app01.School', verbose_name='校区'),
        ),
        migrations.AddField(
            model_name='classlist',
            name='teachers',
            field=models.ManyToManyField(related_name='teach_classes', to='app01.UserInfo', verbose_name='任课老师'),
        ),
        migrations.AddField(
            model_name='classlist',
            name='tutor',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='classes', to='app01.UserInfo', verbose_name='班主任'),
        ),
    ]
