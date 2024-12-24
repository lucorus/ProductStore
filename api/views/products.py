from adrf.views import APIView
from adrf.viewsets import ViewSet
from asgiref.sync import sync_to_async
from drf_spectacular.utils import extend_schema
from rest_framework import status
import logging
from rest_framework.response import Response

from apps.products.models import Product, Category, SubCategory
from apps.core.sorting import get_products_by_filter
from api.serializers import BasketSerializer, UserSerializer, ProductSerializer, SubCategorySerializer

logger = logging.getLogger('main')


@extend_schema(tags=["Категории"])
class CategoriesView(APIView):
    page_size = 3

    async def get(self, request):
        """
        Опционально принимает список (параметры должны быть в []) slug'ов категорий подкатегории которых будут выводиться
        """
        category_slugs = request.data.get("groups_slugs") or None
        page = request.data.get("page") or 0

        subcategories = await sync_to_async(SubCategory.objects.select_related)("category")
        if category_slugs:
            subcategories = await sync_to_async(subcategories.filter)(category__slug__in=category_slugs)
        else:
            subcategories = await sync_to_async(subcategories.all)()
        subcategories = subcategories[page * self.page_size:(page+1) * self.page_size]
        serializer = await sync_to_async(SubCategorySerializer)(subcategories, many=True)
        data = await sync_to_async(serializer.to_representation)(serializer.instance)
        return Response(data, status=status.HTTP_200_OK)


@extend_schema(tags=["Продукты"])
class ProductViewSet(ViewSet):
    page_size = 3

    async def list(self, request):
        """
        Отображает данные о продуктах, фильтруя их по параметрам mix/max price, category, subcategory, и по ключевым
        словам
        """
        try:
            products = await sync_to_async(get_products_by_filter)(request)
            page = request.query_params.get("page") or 0
            products = products[page * self.page_size:(page + 1) * self.page_size]
            serializer = await sync_to_async(ProductSerializer)(products, many=True)
            data = await sync_to_async(serializer.to_representation)(serializer.instance)
            return Response(data, status=status.HTTP_200_OK)
        except Product.DoesNotExist:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        except Exception as ex:
            logger.error(ex)
            return Response(status=status.HTTP_400_BAD_REQUEST)

    async def retrieve(self, request, pk=None):
        try:
            product = await Product.objects.aget(slug=pk)
            serializer = await sync_to_async(ProductSerializer)(product)
            data = await sync_to_async(serializer.to_representation)(serializer.instance)
            return Response(data, status=status.HTTP_200_OK)
        except Product.DoesNotExist:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        except Exception as ex:
            logger.error(ex)
            return Response(status=status.HTTP_400_BAD_REQUEST)
