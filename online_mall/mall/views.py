import os

import pymysql
import redis
from django.core.paginator import Paginator
from django.http import HttpResponse
from django.shortcuts import render, redirect
from mall.utill import username_exist,insert_into_mysql


# Create your views here.
conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='123456', db='mall', charset='utf8')

pool = redis.ConnectionPool(host='localhost', port=6379)
r = redis.Redis(connection_pool=pool)
pipe = r.pipeline(transaction=True)

def Check_Login(func):  #自定义登录验证装饰器
    def wrapper(request,*args,**kwargs):
        is_login = request.COOKIES.get('user')
        if is_login:
            return func(request, *args, **kwargs)
        else:
            return redirect("/mall/login/")
    return wrapper




def index(request): #主页
    if request.COOKIES.get('user'):
        temp = request.COOKIES.get('user')
        li = ['law','it','history','literature','philosophy','natural_scirnce']
        info = {'user': {'name':temp},'law':{},'it':{},'history':{},'literature':{},'philosophy':{},'natural_scirnce':{}}
        conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='123456', db='mall', charset='utf8')
        for i in range(0,6):
            cursor = conn.cursor()
            cursor.execute("SELECT books.book_id,books.book_name,books.book_img,books.book_price FROM books ,type_book WHERE books.book_id = type_book.book_id AND type_book.type_id = %d ORDER BY books.book_sell desc LIMIT 4" % (i+1))
            result = cursor.fetchall()
            info[li[i]]['book'] = result
        return render(request,'index.html',context=info)
    else:
        li = ['law', 'it', 'history', 'literature', 'philosophy', 'natural_scirnce']
        info = {'law': {}, 'it': {}, 'history': {}, 'literature': {}, 'philosophy': {}, 'natural_scirnce': {}}
        conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='123456', db='mall', charset='utf8')
        for i in range(0, 6):
            cursor = conn.cursor()
            cursor.execute("SELECT books.book_id,books.book_name,books.book_img,books.book_price FROM books ,type_book WHERE books.book_id = type_book.book_id AND type_book.type_id = %d ORDER BY books.book_sell desc LIMIT 4" % (i + 1))
            result = cursor.fetchall()
            info[li[i]]['book'] = result
        return render(request, 'index.html',context=info)


def login(request): #登录
    if request.method == "GET":
        return render(request, 'login.html')
    else:
        UserName = request.POST.get('username')
        PassWord = request.POST.get('pwd')
        cursor = conn.cursor()
        cursor.execute("select user_name,user_password from user")
        result = cursor.fetchall()
        cursor.close()
        for i in result:
            if UserName == i[0] and PassWord == i[1]:
                response = redirect('/mall/index/'.format(UserName))
                response.set_cookie('user',UserName)
                return response
        else:
            info = {'error':{'prompt':'用户名或密码错误.'}}
            return render(request,'login.html',context=info)


def register(request):  #注册
    if request.method == 'GET':
        return render(request,'register.html')
    else:
        name = request.POST.get("user_name")
        pword1 = request.POST.get('pwd')
        pword2 = request.POST.get('cpwd')

        if len(name) >= 5 and len(name) <= 20:
            if len(pword1) >= 8 and len(pword1) <= 20:
                insert_into_mysql(user_name=name,pass_word=pword1)
                response = redirect('/mall/index/?u={}'.format(name))
                response.set_cookie('user',name)
                return response
            else:
                return render(request, 'register.html')
        else:
            return render(request, 'register.html')

@Check_Login
def user_center_info(request):  #用户中心基本信息
    conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='123456', db='mall', charset='utf8')
    cursor = conn.cursor()
    cursor.execute("select user_money,user_cost from user where user_name='%s'" % (request.COOKIES.get('user')))
    result = cursor.fetchone()
    cursor.close()
    info = {'user':{'name':request.COOKIES.get('user'),'money':result[0],'cost':result[1]}}
    return render(request,'user_center_info.html',context=info)

@Check_Login
def user_center_manager(request): #密码修改
    if request.method == 'GET':
        return render(request, 'user_center_manager.html')
    else:
        old_user_password = request.POST.get('pwd')
        new_user_password = request.POST.get('npwd')
        if old_user_password != None and new_user_password != None and len(new_user_password) >= 8 and len(new_user_password) <=20:
            cursor = conn.cursor()
            cursor.execute("select user_password from user where user_name='%s'" % (request.COOKIES.get('user')))
            result = cursor.fetchone()[0]
            if old_user_password == result:
                cursor.execute("update user set user_password='%s' where user_name='%s'" % (new_user_password,request.COOKIES.get('user')))
                conn.commit()
                cursor.close()
                return redirect('/mall/user_center_manager')
            else:
                return render(request, 'user_center_manager.html')
        else:
            return render(request, 'user_center_manager.html')

@Check_Login
def user_center_order(request):
    conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='123456', db='mall', charset='utf8')
    u_name = request.COOKIES.get('user')
    cursor = conn.cursor()
    cursor.execute("select user_id from user where user_name='%s'" % (u_name))
    u_id = cursor.fetchone()[0]
    cursor.execute("select group_concat('(',p_car_id,',',p_book_id,',',p_book_name,',',p_book_price,',',p_book_img,',',book_number,',',buy_cost,',',buy_time,')' SEPARATOR '*') from purchase where p_user_id=%d group by p_car_id ;" % (u_id))
    result = cursor.fetchall()
    li = []
    for i in result:
        li.append(i)

    for i in range(len(li)):
        li[i] = li[i][0].split('*')
        for j in range(len(li[i])):
            li[i][j] = li[i][j].strip('(').strip(')').split(',')
    print(li)

    sum = 0
    for i in range(len(li)):
        for j in range(len(li[i])):
            sum += int(li[i][j][6])
        li[i][0].append(sum)
        sum = 0

    print(li)
    info = {'order':li,'user':u_name}
    return render(request,'user_center_order.html',context=info)

@Check_Login
def user_center_browse(request):
    conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='123456', db='mall', charset='utf8')
    u_name = request.COOKIES.get('user')
    cursor = conn.cursor()
    cursor.execute("select user_id from user where user_name='%s'" % (u_name))
    u_id = cursor.fetchone()[0]
    cursor.execute("select time,b_book_name from browse where b_user_id=%d" % (u_id))
    result = cursor.fetchall()
    pindex = request.GET.get("pindex")
    pageinator = Paginator(result, 10)
    if pindex == "" or pindex == None:
        pindex = 1
    page = pageinator.page(pindex)
    info = {'browse':result,'page': page}
    return render(request,'user_center_browse.html',context=info)

@Check_Login
def user_change(request):
    if request.method == 'GET':
        user_id = request.GET.get('u_id')
        info = {'id':user_id}
        return render(request,'user_change.html',context=info)
    else:
        user_id = int(request.GET.get('u_id'))
        user_level = int(request.POST.get('level'))
        user_name = request.POST.get('user_name')
        user_password = request.POST.get('pwd')
        user_money = int(request.POST.get('money'))
        user_cost = int(request.POST.get('cost'))
        cursor = conn.cursor()
        cursor.execute("update user set user_level=%d,user_name='%s',user_password='%s',user_money=%d,user_cost=%d where user_id=%d" % (user_level,user_name,user_password,user_money,user_cost,user_id))
        conn.commit()
        return redirect('/mall/web_manage_user')

@Check_Login
def web_manage_user(request):
    conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='123456', db='mall', charset='utf8')
    u_id = request.GET.get('u_id')
    if u_id == None:
        cursor = conn.cursor()
        cursor.execute("select user_id,user_level,user_name,user_money,user_cost from user")
        result = cursor.fetchall()
        info = {'users': result}
        return render(request, 'web_manage_user.html', context=info)
    else:
        cursor = conn.cursor()
        cursor.execute("delete from user where user_id=%d" % (int(u_id)))
        conn.commit()
        return redirect('/mall/web_manage_user')

@Check_Login
def user_add(request):
    if request.method == 'GET':
        return render(request, 'user_add.html')
    else:
        u_level = int(request.POST.get('level'))
        u_name = request.POST.get('user_name')
        u_password = request.POST.get('pwd')
        u_money = int(request.POST.get('money'))
        u_cost = int(request.POST.get('cost'))
        cursor = conn.cursor()
        cursor.execute("insert into user(user_level,user_name,user_password,user_money,user_cost) value (%d,'%s','%s',%d,%d)" % (u_level,u_name,u_password,u_money,u_cost))
        conn.commit()
        return redirect('/mall/web_manage_user')

@Check_Login
def web_manage_goods(request):
    b_id = request.GET.get('b_id')
    if b_id == None:
        cursor = conn.cursor()
        cursor.execute("SELECT books.book_id,books.book_name,books.book_img,books.book_author,type.type_name,books.book_price FROM books ,type ,type_book WHERE books.book_id = type_book.book_id AND type.type_id = type_book.type_id order by books.book_id")
        result = cursor.fetchall()
        info = {'book': result}
        return render(request, 'web_manage_goods.html', context=info)
    else:
        cursor = conn.cursor()
        cursor.execute("delete from type_book where book_id=%d" % (int(b_id)))
        cursor.execute("delete from books where book_id=%d" % (int(b_id)))
        conn.commit()
        return redirect('/mall/web_manage_goods')

@Check_Login
def goods_add(request):
    if request.method == 'GET':
        return render(request, 'goods_add.html')
    else:
        goods_name = request.POST.get('goods_name')
        goods_img = request.POST.get('goods_img')
        author = request.POST.get('author')
        introduce = request.POST.get('introduce')
        goods_type = request.POST.get('goods_type')
        price = float(request.POST.get('price'))
        cursor = conn.cursor()
        cursor.execute("insert into books(book_name,book_author,book_introduce,book_price,book_img) value('%s','%s','%s',%d,'%s')" % (goods_name, author, introduce, price, goods_img))
        conn.commit()
        cursor.execute("select type_id from type where type_name='%s'" % (goods_type))
        result1 = cursor.fetchone()[0]
        cursor.execute("select book_id from books where book_name='%s'" % (goods_name))
        result2 = cursor.fetchone()[0]
        cursor.execute("insert into type_book value (%d,%d)" % (result1, result2))
        conn.commit()
        return redirect('/mall/web_manage_goods')

def cancel(request):
    response = redirect('/mall/index')
    response.set_cookie('user','')
    return response