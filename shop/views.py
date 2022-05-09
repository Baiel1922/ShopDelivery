from django.shortcuts import render
from .serializers import *
from .models import *
from account.permissions import IsAuthorPermission, IsActivePermission
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from rest_framework import viewsets, generics, filters
from .service import LargeResultPagination
from django_filters.rest_framework import DjangoFilterBackend
class PermissionMixin:
    def get_permissions(self):
        if self.action == "create":
            permissions = [IsAdminUser, ]
        elif self.action in ["update", "partial_update", "destroy"]:
            permissions = [IsAuthorPermission, ]
        else:
            permissions = [AllowAny, ]
        return [permission() for permission in permissions]

class PermissionMixin2:
    def get_permissions(self):
        if self.action == 'create':
            permissions = [IsActivePermission, ]
        elif self.action in ['update', 'partial_update', 'destroy']:
            permissions = [IsAuthorPermission, ]
        else:
            permissions = [AllowAny]
        return [permission() for permission in permissions]

class CategoryListView(generics.ListAPIView):
    permission_classes = [AllowAny]
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

class ShopView(PermissionMixin, viewsets.ModelViewSet):
    queryset = Shop.objects.all()
    serializer_class = ShopSerializer
    pagination_class = LargeResultPagination
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', ]
    ordering_fields = '__all__'


class ProductView(PermissionMixin, viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    pagination_class = LargeResultPagination
    filter_backends = [filters.SearchFilter, DjangoFilterBackend, filters.OrderingFilter]
    search_fields = ['name', 'description']
    filterset_fields = ['category', 'shop']
    ordering_fields = '__all__'

class AddRatingViewSet(PermissionMixin2,viewsets.ModelViewSet):
    queryset = Rating.objects.all()
    serializer_class = CreateRatingSerializer

class SavedView(PermissionMixin2, viewsets.ModelViewSet):
    queryset = Saved.objects.all()
    serializer_class = SavedSerializer