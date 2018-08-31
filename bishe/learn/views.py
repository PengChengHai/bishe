from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from learn import models
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from exam import views as exam_views
import time


def home(request):  # 首页
    return render(request, 'home.html')


def append(request):  # 添加用户
    try:
        user_name = request.session['user']
        return render(request, 'append.html', {'user': user_name})
    except:
        return redirect('/home')


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
    try:
        subject = request.GET['subject']
        if subject == '':
            subject = request.session.get('subject')
            print(subject)
        request.session['subject'] = subject
    except:
        subject = request.session.get('subject')
        print(subject)
    question = models.Question.objects.filter(Q_subject=subject)
    paginator = Paginator(question, 5)
    page = request.GET.get('page', 1)
    try:
        contacts = paginator.page(page)
    except PageNotAnInteger:
        contacts = paginator.page(1)
    except EmptyPage:
        contacts = pageinator.page(paginator.num_pages)
    return render(request, 'show.html', {'contacts': contacts})
    # return HttpResponse('题库')


def questiondb(request):  # 选择题库类型
    try:
        if request.GET['page']:
            return show(request)
    except:
        try:
            if request.GET['subject']:
                return show(request)
        except:
            return render(request, 'questiondb.html')


# def teacher_home(request):
#     return render(request, 'teacher_home.html')


def admin_center(request):
    User = models.User.objects.all()
    # print(User[0].stu_id)
    return render(request, 'admin_center.html', {"User": User})
