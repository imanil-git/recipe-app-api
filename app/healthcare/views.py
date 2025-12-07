"""
Views for the healthcare for APIs.
"""
from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from core.models import Specialization
from healthcare import serializers


class SpecializationViewSet(viewsets.ModelViewSet):
    """View for manage healthcare APIs."""
    serializer_class = serializers.SpecializationSerializer
    queryset = Specialization.objects.all()
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Retrieve recipes for authenticated user."""
        return Specialization.objects.filter(user=self.request.user)
