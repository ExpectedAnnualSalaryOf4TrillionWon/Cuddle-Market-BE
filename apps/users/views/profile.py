# class MyProfileView(APIView):
#     """
#     마이 페이지 API
#     """
#
#     @extend_schema(
#         summary="회원 정보 조회",
#         description="회원 정보를 조회하는 API입니다",
#         responses={200, UserSerializer},
#         tags=["User"],
#     )
#     def get(self, request):
#         user = request.user
#         serializer = UserSerializer(user)
#         return Response(serializer.data, status=status.HTTP_200_OK)
#
#     @extend_schema(
#         summary="회원 정보 수정",
#         description="회원 정보를 수정하는 API입니다",
#         request=UpdateMyPageSerializer,
#         tags=["User"],
#     )
#     def patch(self, request):
#         user = request.user
#
#         if is_valid_email(request.data.get("email")):
#             return Response(
#                 {"error": "올바른 이메일 형식이 아닙니다."},
#                 status=status.HTTP_400_BAD_REQUEST,
#             )
#
#         ori_user = User.objects.filter(id=user.pk).first()
#         # 요청된 데이터 중 비교할 필드만 선택
#         update_fields = {
#             key: value
#             for key, value in request.data.items()
#             if key in ["email", "name", "phone_number"]
#         }
#
#         # 변경 사항 확인
#         if all(
#             getattr(ori_user, field) == update_fields[field] for field in update_fields
#         ):
#             return Response(
#                 {"error": "변경사항이 없습니다"}, status=status.HTTP_400_BAD_REQUEST
#             )
#
#         serializer = UpdateMyPageSerializer(
#             user, data=request.data, partial=True, context={"request": request}
#         )
#
#         if serializer.is_valid():
#             serializer.save()
#             # 로컬 유저인 경우 redis에서 이메일 캐시 삭제
#             if user.provider_id is None:
#                 email = serializer.validated_data["email"]
#                 if email:
#                     REDIS_CLIENT.delete(RedisKeys.get_verified_email_key(email))
#             return Response(
#                 {"detail": "회원 정보 변경이 완료되었습니다."},
#                 status=status.HTTP_200_OK,
#             )
#
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)