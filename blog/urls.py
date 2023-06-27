from . import views
from django.urls import path


urlpatterns = [
    path('PostList', views.post_list, name='post_list'),
    path('PostDetails/', views.PostDetail.as_view(), name="post_detail"),
]