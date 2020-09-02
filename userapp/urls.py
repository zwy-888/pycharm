from django.urls import path

from userapp import views
app_name = 'userapp'
urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),
    path('login_logic/', views.login_logic, name='login_logic'),
    path('getcaptcha/', views.getcaptcha, name='getcaptcha'),
    path('check_name/', views.check_name, name='check_name'),
    path('register_logic/', views.register_logic, name='register_logic'),
    path('loginout/', views.loginout, name='loginout'),
    path('forget_pwd/', views.forget_pwd, name='forget_pwd'),
    path('forget_logic/', views.forget_logic, name='forget_logic'),
    path('active/', views.active, name='active'),
    # path('reactive/', views.reactive, name='reactive'),
    path('reset_pwd/', views.reset_pwd, name='reset_pwd'),
    path('reset_logic/', views.reset_logic, name='reset_logic'),
]