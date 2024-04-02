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
    # new urls
    # path('users/', views.profile_view, name='profile_view'),
    # path('friends/', views.friend_list, name='friend_list'),
    # path('friend-request/send/<int:id>/', views.send_friend_request, name='send_friend_request'),
    # path('friend-request/cancel/<int:id>/', views.cancel_friend_request, name='cancel_friend_request'),
    # path('friend-request/accept/<int:id>/', views.accept_friend_request, name='accept_friend_request'),
    # path('friend-request/delete/<int:id>/', views.delete_friend_request, name='delete_friend_request'),
    # path('friend/delete/<int:id>/', views.delete_friend, name='delete_friend'),
    # path('edit-profile/', views.edit_profile, name='edit_profile'),
    # path('profile/', views.profile, name='profile'),
    # path('search_users/', views.search_users, name='search_users'),
    # path('register/', views.register, name='register'),



] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

