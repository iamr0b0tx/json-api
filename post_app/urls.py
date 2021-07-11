from django.urls import path

urlpatterns = [
    path('ping/', ping),
    path('posts', get_posts),
]
