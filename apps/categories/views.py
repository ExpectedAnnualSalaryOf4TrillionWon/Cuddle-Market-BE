# config/settings/base.py 에 정의된 REDIS_CLIENT를 가져옵니다.
from apps.categories.models import Category, PetType
from apps.categories.serializers import CategorySerializer, PetTypeWithDetailsSerializer
from config.settings.base import REDIS_CLIENT
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
import json
from drf_spectacular.utils import extend_schema


class AllCategoryDataAPIView(APIView):
    """
    프론트엔드 초기화에 필요한 모든 공통 기초 데이터.
    redis-py 클라이언트를 직접 사용하여 Redis에 캐싱합니다.
    (로거 제외, 안정성 강화 버전)
    """

    permission_classes = (AllowAny,)
    authentication_classes = ()

    CACHE_KEY = "direct:all_category_data"
    CACHE_TIMEOUT = 60 * 60 * 24  # 24시간

    @extend_schema(
        summary="카테고리 전체 조회",
        description="서비스 사용에 필요한 모든 종류의 카테고리, 반려동물, 지역 데이터를 하나의 API로 조회합니다.",
        tags=["Category"],
    )
    def get(self, request, *args, **kwargs):
        # --- 1. 캐시 조회 시도 (실패 시 조용히 넘어감) ---
        try:
            cached_data_json = REDIS_CLIENT.get(self.CACHE_KEY)
            if cached_data_json:
                # 캐시 히트: Redis에서 가져온 JSON을 파이썬 객체로 변환 후 반환
                cached_data = json.loads(cached_data_json)
                return Response(cached_data)
        except Exception:
            # Redis 연결 실패 시 아무것도 하지 않고 그냥 넘어갑니다.
            # 이렇게 하면 서비스 중단 없이 DB에서 데이터를 조회하게 됩니다.
            pass

        # --- 2. DB 조회 (캐시가 없거나 Redis 연결 실패 시 실행) ---
        categories = Category.objects.all().order_by("id")
        pet_types = PetType.objects.prefetch_related("details").all().order_by("id")

        categories_data = CategorySerializer(categories, many=True).data
        pet_types_data = PetTypeWithDetailsSerializer(pet_types, many=True).data

        response_data = {
            "categories": categories_data,
            "petTypes": pet_types_data,
        }

        # --- 3. 캐시 저장 시도 (실패 시 조용히 넘어감) ---
        try:
            response_data_json = json.dumps(response_data, ensure_ascii=False)
            REDIS_CLIENT.setex(
                name=self.CACHE_KEY, time=self.CACHE_TIMEOUT, value=response_data_json
            )
        except Exception:
            # 캐시 저장에 실패해도 API 응답은 정상적으로 나가야 하므로,
            # 예외를 무시하고 그냥 넘어갑니다.
            pass

        return Response(response_data)
