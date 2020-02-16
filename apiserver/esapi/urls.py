from django.urls import path

from .views import get_comments_between_date

urlpatterns = [
    path('comments/', get_comments_between_date,
         name="get_comments_between_date"),
]
