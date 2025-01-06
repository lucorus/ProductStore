from adrf.views import APIView
from asgiref.sync import sync_to_async
from django.db.models import Q
from drf_spectacular.utils import extend_schema
from rest_framework import status
import logging
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from apps.products.models import Product
from apps.basket.models import Basket


logger = logging.getLogger('main')


@extend_schema(tags=["Корзина"])
class BasketViews(APIView):
    permission_classes = [IsAuthenticated]

    async def post(self, request):
        """
        Добавляет или убирает товар с product_slug, в зависимости от того существует ли он в корзине текущего
        пользователя или нет
        """
        try:
            product_slug = request.data.get("product_slug")
            if not product_slug:
                return Response("Данные не переданы", status=status.HTTP_400_BAD_REQUEST)
            if product_slug == "__all":
                """
                если передаётся в качестве slug'a продукта __all, значит пользователь хочет польностью удалить все
                товары из корзины
                """
                products = await sync_to_async(Basket.objects.filter)(owner=request.user)
                await products.adelete()
                return Response("Корзина полностью очищена!", status=status.HTTP_200_OK)
            product = await Product.objects.aget(slug=product_slug)
            basket_product = await Basket.objects.aget(Q(owner=request.user) & Q(product=product))
            if basket_product:
                await basket_product.adelete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Basket.DoesNotExist:
            await Basket.objects.acreate(product=product, owner=request.user)
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Product.DoesNotExist:
            return Response("Продукт не найден", status=status.HTTP_400_BAD_REQUEST)
        except Exception as ex:
            logger.error(ex)
            return Response(status=status.HTTP_400_BAD_REQUEST)

    async def patch(self, request):
        """
        Получает параметры product_slug - slug продукта размер подкорзины которого сейчас будут изменять и
        different_count - насколько будут изменять размер корзины (положительные и отрицательные целые числа)
        *все изменения происходят для корзины request.user*
        """
        try:
            different_count = int(request.data.get("different_count"))
            product_slug = request.data.get("product_slug")
            if not product_slug:
                return Response("Данные не переданы", status=status.HTTP_400_BAD_REQUEST)
            basket_product = await Basket.objects.aget(Q(owner=request.user) & Q(product__slug=product_slug))
            if basket_product.count + different_count < 1:
                await basket_product.adelete()
                return Response(f"Товар {product_slug} удалён из корзины!", status=status.HTTP_200_OK)
            basket_product.count += different_count
            await basket_product.asave()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Product.DoesNotExist:
            return Response("Продукт не найден", status=status.HTTP_400_BAD_REQUEST)
        except InterruptedError:
            return Response("Переданы некорректные данные", status=status.HTTP_400_BAD_REQUEST)
        except Exception as ex:
            logger.error(ex)
            return Response(status=status.HTTP_400_BAD_REQUEST)


