# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny  # 필요시 인증 없이 접근 허용
from drf_spectacular.utils import extend_schema

# 필요한 모든 모델과 시리얼라이저를 임포트합니다.
from .models import Category, PetType, State
from .serializers import (
    CategorySerializer,
    PetTypeWithDetailsSerializer,
    StateWithCitiesSerializer,
)


class AllCategoryDataAPIView(APIView):
    """
    프론트엔드 초기화에 필요한 모든 공통 기초 데이터
    (카테고리, 반려동물 종류, 지역 정보)를 한번에 제공하는 API
    """

    permission_classes = (AllowAny,)  # 로그인 없이도 호출 가능하도록 설정
    authentication_classes = ()

    @extend_schema(
        summary="카테고리 전체 조회",
        description="서비스 사용에 필요한 모든 종류의 카테고리, 반려동물, 지역 데이터를 하나의 API로 조회합니다.",
        tags=["Category"],
    )
    def get(self, request, *args, **kwargs):
        # 1. 각 모델에서 모든 데이터를 가져옵니다. (성능 최적화 포함)
        categories = Category.objects.all().order_by("id")
        pet_types = PetType.objects.prefetch_related("details").all().order_by("id")
        # locations = State.objects.prefetch_related("cities").all().order_by("id")

        # 2. 각 데이터셋에 맞는 시리얼라이저로 직렬화합니다.
        categories_data = CategorySerializer(categories, many=True).data
        pet_types_data = PetTypeWithDetailsSerializer(pet_types, many=True).data
        # locations_data = StateWithCitiesSerializer(locations, many=True).data

        # 3. 가독성 좋은 최상위 키를 사용하여 모든 데이터를 하나의 딕셔너리로 묶습니다.
        response_data = {
            "categories": categories_data,
            "petTypes": pet_types_data,
            # "locations": locations_data,
        }

        return Response(response_data)
