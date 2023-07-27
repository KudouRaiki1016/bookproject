from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView

from . import views

app_name = 'accounts'

urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('signup/', views.SignupView.as_view(), name='signup'),
    path('signupview/', views.signup_view, name='signup-view'),
    path('class/', views.class_view, name='class-list'),
    path('class/<int:class_id>/detail/', views.class_detail_view, name='class-detail'),
    path('class/<int:class_pk>/add/', views.class_member_add_view, name='add-class-members'),
    path('class/<int:class_pk>/delete/', views.class_member_delete_view, name='delete-class-members'),
]