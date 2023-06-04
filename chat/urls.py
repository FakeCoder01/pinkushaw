from django.urls import path
from . import views

urlpatterns = [
    path('', views.all_user_chat, name="user_chat_all"),
    path('<str:match_id>/older/', views.older_message, name="older_message"),
]