from django.urls import path
from . import views

urlpatterns = [
    path('', views.index_view, name='index'),
    path('book/', views.ListBookView.as_view(), name='list-book'),
    path('book/<int:pk>/detail/', views.DetailBookView.as_view(), name='detail-book'),
    path('book/create/', views.CreateBookView.as_view(), name='create-book'),
    path('book/<int:pk>/delete/', views.DeleteBookView.as_view(), name='delete-book'),
    path('book/<int:pk>/update/', views.UpdateBookView.as_view(), name='update-book'),
    path('book/<int:book_id>/review/', views.CreateReviewView.as_view(), name='review'),
    path('savebook/', views.savebook_list_view, name='list-savebook'),
    path('savebook/append/', views.savebook_append, name='append-savebook'),
    path('savebook/orderchange/', views.savebook_orderchange_view, name='orderchange-savebook'),
    path('savebook/delete/', views.bookorder_delete, name='delete-savebook'),
    path('like_for_book/', views.like_for_book, name='like_for_book'), 
]