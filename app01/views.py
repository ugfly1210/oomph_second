from django.shortcuts import render,redirect,HttpResponse
from app01 import models
# Create your views here.


from rbac import models
from rbac.service.init_permission import init_permission
def login(request):
    if request.method == 'GET':
        return render(request,'login.html')
    else:
        user = request.POST.get('username')
        pwd = request.POST.get('password')
        user = models.User.objects.filter(username=user, password=pwd).first()
        # print(user.userinfo)
        # print(user.userinfo.name)
        # print(user.userinfo.id)
        # print(user.id)
        if user:
            # 表示已登录
            request.session['user_info'] = {'user_id': user.id, 'uid': user.userinfo.id, 'name': user.userinfo.name}
            # 权限写入session
            init_permission(user, request)
            # 跳转
            return redirect('/index/')

        return render(request, 'login.html')

def index(request):
    return HttpResponse('welcome come back')
