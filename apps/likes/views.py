from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from apps.likes.models import Like
from apps.likes.serializers import LikeCreateSerializer,LikeListSerializer

class LikeAPIView(api_view):
    # 관심 목록 관리 API
    # POST /api/likes/ - 관심 목록 추가
    # DELETE /api/likes/ - 관심 목록 삭제
    permission_class = [IsAuthenticated]

    def get(self, request):
        # 관심 목록 조회
        # GET /api/likes/ - 관심 목록 조회
        likes = Like.objects.filter(user=request.user).select_related(
            'product_post'
        ).prefetch_related('product_images')

        serializer = LikeListSerializer(likes, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def post(self, request):
        # 관심 목록 추가
        serializer = LikeCreateSerializer(data=request.data, context={'request': request})

        if serializer.is_valid():
            serializer.save()
            return Response(
                {"message": "관심 상품 등록 완료"},
                status=status.HTTP_201_CREATED
            )
        
        # 중복 관심 상품 등록 방지 (에러 처리)
        if 'non_field_errors' in serializer.errors:
            return Response(
                {"message": "이미 관심 목록에 등록된 상품입니다."},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # 존재하지 않는 상품 에러 처리
        if 'product_id' in serializer.errors:
            return Response(
                {"message": "존재하지 않는 상품입니다."},
                status=status.HTTP_404_NOT_FOUND
            )
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request):
        # 관심 목록 삭제
        product_id = request.query_params.get('product_id')

        if not product_id:
            return Response(
                {"message": "product_id가 필요합니다."},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            like = Like.objects.get(user=request.user, product_id=product_id)
            like.delete()
            return Response(
                {"message": "관심 상품 헤제 완료"},
                status=status.HTTP_204_NO_CONTENT
            )
        
        except Like.DoesNotExist:
            return Response(
                {"message": "관심 목록에 없는 상품입니다"},
                status=status.HTTP_404_NOT_FOUND
            )