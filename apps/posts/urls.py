from django.urls import path
from .views import (
    CommentCreateView,
    CommentListView,
    CommentDeleteView,
    CommentUpdateView,
)

urlpatterns = [
    path("comments/", CommentCreateView.as_view(), name="comment-create"),  # 댓글 생성
    path("comments/", CommentListView.as_view(), name="comment-list"),  # 내 댓글 조회
    path(
        "comments/<int:comment_id>/", CommentDeleteView.as_view(), name="comment-delete"
    ),  # 댓글삭제
    path(
        "comments/<int:comment_id>/", CommentUpdateView.as_view(), name="comment-update"
    ),  # 댓글 수정
]
