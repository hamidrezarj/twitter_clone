from django.urls import path
from . import views

app_name = 'tweets'

urlpatterns = [
    path('', views.index, name='index'),
    path('ajax/like/', views.like_unlike_view, name='like_view'),
    path('register/', views.register_view, name='register'),
    path('post/', views.post, name='post'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('user/<username>/', views.profile_view, name='profile'),
    path('hashtag/<hashtag>/', views.hashtag_view, name='hashtag'),
    path('comment/<int:post_id>', views.comment_view, name='comment'),

    path('user/<username>/follow', views.toggle_follow_view, name='follow'),
    path('user/<username>/edit_profile', views.edit_profile_view, name='edit_profile'),
    path('user/<username>/followers', views.followers_view, name='followers'),
    path('user/<username>/following', views.following_view, name='following'),
    path('user/notification', views.notification_view, name='notification'),

]
