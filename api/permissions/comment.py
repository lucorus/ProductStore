from rest_framework.permissions import BasePermission


class IsCommentAuthorOrReadOnly(BasePermission):
    """
    Даёт доступ к комментарию, если он осуществляется безопасным методом или если запрос отправляется автор
    или, если пользователь хочет создать комментарий
    """

    def has_object_permission(self, request, view, obj):
        if request.method in ['GET', 'HEAD', 'OPTIONS']:
            return True

        return obj.author == request.user
