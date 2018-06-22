from django.urls import path
from . import views

from django.conf import settings
from django.conf.urls.static import static

app_name = 'my_face'

urlpatterns = [
    # POST
    path('post/create', views.create_post, name='create_post'),
    path('post/<int:post_id>/delete', views.delete_post, name='delete_post'),
    path('post/', views.posts, name='posts'),
    # COMMENT
    path('comment/create', views.create_comment, name='create_comment'),
    path('comment/<int:comment_id>/delete', views.delete_comment, name='delete_comment'),
    # USER
    path('user/register', views.register, name='register'),
    path('user/login', views.login, name='login'),
    path('user/logout', views.logout, name='logout'),
    path('user/search/<str:keyword>', views.search_user, name='search_user'),
    path('user/search/', views.post_search_user, name='post_search_user'),
    path('user/<int:user_id>/followers', views.follower, name='follower'),
    path('user/<int:user_id>/followings', views.following, name='following'),
    path('user/<int:user_id>/', views.wall, name='wall'),
    # user/email/followers
    # user/email/followings
    # PHOTO
    path('photo/', views.photo, name='photo'),
    path('photo/<int:photo_id>', views.delete_photo, name='delete_photo'),

    path('user/follow/<int:follower_id>/<int:following_id>', views.follow, name='follow'),
    path('user/unfollow/<int:follower_id>/<int:following_id>', views.unfollow, name='unfollow'),

    path('user/generate_user', views.generate_user, name='generate_user'),
    path('', views.index, name='index'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)