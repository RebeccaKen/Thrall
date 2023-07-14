from . import views
from django.urls import path, reverse
from django.urls import path
from views import PostDetail, PostLike, PostList

app_name = 'blog'


urlpatterns = [
    path('', PostList.as_view(), name='post_list'),
    path('post/<slug:slug>/', PostDetail.as_view(), name='post_detail'),
    path('like/<slug:slug>', views.PostLike.as_view(), name='post_like'),
]
