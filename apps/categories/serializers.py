from rest_framework import serializers
from apps.categories.models import PetType, PetTypeDetail, State, City, Category


class PetTypeDetailSerializer(serializers.ModelSerializer):
    """PetTypeDetail 모델의 code와 name만 포함하는 시리얼라이저"""

    class Meta:
        model = PetTypeDetail
        fields = ["code", "name"]


class PetTypeWithDetailsSerializer(serializers.ModelSerializer):
    """
    PetType과 그에 속한 PetTypeDetail 목록(related_name='details')을
    중첩하여 함께 보여주는 시리얼라이저
    """

    details = PetTypeDetailSerializer(many=True, read_only=True)

    class Meta:
        model = PetType
        fields = ["code", "name", "details"]


class CitySerializer(serializers.ModelSerializer):
    """
    City(시/군/구) 모델을 위한 Serializer.
    State 정보는 부모 Serializer에서 제공하므로, code와 name만 포함합니다.
    """

    class Meta:
        model = City
        fields = ["code", "name"]


class StateWithCitiesSerializer(serializers.ModelSerializer):
    """
    하나의 State(시/도)와 그에 속한 모든 City 정보를 중첩하여 보여주는 Serializer.
    'cities'라는 이름으로 City 목록을 포함합니다.
    """

    # 1:N 관계를 표현하기 위해 'related_name'인 "cities"를 사용합니다.
    cities = CitySerializer(many=True, read_only=True)

    class Meta:
        model = State
        fields = ["code", "name", "cities"]


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["code", "name"]