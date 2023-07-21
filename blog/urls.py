from django.urls import path
from .views import PostList, PostDetail, PostLike

app_name = 'blog' 

urlpatterns = [
    path('posts/', PostList.as_view(), name='post_list'),
    path('posts/<slug:slug>/', PostDetail.as_view(), name='post_detail'),
    path('posts/<slug:slug>/like/', PostLike.as_view(), name='post_like'),
]