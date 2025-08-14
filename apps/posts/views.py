from django.shortcuts import get_object_or_404
from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Comment
from .serializers import (
    CommentCreateSerializer,
    CommentListSerializer,
    CommentUpdateSerializer,
)


class CommentCreateView(APIView):  # 댓글 작성 전용 API 뷰
    permission_classes = [permissions.IsAuthenticated]  # 로그인한 사용자만 접근 가능

    def post(self, request):  # POST 요청 처리
        serializer = CommentCreateSerializer(
            data=request.data, context={"request": request}
        )  # 데이터 + 유저 정보 전달
        if serializer.is_valid():  # 유효성 검사 통과 시
            serializer.save()  # 댓글 저장
            return Response(
                {"message": "댓글이 작성되었습니다."}, status=status.HTTP_201_CREATED
            )  # 성공 응답
        return Response(
            serializer.errors, status=status.HTTP_400_BAD_REQUEST
        )  # 실패 시 에러 응답


class CommentListView(APIView):  # 댓글 조회 API
    def get(self, request):
        post_id = request.query_params.get("post_id")  # 쿼리스트링에서 post_id 추출
        if not post_id:  # post_id 없으면 에러 응답
            return Response(
                {"error": "post_id가 필요합니다."}, status=status.HTTP_400_BAD_REQUEST
            )

        comments = Comment.objects.filter(post_id=post_id, is_deleted=False).order_by(
            "-created_at"
        )  # 삭제되지 않은 댓글만 조회
        serializer = CommentListSerializer(
            comments, many=True
        )  # 여러 개이므로 many=True
        return Response(
            serializer.data, status=status.HTTP_200_OK
        )  # 직렬화된 데이터 반환


class CommentDeleteView(APIView):  # 댓글 삭제 API
    permission_classes = [permissions.IsAuthenticated]  # 로그인한 사용자만 삭제 가능

    def delete(self, request, comment_id):  # comment_id는 URL path에서 전달됨
        comment = get_object_or_404(
            Comment, id=comment_id, is_deleted=False
        )  # 댓글 존재 여부 확인
        if comment.user != request.user:  # 작성자 본인이 아닌 경우
            return Response(
                {"error": "권한이 없습니다."}, status=status.HTTP_403_FORBIDDEN
            )

        comment.is_deleted = True  # soft delete 처리
        comment.save()  # 변경 사항 저장
        return Response(status=status.HTTP_204_NO_CONTENT)  # 본문 없는 성공 응답


class CommentUpdateView(APIView):  # 댓글 수정 API
    permission_classes = [permissions.IsAuthenticated]  # 로그인 필수

    def patch(self, request, comment_id):  # PATCH 요청 처리
        comment = get_object_or_404(
            Comment, id=comment_id, is_deleted=False
        )  # 존재하는 댓글인지 확인
        if comment.user != request.user:  # 권한 확인
            return Response(
                {"error": "권한이 없습니다."}, status=status.HTTP_403_FORBIDDEN
            )

        serializer = CommentUpdateSerializer(
            comment, data=request.data, partial=True
        )  # 부분 업데이트 허용
        if serializer.is_valid():  # 유효성 검사 통과 시
            serializer.save()  # 수정 내용 저장
            return Response(
                {"message": "댓글이 수정되었습니다."}, status=status.HTTP_200_OK
            )  # 성공 응답
        return Response(
            serializer.errors, status=status.HTTP_400_BAD_REQUEST
        )  # 실패 시 에러 응답
