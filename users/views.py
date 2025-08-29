import secrets
from datetime import timedelta

from django.contrib.auth import get_user_model
from django.core.cache import cache
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from drf_spectacular.utils import extend_schema

from .serializers import RegisterSerializer, EmailSerializer, ResetPasswordSerializer

User = get_user_model()

TOKEN_PREFIX = "pwdreset:"
TOKEN_TTL_SECONDS = 10 * 60  # 10 minutes

from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required

def home_redirect(request):
    if request.user.is_authenticated:
        # Redirect to profile or dashboard
        return redirect('profile')  # or your desired authenticated page
    else:
        return redirect('/api/docs/')

        # return redirect('api/auth/token')  # or 'register'
	
# class RegisterView(APIView):
# 	permission_classes = [AllowAny]

# 	def post(self, request):
# 		serializer = RegisterSerializer(data=request.data)
# 		serializer.is_valid(raise_exception=True)
# 		user = serializer.save()
# 		return Response({"id": user.id, "email": user.email, "full_name": user.first_name}, status=status.HTTP_201_CREATED)

from .serializers import RegisterSerializer, EmailSerializer, ResetPasswordSerializer
from rest_framework import serializers
from drf_spectacular.utils import extend_schema, OpenApiResponse, OpenApiExample

class RegisterResponseSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    email = serializers.EmailField()
    first_name = serializers.CharField()
    last_name = serializers.CharField()

@extend_schema(
    request=RegisterSerializer,
    responses={201: RegisterResponseSerializer},
    description="Register a new user.",
    examples=[
        OpenApiExample(
            "Successful Registration",
            value={"id": 1, "email": "user@example.com", "full_name": "User Name"},
            response_only=True,
        )
    ]
)
class RegisterView(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        
        full_name = user.first_name + " " + user.last_name 
        return Response({"id": user.id, "email": user.email, "full_name": full_name}, status=status.HTTP_201_CREATED)
	
class ForgotPasswordResponseSerializer(serializers.Serializer):
    reset_token = serializers.CharField()
    expires_in = serializers.IntegerField()

@extend_schema(
    request=EmailSerializer,
    responses={200: ForgotPasswordResponseSerializer},
    description="Request a password reset token.",
    examples=[
        OpenApiExample(
            "Forgot Password Response",
            value={"reset_token": "abc123...", "expires_in": 600},
            response_only=True,
        )
    ]
)
class ForgotPasswordView(APIView):
	permission_classes = [AllowAny]

	def post(self, request):
		serializer = EmailSerializer(data=request.data)
		serializer.is_valid(raise_exception=True)
		email = serializer.validated_data["email"].lower()
		try:
			user = User.objects.get(email__iexact=email)
		except User.DoesNotExist:
			# Do not reveal whether user exists
			return Response({"message": _("If the account exists, a reset token has been generated.")})

		# generate and store token in Redis
		token = secrets.token_urlsafe(32)
		cache_key = f"{TOKEN_PREFIX}{token}"
		cache.set(cache_key, {"user_id": user.id, "created": timezone.now().isoformat()}, timeout=TOKEN_TTL_SECONDS)
		return Response({"reset_token": token, "expires_in": TOKEN_TTL_SECONDS})

class ResetPasswordResponseSerializer(serializers.Serializer):
    message = serializers.CharField()

@extend_schema(
    request=ResetPasswordSerializer,
    responses={200: ResetPasswordResponseSerializer},
    description="Reset password using token.",
    examples=[
        OpenApiExample(
            "Password Reset Success",
            value={"message": "Password has been reset successfully."},
            response_only=True,
        )
    ]
)
class ResetPasswordView(APIView):
	permission_classes = [AllowAny]

	def post(self, request):
		serializer = ResetPasswordSerializer(data=request.data)
		serializer.is_valid(raise_exception=True)
		token = serializer.validated_data["token"]
		new_password = serializer.validated_data["new_password"]
		cache_key = f"{TOKEN_PREFIX}{token}"
		payload = cache.get(cache_key)
		if not payload:
			return Response({"detail": _("Invalid or expired token.")}, status=status.HTTP_400_BAD_REQUEST)

		user_id = payload.get("user_id")
		try:
			user = User.objects.get(id=user_id)
		except User.DoesNotExist:
			return Response({"detail": _("Invalid token user.")}, status=status.HTTP_400_BAD_REQUEST)

		user.set_password(new_password)
		user.save()
		cache.delete(cache_key)
		return Response({"message": _("Password has been reset successfully.")})
