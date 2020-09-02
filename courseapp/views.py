from django.core.paginator import Paginator
from django.db import transaction
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect

# Create your views here.

from courseapp.models import Course, Article


def home(request):
    # course = Course.objects.filter(level=1)
    status = request.GET.get('sta')
    if status == '1':
        article = Article.objects.all().order_by('-reading')
    elif status == '2':
        article = Article.objects.all().order_by('-issue_time')
    else:
        article = Article.objects.all().order_by("issue_time") # 全部文章
    if article:
        course = Course.objects.filter(level=1)
        cate = Course.objects.filter(level=2)
        pagenator = Paginator(article,per_page=5)
        num = request.session.get('number')
        number = request.GET.get('num')
        if not number:
            number = 1
            if num:
                number = int(num)
        page = pagenator.page(number)
        return render(request, 'course/home.html',{'page':page,'article':article,'course':course,'cate':cate})
    return render(request, 'course/home.html', {'page': []})


#*  加文章 django传值得到的课程信息
def add_article(request):
    courses = Course.objects.filter(level=1)
    return render(request,'course/addArticle.html', {'courses': courses})


#*  加文章逻辑
def add_article_logic(request):
    name = request.POST.get('name')
    cate = request.POST.get('cate_sel') # 所属课程分类id
    text = request.POST.get('text')
    # artime = request.POST.get('time')
    print(name, cate, text,)
    try:
        print(111)
        with transaction.atomic():
            cate = Course.objects.get(id=int(cate))
            ar = Article.objects.create(name=name, content=text,cate=cate) #issue_time=artime,
            print(ar)
            return HttpResponse('1')
    except:
        return HttpResponse('0')


# 加课程/分类
def addCourse(request):
    return render(request, 'course/addCourse.html')

# 加课程/分类 逻辑
def add_course_logic(request):
    c_name = request.POST.get('c_name') # 要添加的名称
    name2 = request.POST.get('cate_sel') # 课程名称
    boo = request.POST.get('boo')
    print(boo, c_name, name2)
    try:
        if boo == "2":
            c1 = Course.objects.filter(name=name2) # 获取到的课程对象
            if c1:
                if Course.objects.create(name=c_name,level=2,parent_id=c1[0].id):
                    return JsonResponse({'msg': "添加成功","status":1})
        elif boo == '1':
            if Course.objects.create(name = c_name,level=1):
                return JsonResponse({'msg': "添加成功", "status": 1})
        else:
            return JsonResponse({'msg': "添加失败", "status": 0})
    except:
        return JsonResponse({'msg': "添加失败", "status": 0})



# # 获得一级课程数据
def get_course(request):
    course = Course.objects.filter(level=1) # 得到课程
    def mydefault(c):
        if isinstance(c, Course):
            return {"id": c.id, 'name': c.name}
    return JsonResponse(list(course),safe=False,json_dumps_params={'default':mydefault})

#* 获得二级课程数据
def get_cate(request):
    coursename = request.GET.get('coursename')
    c1 = Course.objects.get(name=coursename)# 获取到该课程对象
    print(c1)
    cates = Course.objects.filter(parent_id=c1.id)# 获取到该课程下的所有的二级分类
    print(cates)
    def mydefault(c):
        if isinstance(c,Course):
            return {'id': c.id, 'name':c.name}
    return JsonResponse(list(cates),safe=False,json_dumps_params={'default':mydefault})
    # 非字典就要设置成safe = False

# 修改文章

def modify(request):
    id = request.GET.get('id')
    article = Article.objects.get(id=id)
    course = Course.objects.filter(level=1)
    cate = Course.objects.filter(level=2)
    c2 = Course.objects.get(article=id)
    c1 = Course.objects.get(pk=c2.parent_id)# 获得课程
    c22 = Course.objects.filter(parent_id=c1.id)
    return render(request,'course/modify.html',{'article':article, 'course':course, 'cate':cate,'c1':c1,'c22':c22})


# 修改文章逻辑
def modify_logic(request):
    id = request.POST.get('id')
    article = request.POST.get('article')
    date = request.POST.get('date')
    content = request.POST.get('content')
    two_id = request.POST.get('two_cour')# 获得的是类的id
    rst = Course.objects.filter(article=id)# article__id =      原类
    print(rst,'闫')
    print(id,article,date,content,two_id)
    try:
        with transaction.atomic():
            art = Article.objects.get(id=id)
            art.name = article
            art.cate_id= two_id
            art.content = content
            art.save()
            return JsonResponse({'msg': '修改成功', 'status': 1})
    except:
        return JsonResponse({'msg': '修改失败', 'status': 0})


# 删除
def dele(request):
    id = request.GET.get('id')
    num = request.GET.get('num')
    art = Article.objects.filter(id=id)
    art[0].delete()
    request.session['number'] = num
    return redirect('courseapp:home')

def python(request):
    id = request.GET.get('id')
    c1 = Course.objects.filter(level=1)
    c2 = Course.objects.filter(level=2)
    num = request.GET.get('num')
    course = Course.objects.filter(id=id)
    cate = Course.objects.filter(parent=id)
    article = Article.objects.none()
    for i in course:
        rst = Article.objects.filter(course = i.id)
        article = article | rst
        pg = Paginator(article,per_page=5)
        if num is None:
            num = 1
        page = pg.page(int(num))
        return render(request, 'course/home.html', {'page':page,'course': course, 'cate': cate})



def pythonbase(request):
    id = request.GET.get('id')
    course = Course.objects.filter(level=1)
    cate = Course.objects.filter(level=2)
    num = request.GET.get('num')
    c2 = Course.objects.filter(id=id)
    article = Article.objects.filter(cate=id)
    pg = Paginator(article,per_page=5)
    print(id,course)
    if num is None:
        num = 1
    page = pg.page(int(num))
    return render(request, 'course/home.html', {'page': page, 'course': course, 'cate': cate})




