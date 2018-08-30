from django.conf.urls import url
from django.contrib import admin
from exam import views as exam_views


urlpatterns = [
    url(r'.*?page', exam_views.show),
    url(r'^test', exam_views.test),
    url(r'^admin/', admin.site.urls),
    url(r'^$', exam_views.home, name='home'),
    url(r'^append', exam_views.append, name='append'),
    url(r'^show', exam_views.show, name='show'),
    url(r'^home', exam_views.home, name="home"),
    url(r'^questiondb', exam_views.questiondb, name="questiondb"),
    # url(r'.*?subject', exam_views.show, name="show_qdb"),
    url(r'^teacher_home', exam_views.teacher_home, name="teacher_home"),
    url(r'^admin_center', exam_views.admin_center, name="admin_center"),
]
