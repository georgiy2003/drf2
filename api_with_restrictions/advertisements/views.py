from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.viewsets import ModelViewSet
from rest_framework import permissions


class AdvertisementViewSet(ModelViewSet):
    """ViewSet для объявлений."""
    queryset = Advertisement.objects.all()
    serializer_class = AdvertisementSerializer
    filterset_class = AdvertisementFilter

    def get_permissions(self):
        """Настройка прав доступа."""
        if self.action in ["create", "update", "partial_update"]:
            return [permissions.IsAuthenticated()]
        elif self.action in ["destroy"]:
            return [permissions.IsAuthenticated(), IsAuthorPermission()]
        else:
            return [permissions.AllowAny()]

    def perform_create(self, serializer):
        """Проверка лимита открытых объявлений при создании."""
        user = self.request.user
        validate_open_ads_limit(user)
        serializer.save(author=user)

    def perform_update(self, serializer):
        """Обновление объявления — только автор."""
        serializer.save()

    def destroy(self, request, *args, **kwargs):
        """Удаление — только автор."""
        instance = self.get_object()
        if instance.author != request.user:
            return Response({'detail': 'Удаление чужого объявления запрещено.'}, status=403)
        return super().destroy(request, *args, **kwargs)

from rest_framework.permissions import BasePermission

class IsAuthorPermission(BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.author == request.user

def validate_open_ads_limit(user):
    open_ads_count = Advertisement.objects.filter(author=user, status='OPEN').count()
    if open_ads_count >= 10:
        raise serializers.ValidationError("Достигнут лимит открытых объявлений (10).")