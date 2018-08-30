from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from learn import models
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import time


def home(request):  # 首页
    return render(request, 'home.html')


def append(request):  # 添加用户
    return render(request, 'append.html')


@csrf_exempt  # 增加用户
def test(request):
    uname = str(request.POST['uname'])
    pwd = request.POST['upwd']
    stu_id = request.POST['stu_id']
    try:
        models.User.objects.create(stu_id=stu_id, user_name=uname, pwd=pwd)
        return HttpResponse('OK')
    except:
        return HttpResponse('学生添加失败')


def show(request):  # 题库
    subject = str(request.GET['subject'])
    question = models.Question.objects.filter(Q_subject=subject)
    return render(request, 'show.html', {'question': question})
    # return HttpResponse('题库')


def questiondb(request):  # 选择题库类型
    try:
        if request.GET['subject']:
            return show(request)
    except:
        return render(request, 'questiondb.html')


def teacher_home(request):
    return render(request, 'teacher_home.html')


def admin_center(request):
    User = models.User.objects.all()
    # print(User[0].stu_id)
    return render(request, 'admin_center.html', {"User": User})
