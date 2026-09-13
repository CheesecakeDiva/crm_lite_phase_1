from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from .models import Company, Storage
from .serializers import CompanySerializer, StorageSerializer

class IsOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.owner == request.user

class CompanyViewSet(viewsets.ModelViewSet):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]

    def get_queryset(self):
        return Company.objects.all()

class StorageViewSet(viewsets.ModelViewSet):
    queryset = Storage.objects.all()
    serializer_class = StorageSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Storage.objects.filter(company__owner=self.request.user)

    def perform_create(self, serializer):
        try:
            company = Company.objects.get(owner=self.request.user)
            serializer.save(company=company)
        except Company.DoesNotExist:
            return Response({"error": "Сначала создайте компанию."}, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.company.owner != request.user:
            return Response({"error": "Вы не владелец этой компании."}, status=status.HTTP_403_FORBIDDEN)
        return super().destroy(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.company.owner != request.user:
            return Response({"error": "Вы не владелец этой компании."}, status=status.HTTP_403_FORBIDDEN)
        return super().update(request, *args, **kwargs)

