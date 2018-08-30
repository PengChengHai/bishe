# _*_ coding:utf-8 _*_
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from learn.models import User, Question, Collection, Visit
from exam.models import exam_status, score
import time
import random


# Create your views here.
####
# session所有存入数据表单:
# user:用户id
# exam_title:考试科目
# t_bank:考试试卷题号
# timeout:超时检测计时

####


# 首页页面
def home_html(request):
    try:
        user_login = request.session['user']
        print(user_login)
        return render(request, 'home.html', {'user': user_login})
    except:
        print('not_login')
        return render(request, 'home.html', {'user': 'not_login'})


# 登录页面
def login_html(request):
    return render(request, 'login.html')

# 学生用户中心页面


def stu_home(request):
    return render(request, 'stu_home.html')


# 学生/管理员登录
@csrf_exempt
def login(request):
    if request.method == 'GET':
        return render(request, 'login.html')
    else:
        uname = request.POST.get('uname')
        print(uname)
        pwd = request.POST.get('pwd')
        if len(uname) == 13:
            print('学生登录')
            find_user = User.objects.filter(stu_id=uname)
            print(find_user)
            if len(find_user) > 0:
                if find_user[0].pwd == pwd:
                    request.session['user'] = uname
                    # return render(request,'student.html')
                    return redirect('/home/')
                else:
                    error = '密码错误'
                    return render(request, 'login.html', {'error': error})

            else:
                error = '没有该学生信息'
                return render(request, 'login.html', {'error': error})
        else:
            find_user = User.objects.filter(stu_id=uname)
            if len(find_user) > 0:
                if find_user[0].pwd == pwd:
                    request.session['user'] = uname
                    return render(request, 'teacher_home.html', {'user': uname})
            else:
                error = '用户名或密码错误'
                return render(request, 'login.html', {'error': error})

# 登出


def login_out(request):
    # reset(request)
    request.session.flush()
    return redirect('/home/')


# 测试阶段注册用
def apply_html(request):
    return render(request, 'apply_test.html')


@csrf_exempt
def apply(request):
    stu_id = request.POST["s_id"]
    name = request.POST["name"]
    pwd = request.POST['pwd']

    print(stu_id, name, pwd)

    client = User()
    client.stu_id = stu_id
    client.user_name = name
    client.pwd = pwd
    client.save()

    return redirect('/login/')

# 个人中心页面/管理员页面


def user_home(request):
    try:
        user_id = request.session['user']
        if len(user_id) == 13:
            return render(request, 'stu_home.html')
        else:
            return render(request, 'teacher_home.html', {'user': user_id})
    except:
        redirect('/login/')


# 修改密码
@csrf_exempt
def change_password(request):
    chg_pwd = request.POST['pwd']
    print(chg_pwd)
    user_id = request.session['user']
    user_info = User.objects.get(stu_id=user_id)
    user_info.pwd = chg_pwd
    user_info.save()
    print(user_info.pwd)
    return redirect('/user_home/')


# 用户中心内部页面
# 个人中心
def user_center(request):
    user_id = request.session['user']
    user_info = User.objects.get(stu_id=user_id)
    stu = user_info
    # print(stu)
    return render(request, 'user_center.html', {'stu': stu})

# 历史成绩


def user_score(request):
    user_id = request.session['user']
    all_score = score.objects.filter(stu_id=user_id)

    return render(request, 'user_score.html', {'history': all_score})

# 历史错题


# 收藏夹


# 在线考试跳转页面
def exam_html(request):
    try:
        user_id = request.session['user']
    except:
        return redirect('/login/')
    status = exam_status.objects.filter(status='1')
    stu = User.objects.get(stu_id=user_id)
    if len(status) > 0:
        return render(request, 'exam_online.html', {'title': status, 'stu': stu})
    else:
        return render(request, 'Not_yet_open.html')


# 在线考试开始页面
def exam_start(request):
    # 防止开考时间刷新
    try:
        t_try = request.session['timeout']
    except:
        request.session['timeout'] = time.time()
    # 判断是否登录
    try:
        user_info = request.session['user']
    except:
        return redirect('/login/')
    sub = request.GET['s_subject']  # 接收考试科目
    # 防止题目刷新
    try:
        t_bank = request.session['t_bank']
        some = []
        for b in t_bank:
            someone = Question.objects.get(Q_id=b)
            some.append(someone)
        print(some)
    except:
        status = exam_status.objects.filter(subject=sub).filter(status='1')
        t_count = int(status[0].count)
        t_bank = Question.objects.filter(Q_subject=sub)
        some = random.sample(t_bank, t_count)
        l = []
        for a in some:
            p = a.Q_id
            l.append(p)
        print(l)
        request.session['t_bank'] = l
        request.session['exam_title'] = status[0].title
    print(user_info, '开始考试,开始时间:', request.session['timeout'])
    return render(request, 'exam_start.html', {'exam': some})


# 试卷提交处理
def exam_over(request):
    try:
        subject = request.session['exam_title']
    except:
        # reset()
        request.session.flush()
        return redirect('/login/')
    status = exam_status.objects.get(title=subject)
    print('开始处理')
    # 超时检测
    start = request.session['timeout']
    use_time = time.time() - start
    print(use_time, status.duration)
    if use_time > int(status.duration):
        result = '试卷提交已超时，或考试存在异常'
        exam_re = '考试行为疑似异常'
    else:
        result = '试卷提交成功，本次考试结束'
        exam_re = 'ok'
    # 分数处理
    print('开始计算')
    count = int(status.count)
    one = 100 / count
    t_bank = request.session['t_bank']
    stu_score = 0
    for c in t_bank:
        go = str(c)
        try:
            anw = request.GET[go]
        except:
            continue
        key = Question.objects.get(Q_id=go)
        x, y = str(key.q_key), str(anw)
        if x == y:
            stu_score += one
    # try:
    print('开始录入')
    user_id = request.session['user']
    stu_result = score()
    stu_result.stu_id = user_id
    stu_result.title = subject
    stu_result.count = stu_score
    stu_result.result = exam_re
    stu_result.save()
    request.session.flush()
    request.session['user'] = user_id
    return render(request, 'exam_over.html', {'result': result})


# #重置session
# def reset(request):
#     # del request.session['t_bank']
#     # del request.session['exam_title']
#     # del request.session['timeout']
#     request.session.flush()
