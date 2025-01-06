from adrf.views import APIView
from asgiref.sync import sync_to_async
from drf_spectacular.utils import extend_schema
from rest_framework import status
import logging
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from rest_framework.response import Response

from apps.products.models import Product
from apps.users.models import CustomUser, Comment, Complaints
from api.serializers import ProductSerializer, CommentSerializer
from api.permissions import IsCommentAuthorOrReadOnly


logger = logging.getLogger('main')


@extend_schema(tags=["Комментарии"])
class CommentViews(APIView):
    page_size = 3
    permission_classes = [IsAuthenticatedOrReadOnly, IsCommentAuthorOrReadOnly]

    async def post(self, request):
        try:
            product_slug = request.data.get("product_slug")
            product = await Product.objects.aget(slug=product_slug)
            text = request.data.get('text') or None
            estimation = request.data.get('estimation') or None
            comment_id = request.data.get('comment_id') or None

            if comment_id:
                # если написанный комментарий - ответ на другой комментарий (вопрос)
                question = await Comment.objects.aget(pk=comment_id)
                await question.answers.aadd(
                    await Comment.objects.acreate(author=request.user, product=product, text=text, estimation=0)
                )
                await question.asave()
            else:
                await Comment.objects.acreate(author=request.user, product=product, text=text, estimation=estimation)
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Product.DoesNotExist:
            return Response({"message": "Продукт не найден"}, status=status.HTTP_400_BAD_REQUEST)
        except Comment.DoesNotExist:
            return Response({"message": "Комментарий не найден"}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as ex:
            logger.error(ex)
            return Response({'status': 'error'}, status=status.HTTP_400_BAD_REQUEST)

    async def delete(self, request):
        try:
            comment_id = request.data.get("comment_id")
            comment = await Comment.objects.aget(id=comment_id)
            await sync_to_async(self.check_object_permissions)(request, comment)
            await comment.adelete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Comment.DoesNotExist:
            return Response({"message": "Комментарий не найден"}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as ex:
            logger.error(ex)
            return Response(status=status.HTTP_400_BAD_REQUEST)

    async def patch(self, request):
        try:
            comment_id = request.data.get("comment_id")
            comment = await Comment.objects.aget(id=comment_id)
            await sync_to_async(self.check_object_permissions)(request, comment)
            text = request.data.get('text') or comment.text
            estimation = request.data.get('estimation') or comment.estimation
            comment.text, comment.estimation = text, estimation
            await comment.asave()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Comment.DoesNotExist:
            return Response({"message": "Комментарий не найден"}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as ex:
            logger.error(ex)
            return Response({'status': 'error'}, status=status.HTTP_400_BAD_REQUEST)

    async def get(self, request):
        """
        Получает отзывы на продукт с переданным product_slug или ответы на отзыв с переданным comment_id
        """
        try:
            product_slug = request.query_params.get("product_slug")
            comment_id = request.query_params.get("comment_id")  # айди комментария, на который дают ответ

            if comment_id:
                comment = await Comment.objects.aget(id=comment_id)
                comments = await sync_to_async(comment.answers.showing_comments)()

                comment_serializer = await sync_to_async(CommentSerializer)(comment)
                comment_data = await sync_to_async(comment_serializer.to_representation)(comment_serializer.instance)
                data = {"comment": comment_data}
            else:
                product = await Product.objects.aget(slug=product_slug)
                comments = await sync_to_async(product.comments.filter)(comment=None, showing=True)

                product_serializer = await sync_to_async(ProductSerializer)(product)
                product_data = await sync_to_async(product_serializer.to_representation)(product_serializer.instance)
                data = {"product": product_data}

            page = request.data.get("page") or 0
            comments = comments[page * self.page_size:(page + 1) * self.page_size]

            comment_serializer = await sync_to_async(CommentSerializer)(comments, many=True)
            comments_data = await sync_to_async(comment_serializer.to_representation)(comment_serializer.instance)
            data["comments"] = comments_data
            return Response(data, status=status.HTTP_200_OK)
        except Comment.DoesNotExist:
            return Response({"message": "Комментарий не найден"}, status=status.HTTP_400_BAD_REQUEST)
        except Product.DoesNotExist:
            return Response({"message": "Продукт не найден"}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as ex:
            logger.error(ex)
            return Response(status=status.HTTP_400_BAD_REQUEST)


@extend_schema(tags=["Жалобы"])
class ComplainView(APIView):
    permission_classes = [IsAuthenticated]

    async def post(self, request):
        try:
            comment_id = request.data.get('comment_id') or None
            comment = await Comment.objects.aget(id=comment_id)
            await Complaints.objects.aget_or_create(author=request.user, comment=comment)
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Comment.DoesNotExist:
            return Response({"message": "Комментарий не найден"}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as ex:
            logger.error(ex)
            return Response(status=status.HTTP_400_BAD_REQUEST)
