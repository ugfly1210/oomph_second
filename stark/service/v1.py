import copy
import json
from django.conf.urls import url
from django.shortcuts import HttpResponse,render,redirect
from django.utils.safestring import mark_safe
from django.urls import reverse
from django.http import QueryDict
from django.db.models import Q
"""
请求来之后先到changelist_view里面,
然后把列表页面所有代码放在ChangeList类里面

"""


class FilterOption(object):
    def __init__(self,field_name,multi=False,condition=None,is_choice=False,text_func_name=None,val_func_name=None):
        """
        :param field_name: 字段
        :param multi:  是否多选
        :param condition: 显示数据的筛选条件
        :param is_choice: 是否是choice
        :param text_func_name: 在Model中定义函数,显示文本名称,默认使用str(对象)
        :param val_func_name: 在Model中定义函数,页面生成的a标签中对应的值的函数.  默认使用 对象.pk
        """
        self.field_name = field_name
        self.multi = multi
        self.is_choice = is_choice

        self.condition = condition

        self.text_func_name = text_func_name
        self.val_func_name = val_func_name

    def get_queryset(self,_field):
        if self.condition:
            return _field.rel.to.objects.filter(**self.condition)
        return _field.rel.to.objects.all()

    def get_choices(self,_field):
        return _field.choices


class FilterRow(object):
    def __init__(self,option, data, request):
        self.data = data
        self.option = option # option: 要配置的对象  v1.FilterOption('depart',text_func_name=None,val_func_name=None)
        self.request = request

    def __iter__(self):
        params = copy.deepcopy(self.request.GET)
        params._mutable = True
        current_id = params.get(self.option.field_name) # 3
        current_id_list = params.getlist(self.option.field_name) # [1,2,3]

        if self.option.field_name in params:
            # del params[self.option.field_name]
            origin_list = params.pop(self.option.field_name)
            url = "{0}?{1}".format(self.request.path_info, params.urlencode())
            yield mark_safe('<a href="{0}">全部</a>'.format(url))
            params.setlist(self.option.field_name,origin_list)
        else:
            url = "{0}?{1}".format(self.request.path_info, params.urlencode())
            yield mark_safe('<a class="active" href="{0}">全部</a>'.format(url))
        # ( (1,男),(2,女)  )
        for val in self.data:
            print('val---',val)
            if self.option.is_choice:
                pk,text = str(val[0]),val[1]
            else:
                # 如果你设置了这个函数就走你设置的函数,否则 str(val) str(val.pk)
                text = self.option.text_func_name(val) if self.option.text_func_name else str(val)
                pk = str(self.option.val_func_name(val)) if self.option.val_func_name else str(val.pk)
                # pk = str(self.option.val_func_name(val)) if self.option.val_func_name else str(val.pk)
                # pk,text = str(val.pk), str(val)
            # 当前URL？option.field_name
            # 当前URL？gender=pk
            # self.request.path_info # http://127.0.0.1:8005/arya/crm/customer/?gender=1&id=2
            # self.request.GET['gender'] = 1 # &id=2gender=1
            if not self.option.multi:
                # 单选
                params[self.option.field_name] = pk
                url = "{0}?{1}".format(self.request.path_info,params.urlencode())
                if current_id == pk:
                    yield mark_safe("<a class='active' href='{0}'>{1}</a>".format(url,text))
                else:
                    yield mark_safe("<a href='{0}'>{1}</a>".format(url, text))
            else:
                # 多选 current_id_list = ["1","2"]
                _params = copy.deepcopy(params)
                id_list = _params.getlist(self.option.field_name)

                if pk in current_id_list:
                    id_list.remove(pk)
                    _params.setlist(self.option.field_name, id_list)
                    url = "{0}?{1}".format(self.request.path_info, _params.urlencode())
                    yield mark_safe("<a class='active' href='{0}'>{1}</a>".format(url, text))
                else:
                    id_list.append(pk)
                    # params中被重新赋值
                    _params.setlist(self.option.field_name,id_list)
                    # 创建URL
                    url = "{0}?{1}".format(self.request.path_info, _params.urlencode())
                    yield mark_safe("<a href='{0}'>{1}</a>".format(url, text))


class ChangeList(object):

    def __init__(self,config,queryset):
        self.config = config

        # [checkbox,'id','name',edit,del]
        self.list_display = config.get_list_display()
        self.model_class = config.model_class
        self.request = config.request
        self.show_add_btn = config.get_show_add_btn()
        self.actions = config.get_actions()
        self.show_actions = config.get_show_actions()
        self.comb_filter = config.get_comb_filter()
        self.show_comb_filter = config.get_show_comb_filter()
        self.edit_link = config.get_edit_link()

        # 搜索用
        self.show_search_form = config.get_show_search_form()
        self.search_form_val = config.request.GET.get(config.search_key,'')

        from utils.pager import Pagination
        current_page = self.request.GET.get('page', 1)
        total_count = queryset.count()
        page_obj = Pagination(current_page, total_count, self.request.path_info, self.request.GET, per_page_count=6)
        self.page_obj = page_obj

        self.data_list = queryset[page_obj.start:page_obj.end]

    def modify_actions(self):
        """
        将我们写的函数,改成文本
        用于action中显示数据的文本和value属性值
        """
        result = []
        for func in self.actions:
            temp = {'name':func.__name__,'text':func.short_desc}
            result.append(temp)
        return result

    def add_url(self):
        return self.config.get_add_url()

    def head_list(self):
        """
        构造表头
        :return: 
        """
        result = []
        # [checkbox,'id','name',edit,del]
        for field_name in self.list_display:
            if isinstance(field_name, str):
                # 根据类和字段名称，获取字段对象的verbose_name
                verbose_name = self.model_class._meta.get_field(field_name).verbose_name
            else:
                verbose_name = field_name(self.config, is_header=True)
            result.append(verbose_name)
        return result

    def body_list(self):
        """
        列表页面,数据表内容中显示每一行数据
        """
        # 帮助生成页面上显示的东西
        # 处理表中的数据
        # [ UserInfoObj,UserInfoObj,UserInfoObj,UserInfoObj,]
        # [ UserInfo(id=1,name='ff',age=18),UserInfo(id=2,name='ff2',age=181),]
        data_list = self.data_list
        new_data_list = []
        for row in data_list:
            # row是 UserInfo(id=2,name='dd2',age=181)
            # row.id,row.name,row.age
            temp = []
            for field_name in self.list_display:
                if isinstance(field_name,str):
                    val = getattr(row,field_name) # # 2 ff2
                else:
                    val = field_name(self.config,row)

                # 定制编辑列
                # 判断字段是否在edit_link里面,并生成a标签
                if field_name in self.edit_link:
                    val = self.edit_link_tag(row.pk, val)

                temp.append(val)
            new_data_list.append(temp)

        return new_data_list

    def gen_comb_filter(self):
        """
        生成器函数
        :return: 
        """
        # ['gender','depart','roles']
        # self.model_class = > models.UserInfo

        """
        [
             FilterRow(((1,'男'),(2,'女'),)),
             FilterRow([obj,obj,obj,obj ]),
             FilterRow([obj,obj,obj,obj ]),
        ]
        """
        from django.db.models import ForeignKey,ManyToManyField
        for option in self.comb_filter:
            _field = self.model_class._meta.get_field(option.field_name)
            if isinstance(_field,ForeignKey):
                # 获取当前字段depart，关联的表 Department表并获取其所有数据
                # print(field_name,_field.rel.to.objects.all())
                row = FilterRow(option, option.get_queryset(_field), self.request)
            elif isinstance(_field,ManyToManyField):
                # print(field_name, _field.rel.to.objects.all())
                # data_list.append(  FilterRow(_field.rel.to.objects.all()) )
                row = FilterRow(option,option.get_queryset(_field), self.request)

            else:
                # print(field_name,_field.choices)
                # data_list.append(  FilterRow(_field.choices) )
                row = FilterRow(option,option.get_choices(_field),self.request)
            # 可迭代对象
            yield row # 每一个row就是一行搜索条件,又放到了filterrow类里面

    def edit_link_tag(self,pk,text):
        query_str = self.request.GET.urlencode()
        params = QueryDict(mutable=True)
        params[self.config._query_param_key] = query_str
        return mark_safe('<a href="%s?%s">%s</a>' % (self.config.get_change_url(pk), params.urlencode(),text))  # /stark/app01/userinfo/


class StarkConfig(object):
    """
    用于处理stark中增删改查的基类
    以后每个类的配置需要继承基类, 如 :
    class UserInfoConfig(v1.StarkConfig):
        list_display = ['id','name']

    v1.site(models.UserInfo,UserInfoConfig)
    """

    # 1. 定制列表页面显示的列
    def checkbox(self,obj=None,is_header=False):
        if is_header:
            return '选择'
        return mark_safe('<input type="checkbox" name="pk" value="%s" />' %(obj.id,))
    def edit(self,obj=None,is_header=False):
        if is_header:
            return '编辑'
        # 获取条件
        query_str = self.request.GET.urlencode() # page=2&nid=1
        if query_str:
            # 重新构造
            params = QueryDict(mutable=True)
            params[self._query_param_key] = query_str
            return mark_safe('<a href="%s?%s">编辑</a>' %(self.get_change_url(obj.id),params.urlencode(),)) # /stark/app01/userinfo/
        return mark_safe('<a href="%s">编辑</a>' % (self.get_change_url(obj.id),))  # /stark/app01/userinfo/
    def delete(self,obj=None,is_header=False):
        if is_header:
            return '删除'
        return mark_safe('<a href="%s">删除</a>' %(self.get_delete_url(obj.id),))

    list_display = []

    def get_list_display(self):
        data = []
        if self.list_display:
            data.extend(self.list_display)
            # data.append(StarkConfig.edit)
            data.append(StarkConfig.delete)
            data.insert(0,StarkConfig.checkbox)
        return data

    # 谁是可编辑的
    edit_link = []
    def get_edit_link(self):
        result = []
        if self.edit_link:
            result.extend(self.edit_link)
        return result


    # 2. 是否显示添加按钮
    show_add_btn = True

    def get_show_add_btn(self):
        return self.show_add_btn

    # 3. model_form_class
    model_form_class = None
    def get_model_form_class(self):
        if self.model_form_class:
            return self.model_form_class

        from django.forms import ModelForm
        # class TestModelForm(ModelForm):
        #     class Meta:
        #         model = self.model_class
        #         fields = "__all__"
        # 作业：type创建TestModelForm类
        meta = type('Meta',(object,),{'model':self.model_class,'fields':'__all__'})
        TestModelForm = type('TestModelForm',(ModelForm,),{'Meta':meta})
        return TestModelForm

    # 4. 关键字搜索
    show_search_form = False
    def get_show_search_form(self):
        return self.show_search_form

    search_fields = []
    def get_search_fields(self):
        result = []
        if self.search_fields:
            result.extend(self.search_fields)

        return result

    def get_search_condition(self):
        key_word = self.request.GET.get(self.search_key)
        search_fields = self.get_search_fields()
        condition = Q()
        condition.connector = 'or'
        if key_word and self.get_show_search_form():
            for field_name in search_fields:
                condition.children.append((field_name, key_word))
        return condition

    # 5. actions定制
    show_actions = False
    def get_show_actions(self):
        return self.show_actions

    def default_action(self,request):
        pass
    default_action.short_desc = '请选择action'

    actions = []
    def get_actions(self):
        result = []
        if self.actions:
            result.extend(self.actions)
            result.insert(0,StarkConfig.default_action)
        return result

    # 6. 组合搜索
    comb_filter = []
    def get_comb_filter(self):
        result = []
        if self.comb_filter:
            result.extend(self.comb_filter)
        return result

    # 是否显示组合搜索框
    show_comb_filter = False
    def get_show_comb_filter(self):
        return self.show_comb_filter

    # 7. 排序
    order_by = []
    def get_order_by(self):
        result = []
        result.extend(self.order_by)
        return result

    def __init__(self,model_class,site):
        self.model_class = model_class
        self.site = site

        self.request = None
        self._query_param_key = "_listfilter"
        self.search_key = "_q"

    # ############# URL 相关 ###############
    def wrap(self,view_func):
        def inner(request,*args,**kwargs):
            self.request = request
            return view_func(request,*args,**kwargs)
        return inner
    def get_urls(self):
        app_model_name = (self.model_class._meta.app_label,self.model_class._meta.model_name,)
        url_patterns = [
            url(r'^$',self.wrap(self.changelist_view),name="%s_%s_changlist" %app_model_name),
            url(r'^add/$',self.wrap(self.add_view),name="%s_%s_add" %app_model_name),
            url(r'^(\d+)/delete/$',self.wrap(self.delete_view),name="%s_%s_delete" %app_model_name),
            url(r'^(\d+)/change/$',self.wrap(self.change_view),name="%s_%s_change" %app_model_name),
        ]
        url_patterns.extend(self.extra_url())
        return url_patterns
    def extra_url(self):
        return []

    @property
    def urls(self):
        return self.get_urls()
    def get_change_url(self,nid):
        name = "stark:%s_%s_change" % (self.model_class._meta.app_label, self.model_class._meta.model_name,)
        edit_url = reverse(name, args=(nid,))
        return edit_url
    def get_list_url(self):
        name = "stark:%s_%s_changlist" % (self.model_class._meta.app_label, self.model_class._meta.model_name,)
        edit_url = reverse(name)
        return edit_url
    def get_add_url(self):
        name = "stark:%s_%s_add" % (self.model_class._meta.app_label, self.model_class._meta.model_name,)
        edit_url = reverse(name)
        return edit_url
    def get_delete_url(self,nid):
        name = "stark:%s_%s_delete" % (self.model_class._meta.app_label, self.model_class._meta.model_name,)
        edit_url = reverse(name,args=(nid,))
        return edit_url
    # ############# 处理请求的方法 ################

    def changelist_view(self,request,*args,**kwargs):
        """
        /stark/app01/userinfo/    self.model_class=models.UserInfo
		/stark/app01/role/        self.model_class=models.Role
        :param request:
        :param args:
        :param kwargs:
        :return:
        """

        if request.method == 'POST' and self.get_show_actions():
            func_name_str = request.POST.get('list_action')
            action_func = getattr(self,func_name_str)
            ret = action_func(request)
            if ret:
                return ret

        comb_condition = {}
        option_list = self.get_comb_filter()
        for key in request.GET.keys():
            value_list = request.GET.getlist(key)
            flag = False
            for option in option_list:
                if option.field_name == key:
                    flag = True
                    break

            if flag:
                comb_condition["%s__in" %key] = value_list

        queryset = self.model_class.objects.filter(self.get_search_condition()).filter(**comb_condition).order_by(*self.get_order_by()).distinct()
        # print(queryset) # print(queryset.query) 这里可以看到它生成的sql语句

        cl = ChangeList(self,queryset)  # ChangeList 就是封装列表页面所有功能的
        return render(request,'stark/changelist.html',{'cl':cl})

    def add_view(self,request,*args,**kwargs):
        model_form_class = self.get_model_form_class()
        _popbackid = request.GET.get('_popbackid')
        if request.method == "GET":
            form = model_form_class()
            return render(request,'stark/add_view.html',{'form':form,'config':self})
        else:
            form = model_form_class(request.POST)
            if form.is_valid():
                # 数据库中创建数据
                new_obj = form.save()
                print('new_obj',str(new_obj))
                if _popbackid:
                    # 是popup请求
                    # render一个页面，写自执行函数
                    # popUp('/stark/app01/userinfo/add/?_popbackid=id_consultant&model_name=customer&related_name=consultant')

                    from django.db.models.fields.reverse_related import ManyToOneRel, ManyToManyRel
                    result = {'status':False,'id':None,'text':None,'popbackid':_popbackid}
                    model_name = request.GET.get('model_name')     # 获得当前所在的类名 customer
                    related_name = request.GET.get('related_name') # 获得related_name  consultant                related_name = request.GET.get('related_name') #获得related_name
                    # print(model_name,related_name,new_obj._meta.model_name)   customer consultant userinfo
                    for related_obj in new_obj._meta.related_objects:
                        _model_name = related_obj.model._meta.model_name # 当前增加的表的名称
                        _related_name = related_obj.related_name         # 当前表关联的related_name

                        if type(related_obj) == ManyToOneRel:   # 判断如果是FK的话
                            _field_name = related_obj.field_name # code (to_field) 关联的字段
                        else:
                            _field_name = 'pk'
                        _limit_choices_to = related_obj.limit_choices_to
                        print('471_limit_choices_to',_limit_choices_to)
                        if model_name == _model_name and related_name == str(_related_name):
                            is_exists = self.model_class.objects.filter(**_limit_choices_to,pk=new_obj.id).exists()
                            if is_exists:
                                # 如果是新创建用户是销售部的人, 页面才会显示该新增选项
                                result['status'] = True
                                result['text'] = str(new_obj)
                                result['id'] = getattr(new_obj,_field_name)
                                print(result)
                                return render(request, 'stark/popup_response.html',{'json_result': json.dumps(result, ensure_ascii=False)})
                    # result = {'id':new_obj.pk, 'text':str(new_obj),'popbackid':_popbackid }
                    return render(request,'stark/popup_response.html',{'json_result':json.dumps(result,ensure_ascii=False)})
                else:
                    return redirect(self.get_list_url())
            return render(request, 'stark/add_view.html', {'form': form,'config':self})

    def change_view(self,request,nid,*args,**kwargs):
        # self.model_class.objects.filter(id=nid)
        obj = self.model_class.objects.filter(pk=nid).first()
        if not obj:
            return redirect(self.get_list_url())

        model_form_class = self.get_model_form_class()
        # GET,显示标签+默认值
        if request.method == 'GET':
            form = model_form_class(instance=obj)
            return render(request,'stark/change_view.html',{'form':form,'config':self})
        else:
            form = model_form_class(instance=obj,data=request.POST)
            if form.is_valid():
                form.save()
                list_query_str = request.GET.get(self._query_param_key)
                list_url = "%s?%s" %(self.get_list_url(),list_query_str,)
                return redirect(list_url)
            return render(request, 'stark/change_view.html', {'form': form,'config':self})

    def delete_view(self,request,nid,*args,**kwargs):
        self.model_class.objects.filter(pk=nid).delete()
        return redirect(self.get_list_url())


class StarkSite(object):
    """
    相当于是一个容器，往里面放类，以及处理与另外的类之间的对应关系
    该类主要是用来注册对应关系
            {
                models.UserInfo: StarkConfig(models.UserInfo,self),
                models.Role: StarkConfig(models.Role,self)
            }
    """
    def __init__(self):
        self._registry = {}

    def register(self,model_class,stark_config_class=None):
        if not stark_config_class:
            stark_config_class = StarkConfig
        self._registry[model_class] = stark_config_class(model_class,self)

    def get_urls(self):
        url_pattern = []

        for model_class,stark_config_obj in self._registry.items():
            # 为每一个类，创建4个URL
            """
            {
                models.UserInfo: StarkConfig(models.UserInfo,self),
                models.Role: StarkConfig(models.Role,self)
            }
            /stark/app01/userinfo/
            /stark/app01/userinfo/add/
            /stark/app01/userinfo/(\d+)/change/
            /stark/app01/userinfo/(\d+)/delete/
            """
            app_name = model_class._meta.app_label
            model_name = model_class._meta.model_name

            curd_url = url(r'^%s/%s/' %(app_name,model_name,) , (stark_config_obj.urls,None,None))
            url_pattern.append(curd_url)


        return url_pattern

    @property
    def urls(self):
        return (self.get_urls(),None,'stark')

site = StarkSite()


