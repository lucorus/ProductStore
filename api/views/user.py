from adrf.views import APIView
from asgiref.sync import sync_to_async
from django.core.exceptions import ValidationError
from djoser.views import UserViewSet
from drf_spectacular.utils import extend_schema
from django.core.validators import validate_email
from rest_framework import status
import logging
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from djoser.serializers import UserCreateSerializer

from apps.users.models import CustomUser
from apps.products.models import Product
from apps.basket.models import Basket
from apps.core.sorting import get_products_by_filter
from api.serializers import BasketSerializer, UserSerializer, ProductSerializer, CommentSerializer

logger = logging.getLogger('main')


@extend_schema(tags=["Взаимодействие с пользователем"])
class Profile(APIView):
    permission_classes = [IsAuthenticated]
    page_size = 3

    async def get_object(self):
        user_serializer = await sync_to_async(UserSerializer)(self.request.user)
        user_data = await sync_to_async(user_serializer.to_representation)(user_serializer.instance)
        return user_data

    async def get(self, request):
        try:
            page = int(request.query_params.get("page", 0))
            sorting = request.data.get('sorting') or '-id'
            if sorting[0] == '-':
                reverse = '-'
                sorting = sorting.replace('-', '')
            else:
                reverse = ''

            products = await sync_to_async(get_products_by_filter)(request)

            basket = await sync_to_async(Basket.objects.select_related)('owner', 'product')
            basket = await sync_to_async(basket.filter)(owner=request.user, product__in=products)
            basket = await sync_to_async(basket.order_by)(reverse + 'product__' + sorting)
            basket = basket[page * self.page_size:(page + 1) * self.page_size]

            basket_serializer = await sync_to_async(BasketSerializer)(basket, many=True)
            basket_data = await sync_to_async(basket_serializer.to_representation)(basket_serializer.instance)
            return Response({"user": await self.get_object(), "basket": basket_data}, status=status.HTTP_200_OK)
        except Exception as ex:
            logger.error(ex)
            return Response([], status=status.HTTP_200_OK)

    async def patch(self, request):
        try:
            username = request.data.get("username") or request.user.username
            email = request.data.get("email") or request.user.email

            if await CustomUser.objects.filter(username=username).exclude(id=request.user.id).aexists():
                return Response({"error": "Username is already taken."}, status=status.HTTP_400_BAD_REQUEST)
            if await CustomUser.objects.filter(email=email).exclude(id=request.user.id).aexists():
                return Response({"error": "Email is already taken."}, status=status.HTTP_400_BAD_REQUEST)

            try:
                validate_email(email)
            except ValidationError:
                return Response({"error": "Invalid email format."}, status=status.HTTP_400_BAD_REQUEST)

            request.user.username = username
            request.user.email = email
            await request.user.asave()

            return Response(status=status.HTTP_204_NO_CONTENT)
        except Exception as ex:
            logger.error(ex)
            return Response(status=status.HTTP_400_BAD_REQUEST)


@extend_schema(tags=["Взаимодействие с пользователем"])
class FavoriteProducts(APIView):
    page_size = 3
    permission_classes = [IsAuthenticated]

    async def post(self, request):
        """
        Удаляет товар с переданным product_slug из избранного, если он там уже есть, иначе добавляет
        """
        try:
            slug = request.data.get("product_slug") or None
            if not slug:
                raise Exception("Not found slug")
            product = await Product.objects.aget(slug=slug)
            # если товар уже в избранном, то удаляем его
            prod = await sync_to_async(request.user.favorites.filter)(slug=slug)
            if await sync_to_async(prod.exists)():
                await request.user.favorites.aremove(product)
            else:
                await request.user.favorites.aadd(product)
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Exception as ex:
            logger.error(ex)
            return Response({'status': 'error', 'message': 'product not found'}, status=status.HTTP_400_BAD_REQUEST)

    async def get(self, request):
        """
        Отображает товары, которые находятся в избранном у request.user
        """
        page = int(request.query_params.get("page", 0))
        favorite_products = await sync_to_async(request.user.favorites.all)()
        favorite_products = favorite_products[page * self.page_size:(page + 1) * self.page_size]

        products_serializer = await sync_to_async(ProductSerializer)(favorite_products, many=True)
        products_data = await sync_to_async(products_serializer.to_representation)(products_serializer.instance)
        return Response(products_data, status=status.HTTP_200_OK)


@extend_schema(tags=["Аутентификация"])
class CustomUserViewSet(UserViewSet):
    @action(["post"], detail=False)
    def registration(self, request):
        serializer = UserCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
