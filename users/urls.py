from django.conf import settings
from django.contrib import admin
from django.urls import path,include
from . import views
from django.conf.urls.static import static

urlpatterns =[
    path('register/', views.sign_up, name='register'),
    path('profile/<int:id>', views.profile, name='profile'),
    path('home/', views.home, name='home'),
    path('', views.sign_in, name='login'),
    path('login/', views.sign_in, name='login'),
    path('logout/', views.sign_out, name='logout'),
    path('create_post/',views.create_post, name='post-create'),
    path('posts/', views.posts, name="posts"),
    path('edit_post/<int:id>/', views.edit_post, name='edit_post'),
    path('post_delete/<int:id>',views.delete_post, name='post_delete'),
    path('like_post/<int:id>',views.like_post, name='like_post'),
    path('send-friend-request/<int:id>/', views.send_friend_request, name='send_friend_request'),
    path('accept-friend-request/<int:request_id>/', views.accept_friend_request, name='accept_friend_request'),
    path('received-friend-requests/', views.received_friend_requests, name='received_friend_requests'),
    path('reject-friend-request/<int:request_id>/', views.reject_friend_request, name='reject_friend_request'),


] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

