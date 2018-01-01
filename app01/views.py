from django.shortcuts import render
from app01 import models
# Create your views here.

# def login(request):
#     if request.method == 'GET':
#         return render(request,'login.html')


# def (request):
#     a = models.UserInfo._meta.get_field('name')
#     # app01.UserInfo.name
#     b = models.UserInfo._meta.fields
#     # (<django.db.models.fields.AutoField: id>,
#     # <django.db.models.fields.CharField: name>,
#     # <django.db.models.fields.CharField: username>,
#     # <django.db.models.fields.CharField: password>,
#     # <django.db.models.fields.EmailField: email>,
#     # <django.db.models.fields.related.ForeignKey: depart>)
#     c = models.UserInfo._meta._get_fields()
#     # (< ManyToOneRel: app01.classlist >,
#     # < ManyToManyRel: app01.classlist >,
#     # < ManyToOneRel: app01.customer >,
#     # < ManyToOneRel: app01.customerdistribution >,
#     # < ManyToOneRel: app01.salerank >,
#     # < ManyToOneRel: app01.consultrecord >,
#     # < ManyToOneRel: app01.paymentrecord >,
#     # < ManyToOneRel: app01.courserecord >,
#     # < django.db.models.fields.AutoField: id >,
#     # < django.db.models.fields.CharField: name >,
#     # < django.db.models.fields.CharField: username >,
#     # < django.db.models.fields.CharField: password >,
#     # < django.db.models.fields.EmailField: email >,
#     # < django.db.models.fields.related.ForeignKey: depart >)
#     d = models.UserInfo._meta.many_to_many # ()
