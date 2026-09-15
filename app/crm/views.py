from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from .models import Company, Storage
from .serializers import CompanySerializer, StorageSerializer
from django.db import models


class IsCompanyOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        if hasattr(obj, 'company'):
            return obj.company.owner == request.user

        return getattr(obj, 'owner', None) == request.user


class CompanyViewSet(viewsets.ModelViewSet):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer
    permission_classes = [permissions.IsAuthenticated, IsCompanyOwnerOrReadOnly]

    def get_queryset(self):
        user = self.request.user
        return Company.objects.filter(
            models.Q(owner=user) | models.Q(id=user.company_id if hasattr(user, 'company_id') else None))


class StorageViewSet(viewsets.ModelViewSet):
    queryset = Storage.objects.all()
    serializer_class = StorageSerializer
    permission_classes = [permissions.IsAuthenticated, IsCompanyOwnerOrReadOnly]

    def get_queryset(self):
        user = self.request.user
        return Storage.objects.filter(
            models.Q(company__owner=user) |
            models.Q(company_id=user.company_id if hasattr(user, 'company_id') else None)
        ).distinct()

    def create(self, request, *args, **kwargs):
        try:
            company = Company.objects.get(owner=request.user)
        except Company.DoesNotExist:
            raise ValidationError(
                {"error": "Сначала создайте компанию. Вы не являетесь владельцем какой-либо компании."})

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(company=company)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


