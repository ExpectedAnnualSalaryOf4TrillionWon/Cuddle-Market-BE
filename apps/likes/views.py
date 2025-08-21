from rest_framework import generics, status
from rest_framework.decorators import api_view, parmission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from django.db.models import Count
from django.db import IntegrityError

from .models import ProductLike
from apps.products.models import Product
from apps.likes.serializers import (
    ProductLikeSerializer,
    ProductLikeCreateSerializer,
    ProductLikeToggleSerializer,
    UserLikeListSerializer,
    ProductLikeCountSerializer,
    ProductLikeStatsSerializer
)

class UserLikeListView(generics.ListAPIView):
    # 사용자의 찜 목록 조회
    serializer_class = UserLikeListSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return ProductLike.objects.filter(
            user=self.request.user
        ).select_related('product', 'product_user').prefetch_related('product_images')
    
    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)

        return Response({
            'count': queryset.count(),
            'results': serializer.data
        })
    
class ProductLikeCreateView(generics.CreateAPIView):
    # 찜 추가
    serializer_class = ProductLikeCreateSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data, context={'request': request})

        if serializer.is_valid():
            try:
                serializer.save()
                return Response({
                    'message': '찜 목록에 추가되었습니다.',
                    'data': serializer.data
                }, status=status.HTTP_201_CREATED)
            except IntegrityError:
                return Response({
                    'error': '이미 찜한 상품입니다.'
                }, status=status.HTTP_400_BAD_REQUEST)
            
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class ProductLikeDeleteView(generics.DestroyAPIView):
    # 찜 삭제
    permission_classes = [IsAuthenticated]

    def get_object(self):
        product_id = self.kwargs.get('product_id')
        return get_object_or_404(
            ProductLike,
            user=self.request.user,
            product_id=product_id
        )
    
    def delete(self, request, *args, **kwarg):
        instance = self.get_object()
        instance.delete()
        return Response({
            'massage': '찜 목록에서 제거되었습니다.'
        }, status=status.HTTP_200_OK)
    
class ProductLikeToggleView(APIView):
    # 찜 토글(추가/삭제를 한 번에 처리하는 뷰)
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = ProductLikeToggleSerializer(
            data=request.data,
            context={'request': request}
        )

        if serializer.is_valid():
            result = serializer.save()
            message = "찜 목록에 추가되었습니다." if result['liked'] else "찜 목록에서 제거되었습니다."

            return Response({
                'message': message,
                'liked': result['liked'],
                'action': result['action']
            })
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class ProductLikeStatusView(APIView):
    # 특정 상품의 찜 상태 확인
    permission_classes = [IsAuthenticated]

    def get(self, request, product_id):
        try:
            Product = Product.objects.get(id=product_id)
            is_liked = ProductLike.objects.filter(
                user=request.user,
                product = Product
            ).exists()

            like_count = ProductLike.objects.filter(product = Product).count()

            return Response({
                'product_id': product_id,
                'is_liked': is_liked,
                'like_count': like_count
            })
        
        except Product.DoesNotExist:
            return Response({
                'error': "존재하지 않는 상품입니다."
            }, status=status.HTTP_404_NOT_FOUND)
        
class ProductLikeCountView(generics.RetrieveAPIView):
    # 상품별 찜 갯수와 현재 사용자 찜 상태
    serializer_class = ProductLikeCountSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'pk'

    def get_queryset(self):
        return Product.objects.all()
    
@api_view(['GET'])
@parmission_classes([IsAuthenticated])
def user_like_stats(request):
    # 사용자 찜 통계
    user_likes = Product.objects.filter(user=request.user)

    # 총 찜 개수
    total_likes = user_like_stats.count()

    # 최근 찜한 상품 (최대 5개)
    recent_likes = user_likes.select_related(
        'product', 'product__user'
    ).prefetch_related('product__images').order_by('-created_at')[:5]