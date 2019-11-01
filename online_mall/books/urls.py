from django.urls import path

from books.views import list_law, list_it, detail, list_history, list_literature, list_philosophy, list_natural_science, \
    detail_message, list_search

urlpatterns = [
    path('list_law/',list_law,name='list_law'),
    path('list_it/',list_it,name='list_it'),
    path('list_history/',list_history,name='list_history'),
    path('list_literature/', list_literature, name='list_literature'),
    path('list_philosophy/', list_philosophy, name='list_philosophy'),
    path('list_natural_science/', list_natural_science, name='list_natural_science'),
    path('detail/',detail,name='detail'),
    path('detail_message/', detail_message, name='detail_message'),
    path('list_search/', list_search, name='list_search'),
]