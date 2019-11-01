import time

import pymysql
from django.core.paginator import Paginator
from django.shortcuts import render, redirect

# Create your views here.
from mall.views import Check_Login

conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='123456', db='mall', charset='utf8')


def list_law(request):
    cursor = conn.cursor()
    cursor.execute("SELECT books.book_name,books.book_img,book_price,books.book_id FROM books ,type_book WHERE books.book_id = type_book.book_id AND type_book.type_id = 1 ORDER BY books.book_id DESC ")
    result = cursor.fetchall()
    users = result
    pindex = request.GET.get("pindex")
    pageinator = Paginator(users, 10)
    if pindex == "" or pindex == None:
        pindex = 1
    page = pageinator.page(pindex)
    info = {'books':result,'page':page}
    return render(request,'list_law.html',context=info)

def list_it(request):
    cursor = conn.cursor()
    cursor.execute("SELECT books.book_name,books.book_img,book_price,books.book_id FROM books ,type_book WHERE books.book_id = type_book.book_id AND type_book.type_id = 2 ORDER BY books.book_id DESC ")
    result = cursor.fetchall()
    users = result
    pindex = request.GET.get("pindex")
    pageinator = Paginator(users, 10)
    if pindex == "" or pindex == None:
        pindex = 1
    page = pageinator.page(pindex)
    info = {'books': result, 'page': page}
    return render(request,'list_it.html',context=info)

def list_history(request):
    cursor = conn.cursor()
    cursor.execute("SELECT books.book_name,books.book_img,book_price,books.book_id FROM books ,type_book WHERE books.book_id = type_book.book_id AND type_book.type_id = 3 ORDER BY books.book_id DESC ")
    result = cursor.fetchall()
    users = result
    pindex = request.GET.get("pindex")
    pageinator = Paginator(users, 10)
    if pindex == "" or pindex == None:
        pindex = 1
    page = pageinator.page(pindex)
    info = {'books': result, 'page': page}
    return render(request,'list_history.html',context=info)

def list_literature(request):
    cursor = conn.cursor()
    cursor.execute("SELECT books.book_name,books.book_img,book_price,books.book_id FROM books ,type_book WHERE books.book_id = type_book.book_id AND type_book.type_id = 4 ORDER BY books.book_id DESC ")
    result = cursor.fetchall()
    users = result
    pindex = request.GET.get("pindex")
    pageinator = Paginator(users, 10)
    if pindex == "" or pindex == None:
        pindex = 1
    page = pageinator.page(pindex)
    info = {'books': result, 'page': page}
    return render(request,'list_literature.html',context=info)

def list_philosophy(request):
    cursor = conn.cursor()
    cursor.execute("SELECT books.book_name,books.book_img,book_price,books.book_id FROM books ,type_book WHERE books.book_id = type_book.book_id AND type_book.type_id = 5 ORDER BY books.book_id DESC ")
    result = cursor.fetchall()
    users = result
    pindex = request.GET.get("pindex")
    pageinator = Paginator(users, 10)
    if pindex == "" or pindex == None:
        pindex = 1
    page = pageinator.page(pindex)
    info = {'books': result, 'page': page}
    return render(request,'list_philosophy.html',context=info)

def list_natural_science(request):
    cursor = conn.cursor()
    cursor.execute("SELECT books.book_name,books.book_img,book_price,books.book_id FROM books ,type_book WHERE books.book_id = type_book.book_id AND type_book.type_id = 6 ORDER BY books.book_id DESC ")
    result = cursor.fetchall()
    users = result
    pindex = request.GET.get("pindex")
    pageinator = Paginator(users, 10)
    if pindex == "" or pindex == None:
        pindex = 1
    page = pageinator.page(pindex)
    info = {'books': result, 'page': page}
    return render(request,'list_natural_science.html',context=info)

def detail(request):
    book_id = int(request.GET.get('b_id'))
    u_name = request.COOKIES.get('user')
    cursor = conn.cursor()
    cursor.execute("select user_id from user where user_name='%s'" % (u_name))
    result = cursor.fetchone()
    print(result)
    if result is not None:
        result = result[0]
        cursor.execute("select book_name from books where book_id=%d" % (book_id))
        b_name = cursor.fetchone()[0]
        cursor.execute("insert into browse value(%d,%d,'%s','%s')" % (result, book_id, b_name, time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())))
        conn.commit()

    cursor.execute("SELECT books.book_name,books.book_img,book_introduce,books.book_id FROM books ,type_book WHERE books.book_id = type_book.book_id AND books.book_id = %d" % (book_id))
    result = cursor.fetchone()
    info = {'book':result}
    return render(request,'detail.html',context=info)

@Check_Login
def detail_message(request):
    if request.method == 'GET':
        book_id = int(request.GET.get('b_id'))
        cursor = conn.cursor()
        cursor.execute("SELECT books.book_name,books.book_img,book_introduce,books.book_id FROM books ,type_book WHERE books.book_id = type_book.book_id AND books.book_id = %d" % (book_id))
        result = cursor.fetchone()
        info = {'book':result}
        cursor.execute(("select user_name,content from message where m_book_id=%d" % (book_id)))
        temp = cursor.fetchall()
        info['message'] = temp
        return render(request,'detail_message.html',context=info)
    else:
        u_message = request.POST.get('message')
        book_id = int(request.GET.get('b_id'))
        u_name = request.COOKIES.get('user')
        cursor = conn.cursor()
        cursor.execute("insert into message(user_name,m_book_id,content) value ('%s',%d,'%s')" % (u_name,book_id,u_message))
        conn.commit()
        return redirect('/books/detail_message/?b_id='+str(book_id))

def list_search(request):
    search_list = list(request.POST.get('search_book'))
    search_keys = "%"
    for i in search_list:
        search_keys += "{}%".format(i)
    print(search_keys)
    cursor = conn.cursor()
    cursor.execute("SELECT books.book_name,books.book_img,book_price FROM books ,type_book WHERE books.book_id = type_book.book_id AND books.book_name like '{}' ORDER BY books.book_id DESC ".format(search_keys))
    result = cursor.fetchall()
    users = result
    pindex = request.GET.get("pindex")
    pageinator = Paginator(users, 10)
    if pindex == "" or pindex == None:
        pindex = 1
    page = pageinator.page(pindex)
    info = {'books': result, 'page': page}
    return render(request,'list_search.html',context=info)