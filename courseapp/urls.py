from django.urls import path

from courseapp import views
app_name = 'courseapp'


urlpatterns = [
    path('home/', views.home, name='home'),
    # path('addArticle/', views.addArticle, name='addArticle'),
    path('add_article_logic/', views.add_article_logic, name='add_article_logic'),
    path('addCourse/', views.addCourse, name='addCourse'),
    path('modify/', views.modify, name='modify'),
    path('dele/', views.dele, name='dele'),
    path('get_course/', views.get_course, name='get_course'),
    path('addarticle/', views.add_article, name='addarticle'),
    path('get_cate/', views.get_cate, name='get_cate'),
    path('modify_logic/', views.modify_logic, name='modify_logic'),
    path('add_course_logic/', views.add_course_logic, name='add_course_logic'),
    path('python/', views.python, name='python'),
    path('pythonbase/', views.pythonbase, name='pythonbase'),
    # path('index/', views.index, name='index'),
]