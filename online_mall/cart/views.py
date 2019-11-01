import pymysql
from django.shortcuts import render, redirect
import redis,time

from mall.views import Check_Login

conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='123456', db='mall', charset='utf8')

pool = redis.ConnectionPool(host='localhost', port=6379)
r = redis.Redis(connection_pool=pool)
pipe = r.pipeline(transaction=True)

# Create your views here.
@Check_Login
def my_cart(request):
    u_name = request.COOKIES.get('user')
    li = r.lrange(u_name,0,-1)
    info = {'user':u_name,'cart':[],'count':len(li),'money':0}
    for i in li:
        i = eval(i)
        i['sum'] = str(float(i['price'].strip('.00'))*i['number'])
        info['cart'].append(i)
        info['money'] += float(i['sum'])
    return render(request,'cart.html',context=info)

@Check_Login
def add_to_cart(request):
    b_id = request.GET.get('b_id')
    print(b_id,type(b_id))
    u_name = request.COOKIES.get('user')
    cursor = conn.cursor()
    cursor.execute("select max(p_car_id) from purchase")
    max_car_id = cursor.fetchone()[0]
    if max_car_id == None:
        max_car_id = str(0)
    else:
        max_car_id = str(int(max_car_id)+1)
    cursor.execute("select user_id from user where user_name='%s'" % (u_name))
    u_id = cursor.fetchone()[0]
    cursor.execute("select book_name from books where book_id=%d" % (int(b_id)))
    b_name = cursor.fetchone()[0]
    cursor.execute("select book_price from books where book_id=%d" % (int(b_id)))
    b_price = str(cursor.fetchone()[0])
    cursor.execute("select book_img from books where book_id=%d" % (int(b_id)))
    b_img = cursor.fetchone()[0]
    r.rpush(u_name,str({'cart_id':max_car_id,'user_id':u_id,'book_id':b_id,'book_name':b_name,'number':1,'price':b_price,'b_img':b_img,'time':time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())}))
    cursor.execute("select type_id from type_book where book_id=%d" % (int(b_id)))
    b_type = cursor.fetchone()[0]
    print(b_type)
    if b_type == 1:
        b_type = 'list_law'
    elif b_type == 2:
        b_type = 'list_it'
    elif b_type == 3:
        b_type = 'list_history'
    elif b_type == 4:
        b_type = 'list_literature'
    elif b_type == 5:
        b_type = 'list_philosophy'
    elif b_type == 6:
        b_type = 'list_natural_science'
    return redirect('/books/'+b_type)

@Check_Login
def book_add(request):
    u_name = request.COOKIES.get('user')
    b_id = request.GET.get('b_id')
    li = r.lrange(u_name,0,-1)
    for i in range(len(li)):
        li[i] = eval(li[i])
        if li[i]['book_id'] == b_id:
            li[i]['number'] += 1
    r.delete(u_name)
    for i in li:
        r.rpush(u_name,str(i))
    return redirect('/cart/my_cart/')

@Check_Login
def book_minus(request):
    u_name = request.COOKIES.get('user')
    b_id = request.GET.get('b_id')
    li = r.lrange(u_name,0,-1)
    for i in range(len(li)):
        li[i] = eval(li[i])
        if li[i]['book_id'] == b_id:
            li[i]['number'] -= 1
    r.delete(u_name)
    for i in li:
        r.rpush(u_name,str(i))
    return redirect('/cart/my_cart/')

@Check_Login
def book_delete(request):
    u_name = request.COOKIES.get('user')
    b_id = request.GET.get('b_id')
    li = r.lrange(u_name,0,-1)
    for i in range(len(li)):
        li[i] = eval(li[i])

    for i in li:
        if i['book_id'] == b_id:
            li.remove(i)

    r.delete(u_name)
    for i in li:
        r.rpush(u_name,str(i))
    return redirect('/cart/my_cart/')

@Check_Login
def place_order(request):
    u_name = request.COOKIES.get('user')
    li = r.lrange(u_name,0,-1)
    info = {'user':u_name,'cart':[],'count':len(li),'money':0}
    for i in li:
        i = eval(i)
        i['sum'] = str(int(i['price'].strip('.00'))*i['number'])+'.00'
        info['cart'].append(i)
        info['money'] += int(i['sum'].strip('.00'))
        info['final'] = info['money']+10
    return render(request,'place_order.html',context=info)

@Check_Login
def add_to_order(request):
    u_name = request.COOKIES.get('user')
    li = r.lrange(u_name,0,-1)
    info = {'user': u_name, 'cart': [], 'count': len(li), 'money': 0}
    cursor = conn.cursor()
    for i in li:
        i = eval(i)
        i['sum'] = str(int(i['price'].strip('.00')) * i['number']) + '.00'
        info['cart'].append(i)
        info['money'] += int(i['sum'].strip('.00'))
        info['final'] = info['money'] + 10
        cursor.execute("insert into purchase(p_car_id,p_user_id,p_book_id,p_book_name,p_book_price,p_book_img,book_number,buy_cost,buy_time) value(%d,%d,%d,'%s',%d,'%s',%d,%d,'%s')" % (int(i['cart_id']),int(i['user_id']),int(i['book_id']),i['book_name'],int(i['price'].strip('.00')),i['b_img'],i['number'],int(i['sum'].strip('.00')),i['time']))
        conn.commit()
        cursor.execute("select user_money from user where user_id='%s'" % (i['user_id']))
        result = cursor.fetchone()[0]
        cursor.execute("update user set user_money=%d where user_id='%s'" % (result-int(i['sum'].strip('.00')),i['user_id']))
        conn.commit()
        cursor.execute("select book_sell from books where book_id=%d" % (int(i['book_id'])))
        result = int(cursor.fetchone()[0])
        sell = result + i['number']
        cursor.execute("update books set book_sell=%d where book_id='%s'" % (sell,i['book_id']))
        conn.commit()

    cursor.execute("select user_money from user where user_id='%s'" % (i['user_id']))
    result = cursor.fetchone()[0]
    cursor.execute("update user set user_money=%d where user_id='%s'" % (result - 10, i['user_id']))
    conn.commit()
    r.delete(u_name)

    return render(request, 'final_order.html', context=info)


@Check_Login
def add_to_cart2(request):
    b_id = request.GET.get('b_id')
    print(b_id,type(b_id))
    u_name = request.COOKIES.get('user')
    cursor = conn.cursor()
    cursor.execute("select max(p_car_id) from purchase")
    max_car_id = cursor.fetchone()[0]
    if max_car_id == None:
        max_car_id = str(0)
    else:
        max_car_id = str(int(max_car_id)+1)
    cursor.execute("select user_id from user where user_name='%s'" % (u_name))
    u_id = cursor.fetchone()[0]
    cursor.execute("select book_name from books where book_id=%d" % (int(b_id)))
    b_name = cursor.fetchone()[0]
    cursor.execute("select book_price from books where book_id=%d" % (int(b_id)))
    b_price = str(cursor.fetchone()[0])
    cursor.execute("select book_img from books where book_id=%d" % (int(b_id)))
    b_img = cursor.fetchone()[0]
    r.rpush(u_name,str({'cart_id':max_car_id,'user_id':u_id,'book_id':b_id,'book_name':b_name,'number':1,'price':b_price,'b_img':b_img,'time':time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())}))
    return redirect('/books/detail/?b_id='+b_id)