from rest_framework import status, viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import get_user_model
from django.db.models import Q, Count

from .serializers import (
    ProfileSerializer, ProfileUpdateSerializer, UserListSerializer, UserDetailSerializer
)
from .exceptions import UserNotFound
from apps.core.permissions import IsManagerOrAdmin


User = get_user_model()


class ProfileView(APIView):
    def get(self, request):
        if not request.user:
            raise UserNotFound
        serializer = ProfileSerializer(request.user)

        return Response(serializer.data, status=status.HTTP_200_OK)

    def patch(self, request):
        user = request.user
        serializer = ProfileUpdateSerializer(user, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response({
            'message': 'Profile updated successfully',
            'user': ProfileSerializer(user).data
        }, status=status.HTTP_200_OK)


class UsersViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated, IsManagerOrAdmin]

    def get_serializer_class(self):
        if self.action == "retrieve":
            return UserDetailSerializer
        return UserListSerializer

    def get_queryset(self):
        queryset = User.objects.all().annotate(
                orders_count=Count("client_orders")
            )

        role = self.request.query_params.get("role")
        search = self.request.query_params.get("search")

        if role:
            queryset = queryset.filter(role=role)
        if search:
            queryset = queryset.filter(
                Q(first_name__icontains=search) |
                Q(last_name__icontains=search) |
                Q(email__icontains=search)
            )

        return queryset
