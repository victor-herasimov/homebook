from django.urls import path
from . import views

app_name = "comments"

urlpatterns = [
    path("<int:book_id>/", views.CommentListView.as_view(), name="comment_list"),
    path("create/", views.CreateCommentView.as_view(), name="comment_create"),
]
