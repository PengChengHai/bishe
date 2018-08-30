from django.conf.urls import url
from django.contrib import admin
from learn import views as learn_views
from exam import views as exam_views

urlpatterns = [
    url(r'.*?page', learn_views.show),
    url(r'^test', learn_views.test),
    url(r'^admin/', admin.site.urls),
    url(r'^$', learn_views.home, name='home'),
    url(r'^append', learn_views.append, name='append'),
    url(r'^show', learn_views.show, name='show'),
    # url(r'^home', learn_views.home, name="home"),
    url(r'^questiondb', learn_views.questiondb, name="questiondb"),
    # url(r'.*?subject', learn_views.show, name="show_qdb"),
    url(r'^admin_center', learn_views.admin_center, name="admin_center"),
    # url(r'^admin/', admin.site.urls),
    url(r'^home/$',exam_views.home_html),
    url(r'^login/$', exam_views.login_html),
    url(r'^login_go/$', exam_views.login),
    url(r'^login_out/$', exam_views.login_out),
    url(r'^apply_test/$', exam_views.apply),
    url(r'^apply/$', exam_views.apply_html),
    url(r'^user_home/$', exam_views.user_home),
    url(r'^login_out/$', exam_views.login_out),
    url(r'^chg_pwd/$', exam_views.change_password),
    url(r'^user_center/$', exam_views.user_center),
    url(r'^user_score/$', exam_views.user_score),
    url(r'^exam_online/$', exam_views.exam_html),
    url(r'^exam_start/$', exam_views.exam_start),
    url(r'^exam_over/$', exam_views.exam_over),
]
