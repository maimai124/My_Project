from django.urls import path

from cart.views import my_cart, add_to_cart, book_add, book_minus, book_delete, place_order, add_to_order, add_to_cart2

urlpatterns = [
    path('my_cart/',my_cart,name='my_cart'),
    path('add_to_cart/',add_to_cart,name='add_to_cart'),
    path('book_add/',book_add,name='book_add'),
    path('book_minus/',book_minus,name='book_minus'),
    path('book_delete/',book_delete,name='book_delete'),
    path('place_order/',place_order,name='place_order'),
    path('add_to_order/',add_to_order,name='add_to_order'),
    path('add_to_cart2/',add_to_cart2,name='add_to_cart2'),
]