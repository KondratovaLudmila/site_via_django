from django.urls import path

from . import views

app_name = 'quotesapp'

urlpatterns = [
    path('', views.main, name='main'),
    path("<int:page>", views.main, name='main_paginate'),
    path('tag/', views.tag, name='tag'),
    path('author/', views.author, name='author'),
    path('quote', views.quote, name = 'quote'),
    path('author_detail/<int:author_id>', views.author_detail, name='author_detail'),
    path('by_tag/<int:tag_id>', views.quotes_by_tag, name='by_tag'),
    path('by_tag/<int:tag_id>/<int:page>', views.quotes_by_tag, name='by_tag_paginate'),
    path('load_data', views.load_data, name='load_data'),
    path('load_check', views.load_check, name='load_check'),
]