import json

from django.conf.urls import url
from django.urls import reverse
from django.utils.safestring import mark_safe
from django.shortcuts import render,HttpResponse,redirect

from app01 import models
from stark.service import v1


class StudentConfig(v1.StarkConfig):



    def display_score(self,obj=None,is_header=False):
        if is_header:
            return '成绩'

    list_display = ['username', 'emergency_contract']