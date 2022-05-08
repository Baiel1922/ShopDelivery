from .views import *
from rest_framework.routers import DefaultRouter
from django.urls import path, include

router = DefaultRouter()
router.register(r'shops', ShopView)
router.register(r'products', ProductView)
router.register(r'ratings', AddRatingViewSet)
router.register(r'saved', SavedView)

urlpatterns = [
    path('categories/', CategoryListView.as_view()),
    path('', include(router.urls)),
]