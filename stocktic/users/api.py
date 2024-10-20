from rest_framework import viewsets, status
from rest_framework.decorators import action as action_decorator, api_view
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from .models import User
from .serializers import UserSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_permissions(self):
        if self.action == "create":
            self.permission_classes = [AllowAny]
        else:
            self.permission_classes = [IsAuthenticated]
        return super().get_permissions()

    @action_decorator(detail=False, methods=["get"])
    def get_by_telegram_id(self, request):
        telegram_user_id = request.query_params.get("telegram_user_id", None)
        if telegram_user_id is not None:
            user = self.queryset.filter(telegram_user_id=telegram_user_id).first()
            if user:
                serializer = self.get_serializer(user)
                return Response(serializer.data)
        return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)

    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)


@api_view(["POST"])
def get_token_by_telegram_id(request):
    telegram_user_id = request.data.get("telegram_user_id")
    if not telegram_user_id:
        return Response({"detail": "Telegram user ID is required"}, status=400)

    try:
        user = User.objects.get(telegram_user_id=telegram_user_id)
    except User.DoesNotExist:
        return Response({"detail": "User not found"}, status=404)

    refresh = RefreshToken.for_user(user)
    return Response(
        {
            "refresh": str(refresh),
            "access": str(refresh.access_token),
        }
    )
