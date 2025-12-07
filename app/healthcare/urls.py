"""
URL mappings for the healthcare app.
"""
from django.urls import (
    path,
    include,
)

from rest_framework.routers import DefaultRouter

from healthcare import views


router = DefaultRouter()
router.register('specializations', views.SpecializationViewSet)

app_name = 'specialization'

urlpatterns = [
    path('', include(router.urls)),
]
